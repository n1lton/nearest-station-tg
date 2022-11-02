from geopy.geocoders import Nominatim
from math import sqrt
from json import load
import osmnx as ox
import networkx as nx

geolocator = Nominatim(user_agent="nearest_station")


def get_cords(start_point, end_point):
    lat_s = float(start_point[0])
    lon_s = float(start_point[1])
    lat_e = float(end_point[0])
    lon_e = float(end_point[1])

    north = max(lat_s, lat_e) + 0.003
    south = min(lat_s, lat_e) - 0.003
    east = max(lon_s, lon_e) + 0.003
    west = min(lon_s, lon_e) - 0.003

    return north, south, east, west



def create_map(start_point: tuple, end_point: tuple):
    graph = ox.graph_from_bbox(*get_cords(start_point, end_point))
    orig_node = ox.nearest_nodes(graph, start_point[1], start_point[0])
    dest_node = ox.nearest_nodes(graph, end_point[1], end_point[0])
    shortest_route = nx.shortest_path(graph, orig_node, dest_node)

    return ox.plot_route_folium(graph, shortest_route)



def check_city(lat, lon):
    location = geolocator.reverse(f"{lat}, {lon}")
    if "state" in location.raw["address"].keys() and location.raw["address"]["state"] == "Москва":
        return True


def find_nearest(lat, lon):
    with open("data/moscow.json", "r", encoding="utf-8") as f:
        stations = load(f)

    # [Расстояние, Данные о станции]
    nearest = None
    nearest_distance = 99

    for data in stations:
        distance_lat = abs(float(data["lat"]) - float(lat))
        distance_lon = abs(float(data["lng"]) - float(lon))
        distance = sqrt(distance_lat ** 2 + distance_lon ** 2)

        if distance < nearest_distance:
            nearest_distance = distance
            nearest = data
    
    return nearest
