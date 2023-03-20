import streamlit as st
import sys
import datetime
import requests

sys.path.append('../api/')

from api import origin_coord,destination_coord,split_route,waypoints,route_points,every_stop,location_marker,location_marker,get_country,natural_feature,natural_feature,landmarks,main_route

'''
# Trip Planner

This front queries the Google Maps API
'''
try:
    # user input
    start = st.text_input('Origin:')
    destination = st.text_input('Destination:')
    max_dist = (st.number_input('Enter the duration to drive per day, in hours:')) * 80 * 1000

    st.button('Create Route')

    origin_location = origin_coord(start)
    destination_location = destination_coord(destination)
    route_coord = split_route(start, destination, max_dist, origin_location)
    waypoint_coord = waypoints(route_coord)
    route_markers = route_points(start, destination)
    stop_coord = every_stop(waypoint_coord, destination_location, origin_location)
    hotel_markers = location_marker(stop_coord, 'lodging')
    rest_markers = location_marker(stop_coord, 'restaurant')
    tourism_markers = location_marker(stop_coord, 'tourist_attraction')
    dest_country = get_country(stop_coord)
    natural_markers = natural_feature(dest_country, 'natural feature')
    park_markers = natural_feature(dest_country, 'national park')
    landmark_markers = landmarks(dest_country, 'landmark')
    fig_oneway = main_route(origin_location, destination_location, waypoint_coord, hotel_markers, rest_markers, natural_markers, route_markers, park_markers, landmark_markers, tourism_markers)

    fig = main_route(origin_location, destination_location, waypoint_coord, hotel_markers, rest_markers, natural_markers, route_markers, park_markers, landmark_markers, tourism_markers)
    from ipywidgets import embed
    snippet = embed.embed_snippet(views=fig)
    html = embed.html_template.format(title="", snippet=snippet)

    import streamlit.components.v1 as components
    components.html(html, height=1024,width=1024)
except:
    pass
