from .heatmap import *
from .ranksymbolthememap import *
from .mapvmap import *
from .geolines import *
from functools import wraps
from typing import List
from iclientpy import SymbolSetting, MapvOptions


def init_map_decorator(clz: type):
    def init_method(func):
        @wraps(func)
        def init_map(*args, **kwargs):
            return clz(*args, **kwargs)

        return init_map

    return init_method


def build_parameter_class(clz: type, clz_field_name: str, fields: List[str]):
    def wrapped_func(func):
        @wraps(func)
        def run_class_param_func(*args, **kwargs):
            kls_kwargs = {k: v for k, v in kwargs.items() if k in fields}
            method_kwargs = {k: v for k, v in kwargs.items() if k not in fields}
            kls = clz(**kls_kwargs)
            return func(*args, **method_kwargs, **{clz_field_name: kls})

        return run_class_param_func

    return wrapped_func


@init_map_decorator(HeatMap)
def heat(*, data, radius: int = 100, min_opacity: float = 0.9, blur: int = 100, max_zoom: int = -1, max: float = 1.0,
         gradient: dict = {}):
    """
    生成热点图

    Args:
        data: 热点图数据
        radius: 半径大小
        min_opacity: 最小透明度
        blur: 模糊度
        max_zoom: 最大缩放成都
        max: 最大值
        gradient: 级别
    """
    pass


@build_parameter_class(SymbolSetting, clz_field_name="symbol_setting",
                       fields=["codomain", "max_r", "min_r", "fill_opacity", "circle_hover_style_fill_opacity"])
@init_map_decorator(RankSymbolThemeMap)
def ranksymboltheme(*, data, address_key: str = '', value_key: str = '', is_over_lay: bool = True,
                    codomain: tuple = (0, 100), max_r: int = 100, min_r: int = 10, fill_color: str = '#FFA500',
                    fill_opacity: float = 0.8, circle_hover_style_fill_opacity: float = 0.8):
    """
    生成等级符号专题图

    Args:
        data: 数据
        address_key: 地址字段key
        value_key: 显示字段key
        is_over_lay: 是否压盖
        codomain: 显示阈值范围
        max_r: 最大半径
        min_r: 最小半径
        fill_color: 填充颜色
        fill_opacity: 透明度
        circle_hover_style_fill_opacity: 鼠标悬浮时圆的透明度
    """
    pass


@build_parameter_class(MapvOptions, clz_field_name="map_v_options",
                       fields=["shadow_color", "shadow_blur", "size", "label_show", "label_fill_style", "global_alpha",
                               "gradient"])
@init_map_decorator(MapvMap)
def honeycomb(*, data, address_key, value_key, fill_style: str = '', shadow_color: str = '', shadow_blur: int = 35,
              size: int = 5, label_show: bool = True, label_fill_style: str = '', global_alpha: float = 1,
              gradient: dict = None):
    """
    生成蜂巢图

    Args:
        data: 数据
        fill_style: 填充颜色
        shadow_color: 投影颜色
        shadow_blur: 投影模糊级数
        size: 大小
        label_show: 是否显示count值
        label_fill_style:c ount值填充样式
        global_alpha: 透明度
        gradient: 渐变颜色值设置
    """
    pass


@init_map_decorator(GeoLines)
def geolines(*, data, names: List[str], symbol_size: int = 15, symbol: str = 'plane', colors: List[str] = None):
    pass
