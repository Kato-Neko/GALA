import requests

def get_address_from_coordinates(latitude, longitude, api_key):
    url = f"https://api.geocode.earth/v1/reverse"
    params = {
        "point.lat": latitude,
        "point.lon": longitude,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("features"):
            return data["features"][0]["properties"].get("label", "Unknown Address")
    return "Unknown Address"

def get_weather_data(latitude, longitude, api_key):
    api_url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['current']['condition']['text']
        temperature = data['current']['temp_c']
        return f"{weather_description}, {temperature}°C"
    return "Weather data unavailable"