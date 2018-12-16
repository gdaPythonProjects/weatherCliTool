import unittest

from weather import read_config_file, get_coordinates, get_current_weather


class TestWeather(unittest.TestCase):

    CONFIG_FILE_PATH = 'config.ini'

    def test_config_content(self):
        config = read_config_file(cfg_path=self.CONFIG_FILE_PATH)
        self.assertIn('GEOLOCALIZATION', config)
        self.assertIn('website', config['GEOLOCALIZATION'])
        self.assertIn('apikey', config['GEOLOCALIZATION'])
        self.assertIn('WEATHER', config)
        self.assertIn('website', config['WEATHER'])
        self.assertIn('apikey', config['WEATHER'])
        self.assertIn('realtime_endpoint', config['WEATHER'])
        self.assertIn('forecast_daily_endpoint', config['WEATHER'])

    def test_get_coordinates_ret_value(self):
        config = read_config_file()
        geolocalization_data = config['GEOLOCALIZATION']
        coordinates = get_coordinates(website=geolocalization_data['website'], apikey=geolocalization_data['apikey'],
                                      location='gdansk')
        self.assertIn('lat', coordinates)
        self.assertIn('lng', coordinates)

    def test_gdansk_coordinates(self):
        config = read_config_file()
        geolocalization_data = config['GEOLOCALIZATION']
        coordinates = get_coordinates(website=geolocalization_data['website'], apikey=geolocalization_data['apikey'],
                                      location='gdansk')
        self.assertEqual(coordinates['lat'], 54.348226)
        self.assertEqual(coordinates['lng'], 18.654289)

    def test_get_current_weather_ret_value(self):
        config = read_config_file()
        geolocalization_data = config['GEOLOCALIZATION']
        weather_data = config['WEATHER']
        coordinates = get_coordinates(website=geolocalization_data['website'], apikey=geolocalization_data['apikey'],
                                      location='gdansk')
        d = get_current_weather(website=weather_data['website'], apikey=weather_data['apikey'],
                                endpoint=weather_data['realtime_endpoint'], longitude=coordinates["lng"],
                                latitude=coordinates["lat"])
        self.assertIn('temp', d)
        self.assertIn('feels_like', d)
        self.assertIn('humidity', d)
        self.assertIn('wind_speed', d)
        self.assertIn('cloud_cover', d)


if __name__ == '__main__':
    unittest.main()
