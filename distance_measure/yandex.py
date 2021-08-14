from flask import Blueprint
import requests as req
from math import sin, cos, sqrt, atan2, radians

PREFIX = '/yandex'
BASE_URL = 'https://geocode-maps.yandex.ru/1.x/?'
CENTER_MKAD = "37.6222,55.7518"
RADIUS_MKAD = "0.2152,0.16"
API_KEY = '941a8b32-8628-4286-9ed1-0e4fc2bf797b'
EARTH_RADIUS = 6373.0


yandex_lib = Blueprint('yandex_lib', __name__, url_prefix=PREFIX)


@yandex_lib.route("/", methods=["GET"])
def home():
    return "Please use {}/distance".format(PREFIX)

@yandex_lib.route("/distance/<address>")
def distance_from_mkad(address):
    if isInMKAD(address):
        return str(0)
    address1 = "Moscow Ring Road"
    address2 = address
    return distance_two_points(address1, address2)

@yandex_lib.route("/distance/<address1>/<address2>")
def distance_two_points(address1, address2):
    point1 = get_coordinate(address1)
    point2 = get_coordinate(address2)

    distance = calculate_distance(point1, point2)

    return str(distance)

def isInMKAD(address):
    point1 = get_coordinate(address)
    point2 = get_coordinate(address, checkMKAD=True)

    if point1==point2:
        return True
    return False


def get_coordinate(address, checkMKAD=False):
    url = (BASE_URL + 'apikey=' + API_KEY
                + '&geocode=' + address
                + '&format=' + 'json'
                + '&results=1'
                + '&lang=en-US'
            )
    if checkMKAD :
        url += ('&ll='+ CENTER_MKAD
                + '&spn='+ RADIUS_MKAD
                + '&rspn=1' 
            )

    response = req.get(url).json()
    try:
        pos = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        pos = pos.split(' ')
        pos = list(map(float, pos))
        target = [pos[1], pos[0]]
        return target
    except:
        return [0,0]

def calculate_distance(point1, point2):
    latitude = [radians(point1[0]), radians(point2[0])]
    longitude = [radians(point1[1]), radians(point2[1])]
    distance_latitude = latitude[0] - latitude[1]
    distance_logitude = longitude[0] - longitude[1]

    a = sin(distance_latitude / 2)**2 + cos(latitude[0]) * cos(latitude[1]) * sin(distance_logitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c

    return distance
