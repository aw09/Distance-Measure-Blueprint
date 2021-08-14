'''
This file using geopy library
I found this API before using Yandex
After I understand the Yandex API I focus on it
'''
from flask import Blueprint, current_app
from geopy.geocoders import Nominatim
from geopy import distance

PREFIX = '/geopy'

geopy_lib = Blueprint('geopy_lib', __name__, url_prefix=PREFIX)
geolocator = Nominatim(user_agent="Distance Measure")

@geopy_lib.route("/", methods=["GET"])
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
    </table>
    '''

@geopy_lib.route("/<address>")
def distance_from_mkad(address):
    address1 = "Moscow Ring Road"
    address2 = address
    return distance_two_points(address1, address2)
    

@geopy_lib.route("/<address1>/<address2>")
def distance_two_points(address1, address2):
    target1 = geolocator.geocode(address1)
    target2 = geolocator.geocode(address2)
    distance_target = distance.distance((target1.latitude, target1.longitude), (target2.latitude, target2.longitude)).km
    log =  address1 + ' ' + str([target1.latitude, target1.longitude]) + ' - ' \
            + address2 + ' ' + str([target2.latitude, target2.longitude]) + ' ' \
            + 'distance: ' + str(distance_target) + ' km'
    current_app.logger.info(log)
    return str(distance_target)
