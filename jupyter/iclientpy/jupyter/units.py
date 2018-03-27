import os
import geojson
import pandas as pd


def load_geojson_data():
    """
    从chinageojson.json文件加载geojson对象

    Returns:
        json对象
    """
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chinageojson.json"), 'r',
              encoding='utf-8') as geoJsonFile:
        return geojson.load(geoJsonFile)


def get_geojson_data(geojson, name):
    """
    返回指定名称的geojson对象

    Args:
        geojson: 所有省份的geojson对象
        name: 省份名称

    Returns:
        返回json对象
    """
    for i in range(0, len(geojson["features"])):
        feature = geojson["features"][i]
        if (name in feature["properties"]["name"]):
            return feature


def convert_data_frame_to_dataset(data, lng_key=0, lat_key=1, value_key=2):
    """
    将pandas的dataframe类型转为mapv数据需要的dataset类型

    Args:
        data: dataframe的数据
        lng_key: 经度的key
        lat_key: 纬度的key
        value_key: 目标值的key

    Returns:
        返回dataset类型数据
    """
    result = []
    if isinstance(data, pd.DataFrame):
        for index, row in data.iterrows():
            point = geojson.Point((data[lng_key][index], data[lat_key][index]))
            element = {"geometry": point, "count": data[value_key][index]}
            result.append(element)
    else:
        raise Exception("格式不支持")
    return result
