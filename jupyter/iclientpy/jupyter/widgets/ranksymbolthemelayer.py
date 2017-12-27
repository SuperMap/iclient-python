import math
import pandas as pd
from ipyleaflet import Layer
from ipywidgets import VBox, Layout, ColorPicker, IntRangeSlider
from traitlets import Unicode, Any, Bool, Tuple, Int, Float, Dict, default, validate, link
from iclientpy._version import EXTENSION_VERSION
from .basesetting import BaseSetting
from ..units import load_geojson_data, get_privince_geojson_data


class SymbolSetting(BaseSetting):
    codomain = Tuple(default_value=(0, 100)).tag(settings=True)
    max_r = Int(default_value=100).tag(settings=True)
    min_r = Int(default_value=10).tag(settings=True)
    fill_color = Unicode(default_value='#FFA500').tag(settings=True)

    fill_opacity = Float(default_value=0.8).tag(cs=True)

    @validate('fill_opacity')
    def _validate_fill_opacity(self, proposal):
        if (proposal['value'] > 1 or proposal['value'] < 0):
            raise Exception("透明度范围是0-1之间")
        return proposal['value']

    circle_style = Dict().tag(settings=True)

    @default('circle_style')
    def _default_circle_style(self):
        tmp_cs = {}
        for name in self.traits(cs=True):
            v = getattr(self, name)
            if not v:
                continue
            tmp_cs[name] = v
        return tmp_cs

    circle_hover_style_fill_opacity = Float(default_value=0.8).tag(chs=True)
    circle_hover_style = Dict().tag(settings=True)

    @default('circle_hover_style')
    def _default_circle_hover_style(self):
        tmp_chs = {}
        for name in self.traits(chs=True):
            v = getattr(self, name)
            if not v:
                continue
            tmp_chs[name] = v
        return tmp_chs


class RankSymbolThemeLayer(Layer):
    _view_name = Unicode("SuperMapRankSymbolThemeLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapRankSymbolThemeLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    theme_field = Unicode('value').tag(sync=True)
    symbol_type = Unicode('CIRCLE').tag(sync=True)
    symbol_setting = Any({}).tag(sync=True)
    name = Unicode('').tag(sync=True)
    data = Any([]).tag(sync=True)
    is_over_lay = Bool(True).tag(sync=True, o=True)
    address_key = Any(0)
    value_key = Any(1)
    codomain = Tuple((0, 40000)).tag(sync=True)
    rrange = Tuple((0, 100)).tag(sync=True)
    color = Unicode('#FFA500').tag(sync=True)
    codomainmin = Int(0)
    codomainmax = Int(1)

    _privinces_geojson = []

    @validate('symbol_setting')
    def _validate_symbol_setting(self, proposal):
        if isinstance(proposal['value'], SymbolSetting):
            symbol_setting = proposal['value'].get_settings()
            self.codomain = (proposal['value'].codomain[0], proposal['value'].codomain[1])
            self.rrange = (proposal['value'].min_r, proposal['value'].max_r)
            self.color = proposal['value'].fill_color
        else:
            symbol_setting = proposal['value']
            self.codomain = (proposal['value']['codomain'][0], proposal['value']['codomain'][1])
            self.rrange = (proposal['value']['minR'], proposal['value']['maxR'])
            self.color = proposal['value']['fillColor']
        return symbol_setting

    @validate('data')
    def _validate_data(self, proposal):
        if (proposal['value'] is None):
            raise Exception("error data")

        if not self._privinces_geojson:
            self._privinces_geojson = load_geojson_data()

        tempdata = []
        if isinstance(proposal['value'], list):
            for d in proposal['value']:
                feature = get_privince_geojson_data(geojson=self._privinces_geojson, name=d[self.address_key])
                row = (d[self.address_key], d[self.value_key], feature["properties"]["cp"][0],
                       feature["properties"]["cp"][1])
                tempdata.append(row)

        elif isinstance(proposal['value'], pd.DataFrame):
            for index, row in proposal['value'].iterrows():
                feature = get_privince_geojson_data(geojson=self._privinces_geojson,
                                                    name=proposal['value'][self.address_key][index])
                trow = (proposal['value'][self.address_key][index], proposal['value'][self.value_key][index],
                        feature["properties"]["cp"][0],
                        feature["properties"]["cp"][1])
                tempdata.append(trow)

        cmin = min(dt[1] for dt in tempdata)
        cminlog10 = math.floor(math.log10(abs(cmin)))
        cminmod = cmin // math.pow(10, cminlog10)
        self.codomainmin = int(cminmod * math.pow(10, cminlog10))

        cmax = max(dt[1] for dt in tempdata)
        cmaxlog10 = math.floor(math.log10(abs(cmax)))
        cmaxmod = cmax // math.pow(10, cmaxlog10)
        self.codomainmax = int((cmaxmod + 1) * math.pow(10, cmaxlog10))
        return tempdata

    def __init__(self, name, data, **kwargs):
        super(RankSymbolThemeLayer, self).__init__(**kwargs)
        self.name = name
        self.data = data

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
        rslider = IntRangeSlider(value=[self.rrange[0], self.rrange[1]],
                                 min=self.rrange[0],
                                 max=self.rrange[1],
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
                            value=self.color,
                            disabled=False,
                            layout=Layout(width="350px"))
        link((color, 'value'), (self, 'color'))
        return VBox([codomainslider, rslider, color])
