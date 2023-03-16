#!/usr/bin/env python
# coding: utf-8

# In[143]:


import math
import googlemaps
import requests
import gmaps
import json
from geopy.geocoders import Nominatim
import ipywidgets as widgets
import ipywidgets as widgets
import gmaps.datasets
import requests
import json
from datetime import timedelta
import gmaps
import gmaps.datasets
import seaborn as sns
import matplotlib.pyplot as plt
import random

import collections
collections.Iterable = collections.abc.Iterable


# In[144]:


gmaps.configure(api_key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')
client = googlemaps.Client('AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')
google = googlemaps.Client(key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')


# In[ ]:


city_name = input("Where will you start your road trip? ")
duration = int(input("Enter the duration of the trip in days: "))
hours_per_day = int(input("Enter the number of hours per day you are willing to drive: "))
geocode_result = google.geocode(city_name)

duration_timedelta = timedelta(days=duration)
total_hours = duration_timedelta.days * hours_per_day
total_distance = total_hours * 80
radius = total_distance / (2 * 3.14159)

# Extract latitude and longitude
start_lat = geocode_result[0]['geometry']['location']['lat']
start_lng = geocode_result[0]['geometry']['location']['lng']

for component in geocode_result[0]['address_components']:
    if "country" in component['types']:
        country = component['long_name']

if country:
    print(f"The country for {city_name} is {country}.")
else:
    print("Could not find the country for the specified city.")


# In[ ]:


radius


# In[ ]:


api_endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
API_KEY = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def get_natural_feature(city,country):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query": "natural feature in " + city + " "+ country, "key": API_KEY}
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

def get_national_parks(city, country):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query": "national park in "+ city + " "+ country, "key": API_KEY}
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


# In[ ]:


# # Famous landmarks
query = f'{city_name} {country} landmarks'
params = {
    'query': query,
    'key': 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
}
response = requests.get(base_url, params=params)
data = response.json()
results = data['results']
famous_landmarks_city = []

for result in results[:60]:
    name = result['name']
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    famous_landmarks_city.extend([name,(lat,lng)])


query = f'{country} landmarks'
params = {
    'query': query,
    'key': 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
}
response = requests.get(base_url, params=params)
data = response.json()
results = data['results']
famous_landmarks_country = []

for result in results[:60]:
    name = result['name']
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    famous_landmarks_country.extend([name,(lat,lng)])


# In[ ]:


# # Tourist attractions
from geopy.geocoders import Nominatim
address= city_name + ' ' + country
geolocator = Nominatim(user_agent="Your_Name")
geolocation = geolocator.geocode(address)
lat= geolocation.latitude
long= geolocation.longitude

API_KEY = 'AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI'
BASE_URL2 = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius=50000&types=tourist_attraction&key=AIzaSyBuEH6ka2tFVp4P3zP6r5DRBoBQdTIpYOI"


params = {
    "location": city_name +" "+ country,
    "types": "tourist_attraction",
    "key": API_KEY,
}


response = requests.get(BASE_URL2, params=params)
response_json = json.loads(response.text)
tourist_attractions_city = []

sort_rating_ignoring_unrated = sorted([a for a in response_json['results'] if 'rating' in a], key=lambda x: x['rating'], reverse=True)
sorted_rating= sorted(sort_rating_ignoring_unrated, key=lambda x: x['rating'], reverse=True)

for result in sorted_rating:
    name = result["name"]
    rating = result.get("rating", "not available")
    place_type = result["types"][0]
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    tourist_attractions_city.extend([name,(lat,lng)])
 
    if place_type == "tourist_attraction":
        tourist_attractions_city.extend([name,(lat,lng)])

params = {
    "location": country,
    "types": "tourist_attraction",
    "key": API_KEY,
}


response = requests.get(BASE_URL2, params=params)
response_json = json.loads(response.text)
tourist_attractions_country = []

sort_rating_ignoring_unrated = sorted([a for a in response_json['results'] if 'rating' in a], key=lambda x: x['rating'], reverse=True)
sorted_rating= sorted(sort_rating_ignoring_unrated, key=lambda x: x['rating'], reverse=True)

for result in sorted_rating:
    name = result["name"]
    rating = result.get("rating", "not available")
    place_type = result["types"][0]
    location = result['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    tourist_attractions_country.extend([name,(lat,lng)])
 
    if place_type == "tourist_attraction":
        tourist_attractions_country.extend([name,(lat,lng)])


# In[ ]:


natural_feature_city = get_natural_feature(city_name,country)
natural_parks_city = get_national_parks(city_name, country)
natural_feature_country = get_natural_feature('',country)
natural_parks_country = get_national_parks('', country)

def merged(): 
    result= Convert(natural_feature_city) | Convert(natural_parks_city) | Convert(natural_feature_country) | Convert(natural_parks_country) | Convert(tourist_attractions_city) | Convert(famous_landmarks_city) | Convert(tourist_attractions_country) | Convert(famous_landmarks_country)
    return result

def merged_waypoint(): 
    result=(
    Convert(random.choice(list(Convert(natural_feature_city).items()))) | 
    Convert(random.choice(list(Convert(natural_parks_city).items()))) | 
    Convert(natural_feature_country) | 
    Convert(natural_parks_country) | 
    Convert(random.choice(list(Convert(tourist_attractions_city).items()))) | 
    Convert(random.choice(list(Convert(famous_landmarks_city).items()))) | 
    Convert(tourist_attractions_country) | 
    Convert(famous_landmarks_country))
    return result


# In[ ]:


waypoint_city = merged_waypoint()


# In[ ]:


merged = merged()
coords=[]
for k, v in merged.items():
    coords.append(v)


# In[ ]:


filtered_coords = []
for coord in coords:
  lat, lng = coord
  d_lat = math.radians(lat - start_lat)
  d_lng = math.radians(lng - start_lng)
  a = math.sin(d_lat/2)**2 + math.cos(math.radians(start_lat)) * math.cos(math.radians(lat)) * math.sin(d_lng/2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  distance = 6371 * c  # radius of the Earth in km
  if distance <= radius:
    filtered_coords.append(coord)


# In[ ]:


len(filtered_coords)


# In[ ]:


fig = gmaps.figure(center=(start_lat, start_lng), zoom_level=10)


# In[ ]:


locations = [coord for coord in filtered_coords]


# In[ ]:


len(locations)


# In[ ]:


marker_layer = gmaps.marker_layer(locations)


# In[ ]:


fig.add_layer(marker_layer)


# In[ ]:


import googlemaps
from datetime import datetime
import random


# In[ ]:


gmaps_key = 'AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI'
gmaps_client = googlemaps.Client(key=gmaps_key)


# In[ ]:


origin =locations[0]
destination = origin
waypoints = locations[1:-2]

for waypoint in waypoints:
    distance=gmaps_client.directions(f"{origin[0]},{origin[1]}", f"{waypoint[0]},{waypoint[1]}", mode='driving')
    if distance==[]:
        print('not acessible')
        waypoints.remove(waypoint)
        print(len(waypoints))


# In[ ]:


waypoint


# In[ ]:


if len(waypoints) <= 24:
    markers = waypoints
    waypoints = '|'.join([f"{coord[0]},{coord[1]}" for coord in waypoints])
else:
    random_indices = random.sample(range(len(waypoints)), 24)
    markers = [location for i, location in enumerate(waypoints) if i not in random_indices]
    #waypoints = [filtered_coords[i] for i in random_indices]
lst = []
for i in random_indices:
    lst.append(waypoints[i])
    
#waypoints_str = '|'.join([f"{waypoints[i][0]},{waypoints[i][1]}" for i in random_indices])


# In[ ]:


now = datetime.now()
directions_result=[]
while directions_result==[]:
    if len(waypoints) <= 24:
        markers = waypoints
        waypoints = '|'.join([f"{coord[0]},{coord[1]}" for coord in waypoints])
    else:
        random_indices = random.sample(range(len(waypoints)), 24)
        markers = [location for i, location in enumerate(waypoints) if i not in random_indices]
        #waypoints = [filtered_coords[i] for i in random_indices]
    lst = []
    for i in random_indices:
        lst.append(waypoints[i])

    waypoints_str = '|'.join([f"{waypoints[i][0]},{waypoints[i][1]}" for i in random_indices])
    now = datetime.now()
    directions_result = gmaps_client.directions(origin,
                                             destination,
                                             mode="driving",
                                             waypoints=waypoints_str,
                                             optimize_waypoints=True,
                                             departure_time=now)


# In[ ]:


directions_result


# In[ ]:


waypoint_order = directions_result[0]['waypoint_order']


# In[ ]:


ordered_coords = [lst[i] for i in waypoint_order]


# In[ ]:


fig = gmaps.figure(center=(start_lat, start_lng), zoom_level=10)
locations = [coord for coord in ordered_coords]
marker_layer = gmaps.marker_layer(markers)
fig.add_layer(marker_layer)


# In[ ]:


main = gmaps.directions_layer(origin, destination, waypoints=ordered_coords, optimize_waypoints=True)
fig.add_layer(main)
fig


# In[ ]:




