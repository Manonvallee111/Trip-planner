#!/usr/bin/env python
# coding: utf-8

# In[268]:


#FIND OUT HOW TO ADD MORE LANDMARKS TO THE LIST


# In[269]:


import requests


# In[270]:


api_key = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


# In[271]:


country = input('Enter the country you want to search for landmarks in: ')


# In[272]:


query = f'{country} landmarks'
params = {
    'query': query,
    'key': api_key
}


# In[273]:


response = requests.get(base_url, params=params)
data = response.json()


# In[274]:


results = sorted(data['results'], key=lambda x: x['user_ratings_total'], reverse=True)
locations = []


# In[275]:


for result in results[:60]:
    name = result['name']
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    locations.extend([name,(lat,lng)])
   
    print(locations) 


# In[276]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[277]:


landmarks= Convert(locations)


# In[ ]:




