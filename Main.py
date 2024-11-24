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
    return lon, lat


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
        coords_coffeeshop = coffee['Longitude_WGS84'], coffee['Latitude_WGS84']
        coffeeshop['Distance'] = (distance.distance(coords[-90:90],
                                                    coords_coffeeshop).km)
        coffeeshop['Latitude'] = coffee['Latitude_WGS84']
        coffeeshop['Longitude'] = coffee['Longitude_WGS84']
        coffee_information.append(coffeeshop)

    sorted_coffeeshop = sorted(coffee_information, key=get_coffeeshop_distance)
    first_coffeeshop = sorted_coffeeshop[:5]
    
    m = folium.Map(coords[-90:90], zoom_start=12)

    folium.Marker(
        location=(first_coffeeshop[0]['Latitude'],
                  first_coffeeshop[0]['Longitude']),
        tooltip='Click me!',
        popup=first_coffeeshop[0]['Name'],
        icon=folium.Icon(color='red'),
    ).add_to(m)

    folium.Marker(
        location=(first_coffeeshop[1]['Latitude'],
                  first_coffeeshop[1]['Longitude']),
        tooltip='Click me!',
        popup=first_coffeeshop[1]['Name'],
        icon=folium.Icon(color='red'),
    ).add_to(m)

    folium.Marker(
        location=(first_coffeeshop[2]['Latitude'],
                  first_coffeeshop[2]['Longitude']),
        tooltip='Click me!',
        popup=first_coffeeshop[2]['Name'],
        icon=folium.Icon(color='red'),
    ).add_to(m)

    folium.Marker(
        location=(first_coffeeshop[3]['Latitude'],
                  first_coffeeshop[3]['Longitude']),
        tooltip='Click me!',
        popup=first_coffeeshop[3]['Name'],
        icon=folium.Icon(color='red'),
    ).add_to(m)

    folium.Marker(
        location=(first_coffeeshop[4]['Latitude'],
                  first_coffeeshop[4]['Longitude']),
        tooltip='Click me!',
        popup=first_coffeeshop[4]['Name'],
        icon=folium.Icon(color='red'),
    ).add_to(m)
    m.save('coffeeshops.html')

if __name__ == '__main__':
    main()