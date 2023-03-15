#!/usr/bin/env python
# coding: utf-8

# In[493]:


import requests
import json


# In[494]:


api_endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
API_KEY = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'


# In[495]:


country = input("Enter a country or city name: ")


# # Natural features

# In[496]:


def get_natural_feature(country):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query": "natural feature in " + country, "key": API_KEY}
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


# In[497]:


info = get_natural_feature(country)


# In[498]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[499]:


Convert(info)


# # Famous landmarks

# In[500]:


query = f'{country} landmarks'
params = {
    'query': query,
    'key': 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
}


# In[501]:


response = requests.get(base_url, params=params)
data = response.json()


# In[502]:


results = sorted(data['results'], key=lambda x: x['user_ratings_total'], reverse=True)
locations = []


# In[503]:


for result in results[:60]:
    name = result['name']
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    locations.extend([name,(lat,lng)])
   


# In[504]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[505]:


Convert(locations)


# # National parks

# In[506]:


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


# In[507]:


infos = get_national_parks(country)


# In[508]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[509]:


Convert(infos)


# In[510]:


print(infos)


# # Tourist attractions

# In[511]:


from geopy.geocoders import Nominatim
address= country
geolocator = Nominatim(user_agent="Your_Name")
geolocation = geolocator.geocode(address)
lat= geolocation.latitude
long= geolocation.longitude


# In[512]:


params = {
    "location": country,
    "types": "tourist_attraction",
    "key": API_KEY,
}


# In[513]:


API_KEY = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
BASE_URL2 = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius=50000&types=tourist_attraction&key=AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI"


# In[514]:


response = requests.get(BASE_URL2, params=params)
response_json = json.loads(response.text)
location1 = []


# In[515]:


sort_rating_ignoring_unrated = sorted([a for a in response_json['results'] if 'rating' in a], key=lambda x: x['rating'], reverse=True)
sorted_rating= sorted(sort_rating_ignoring_unrated, key=lambda x: x['rating'], reverse=True)

for result in sorted_rating:
    name = result["name"]
    rating = result.get("rating", "not available")
    place_type = result["types"][0]
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    locations.extend([name,(lat,lng)])
 
    if place_type == "tourist_attraction":
        location1.extend([name,(lat,lng)])


# In[516]:


location1


# In[517]:


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


# In[518]:


Convert(location1)


# # Merging

# In[519]:


def merged(): 
    result=Convert(infos) | Convert(locations) | Convert(info) | Convert(location1)
    return result
    
 


# In[520]:


merged()


# In[ ]:




