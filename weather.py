import argparse
import json
import sys
import requests

WEATHER_WEBSITE = "https://api2.climacell.co/v2/realtime"
GEOLOCALIZATION_WEBSITE = "http://www.mapquestapi.com/geocoding/v1/address"

try:
    with open("apikey", "r") as f:
        API_KEY = f.readline()
    with open("geoKey", "r") as f:
        GEO_KEY = f.readline()
except IOError as er:
    print("Unable to open file containing apikey - exiting")
    sys.exit(1)


def get_coordinates(location):
    """ pobiera współrzędne na podstawie lokalizacji """
    location_data = {
        "key": GEO_KEY,
        "location": location
    }
    r = requests.get(GEOLOCALIZATION_WEBSITE, location_data)
    if r.status_code != 200:
        print("Unable to get location coordinates")
        return
    json_acceptable_string = r.text.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    coordinates = d["results"][0]["locations"][0]["latLng"]
    print(location)
    return coordinates


def get_current_weather(longitude, latitude):
    """ pobiera inf o aktualnej pogodzie dla podanje lokalizacji """
    data = {
        "geocode": {
            "lon": longitude,
            "lat": latitude
        },
        "location_id": "",
        "fields": [
            {
                "name": "temp",
                "units": "C"
            }
        ]
    }
    r = requests.post(WEATHER_WEBSITE, json.dumps(data), headers={"apikey": API_KEY, "Content-Type": "application/json"})
    if r.status_code != 200:
        print("Unable to get current weather information")
        return
    json_acceptable_string = r.text.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    print(f'Current temp: {d["temp"]["value"]}')


def get_weather_forecast():
    """ pobiera inf o prognozie pogody na kolejny dzien """
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument("--coordinates", dest="coordinates", action="store", help="location coordinates X,Y")
    location_group.add_argument("--city", dest="city", action="store", help="location city")
    location_group.add_argument("--address", dest="address", action="store", help="location address")
    args = parser.parse_args()
    coordinates = get_coordinates(args.city)
    get_current_weather(coordinates["lng"], coordinates["lat"])

