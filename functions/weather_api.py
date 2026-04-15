import pprint
from datetime import date

import requests


def weather_point_now(cords):
    current_date = date.today()
    data = {}
    API_KEY = 'fa0f11a5-fd86-48c2-b07f-ef6e45a933a8'
    headers = {
        "X-Yandex-Weather-Key": API_KEY
    }
    query = f"""{{
      weatherByPoint(request: {{ lat: {cords[1]}, lon: {cords[0]} }}) {{
        now {{
          temperature
          humidity
          pressure
          windSpeed
        }}
      }}
    }}"""
    response = requests.post(
        'https://api.weather.yandex.ru/graphql/query',
        headers=headers,
        json={'query': query}
    )
    response_json = response.json()
    data['температура'] = response_json['data']['weatherByPoint']['now']['temperature']
    data['давление'] = response_json['data']['weatherByPoint']['now']['pressure']
    data['скорость'] = response_json['data']['weatherByPoint']['now']['windSpeed']
    data['влажность'] = response_json['data']['weatherByPoint']['now']['humidity']
    data['дата'] = current_date
    return data


def weather_point_forecast(cords, days: int):
    API_KEY = 'fa0f11a5-fd86-48c2-b07f-ef6e45a933a8'
    headers = {
        "X-Yandex-Weather-Key": API_KEY
    }
    query = f"""{{
      weatherByPoint(request: {{ lat: {cords[1]}, lon: {cords[0]} }}) {{
        forecast {{
            days(limit: {str(days)}) {{
                time
                parts {{
                    day {{
                      avgTemperature
                      humidity
                      pressure
                      windSpeed
                    }}
                }}
            }}
        }}
      }}
    }}"""
    response = requests.post(
        'https://api.weather.yandex.ru/graphql/query',
        headers=headers,
        json={'query': query}
    )
    response_json = response.json()
    day = response_json['data']['weatherByPoint']['forecast']['days'][-1]
    return {
        'температура': str(day['parts']['day']['avgTemperature']),
        'давление': str(day['parts']['day']['pressure']),
        'скорость': str(day['parts']['day']['windSpeed']),
        'влажность': str(day['parts']['day']['humidity']),
        'дата': day['time'].split('T')[0]
    }
