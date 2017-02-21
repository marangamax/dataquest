
# coding: utf-8

# # Read in the data

# In[29]:

import pandas
import numpy
import re

data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]

data = {}

for f in data_files:
    d = pandas.read_csv("schools/{0}".format(f))
    data[f.replace(".csv", "")] = d


# # Read in the surveys

# In[30]:

all_survey = pandas.read_csv("schools/survey_all.txt", delimiter="\t", encoding='windows-1252')
d75_survey = pandas.read_csv("schools/survey_d75.txt", delimiter="\t", encoding='windows-1252')
survey = pandas.concat([all_survey, d75_survey], axis=0)

survey["DBN"] = survey["dbn"]

survey_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_10", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
]
survey = survey.loc[:,survey_fields]
data["survey"] = survey


# # Add DBN columns

# In[31]:

data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return "0" + string_representation
    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]


# # Convert columns to numeric

# In[32]:

cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pandas.to_numeric(data["sat_results"][c], errors="coerce")

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]

def find_lat(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

def find_lon(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_lon)

data["hs_directory"]["lat"] = pandas.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pandas.to_numeric(data["hs_directory"]["lon"], errors="coerce")


# # Condense datasets

# In[33]:

class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]

class_size = class_size.groupby("DBN").agg(numpy.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size

data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]

data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]


# # Convert AP scores to numeric

# In[34]:

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pandas.to_numeric(data["ap_2010"][col], errors="coerce")


# # Combine the datasets

# In[35]:

combined = data["sat_results"]

combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")

to_merge = ["class_size", "demographics", "survey", "hs_directory"]

for m in to_merge:
    combined = combined.merge(data[m], on="DBN", how="inner")

combined = combined.fillna(combined.mean())
combined = combined.fillna(0)


# # Add a school district column for mapping

# In[36]:

def get_first_two_chars(dbn):
    return dbn[0:2]

combined["school_dist"] = combined["DBN"].apply(get_first_two_chars)


# # Find correlations

# In[37]:

correlations = combined.corr()
correlations = correlations["sat_score"]
print(correlations)


# # Finding correlations between survey data and SAT scores

# In[38]:

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

survey_correlations = correlations[survey_fields]

num_cols = len(survey_correlations)
bar_heights = survey_correlations
bar_positions = np.arange(num_cols)+0.5
xlabel = survey_fields

print(bar_heights)
print(bar_positions)

fig, ax = plt.subplots()
plt.figsize=(300, 50)
ax.bar(bar_positions, bar_heights, 0.5, tick_label = xlabel)
plt.xticks(rotation='vertical')
plt.show()


# In[50]:

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

plt.scatter(combined['saf_s_11'], combined['sat_score'])
plt.show()

m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

districts = combined.groupby(combined['school_dist']).mean()
districts.reset_index(inplace=True)

longitudes = districts['lon'].tolist()
latitudes = districts['lat'].tolist()

m.scatter(longitudes,latitudes, s=50, zorder=2, latlon=True, c=districts['saf_s_11'], cmap='summer')
plt.show()


# I don't know NYC very well but the safety level is ranked much lower across the river and towards the Northern part of the city. Whilst downtown and towards Long Island look much better, I'm assuming the areas where safety is much lower are the Bronx, Queens, and Brooklyn

# In[104]:

races = ['white_per', 'asian_per', 'black_per', 'hispanic_per']

fig, ax = plt.subplots()
i = 1

for race in races:
    correlation = combined[race].corr(combined['sat_score'])
    combined[race+'_corr'] = correlation
    ax = plt.subplot(2,2,i)
    plt.legend(combined[race], loc='upper right')
    ax = plt.scatter(combined[race], combined['sat_score'])
    i = i + 1
    
combined.head(3)


# In[98]:

print(combined['hispanic_per'].head(3))
five_hispanic_per = combined[combined['hispanic_per']>95.0]
print(five_hispanic_per['SCHOOL NAME'])

ten_hispanic_per = combined[(combined['hispanic_per']<10.0)&(combined['sat_score']>1800)]
print(ten_hispanic_per['SCHOOL NAME'])


# In[99]:

genders = ['male_per', 'female_per']

fig, ax = plt.subplots()
i = 1

for gender in genders:
    correlation = combined[gender].corr(combined['sat_score'])
    combined[gender+'_corr'] = correlation
    ax = plt.subplot(2,1,i)
    ax = plt.scatter(combined[gender], combined['sat_score'])
    i = i + 1
    
combined.head(2)


# In[106]:

plt.scatter(combined['female_per'], combined['sat_score'])
plt.show()


# There's not much interesting correlation, however one can observe a slight trend towards a greater percentage girls implying a higher average SAT score, i.o.w. girls do better on the SAT then boys.

# In[107]:

sixty_female_per = combined[(combined['female_per']>60)&(combined['sat_score']>1700)]
print(sixty_female_per['SCHOOL NAME'])


# In[109]:

combined['ap_per'] = combined['AP Test Takers '] / combined['total_enrollment']
plt.scatter(combined['ap_per'], combined['sat_score'])
print(combined['sat_score'].corr(combined['ap_per']))
plt.show()


# Interestingly enough, there's not as much strong correlation between percentage of AP test takers and SAT score as expected. There's even schools where the number of AP test takers is greater than 80% and the average SAT score is around 1200 which is a little ridiculous.

# In[ ]:



