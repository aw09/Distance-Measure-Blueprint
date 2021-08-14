import json

def test_outside_MKAD(client):
    res = client.get('/yandex/distance/Surabaya')
    assert res.status_code == 200
    print(json.loads(res.get_data(as_text=True)))
    expected = 10
    assert expected < float(json.loads(res.get_data(as_text=True)))

def test_inside_MKAD(client):
    res = client.get('/yandex/distance/Ramenki District')
    assert res.status_code == 200
    print(json.loads(res.get_data(as_text=True)))
    expected = 0
    assert expected == float(json.loads(res.get_data(as_text=True)))

