from ipyleaflet import Map
from traitlets import Unicode, List, Bool, Int, default
from ipywidgets import Layout
from iclientpy._version import EXTENSION_VERSION
from .cloudtilelayer import CloudTileLayer


class MapView(Map):
    """
    超图地图组件
    """

    @default('layout')
    def _default_layout(self):
        return Layout(height='500px', align_self='stretch')

    _view_name = Unicode("SuperMapMapView").tag(sync=True)
    _model_name = Unicode("SuperMapMapModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    center = List([34.5393842300, 108.9282514100]).tag(sync=True, o=True)  #:地图中心点位置
    zoom = Int(15).tag(sync=True, o=True)  #:缩放级别
    crs = Unicode('EPSG3857').tag(sync=True, o=True)  #:投影类型
    prefer_canvas = Bool(False).tag(sync=True, o=True)  #:使用canvas渲染，默认使用svg渲染

    @default('default_tiles')
    def _default_tiles(self):
        """
        设置默认底图
        """
        return CloudTileLayer()
