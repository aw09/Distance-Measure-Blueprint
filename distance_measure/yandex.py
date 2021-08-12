from flask import Blueprint
import requests as req
import json
from math import sin, cos, sqrt, atan2, radians

PREFIX = '/yandex'
BASE_URL = 'https://geocode-maps.yandex.ru/1.x/?'
CENTER_MKAD = (55.75157, 37.61632)
API_KEY = '941a8b32-8628-4286-9ed1-0e4fc2bf797b'
EARTH_RADIUS = 6373.0

yandex_lib = Blueprint('yandex_lib', __name__, url_prefix=PREFIX)


@yandex_lib.route("/", methods=["GET"])
def home():
    return "Please use {}/distance".format(PREFIX)

@yandex_lib.route("/distance/<address>")
def distance_from_mkad(address):
    address1 = "Moscow Ring Road"
    address2 = address
    return distance_two_points(address1, address2)

@yandex_lib.route("/distance/<address1>/<address2>")
def distance_two_points(address1, address2):
    point1 = get_coordinate(address1)
    point2 = get_coordinate(address2)

    distance = calculate_distance(point1, point2)


    return str(distance)

def get_coordinate(address):
    url = (BASE_URL + 'apikey=' + API_KEY
                + '&geocode=' + address
                + '&format=' + 'json'
                + '&results=1'
                + '&lang=en-US'
            )

    response = req.get(url).json()
    pos = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    pos = pos.split(' ')
    pos = list(map(float, pos))
    target = [pos[1], pos[0]]
    return target

def calculate_distance(point1, point2):
    latitude = [radians(point1[0]), radians(point2[0])]
    longitude = [radians(point1[1]), radians(point2[1])]
    distance_latitude = latitude[0] - latitude[1]
    distance_logitude = longitude[0] - longitude[1]

    a = sin(distance_latitude / 2)**2 + cos(latitude[0]) * cos(latitude[1]) * sin(distance_logitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c

    return distance


# resp = req.get(url)
# print(resp.text)
# apikey=941a8b32-8628-4286-9ed1-0e4fc2bf797b&geocode=Moscow Ring Road &results=5&lang=en-US