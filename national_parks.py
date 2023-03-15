#!/usr/bin/env python
# coding: utf-8

# In[130]:


import requests
import json


# In[131]:


api_endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
API_KEY = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'


# In[132]:


country = input("Enter a country or city name: ")


# In[138]:


def get_national_parks(country):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query": "national park in " + country, "key": API_KEY}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    locations = []

    if data['status'] == 'OK':
        results = data['results']
        for result in results:
            name = result['name']
            location = result['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            locations.extend([name,(lat,lng)])

    else:
        return("Error:", data['status'])

    return locations


# In[140]:


infos = get_national_parks(country)


# In[141]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[142]:


parks = Convert(infos)

