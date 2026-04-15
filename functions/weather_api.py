import requests


def weather_point(cords):
    data = {

    }
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
    print(response.status_code)
    response_json = response.json()
    data['температура'] = response_json['data']['weatherByPoint']['now']['temperature']
    data['давление'] = response_json['data']['weatherByPoint']['now']['pressure']
    data['скорость'] = response_json['data']['weatherByPoint']['now']['windSpeed']
    data['влажность'] = response_json['data']['weatherByPoint']['now']['humidity']
    return data
