import secrets_1
import streamlit as st
import requests
import folium
from geopy.geocoders import Nominatim
from io import BytesIO
import matplotlib.pyplot as plt


API_KEY = secrets_1.api

def get_coordinates(location):
    url = f'https://api.tomtom.com/search/2/geocode/{location}.json'
    params = {'key': API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('results') and data['results'][0].get('position'):
        latitude, longitude = data['results'][0]['position']['lat'], data['results'][0]['position']['lon']
        return latitude, longitude
    else:
        raise ValueError("Location not found. Please try again with a different place name.")

def calculate_route(starting_point, destination):
    starting_point_str = f"{starting_point[0]},{starting_point[1]}"
    destination_str = f"{destination[0]},{destination[1]}"

    url = f'https://api.tomtom.com/routing/1/calculateRoute/{starting_point_str}:{destination_str}/json'
    params = {'key': API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if 'routes' in data and data['routes']:
        return data['routes'][0]['legs'][0]['points']
    else:
        raise ValueError("No route found. Please check your starting point and destination.")


def display_map(starting_point, destination, route_data):
    m = folium.Map()

    # Add markers for the starting point and destination
    folium.Marker(location=starting_point, tooltip='Starting Point', icon=folium.Icon(icon='play')).add_to(m)
    folium.Marker(location=destination, tooltip='Destination', icon=folium.Icon(icon='stop')).add_to(m)

    points_list = [[point['latitude'], point['longitude']] for point in route_data]
    folium.PolyLine(locations=points_list, color='blue', dash_array='5, 5').add_to(m)

    # Render the map as an HTML string
    map_html = m._repr_html_()

    # Display the map using st.components.v1.html
    st.components.v1.html(map_html, height=600)

def main():
    st.title('Guiding Your Journey, Your Way')
    
    starting_point = st.text_input('Enter the starting point:')
    destination = st.text_input('Enter the destination:')

    if st.button('Plan Route'):
        try:
            starting_location = get_coordinates(starting_point)
            destination_location = get_coordinates(destination)
            route_data = calculate_route(starting_location, destination_location)
            display_map(starting_location, destination_location, route_data)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
