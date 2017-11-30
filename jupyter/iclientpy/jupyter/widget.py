from ipyleaflet import Map, TileLayer, Layer
from traitlets import Unicode, List, Int, default, validate, Dict, Any
from ipywidgets import Layout
import pandas as pd
import geojson
import os
from .._version import EXTENSION_VERSION


class CloudTileLayer(TileLayer):
    _view_name = Unicode("SuperMapCloudTileLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapCloudTileLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    mapName = Unicode('').tag(sync=True, o=True)
    type = Unicode('').tag(sync=True, o=True)


class TileMapLayer(TileLayer):
    _view_name = Unicode("SuperMapTileMapLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapTileMapLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)


class RankSymbolThemeLayer(Layer):
    _view_name = Unicode("SuperMapRankSymbolThemeLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapRankSymbolThemeLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    themeField = Unicode('value').tag(sync=True)
    symbolType = Unicode('CIRCLE').tag(sync=True)
    symbolSetting = Dict({}).tag(sync=True)
    name = Unicode('').tag(sync=True)
    sdata = Any([])
    data = List([]).tag(sync=True)
    address_key = Any(0)
    value_key = Any(1)

    # address_key = Any(0).tag(sync=True)
    # value_key = Any(1).tag(sync=True)
    # lng_key = Any(2).tag(sync=True)
    # lat_key = Any(3).tag(sync=True)

    @validate('sdata')
    def _validate_sdata(self, proposal):
        if (proposal['value'] is None):
            raise Exception("error data")
        tempdata = []
        if isinstance(proposal['value'], list):
            for d in proposal['value']:
                feature = get_privince_geojson_data(d[self.address_key])
                row = (d[self.address_key], d[self.value_key], feature["properties"]["cp"][0],
                       feature["properties"]["cp"][1])
                tempdata.append(row)

        elif isinstance(proposal['value'], pd.DataFrame):
            for index, row in proposal['value'].iterrows():
                feature = get_privince_geojson_data(proposal['value'][self.address_key][index])
                trow = (proposal['value'][self.address_key][index], proposal['value'][self.value_key][index],
                        feature["properties"]["cp"][0],
                        feature["properties"]["cp"][1])
                tempdata.append(trow)

        self.data = tempdata
        return proposal['value']

    def __init__(self, name, data, **kwargs):
        super(RankSymbolThemeLayer, self).__init__(**kwargs)
        self.name = name
        self.sdata = data


class MapView(Map):
    @default('layout')
    def _default_layout(self):
        return Layout(height='500px', align_self='stretch')

    _view_name = Unicode("SuperMapMapView").tag(sync=True)
    _model_name = Unicode("SuperMapMapModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    center = List([34.5393842300, 108.9282514100]).tag(sync=True, o=True)
    zoom = Int(15).tag(sync=True, o=True)
    crs = Unicode('EPSG3857').tag(sync=True, o=True)

    @default('default_tiles')
    def _default_tiles(self):
        return CloudTileLayer()


def get_privince_geojson_data(name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chinageojson.json"), 'r',
              encoding='utf-8') as geoJsonFile:
        fc = geojson.load(geoJsonFile)
        for i in range(0, len(fc["features"])):
            feature = fc["features"][i]
            if (name in feature["properties"]["name"]):
                return feature
