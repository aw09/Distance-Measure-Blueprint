import json

def test_one_address(client):
    res = client.get('/geopy/Surabaya')
    assert res.status_code == 200
    expected = 1000
    assert expected < float(json.loads(res.get_data(as_text=True)))

def test_two_address(client):
    res = client.get('/geopy/Jember/Surabaya')
    assert res.status_code == 200
    expected = 10
    assert expected < float(json.loads(res.get_data(as_text=True)))

