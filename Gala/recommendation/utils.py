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
