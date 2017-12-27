from unittest import TestCase
from iclientpy.jupyter import load_geojson_data, get_privince_geojson_data


class TestUnits(TestCase):
    def test_get_privince_geojson(self):
        geojsondata = load_geojson_data()
        privName = '天津'
        feature = get_privince_geojson_data(geojsondata, privName)
        self.assertEqual('天津市', feature["properties"]["name"])
        self.assertEqual([117.215268, 39.120963], feature["properties"]["cp"])
