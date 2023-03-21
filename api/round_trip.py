
import math
import requests
import json

import ipywidgets as widgets
import gmaps.datasets
import requests
import json

import gmaps
import gmaps.datasets
import seaborn as sns
import matplotlib.pyplot as plt
import random
import googlemaps

from googlemaps import places
from math import sin, cos, sqrt, atan2, radians
from datetime import timedelta,datetime
from geopy.geocoders import Nominatim

import random
import collections
collections.Iterable = collections.abc.Iterable


gmaps.configure(api_key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')
client = googlemaps.Client('AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')
google = googlemaps.Client(key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')


#city_name = input("Where will you start your road trip? ")
#duration = int(input("Enter the duration of the trip in days: "))-2
#hours_per_day = int(input("Enter the number of hours per day you are willing to drive: "))

def round_trip(city_name,duration,hours_per_day):
    geocode_result = google.geocode(city_name)

    duration_timedelta = timedelta(days=duration)
    total_hours = duration_timedelta.days * hours_per_day
    total_distance = total_hours * 80
    radius = (total_distance) / (2 * 3.14159)

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



    max_distance_per_day_meters = 80*(hours_per_day)
    # max_distance_per_day_meters

    # radius

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



    natural_feature_city = get_natural_feature(city_name,country)
    natural_parks_city = get_national_parks(city_name, country)
    natural_feature_country = get_natural_feature('',country)
    natural_parks_country = get_national_parks('', country)

    def merged():
        result= Convert(natural_feature_country) | Convert(natural_parks_country) | Convert(tourist_attractions_city) | Convert(famous_landmarks_city) | Convert(tourist_attractions_country) | Convert(famous_landmarks_country)
        return result

    def merged_waypoint():
        result=(
        Convert(random.choice(list(Convert(natural_feature_city).items()))) |
        Convert(natural_feature_country) |
        Convert(natural_parks_country) |
        Convert(random.choice(list(Convert(famous_landmarks_city).items()))) |
        Convert(tourist_attractions_country) |
        Convert(famous_landmarks_country))
        return result



    important_markers = Convert(natural_feature_country) | Convert(natural_parks_country) | Convert(famous_landmarks_city) | Convert(tourist_attractions_country)



    waypoint_city = merged_waypoint()


    merged = merged_waypoint()
    coords=[]
    for k, v in merged.items():
        coords.append(v)


    filtered_coords = []
    filtered_coords_dict = []
    for coord in coords:
        lat, lng = coord
        d_lat = math.radians(lat - start_lat)
        d_lng = math.radians(lng - start_lng)
        a = math.sin(d_lat/2)**2 + math.cos(math.radians(start_lat)) * math.cos(math.radians(lat)) * math.sin(d_lng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6371 * c  # radius of the Earth in km
        if distance <= radius:
            filtered_coords.append(coord)
            # Get the values from the dictionary as a list
            values = list(merged.values())
            # Find the index of the value in the list
            index = values.index(coord)
            # Get the key from the dictionary using the index
            result = list(merged.keys())[index]
            # The result is printed
            temp_dict = {}
            temp_dict.update(name=result)
            temp_dict.update(location=coord)
            filtered_coords_dict.append(temp_dict)


    filtered_coords_dict


    print(len(merged))
    print(len(filtered_coords))


    merged


    #import re
    #for lat, lng in filtered_coords:
    #   location = geolocator.reverse((lat, lng), exactly_one=True)
    #  # extract the name of the attraction from the address
    # name = re.sub(r',?\s*\b\d{5}\b\s*', '', location.address).split(',')[0]
        #print(name)


    fig = gmaps.figure(center=(start_lat, start_lng), zoom_level=10)


    locations = [coord for coord in filtered_coords]


    all_marker_layer = gmaps.marker_layer(locations)
    fig.add_layer(all_marker_layer)


    fig.add_layer(all_marker_layer)


    fig


    gmaps_key = 'AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI'
    gmaps_client = googlemaps.Client(key=gmaps_key)


    origin =locations[0]
    destination = origin
    waypoints = locations[1:-2]
    waypoints_not_filtered = locations[1:-2]

    for waypoint in waypoints:
        distance=gmaps_client.directions(f"{origin[0]},{origin[1]}", f"{waypoint[0]},{waypoint[1]}", mode='driving')
        distance_origin=client.distance_matrix(origin,waypoints[0], mode='driving')
        distance_origin=distance_origin['rows'][0]['elements'][0]['distance']['value']
        if distance==[]:
            print('not acessible')
            waypoints.remove(waypoint)
            print(len(waypoints))
        if distance_origin<5*1000:
            print('too close')
            waypoints.remove(waypoint)
            print(len(waypoints))


    now = datetime.now()
    directions_result=[]
    lst=[]
    while directions_result==[]:
        if len(waypoints) <= 24:
            markers = waypoints
            waypoints_str = '|'.join([f"{coord[0]},{coord[1]}" for coord in waypoints])
        else:
            random_indices = random.sample(range(len(waypoints)), 24)
            markers = [location for i, location in enumerate(waypoints) if i not in random_indices]
            #waypoints = [filtered_coords[i] for i in random_indices]

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


    waypoint_order = directions_result[0]['waypoint_order']


    if lst!=[]:
        ordered_coords = [lst[i] for i in waypoint_order]
    else:
        ordered_coords=markers


    fig = gmaps.figure(center=(start_lat, start_lng), zoom_level=10)
    all_locations = locations
    locations = [coord for coord in ordered_coords]
    marker_layer = gmaps.marker_layer(markers)
    fig.add_layer(marker_layer)


    main = gmaps.directions_layer(origin, destination, waypoints=ordered_coords, optimize_waypoints=True)
    fig.add_layer(main)


    # # Finding nearby cities


    total_distance = 0
    for step in directions_result[0]['legs'][0]['steps']:
        total_distance += step['distance']['value']


    total_distance #in km


    route_coords = []
    for step in directions_result[0]['legs']:
        start_loc = step['start_location']
        end_loc = step['end_location']
        route_coords.append((start_loc['lat'], start_loc['lng']))
        route_coords.append((end_loc['lat'], end_loc['lng']))


    from googlemaps import Client
    client = Client(key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    geolocator = Nominatim(user_agent="my_app")
    #gmaps = googlemaps.Client(key='AIzaSyDnNZeV-Rm2oWkZxNWMF2ZBvnCuCMYbVAI')



    # Use Google Maps Places API to search for nearby cities within a 50km radius of each coordinate that is a multiple of the defined distance interval (x)
    #nearby_cities = []
    #for i in range(len(route_coords)):
    #   if i % (x / total_distance) == 0:
    #      places_result = client.places_nearby(location=route_coords[i], radius=50000, type='locality')
    #     for place in places_result['results']:
        #        if place['name'] not in nearby_cities:
        #           nearby_cities.append(place['name'])


    # Print the list of nearby cities
    #nearby_cities


    total_distance = 0
    total_time = 0
    last_city = None
    stop_cities = []



    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            # Get the distance and duration of the step
            distance = step['distance']['value']
            duration = step['duration']['value']

            # Calculate the distance traveled and time taken
            total_distance += distance
            total_time += duration

            # If the distance traveled is greater than 50km, find the nearest city
            if total_distance >= 50*1000:
                # Find the latitude and longitude of the last point in the step
                end_location = step['end_location']
                lat = end_location['lat']
                lng = end_location['lng']

                # Use the reverse geocoding API to find the city nearest to the current point
                reverse_geocode_result = google.reverse_geocode((lat, lng))
                for address_component in reverse_geocode_result[0]['address_components']:
                    if any(
                        item in ['locality','administrative_area_level_3','administrative_area_level_4']
                        for item in address_component['types']
                    ):
                        city = address_component['long_name']
                        break

                # Add the city to the list of stop cities
                if city and city != last_city:
                    stop_cities.append(city + ' '+ country)
                    last_city = city

                # Reset the distance traveled to the remaining distance
                remaining_distance = total_distance - 50*1000
                total_distance = 0



    for city in stop_cities:
        geocode_result = google.geocode(city)
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        symbol = {
            "path": "circle",
            "fillColor": "blue",
            "fillOpacity": 1,
            "strokeWeight": 0,
            "scale": 7
        }
        marker_layer = gmaps.marker_layer([(lat, lng)], hover_text=city)
        symbol_layer = gmaps.symbol_layer([(lat, lng)], fill_color='maroon', stroke_color='maroon',hover_text=city,scale=6 )
        fig.add_layer(symbol_layer)



    fig


    # # Adding hotels and restaurants to the city_stops


    stop_cities


    location


    stop_cities_coordinates= []

    for city in stop_cities:
        geocode_result = google.geocode(city)
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        # Add the coordinates to the list
        temp_dict = {}
        temp_dict.update(name=city)
        temp_dict.update(location=(lat, lng))
        stop_cities_coordinates.append(temp_dict)
    print(stop_cities_coordinates)


    temp_dict


    def location_marker(waypoint_coord,type_location):
        location_dest = []
        all_locations = []
        for stop in waypoint_coord:
            stop=stop['location']
            location_search = []
            locations = client.places_nearby(stop, radius=100000, type=type_location)['results']
            location_search.append(locations)
            location_names = []
            location_rating = []
            location_coord = []
            location_adress = []
            for result in location_search[0]:
                dictionary1 = {'name': result['name']}
                location_names.append(dictionary1)
                try:
                    dictionary2 = {'rating': result['rating']}
                    location_rating.append(dictionary2)
                except:
                    dictionary2 = {'rating': 0
                                }
                    location_rating.append(dictionary2)
                tuple1 = (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
                dictionary3 = {'location': tuple1}
                location_coord.append(dictionary3)
                dictionary4 = {'adress': result['vicinity']}
                location_adress.append(dictionary4)
            location_info = []
            for i in range(len(location_names)):
                temp_dict = {}
                temp_dict.update(location_names[i])
                temp_dict.update(location_coord[i])
                temp_dict.update(location_rating[i])
                temp_dict.update(location_adress[i])
                location_info.append(temp_dict)
            sorted_rating= sorted(location_info, key=lambda x: x['rating'], reverse=True)
            location_dest.append(sorted_rating[:8])
            for i in range(len(location_dest)):
                all_locations = all_locations + location_dest[i]

        return all_locations


    hotel_dest = location_marker(stop_cities_coordinates, 'lodging')


    rest_dest = location_marker(stop_cities_coordinates, 'restaurant')


    # # Generating map


    import pandas as pd


    from geopy import distance
    import numpy as np

    origin_list=[]
    destination_list=[]
    for x in range(len(route_coords)-1):
        directions_result = client.directions(route_coords[x], route_coords[x+1], mode='driving')
        for step in directions_result[0]['legs'][0]['steps']:
            origin_start = step['start_location']
            destination_end = step['end_location']
            origin_list.append(origin_start)
            destination_list.append(destination_end)


    import polyline

    poly_list = []
    for orgin, destination in zip(origin_list,destination_list):
        poly = client.directions(origin, destination, mode='driving')[0]['legs'][0]['steps']
        for step in poly:
            poly_list.append(step['polyline']['points'])



    total_distance=0
    route_marker = []
    for poly in poly_list:
        coordenadas = polyline.decode(poly)
        for i in range(len(coordenadas) - 1):
            distancia = distance.distance(coordenadas[i], coordenadas[i+1]).km
            total_distance = total_distance + distancia
            if total_distance > 100:
                num_pontos_intermediarios = 10
                lat1, lon1 = coordenadas[i]
                lat2, lon2 = coordenadas[i+1]
                delta_lat = (lat2 - lat1) / (num_pontos_intermediarios + 1)
                delta_lon = (lon2 - lon1) / (num_pontos_intermediarios + 1)
                total_distance=0
                for j in range(num_pontos_intermediarios):
                    nova_lat = lat1 + delta_lat * (j + 1)
                    nova_lon = lon1 + delta_lon * (j + 1)
                    route_marker.append((nova_lat, nova_lon))
            elif total_distance > 50:
                num_pontos_intermediarios = 5
                lat1, lon1 = coordenadas[i]
                lat2, lon2 = coordenadas[i+1]
                delta_lat = (lat2 - lat1) / (num_pontos_intermediarios + 1)
                delta_lon = (lon2 - lon1) / (num_pontos_intermediarios + 1)
                total_distance=0
                for j in range(num_pontos_intermediarios):
                    nova_lat = lat1 + delta_lat * (j + 1)
                    nova_lon = lon1 + delta_lon * (j + 1)
                    route_marker.append((nova_lat, nova_lon))
            elif total_distance > 20:
                num_pontos_intermediarios = 1
                lat1, lon1 = coordenadas[i]
                lat2, lon2 = coordenadas[i+1]
                delta_lat = (lat2 - lat1) / (num_pontos_intermediarios + 1)
                delta_lon = (lon2 - lon1) / (num_pontos_intermediarios + 1)
                total_distance=0
                for j in range(num_pontos_intermediarios):
                    nova_lat = lat1 + delta_lat * (j + 1)
                    nova_lon = lon1 + delta_lon * (j + 1)
                    route_marker.append((nova_lat, nova_lon))


    def round_route(origin, destination, hotel_markers, ordered_coords, rest_markers, city_markers,marker_layer, route_marker,locations,filtered_coords_dict):
        fig = gmaps.figure()

        main = gmaps.directions_layer(origin, destination, waypoints=ordered_coords, optimize_waypoints=True)
        route_marker = gmaps.symbol_layer(route_marker, fill_color='#00BFFF', stroke_color='#00BFFF',  scale=2)

        filtered_location = [filtered_coords_dict['location'] for filtered_coords_dict in filtered_coords_dict]
        info_box_template = """
        <dl>
        <dt>Place to Visit</dt><dd>{name}</dd>
        </dl>
        """
        info_filtered_location = [info_box_template.format(**filtered) for filtered in filtered_coords_dict]
        filtered_location_markers = gmaps.marker_layer(filtered_location,info_box_content=info_filtered_location)

        ciy_location = [city['location'] for city in city_markers]
        info_box_template = """
        <dl>
        <dt>City</dt><dd>{name}</dd>
        </dl>
        """
        info_city = [info_box_template.format(**city) for city in city_markers]
        city_markers = gmaps.symbol_layer(ciy_location, hover_text='City', fill_color='maroon', stroke_color='maroon',  scale=6, info_box_content=info_city)


        hotel_location = [hotel['location'] for hotel in hotel_markers]
        info_box_template = """
        <dl>
        <dt>Hotel</dt><dd>{name}</dd>
        <dt>Rating</dt><dd>{rating}</dd>
        </dl>
        """
        info_hotel = [info_box_template.format(**hotel) for hotel in hotel_markers]
        hotel_markers = gmaps.symbol_layer(hotel_location, hover_text='Hotel', fill_color='#CD9B1D', stroke_color='#CD9B1D',  scale=3, info_box_content=info_hotel)



        rest_location = [rest['location'] for rest in rest_markers]
        info_box_template = """
        <dl>
        <dt>Restaurant</dt><dd>{name}</dd>
        <dt>Rating</dt><dd>{rating}</dd>
        </dl>
        """
        info_rest = [info_box_template.format(**hotel) for hotel in rest_markers]
        rest_markers = gmaps.symbol_layer(rest_location, hover_text='Restaurant', fill_color='#CD6090', stroke_color='#CD6090',  scale=3, info_box_content=info_rest)

        all_marker_layer = gmaps.marker_layer(locations)
        fig.add_layer(all_marker_layer)
        fig.add_layer(hotel_markers)
        fig.add_layer(rest_markers)
        fig.add_layer(main)
        fig.add_layer(city_markers)
        fig.add_layer(symbol_layer)
        fig.add_layer(marker_layer)
        fig.add_layer(route_marker)
        fig.add_layer(filtered_location_markers)
        return fig


    map2 = round_route(origin, hotel_dest, ordered_coords, rest_dest, stop_cities_coordinates,all_marker_layer,route_marker, locations,filtered_coords_dict)
    return map2

import streamlit as st
st.markdown('test')
st.markdown(round_trip('madrid',5,4))
