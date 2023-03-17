import streamlit as st
import sys
import datetime
import requests

sys.path.append('../api/')

from api import origin_coord, destination_coord, split_route, waypoints, location_marker, attraction_feature,main_route,route
'''
# Trip Planner

This front queries the Google Maps API
'''

# user input
start = st.text_input('Origin:')
destination = st.text_input('Destination:')
max_dist = (st.number_input('Maximum distance per day:')) * 80 * 1000

st.button('Create Route')

query = "natural feature"
origin_location = origin_coord(start)
destination_location = destination_coord(destination)
route_coord = split_route(start, destination, max_dist)
waypoint_coord = waypoints(route_coord)
hotel_markers = location_marker(waypoint_coord, 'lodging')
rest_markers = location_marker(waypoint_coord, 'restaurant')
natural_markers = attraction_feature(start, query)

fig = main_route(origin_location, destination_location, waypoint_coord, hotel_markers, rest_markers, natural_markers)
route_fig = route(origin_location, destination_location, waypoint_coord)

from ipywidgets import embed
snippet = embed.embed_snippet(views=fig)
html = embed.html_template.format(title="", snippet=snippet)

import streamlit.components.v1 as components
components.html(html, height=1024,width=1024)
