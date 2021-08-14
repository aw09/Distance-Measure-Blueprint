from flask import Blueprint, current_app
from geopy.geocoders import Nominatim
from geopy import distance

PREFIX = '/geopy'
CENTER_MKAD = (55.75157, 37.61632)

geopy_lib = Blueprint('geopy_lib', __name__, url_prefix=PREFIX)
geolocator = Nominatim(user_agent="Distance Measure")

@geopy_lib.route("/", methods=["GET"])
def home():
    return "Please use {}/distance".format(PREFIX)

@geopy_lib.route("/distance/<address>")
def distance_from_mkad(address):
    # target = geolocator.geocode(address)
    # distance_target = distance.distance(CENTER_MKAD, (target.latitude, target.longitude)).km

    # return str(distance_target)
    address1 = "Moscow Ring Road"
    address2 = address
    return distance_two_points(address1, address2)
    

@geopy_lib.route("/distance/<address1>/<address2>")
def distance_two_points(address1, address2):
    target1 = geolocator.geocode(address1)
    target2 = geolocator.geocode(address2)
    distance_target = distance.distance((target1.latitude, target1.longitude), (target2.latitude, target2.longitude)).km
    log =  address1 + ' ' + str([target1.latitude, target1.longitude]) + ' - ' \
            + address2 + ' ' + str([target2.latitude, target2.longitude]) + ' ' \
            + 'distance: ' + str(distance_target) + ' km'
    current_app.logger.info(log)
    return str(distance_target)

@geopy_lib.route("/distance")
def empty_address():
    return "Address parameter cannot be empty!"