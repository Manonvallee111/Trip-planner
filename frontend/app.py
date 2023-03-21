import streamlit as st
import sys
import datetime
import requests

sys.path.append('../api/')

from api import origin_coord, destination_coord, split_route, waypoints, route_points, every_stop, get_city_names, location_marker, location_marker, get_country, natural_feature, natural_feature, landmarks, main_route
from round_trip import round_trip

st.set_page_config(
            page_title="Road Trip Planner", # => Quick reference - Streamlit
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


with st.sidebar:
    '''
    # Road Trip Planner
    '''
    direction = st.radio('Select a Trip you want to do', ('One way Trip', 'Round Trip', 'Destination Attractions'))
    st.write(direction)

    if direction == 'One way Trip':
        try:
            # user input
            start = st.text_input('Origin:')
            destination = st.text_input('Destination:')
            max_dist = (st.number_input("Enter the number of hours per stop you are willing to drive:")) * 80 * 1000

            st.button('Create Route')

            origin_location = origin_coord(start)
            destination_location = destination_coord(destination)
            route_coord = split_route(start, destination, max_dist, origin_location)
            waypoint_coord = waypoints(route_coord)
            route_markers = route_points(start, destination)
            stop_coord = every_stop(waypoint_coord, destination_location, origin_location)
            city_names = get_city_names(stop_coord)
            hotel_markers = location_marker(stop_coord, 'lodging')
            rest_markers = location_marker(stop_coord, 'restaurant')
            tourism_markers = location_marker(stop_coord, 'tourist_attraction')
            dest_country = get_country(stop_coord)
            natural_markers = natural_feature(dest_country, 'natural feature')
            park_markers = natural_feature(dest_country, 'national park')
            landmark_markers = landmarks(dest_country, 'landmark')
            fig_oneway = main_route(origin_location, destination_location, waypoint_coord, hotel_markers, rest_markers, natural_markers, route_markers, park_markers, landmark_markers, tourism_markers, city_names)

        except:
            pass

    elif direction == 'Round Trip':

        try:
            city_name = st.text_input("Where will you start your road trip?")
            duration = (st.number_input("Enter the duration of the trip in days:"))-2
            hours_per_day = int(st.number_input("Enter the number of hours per day you are willing to drive:"))

            st.button('Create Route')

            map2=round_trip(city_name, duration, hours_per_day)
        except:
            pass

col1, col2, col3 = st.columns(3)

with col1:
    try:
        from ipywidgets import embed
        snippet = embed.embed_snippet(views=fig_oneway)
        html = embed.html_template.format(title="", snippet=snippet)

        import streamlit.components.v1 as components
        components.html(html, height=1200,width=768)
    except:
        pass

    try:
        from ipywidgets import embed
        snippet = embed.embed_snippet(views=map2)
        html = embed.html_template.format(title="", snippet=snippet)

        import streamlit.components.v1 as components
        components.html(html, height=1200,width=768)
    except:
        pass

with col2:
    st.write('')

with col3:
    st.write('')

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#     try:
#         from ipywidgets import embed
#         snippet = embed.embed_snippet(views=fig_oneway)
#         html = embed.html_template.format(title="", snippet=snippet)

#         import streamlit.components.v1 as components
#         components.html(html, height=2048,width=1024)
#     except:
#             pass

#     try:
#         from ipywidgets import embed
#         snippet = embed.embed_snippet(views=map2)
#         html = embed.html_template.format(title="", snippet=snippet)

#         import streamlit.components.v1 as components
#         components.html(html, height=1024,width=1024)
#     except:
#             pass
