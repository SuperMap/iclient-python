import os
import geojson


def load_geojson_data():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chinageojson.json"), 'r',
              encoding='utf-8') as geoJsonFile:
        return geojson.load(geoJsonFile)


def get_privince_geojson_data(geojson, name):
    for i in range(0, len(geojson["features"])):
        feature = geojson["features"][i]
        if (name in feature["properties"]["name"]):
            return feature
