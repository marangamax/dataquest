
# coding: utf-8

# In[74]:

import pandas as pd
star_wars = pd.read_csv('star_wars.csv', encoding='ISO-8859-1')

t_f = {
    'Yes': True,
    'No': False
}

star_wars['Have you seen any of the 6 films in the Star Wars franchise?'] = star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].map(t_f)
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'] = star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].map(t_f)

star_wars.head(1)


# In[75]:

m = {
    'Star Wars: Episode I  The Phantom Menace': True,
    'Star Wars: Episode II  Attack of the Clones': True,
    'Star Wars: Episode III  Revenge of the Sith': True,
    'Star Wars: Episode IV  A New Hope': True,
    'Star Wars: Episode V The Empire Strikes Back': True,
    'Star Wars: Episode VI Return of the Jedi': True,
    'NaN': False
}

star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'] = star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'].map(m)
star_wars['Unnamed: 4'] = star_wars['Unnamed: 4'].map(m)
star_wars['Unnamed: 5'] = star_wars['Unnamed: 5'].map(m)
star_wars['Unnamed: 6'] = star_wars['Unnamed: 6'].map(m)
star_wars['Unnamed: 7'] = star_wars['Unnamed: 7'].map(m)
star_wars['Unnamed: 8'] = star_wars['Unnamed: 8'].map(m)

r = {
    'Which of the following Star Wars films have you seen? Please select all that apply.': 'seen_1',
    'Unnamed: 4': 'seen_2',
    'Unnamed: 5': 'seen_3',
    'Unnamed: 6': 'seen_4',
    'Unnamed: 7': 'seen_5',
    'Unnamed: 8': 'seen_6'
}

star_wars = star_wars.rename(columns=r)

star_wars.head(4)



# In[76]:

star_wars = star_wars.drop(0)
print(star_wars.head(2))

columns = star_wars.columns[9:15]
for column in columns:
    star_wars[column] = star_wars[column].astype(float)

r = {
    'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.': 'ranking_1',
    'Unnamed: 10': 'ranking_2',
    'Unnamed: 11': 'ranking_3',
    'Unnamed: 12': 'ranking_4',
    'Unnamed: 13': 'ranking_5',
    'Unnamed: 14': 'ranking_6'
}

star_wars = star_wars.rename(columns=r)


# In[77]:

star_wars.head(20)


# In[78]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

columns = star_wars.columns[9:15]
means = {}
for c in columns:
    mean = star_wars[c].mean()
    means[c] = mean

x = range(len(means))
y = means.values()
labels = means.keys()
width = 0.5
plt.bar(x, y, width, color='red', label=labels)
plt.show()

print(means)


# Clearly the first three Star Wars have been rated better, the best one of all being #5.

# In[80]:

seen = star_wars.columns[3:9]

pct_seen = {}
for m in seen:
    s = star_wars[m].sum()
    pct_seen[m] = s

x = range(len(pct_seen))
y = pct_seen.values()
labels = pct_seen.keys()
width = 0.5
plt.bar(x, y, width, color='red', label=labels)
plt.show()

print(pct_seen)


# In[ ]:



