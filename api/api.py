# One-way route
import sys
sys.path.append('../api_keys/')

## Imports
import googlemaps
import gmaps
import collections
from api_key import api_key
collections.Iterable = collections.abc.Iterable
collections.Sequence = collections.abc.Sequence

import requests
import json

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

def split_route(start, destination, max_dist):
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

    return stopover
### Defining the waypoints coordinates

def waypoints(stop_coord):
    waypoints = stop_coord[1:-1]

    city_waypoint = []
    for coord in waypoints:
        city_location = client.places_nearby(coord, radius=20000, type='locality')['results'][0]['geometry']['location']
        city_coord = (city_location['lat'], city_location['lng'])
        city_waypoint.append(city_coord)

    return city_waypoint

## Finding nearest hotels and restaurant based in each stopover

def location_marker(waypoint_coord,type_location):
    location_dest = []
    all_locations = []
    for stop in waypoint_coord:
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

        for i in range(len(location_dest)):
            all_locations = all_locations + location_dest[i]
    return all_locations

## Getting the famous tourist attractions

query = "natural feature"

def attraction_feature(place, query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    querystring = {"query": f'{query} in' + place, "key": key}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)

    locations = []

    if data['status'] == 'OK':
        results = data['results']

        attraction_names = []
        attraction_rating = []
        attraction_coord = []

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

        attraction_info = []

        for i in range(len(attraction_names)):
            temp_dict = {}
            temp_dict.update(attraction_names[i])
            temp_dict.update(attraction_coord[i])
            temp_dict.update(attraction_rating[i])
            attraction_info.append(temp_dict)


#     else:
#             print("Error:", data['status'])

    return attraction_info

def route(origin_coord, destination_coord, waypoints):
    fig = gmaps.figure()
    main = gmaps.directions_layer(origin_coord, destination_coord, waypoints=waypoints)
    fig.add_layer(main)
    return fig

## Generate the map, with the main route and the stopover, including hotels and restaurants for each stop.
def main_route(origin_coord, destination_coord, waypoints, hotel_markers, rest_markers, natural_markers):
    fig = gmaps.figure()

    main = gmaps.directions_layer(origin_coord, destination_coord, waypoints=waypoints)

    hotel_location = [hotel['location'] for hotel in hotel_markers]
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    <dt>Adress</dt><dd>{adress}</dd>
    </dl>
    """
    info_hotel = [info_box_template.format(**hotel) for hotel in hotel_markers]
    hotel_markers = gmaps.symbol_layer(hotel_location, hover_text='Hotel', fill_color='red', stroke_color='red',  scale=4, info_box_content=info_hotel)

    rest_location = [rest['location'] for rest in rest_markers]
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    <dt>Adress</dt><dd>{adress}</dd>
    </dl>
    """
    info_rest = [info_box_template.format(**rest) for rest in rest_markers]
    rest_markers = gmaps.symbol_layer(rest_location, hover_text='Restaurant', fill_color='red', stroke_color='blue',  scale=4, info_box_content=info_rest)

    natural_location = [natural['location'] for natural in natural_markers]
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>Rating</dt><dd>{rating}</dd>
    </dl>
    """
    info_natural = [info_box_template.format(**natural) for natural in natural_markers]
    natural_markers = gmaps.symbol_layer(natural_location, hover_text='Natural Feature', fill_color='red', stroke_color='green',  scale=4, info_box_content=info_natural)

    fig.add_layer(main)
    fig.add_layer(hotel_markers)
    fig.add_layer(rest_markers)
    fig.add_layer(natural_markers)

    return fig
