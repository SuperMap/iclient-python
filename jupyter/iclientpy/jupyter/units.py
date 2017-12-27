import os
import geojson
import pandas as pd


def load_geojson_data():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chinageojson.json"), 'r',
              encoding='utf-8') as geoJsonFile:
        return geojson.load(geoJsonFile)


def get_privince_geojson_data(geojson, name):
    for i in range(0, len(geojson["features"])):
        feature = geojson["features"][i]
        if (name in feature["properties"]["name"]):
            return feature


def convert_data_frame_to_dataset(data, lng_key=0, lat_key=1, value_key=2):
    result = []
    if isinstance(data, pd.DataFrame):
        for index, row in data.iterrows():
            point = geojson.Point((data[lng_key][index], data[lat_key][index]))
            element = {"geometry": point, "count": data[value_key][index]}
            result.append(element)
    else:
        raise Exception("格式不支持")
    return result
