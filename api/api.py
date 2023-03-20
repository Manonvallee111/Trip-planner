# One-way route
import sys
sys.path.append('../')

## Imports
import googlemaps
import gmaps
import collections
import polyline
import requests
import json
from geopy import distance
from api_keys.api_key import api_key
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence

## Instaciate the API

key = api_key
client = googlemaps.Client(key)
gmaps.configure(api_key=key)

api_endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


## Defining the coordinates of the origin and the destination

### Origin

def origin_coord(start):
    start_id = client.places_autocomplete(start)[0]['place_id']

    start_coord = client.geocode(place_id=start_id)[0]['geometry']['location']

    start_list = (start_coord['lat'], start_coord['lng'])

    return start_list


### Destination

def destination_coord(destination):
    destination_id = client.places_autocomplete(destination)[0]['place_id']

    destination_coord = client.geocode(place_id=destination_id)[0]['geometry']['location']

    dest_list = (destination_coord['lat'], destination_coord['lng'])

    return dest_list

## Split the route based on the maximum distance to be traveled per day

def split_route(start, destination, max_dist, origin_location):
# Takes the origin and the destination and split the route into smaller pieces and get
# the coordinates of every point of the route.
    origin = client.places_autocomplete(start)[0]['description']
    destination = client.places_autocomplete(destination)[0]['description']

    route = client.directions(origin, destination, mode='driving')[0]['legs'][0]['steps']

    sum = 0
    coordinates = []
    for step in route:
        sum = sum + step['distance']['value']
        if sum >= max_dist:
            sum = 0
            coordinates.append(step['start_location'])

    coordinates.append(client.directions(origin, destination, mode='driving')[0]['legs'][0]['steps'][-1]['end_location'])

    stopover = []

    for coord in coordinates:
        coord_tuple = (coord['lat'], coord['lng'])
        stopover.append(coord_tuple)

    stopover.insert(0, origin_location)

    return stopover

def waypoints(route_coord):
    waypoints = route_coord[1:-1]

    city_waypoint = []
    for coord in waypoints:
        city_location = client.places_nearby(coord, radius=200000, type='locality')['results'][0]['geometry']['location']
        city_coord = (city_location['lat'], city_location['lng'])
        city_waypoint.append(city_coord)

    return city_waypoint

def route_points(start, destination):
    origin = client.places_autocomplete(start)[0]['description']
    destination = client.places_autocomplete(destination)[0]['description']

    poly = client.directions(origin, destination, mode='driving')[0]['legs'][0]['steps']

    poly_list = []
    for step in poly:
        poly_list.append(step['polyline']['points'])

    nova_coordenadas = []

    for poly in poly_list:
        coordenadas = polyline.decode(poly)
        total_distance = 0
        for i in range(len(coordenadas) - 1):
            distancia = distance.distance(coordenadas[i], coordenadas[i+1]).km
            total_distance = total_distance + distancia
            if total_distance > 10:
                num_pontos_intermediarios = 7
                lat1, lon1 = coordenadas[i]
                lat2, lon2 = coordenadas[i+1]
                delta_lat = (lat2 - lat1) / (num_pontos_intermediarios + 1)
                delta_lon = (lon2 - lon1) / (num_pontos_intermediarios + 1)
                total_distance=0
                for j in range(num_pontos_intermediarios):
                    nova_lat = lat1 + delta_lat * (j + 1)
                    nova_lon = lon1 + delta_lon * (j + 1)
                    nova_coordenadas.append((nova_lat, nova_lon))

    return nova_coordenadas

### Defining the waypoints coordinates

def every_stop(waypoint_coord, destination_location, origin_location):
    lines_coord = waypoint_coord
    lines_coord.append(destination_location)
    lines_coord.insert(0, origin_location)

    return lines_coord

## Finding nearest hotels and restaurant based in each stopover

def location_marker(stop_coord, type_location):
    location_dest = []

    for stop in stop_coord:
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
                dictionary2 = {'rating': "No Rating"}
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

        location_dest.append(location_info)
        all_locations = []
        for i in range(len(location_dest)):
            all_locations = all_locations + location_dest[i]
    return all_locations

## Getting the famous tourist attractions

def get_country(stop_coord):
    cities = []
    for stop in stop_coord:
        city_location = client.places_nearby(stop, radius=20000, type='locality')['results'][0]['name']
        cities.append(city_location)

    dest_country = []
    for city in cities:
        country_city = client.places_autocomplete(city)[0]['terms'][-1]['value']
        dest_country.append(country_city)

    dest_country = list(dict.fromkeys(dest_country))

    return dest_country

def natural_feature(dest_country, query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    attraction_names = []
    attraction_rating = []
    attraction_coord = []
    natural_info = []
    for country in dest_country:
        querystring = {"query": f'{query} in' + country,
                       "key": key}
        response = requests.request("GET", url, params=querystring)
        data = json.loads(response.text)

        if data['status'] == 'OK':
            results = data['results']


            for result in results:
                dictionary1 = {'name': result['name']}
                attraction_names.append(dictionary1)

                try:
                    dictionary2 = {'rating': result['rating']}
                    attraction_rating.append(dictionary2)
                except:
                    dictionary2 = {'rating': "No Rating"}
                    attraction_rating.append(dictionary2)

                tuple1 = (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
                dictionary3 = {'location': tuple1}
                attraction_coord.append(dictionary3)



            for i in range(len(attraction_names)):
                temp_dict = {}
                temp_dict.update(attraction_names[i])
                temp_dict.update(attraction_coord[i])
                temp_dict.update(attraction_rating[i])
                natural_info.append(temp_dict)

    return natural_info

def landmarks(dest_country, query):
    landmark_info = []
    landmark_names = []
    landmark_rating = []
    landmark_coord = []
    for country in dest_country:
        query = f'{country} landmarks'
        params = {
        'query': query,
        'key': key}

        response = requests.get(base_url, params=params)
        data = response.json()

        results = sorted(data['results'], key=lambda x: x['user_ratings_total'], reverse=True)

        for result in results[:60]:
            dictionary1 = {'name': result['name']}
            landmark_names.append(dictionary1)

            try:
                dictionary2 = {'rating': result['rating']}
                landmark_rating.append(dictionary2)
            except:
                dictionary2 = {'rating': "No Rating"}
                landmark_rating.append(dictionary2)

            tuple1 = (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
            dictionary3 = {'location': tuple1}
            landmark_coord.append(dictionary3)

        for i in range(len(landmark_names)):
            temp_dict = {}
            temp_dict.update(landmark_names[i])
            temp_dict.update(landmark_coord[i])
            temp_dict.update(landmark_rating[i])
            landmark_info.append(temp_dict)
    return landmark_info

## Generate the map, with the main route and the stopover, including hotels and restaurants for each stop.
def main_route(origin_location, destination_location, waypoint_coord, hotel_markers, rest_markers, natural_markers, route_markers, park_markers, landmark_markers, tourism_markers):
    fig = gmaps.figure()

    main = gmaps.directions_layer(origin_location, destination_location, waypoints=waypoint_coord)

    route_markers = gmaps.symbol_layer(route_markers, fill_color='#00BFFF', stroke_color='#00BFFF',  scale=2)

    hotel_location = [hotel['location'] for hotel in hotel_markers]
    info_box_template = """
    <dl>
    <dt>Hotel</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    <dt>Adress</dt><dd>{adress}</dd>
    </dl>
    """
    info_hotel = [info_box_template.format(**hotel) for hotel in hotel_markers]
    hotel_markers = gmaps.symbol_layer(hotel_location, hover_text='Hotel', fill_color='#FF82AB', stroke_color='#FF82AB',  scale=3, info_box_content=info_hotel)

    ###########################

    rest_location = [rest['location'] for rest in rest_markers]
    info_box_template = """
    <dl>
    <dt>Restaurant</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    <dt>Adress</dt><dd>{adress}</dd>
    </dl>
    """
    info_rest = [info_box_template.format(**rest) for rest in rest_markers]
    rest_markers = gmaps.symbol_layer(rest_location, hover_text='Restaurant', fill_color='#FFA500', stroke_color='#FFA500',  scale=3, info_box_content=info_rest)

    ###########################

    natural_location = [natural['location'] for natural in natural_markers]
    info_box_template = """
    <dl>
    <dt>Natural Feature</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    </dl>
    """
    info_natural = [info_box_template.format(**natural) for natural in natural_markers]
    natural_markers = gmaps.symbol_layer(natural_location, hover_text='Natural Feature', fill_color='#3D9140', stroke_color='#3D9140',  scale=5, info_box_content=info_natural)

    ###########################

    park_location = [park['location'] for park in park_markers]
    info_box_template = """
    <dl>
    <dt>National Park</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    </dl>
    """
    info_park = [info_box_template.format(**park) for park in park_markers]
    park_markers = gmaps.symbol_layer(park_location, hover_text='National Park', fill_color='#006400', stroke_color='#006400',  scale=5, info_box_content=info_park)

    ###########################

    landmark_location = [landmark['location'] for landmark in landmark_markers]
    info_box_template = """
    <dl>
    <dt>Landmark</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    </dl>
    """
    info_landmark = [info_box_template.format(**landmark) for landmark in landmark_markers]
    landmark_markers = gmaps.symbol_layer(landmark_location, hover_text='Landmark', fill_color='#8E388E', stroke_color='#8E388E',  scale=5, info_box_content=info_landmark)

    ###########################

    attraction_location = [attraction['location'] for attraction in tourism_markers]
    info_box_template = """
    <dl>
    <dt>Tourist Attraction</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    </dl>
    """
    info_attraction = [info_box_template.format(**attraction) for attraction in tourism_markers]
    attraction_markers = gmaps.symbol_layer(attraction_location, hover_text='Tourist Attraction', fill_color='#CD0000', stroke_color='#CD0000',  scale=4, info_box_content=info_attraction)

    ###########################

    fig.add_layer(main)
    fig.add_layer(route_markers)
    fig.add_layer(hotel_markers)
    fig.add_layer(rest_markers)
    fig.add_layer(natural_markers)
    fig.add_layer(park_markers)
    fig.add_layer(landmark_markers)
    fig.add_layer(attraction_markers)

    return fig
