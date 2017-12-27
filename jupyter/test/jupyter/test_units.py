from unittest import TestCase
import pandas as pd
from iclientpy.jupyter import load_geojson_data, get_privince_geojson_data, convert_data_frame_to_dataset


class TestUnits(TestCase):
    def test_get_privince_geojson(self):
        geojsondata = load_geojson_data()
        privName = '天津'
        feature = get_privince_geojson_data(geojsondata, privName)
        self.assertEqual('天津市', feature["properties"]["name"])
        self.assertEqual([117.215268, 39.120963], feature["properties"]["cp"])

    def test_convert_data_frame_to_dataset(self):
        data = {"lat": [24.79, 29.77], "lng": [117.65, 115.40], "value": [14.49, 14.06]}
        df = pd.DataFrame.from_dict(data)
        data_set = convert_data_frame_to_dataset(df, "lng", "lat", "value")
        self.assertEqual(len(data_set), 2)
        self.assertEqual(data_set[0]['geometry']['type'], 'Point')
        self.assertEqual(data_set[0]['geometry']['coordinates'][0], 117.65)
        self.assertEqual(data_set[0]['geometry']['coordinates'][1], 24.79)
        self.assertEqual(data_set[0]['count'], 14.49)
        self.assertEqual(data_set[1]['geometry']['type'], 'Point')
        self.assertEqual(data_set[1]['geometry']['coordinates'][0], 115.40)
        self.assertEqual(data_set[1]['geometry']['coordinates'][1], 29.77)
        self.assertEqual(data_set[1]['count'], 14.06)
