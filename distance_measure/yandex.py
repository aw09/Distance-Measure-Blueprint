from flask import Blueprint, current_app, jsonify
import requests as req
from math import sin, cos, sqrt, atan2, radians

PREFIX = '/yandex'
BASE_URL = 'https://geocode-maps.yandex.ru/1.x/?'
CENTER_MKAD = "37.6222,55.7518"
RADIUS_MKAD = "0.2152,0.16"
API_KEY = '941a8b32-8628-4286-9ed1-0e4fc2bf797b'
EARTH_RADIUS = 6373.0

yandex_lib = Blueprint('yandex_lib', __name__, url_prefix=PREFIX)

point1, point2, point2_in_mkad = '','',''

@yandex_lib.route("/", methods=["GET"])
def home():
    return '''
    <table>
    <tr>
        <td>/(address)</td>
        <td>for calculate address from Moscow Ring Road</td>
    </tr>
    <tr>
        <td>/(address1)/(address2)</td>
        <td>for calculate two address</td>
    </tr>
    <tr>
        <td>/miles/(address) </td>
        <td>for miles</td>
    </tr>
    </table>
    '''

@yandex_lib.route("/miles/<address>")
def miles_one_address(address):
    # Change unit to mile and use one_address function
    return one_address(address, to_mile=True)

@yandex_lib.route("/miles/<address1>/<address2>")
def miles_two_address(address1, address2):
    # Change unit to mile and use two_address function
    return two_address(address1, address2, to_mile=True)


@yandex_lib.route("/<address>")
def one_address(address, to_mile=False):
    # This method receive only one param then calculate distance
    # with Moscow Ring Road

    address1 = "Moscow Ring Road"
    address2 = address
    return two_address(address1, address2, to_mile)

@yandex_lib.route("/<address1>/<address2>")
def two_address(address1, address2, to_mile=False):
    # This method receive two param 
    # and also return and logging based on condition 

    unit = 'mile' if to_mile else 'km'

    try:
        get_all_coordinates(address1, address2)
    except:
        return jsonify({'status':504, 'message':'Gateway Timeout'})

    if point1 == [0,0] or point2 == [0,0]:
        location_error = address1 if point1 == [0,0] else address2
        log = location_error + ' ' + " not found!"
        current_app.logger.error(log)
        return jsonify({'status':400, 'message':'Bad Request', 'data':log})

    elif (address1 == "Moscow Ring Road") and (isInMKAD()):
        log = address2 + ' is inside MKAD, distance: 0'
        current_app.logger.info(log)
        return jsonify({
            'status':200,
            'message':'Success',
            'data':{
                'address1' : address1,
                'coordinate1': point1,
                'address2': address2,
                'coordinate2': point2,
                'distance': 0,
                'unit': unit,
                'info': log
            }})

    else:
        distance = calculate_distance(point1, point2, to_mile)

        log =  address1 + ' ' + str(point1) + ' - ' \
                + address2 + ' ' + str(point2) + ' ' \
                + 'distance: ' + str(distance) + ' km'
        current_app.logger.info(log)

        return jsonify({
            'status':200,
            'message':'Success',
            'data':{
                'address1' : address1,
                'coordinate1': point1,
                'address2': address2,
                'coordinate2': point2,
                'distance': distance,
                'unit':unit,
                'info': ''
            }})
    

def isInMKAD():
    # This method return True if point2 also found in mkad
    # it means the location is in mkad and the distance does not need to be calculated 
    global point2, point2_in_mkad
    return True if point2 == point2_in_mkad else False 

def get_all_coordinates(address1, address2):
    # This method get all coordinate 
    # and store it in global variable
    # This approach is taken to minimize request to API

    global point1, point2, point2_in_mkad
    point1 = get_coordinate(address1)
    point2 = get_coordinate(address2)
    point2_in_mkad = get_coordinate(address2, checkMKAD=True)

def get_coordinate(address, checkMKAD=False):
    # This method to get coordinate
    # param checkMKAD to set center and radius from MKAD
    # and send it to API for limit search area

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
        target = [pos[1], pos[0]]       # Need swap because Yandex API return logitude, latitude
        return target
    except:
        return [0,0]
            

def calculate_distance(point1, point2, to_mile=False):
    # Because Yandex API doesn't have calculate distance method
    # Source code from https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python

    latitude = [radians(point1[0]), radians(point2[0])]
    longitude = [radians(point1[1]), radians(point2[1])]
    distance_latitude = latitude[0] - latitude[1]
    distance_logitude = longitude[0] - longitude[1]

    a = sin(distance_latitude / 2)**2 + cos(latitude[0]) * cos(latitude[1]) * sin(distance_logitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c

    if to_mile :
        distance /= 1.609

    return distance
