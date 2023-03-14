import googlemaps

api_key = 'AIzaSyA-VGNvkw5H7tS-KoMqE1SLnnB2NAkWifk'
gmaps = googlemaps.Client(api_key)

def split_route(start_loc, dest):
# Takes the origin and the destination and split the route into smaller pieces and get
# the coordinates of every point of the route.
    origin = gmaps.places_autocomplete(start_loc)[0]['description']
    destination = gmaps.places_autocomplete(dest)[0]['description']

    route = gmaps.directions(origin, destination, mode='driving')[0]['legs'][0]['steps']

    sum = 0
    coordinates = []
    for step in route:
        sum = sum + step['distance']['value']
        if sum>=50000:
            sum = 0
            coordinates.append(step['start_location'])

    return coordinates


print(split_route('barcelona', 'madrid'))
