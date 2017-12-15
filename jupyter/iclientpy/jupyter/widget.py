from ipyleaflet import Map, TileLayer, Layer
from traitlets import Unicode, List, Int, default, validate, Dict, Any, Tuple, link, Bool, Float, CaselessStrEnum
from ipywidgets import Layout, IntRangeSlider, ColorPicker, IntSlider, FloatSlider
import ipywidgets as widgets
import pandas as pd
import geojson
import os
import math
from .._version import EXTENSION_VERSION


class HeatLayer(Layer):
    _view_name = Unicode("SuperMapHeatLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapHeatLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    heat_points = List([]).tag(sync=True)

    @validate('heat_points')
    def _validate_heat_points(self, proposal):
        if (proposal['value'] is None):
            raise Exception("error data")
        self.max = max(dt[2] for dt in self.heat_points)
        return proposal['value']

    radius = Int(25).tag(sync=True, o=True)
    min_opacity = Float(0.05).tag(sync=True, o=True)
    max_zoom = Int().tag(sync=True, o=True)
    max = Float(1.0).tag(sync=True, o=True)
    blur = Int(15).tag(sync=True, o=True)
    gradient = Dict().tag(sync=True, o=True)

    def interact(self):
        radiusintslider = IntSlider(value=self.radius,
                                    min=1,
                                    max=100,
                                    step=1,
                                    description='半径:',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='horizontal',
                                    readout=True,
                                    readout_format='d',
                                    layout=Layout(width="350px"))
        link((radiusintslider, 'value'), (self, 'radius'))
        minopacityslider = FloatSlider(value=self.min_opacity,
                                       min=0,
                                       max=1.0,
                                       step=0.05,
                                       description='透明度:',
                                       disabled=False,
                                       continuous_update=False,
                                       orientation='horizontal',
                                       readout=True,
                                       readout_format='.1f',
                                       layout=Layout(width="350px"))
        link((minopacityslider, 'value'), (self, 'min_opacity'))
        blurintslider = IntSlider(value=self.blur,
                                  min=1,
                                  max=100,
                                  step=1,
                                  description='模糊:',
                                  disabled=False,
                                  continuous_update=False,
                                  orientation='horizontal',
                                  readout=True,
                                  readout_format='d',
                                  layout=Layout(width="350px"))
        link((blurintslider, 'value'), (self, 'blur'))
        maxslider = IntSlider(value=1,
                              min=0,
                              max=math.ceil(self.max),
                              step=1,
                              description='max:',
                              disabled=False,
                              continuous_update=False,
                              orientation='horizontal',
                              readout=True,
                              readout_format='d',
                              layout=Layout(width="350px"))
        link((maxslider, 'value'), (self, 'max'))
        return widgets.VBox([radiusintslider, minopacityslider, blurintslider, maxslider])


class MapVLayer(Layer):
    _view_name = Unicode("SuperMapMapVLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapMapVLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    data_set = List([]).tag(sync=True)
    map_v_options = Dict().tag(sync=True)

    @validate('map_v_options')
    def _validate_map_v_options(self, proposal):
        self.size = proposal['value']['size'] if 'size' in proposal['value']else 5
        self.global_alpha = proposal['value']['globalAlpha'] if 'globalAlpha' in proposal['value'] else 1
        self.fill_style = proposal['value']['fillStyle'] if 'fillStyle' in proposal['value'] else'#3732FA'
        self.shadow_color = proposal['value']['shadowColor'] if 'shadowColor' in proposal['value'] else'#FFFA32'
        self.shadow_blur = proposal['value']['shadowBlur'] if 'shadowBlur' in proposal['value'] else 35
        # self.line_width = proposal['value']['lineWidth'] if 'lineWidth' in proposal['value'] else 4
        return proposal['value']

    size = Int().tag(sync=True)
    global_alpha = Float().tag(sync=True)
    fill_style = Unicode('').tag(sync=True)
    shadow_color = Unicode('').tag(sync=True)
    shadow_blur = Int().tag(sync=True)

    # line_width = Int(4).tag(sync=True)

    def interact(self):
        sizeslider = IntSlider(value=self.size,
                               min=0,
                               max=100,
                               step=1,
                               description='大小:',
                               disabled=False,
                               continuous_update=False,
                               orientation='horizontal',
                               readout=True,
                               readout_format='d',
                               layout=Layout(width="350px"))
        link((sizeslider, 'value'), (self, 'size'))
        global_alpha_slider = FloatSlider(value=self.global_alpha,
                                          min=0,
                                          max=1.0,
                                          step=0.1,
                                          description='透明度:',
                                          disabled=False,
                                          continuous_update=False,
                                          orientation='horizontal',
                                          readout=True,
                                          readout_format='.1f',
                                          layout=Layout(width="350px"))
        link((global_alpha_slider, 'value'), (self, 'global_alpha'))
        fill_style_color = ColorPicker(concise=False,
                                       description='填充颜色：',
                                       value=self.fill_style,
                                       disabled=False,
                                       layout=Layout(width="350px"))
        link((fill_style_color, 'value'), (self, 'fill_style'))
        shadow_color_color = ColorPicker(concise=False,
                                         description='描边颜色：',
                                         value=self.shadow_color,
                                         disabled=False,
                                         layout=Layout(width="350px"))
        link((shadow_color_color, 'value'), (self, 'shadow_color'))
        shadow_blur_slider = IntSlider(value=self.shadow_blur,
                                       min=0,
                                       max=100,
                                       step=1,
                                       description='投影模糊级数:',
                                       disabled=False,
                                       continuous_update=False,
                                       orientation='horizontal',
                                       readout=True,
                                       readout_format='d',
                                       layout=Layout(width="350px"))
        link((shadow_blur_slider, 'value'), (self, 'shadow_blur'))

        # line_width_slider = IntSlider(value=self.line_width,
        #                               min=0,
        #                               max=100,
        #                               step=1,
        #                               description='描边宽度:',
        #                               disabled=False,
        #                               continuous_update=False,
        #                               orientation='horizontal',
        #                               readout=True,
        #                               readout_format='d',
        #                               layout=Layout(width="350px"))
        # link((shadow_blur_slider, 'value'), (self, 'line_width'))
        return widgets.VBox([sizeslider, global_alpha_slider, shadow_color_color, fill_style_color, shadow_blur_slider])


class CloudTileLayer(TileLayer):
    _view_name = Unicode("SuperMapCloudTileLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapCloudTileLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    url = Unicode('').tag(sync=True)
    attribution = Unicode('').tag(sync=True, o=True)
    map_name = Unicode('').tag(sync=True, o=True)
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

    theme_field = Unicode('value').tag(sync=True)
    symbol_type = Unicode('CIRCLE').tag(sync=True)
    symbol_setting = Dict({}).tag(sync=True)
    name = Unicode('').tag(sync=True)
    sdata = Any([])
    data = List([]).tag(sync=True)
    is_over_lay = Bool(True).tag(sync=True, o=True)
    address_key = Any(0)
    value_key = Any(1)
    codomain = Tuple((0, 40000)).tag(sync=True)
    rrange = Tuple((0, 100)).tag(sync=True)
    color = Unicode('#FFA500').tag(sync=True)
    codomainmin = Int(0)
    codomainmax = Int(1)

    def interact(self, **kwargs):
        codomainslider = IntRangeSlider(value=[self.codomain[0], self.codomain[1]],
                                        min=self.codomainmin,
                                        max=self.codomainmax,
                                        step=1,
                                        description='值域范围:',
                                        disabled=False,
                                        continuous_update=False,
                                        orientation='horizontal',
                                        readout=True,
                                        readout_format='d',
                                        layout=Layout(width="350px"))
        link((codomainslider, 'value'), (self, 'codomain'))
        rslider = IntRangeSlider(value=[0, 100],
                                 min=0,
                                 max=100,
                                 step=1,
                                 description='半径范围:',
                                 disabled=False,
                                 continuous_update=False,
                                 orientation='horizontal',
                                 readout=True,
                                 readout_format='d',
                                 layout=Layout(width="350px"))
        link((rslider, 'value'), (self, 'rrange'))
        color = ColorPicker(concise=False,
                            description='填充颜色：',
                            value='#FFA500',
                            disabled=False,
                            layout=Layout(width="350px"))
        link((color, 'value'), (self, 'color'))
        # accordion = widgets.Accordion(children=[codomainslider, rslider, color])
        # accordion.set_title(0, '值域范围')
        # accordion.set_title(1, '半径范围')
        # accordion.set_title(2, '颜色')
        # return accordion
        return widgets.VBox([codomainslider, rslider, color])

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
        cmin = min(dt[1] for dt in self.data)
        cminlog10 = math.floor(math.log10(abs(cmin)))
        cminmod = cmin // math.pow(10, cminlog10)
        self.codomainmin = int(cminmod * math.pow(10, cminlog10))

        cmax = max(dt[1] for dt in self.data)
        cmaxlog10 = math.floor(math.log10(abs(cmax)))
        cmaxmod = cmax // math.pow(10, cmaxlog10)
        self.codomainmax = int((cmaxmod + 1) * math.pow(10, cmaxlog10))
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
    prefer_canvas = Bool(False).tag(sync=True, o=True)

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
