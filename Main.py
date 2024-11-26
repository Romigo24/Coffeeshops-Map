import requests
from geopy import distance
import json
import folium
import os
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_coffeeshop_distance(coffeeshop):
    return coffeeshop['Distance']


def main():
    load_dotenv()
    apikey = os.environ['YANDEX_API_KEY']
    adress = input('Где вы находитесь?')
    coords = fetch_coordinates(apikey, adress)
    with open("coffee.json", "r", encoding='CP1251') as my_file:
        contents_json = my_file.read()
    file_contents = json.loads(contents_json)

    coffee_information = []

    for coffee in file_contents:
        coffeeshop = dict()
        coffeeshop['Name'] = coffee['Name']
        coords_coffeeshop = coffee['Latitude_WGS84'], coffee['Longitude_WGS84']
        coffeeshop['Distance'] = (distance.distance(coords,
                                                    coords_coffeeshop).km)
        coffeeshop['Latitude'] = coffee['Latitude_WGS84']
        coffeeshop['Longitude'] = coffee['Longitude_WGS84']
        coffee_information.append(coffeeshop)

    sorted_coffeeshop = sorted(coffee_information, key=get_coffeeshop_distance)
    first_coffeeshop = sorted_coffeeshop[:5]

    m = folium.Map(coords, zoom_start=12)

    folium.Marker(
        location = coords,
        tooltip = 'Click me!',
        popup = 'Me',
        icon = folium.Icon(icon='user', color='blue'),
    ).add_to(m)

    for coffeeshop in first_coffeeshop:
        folium.Marker(
            location = (coffeeshop['Latitude'],
                      coffeeshop['Longitude']),
            tooltip = 'Click me!',
            popup = coffeeshop['Name'],
            icon = folium.Icon(color='red'),
        ).add_to(m)
    m.save('coffeeshops.html')

if __name__ == '__main__':
    main()