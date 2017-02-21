
# coding: utf-8

# In[3]:

import pandas as pd
data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")
data.head(1)


# In[2]:

import pandas as pd
data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")
count = data.value_counts("Do you celebrate Thanksgiving", "Yes")
print(count)


# In[3]:

import pandas as pd
data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")
celebrate = data["Do you celebrate Thanksgiving?"]
count = celebrate.value_counts()
print(count)

# In[5]:

data2 = data[data["Do you celebrate Thanksgiving?"]=="Yes"]


# In[6]:

celebrate = data2["Do you celebrate Thanksgiving?"]
count = celebrate.value_counts()
print(count)


# In[7]:

dishes = data2["What is typically the main dish at your Thanksgiving dinner?"]
count = dishes.value_counts()
print(count)

# In[3]:

tofurkey = data[data["What is typically the main dish at your Thanksgiving dinner?"]=="Tofurkey"]
print(tofurkey["Do you typically have gravy?"])


# In[5]:

apple_pie = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"]
pumpkin_pie = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"]
pecan_pie = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"]

apple_isnull = apple_pie.isnull()
pumpkin_isnull = pumpkin_pie.isnull()
pecan_isnull = pecan_pie.isnull()
ate_pies = apple_isnull&pumpkin_isnull&pecan_isnull
print(ate_pies.value_counts())


# In[60]:

import pandas as pd
data = pd.read_csv("thanksgiving.csv", encoding='Latin-1')

def get_age(column):
    if pd.isnull(column)==True:
        return
    else:
        split_age = column.split(' ')
        final_age_with_plus = split_age[0]
        final_age_str = final_age_with_plus.replace("+","")
        final_age = int(final_age_str)
        return(final_age)

int_age_series = data["Age"]
data['int_age'] = int_age_series.apply(get_age)
values = int_age.value_counts()
print(values)
print(int_age.describe())


# In[63]:

income = data["How much total combined money did all members of your HOUSEHOLD earn last year?"]

def get_income(column):
    if pd.isnull(column)==True:
        return
    split_column = column.split()
    if split_column[0]=='Prefer':
        return
    else:
        income_str = split_column[0].replace(',', '')
        income_str = income_str.replace('$', '')
        income_value = int(income_str)
        return(income_value)

data['int_income'] = income.apply(get_income)
data['int_income'].describe()
data['int_income'].value_counts()
    


# In[42]:



income_less_than_150000 = data[data['int_income'] < 150000]
poor_people_travel = income_less_than_150000['How far will you travel for Thanksgiving?']
poor_people_travel.value_counts()



rich_people = data[data['int_income'] >= 150000]
rich_people_travel = rich_people['How far will you travel for Thanksgiving?']
rich_people_travel.value_counts()


# In[64]:

pivot = pd.pivot_table(data,values='int_income', index="Have you ever tried to meet up with hometown friends on Thanksgiving night?", columns='Have you ever attended a "Friendsgiving?"')
print(pivot)




