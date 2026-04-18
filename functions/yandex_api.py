from dotenv import load_dotenv
from datetime import datetime
import requests
import os

load_dotenv()


def search_cords(place):
    apikey = os.getenv('SEARCH_APIKEY')
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


def static_maps(cords, spn):
    day_time = int(datetime.now().strftime("%H"))
    if day_time >= 18 or day_time <= 4:
        day_time = 'dark'
    else:
        day_time = 'light'
    lon, lat = cords
    api_key = os.getenv('MAPS_APIKEY')
    params = {
        'apikey': api_key,
        'lang': 'ru_RU',
        'll': f'{lon},{lat}',
        'spn': spn,
        'pt': f'{lon},{lat},vkbkm',
        'size': '650,450',
        'style': "tags.any:admin;landscape|stylers.visibility:off",
        'theme': day_time
    }

    response = requests.get('https://static-maps.yandex.ru/v1', params=params)
    return response.url
