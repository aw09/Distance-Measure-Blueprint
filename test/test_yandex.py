import json

def test_outside_MKAD(client):
    # Testing with Surabaya, outside MKAD

    res = client.get('/yandex/Surabaya')
    expected = {
                "data": {
                    "address1": "Moscow Ring Road",
                    "address2": "Surabaya",
                    "coordinate1": [55.766557, 37.623429],
                    "coordinate2": [-7.274237, 112.735199],
                    "distance": 9764.00790757382,
                    "info": "",
                    "unit": "km"
                },
                "message": "Success",
                "status": 200
            }

    assert expected == json.loads(res.get_data(as_text=True))

def test_inside_MKAD(client):
    # Testing with district in MKAD
    # It will return 0 

    res = client.get('/yandex/Ramenki District')
    expected = {
                "data": {
                    "address1": "Moscow Ring Road",
                    "address2": "Ramenki District",
                    "coordinate1": [55.766557, 37.623429],
                    "coordinate2": [55.708034, 37.515775],
                    "distance": 0,
                    "info": "Ramenki District is inside MKAD, distance: 0",
                    "unit": "km"
                },
                "message": "Success",
                "status": 200
            }

    assert expected == (json.loads(res.get_data(as_text=True)))

def test_two_address(client):
    # Testing with two addresses
    
    res = client.get('/yandex/Jember/Surabaya')
    expected = {
                "data": {
                    "address1": "Jember",
                    "address2": "Surabaya",
                    "coordinate1": [-8.148983, 113.712162],
                    "coordinate2": [-7.274237, 112.735199],
                    "distance": 145.1296397925564,
                    "info": "",
                    "unit": "km"
                },
                "message": "Success",
                "status": 200
            }

    assert expected == json.loads(res.get_data(as_text=True))

def test_miles_unit(client):
    # Testing mile unit
    # km : mile = 1 : 0,621371

    res = client.get('/yandex/miles/Jember/Surabaya')
    expected = {
                "data": {
                    "address1": "Jember",
                    "address2": "Surabaya",
                    "coordinate1": [-8.148983, 113.712162],
                    "coordinate2": [-7.274237, 112.735199],
                    "distance": 90.19865742234704,
                    "info": "",
                    "unit": "mile"
                },
                "message": "Success",
                "status": 200
            }

    assert expected == json.loads(res.get_data(as_text=True))

def test_invalid_input(client):
    # Testing with not found input

    # I don't know what invalid input on address
    # Because if I just search for integers on google maps 
    # it still return value

    res = client.get('/yandex/12x34')
    expected = {"data":"12x34  not found!","message":"Bad Request","status":400}
    assert expected == (json.loads(res.get_data(as_text=True)))