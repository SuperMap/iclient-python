from .heatmap import *
from .ranksymbolthememap import *
from .mapvmap import *
from functools import wraps
from iclientpy import SymbolSetting, MapvOptions


def init_map_decorator(clz: type):
    def init_method(func):
        @wraps(func)
        def init_map(*args, **kwargs):
            return clz(*args, **kwargs)

        return init_map

    return init_method


@init_map_decorator(HeatMap)
def heatmap(data, radius: int = 100, min_opacity: float = 0.9, blur: int = 100, max_zoom: int = -1, max: float = 1.0,
            gradient: dict = {}):
    pass


@init_map_decorator(RankSymbolThemeMap)
def ranksymbolthememap(data, symbol_setting: SymbolSetting = None, address_key: str = '', value_key: str = '',
                       is_over_lay: bool = True):
    pass


@init_map_decorator(MapvMap)
def honeycombmap(data, map_v_options: MapvOptions = None):
    pass
