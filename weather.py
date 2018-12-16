import argparse
import datetime
import json
import requests
import configparser


def get_coordinates(website, apikey, location):
    """
    Pobiera współrzędne na podstawie lokalizacji
    :param website: endpoint API do pobrania koordynatów na podstawie parametru location
    :param apikey: klucz do autoryzacji w serwisie
    :param location: lokalizacja w formie nazwy miasta lub adresu
    :return: koordynaty w formie słownika
    """
    location_data = {
        "key": apikey,
        "location": location
    }
    r = requests.get(website, location_data)
    if r.status_code != 200:
        print("Unable to get location coordinates")
        return
    json_acceptable_string = r.text.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    try:
        coordinates = d["results"][0]["locations"][0]["latLng"]
    except IndexError:
        print('Unknown weather for the specified location: ' + location)
        raise
    return coordinates


def get_current_weather(website, apikey, endpoint, longitude, latitude):
    """
    Wyswietla aktualna pogode dla podanej lokalizacji
    :param website: strona do pobrania informacji o aktualnej pogodzie dla określonych współrzędnych
    :param apikey: klucz do autoryzacji w serwisie
    :param endpoint: endpoint API strony
    :param longitude: dlugosc geograficzna (float)
    :param latitude: szerokosc geograficzna (float)
    :return: informacje o pogodzie w formie slownika
    """
    url = website + endpoint
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
            },
            {
                "name": "feels_like",
                "units": "C"
            },
            {
                "name": "humidity"
            },
            {
                "name": "wind_speed"
            },
            {
                "name": "cloud_cover"
            }
        ]
    }
    r = requests.post(url, json.dumps(data), headers={"apikey": apikey, "Content-type": "application/json"})
    if r.status_code != 200:
        print("Unable to get current weather information")
        return
    json_acceptable_string = r.text.replace("'", "\"")
    return json.loads(json_acceptable_string)


def get_forecast_weather(website, endpoint, apikey, longitude, latitude, num_of_days):
    """
    Wyswietla prognoze pogody dla podanej lokalizacji
    :param website: strona do pobrania informacji o aktualnej pogodzie dla określonych współrzędnych
    :param endpoint: endpoint API strony
    :param apikey: klucz do autoryzacji w serwisie
    :param longitude: dlugosc geograficzna
    :param latitude: szerokosc geograficzna
    :param num_of_days: liczba dni, dla ktorych nalezy wyswietlic prognoze
    :return: informacje o pogodzie w formie slownika
    """
    url = website + endpoint
    data = {
        "lon": longitude,
        "lat": latitude,
        "num_days": num_of_days,
        "unit_system": "si",
        "fields": "temp,feels_like,humidity,wind_speed"
    }
    r = requests.get(url, params=data, headers={"apikey": apikey, "accept": "application/json"})
    if r.status_code != 200:
        print("Unable to get current weather information")
        print(r.text)
        return
    json_acceptable_string = r.text.replace("'", "\"")
    return json.loads(json_acceptable_string)


def read_input_arguments():
    """ Czyta argumenty wejsciowe """
    parser = argparse.ArgumentParser()
    parser.add_argument("--forecast-days", dest="num_days", action="store", default="0", help="get forecast max 3 days")
    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument("--coordinates", dest="coordinates", action="store", help="location coordinates X,Y")
    location_group.add_argument("--address", dest="address", action="store", help="location address")
    return parser.parse_args()


def read_config_file(cfg_path="config.ini"):
    """ Czyta plik konfiguracyjny """
    config = configparser.ConfigParser()
    config.read(cfg_path)
    return config


if __name__ == "__main__":
    input_args = read_input_arguments()
    config = read_config_file()
    geolocalization_data = config['GEOLOCALIZATION']
    weather_data = config['WEATHER']
    coordinates = get_coordinates(website=geolocalization_data['website'], apikey=geolocalization_data['apikey'],
                                  location=input_args.address)
    print(f"Prognoza pogody dla: {input_args.address}")
    if input_args.num_days == "0" or input_args.num_days == "1":
        d = get_current_weather(website=weather_data['website'], apikey=weather_data['apikey'],
                                endpoint=weather_data['realtime_endpoint'], longitude=coordinates["lng"],
                                latitude=coordinates["lat"])
        print("Aktualna pogoda")
        print(f'Temperatura rzeczywista: {d["temp"]["value"]}')
        print(f'Temperatura odczuwalna: {d["feels_like"]["value"]}')
        print(f'Wilgotność powietrza: {d["humidity"]["value"]} %')
        print(f'Prędkość wiatru: {d["wind_speed"]["value"]} m/s')
        print(f'Zachmurzenie: {d["cloud_cover"]["value"]} %')
    else:
        d = get_forecast_weather(website=weather_data['website'], endpoint=weather_data['forecast_daily_endpoint'],
                                 apikey=weather_data['apikey'], longitude=coordinates["lng"],
                                 latitude=coordinates["lat"], num_of_days=int(input_args.num_days) - 1)
        current_dt = datetime.datetime.now()
        header = '{:12}|{:9}|{:9}|{:9}|{:10}|{:10}|{:10}|{:15}|{:13}' \
            .format('Data', ' Tmp min', ' Tmp max', ' Odcz min', ' Odcz max', ' Wilg min', ' Wilg max',
                    ' Pr wiatru min',
                    'Pr wiatru max')
        print(header)
        print('-' * len(header))
        for index, day in enumerate(d):
            date = (current_dt + datetime.timedelta(days=index)).strftime("%Y-%m-%d")
            print('{:12}|{:9}|{:9}|{:9}|{:10}|{:10}|{:10}|{:15}|{:13}'
                  .format(date, day["temp"][0]["min"]["value"], day["temp"][1]["max"]["value"],
                          day["feels_like"][0]["min"]["value"], day["feels_like"][1]["max"]["value"],
                          day["humidity"][0]["min"]["value"], day["humidity"][1]["max"]["value"],
                          day["wind_speed"][0]["min"]["value"], day["wind_speed"][1]["max"]["value"]))
