import requests


def get_weather(location):

    api_key = 'efe7d9b08f2b66f6e01c411d23e197bd'
    r = requests.get('http://api.weatherstack.com/current?access_key='+ api_key +'&query='+ location +'')
    data = r.json()

    result = f"\nlocation: {data['location']['name']}\n"

    for k, v in data.items():
        if k in ('current',):
            for key, value in v.items():
                if key not in ("weather_code", "weather_icons", "is_day"):
                    s = f"   {key}:{value}\n"
                    result += s
    return result

