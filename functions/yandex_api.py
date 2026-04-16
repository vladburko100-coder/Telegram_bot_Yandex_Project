import pprint

import requests


def search_cords(place):
    apikey = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": apikey,
        "text": place,
        "lang": "ru_RU",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            response_json = response.json()
            cords = response_json['features'][0]['geometry']['coordinates']
            return cords
        except IndexError:
            return None
    else:
        return None


def static_maps(cords):
    lon, lat = cords
    api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    params = {
        'apikey': api_key,
        'll': f'{lon},{lat}',
        'z': 15,
        'l': 'map',
        'pt': f'{lon},{lat},vkbkm',
        'size': '650,450',
        'style': "elements:label|stylers.visibility:off"
    }

    response = requests.get('https://static-maps.yandex.ru/v1', params=params)
    return response.url