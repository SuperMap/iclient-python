from ipyleaflet import Map
from traitlets import Unicode, List, Bool, Int, default
from ipywidgets import Layout
from iclientpy._version import EXTENSION_VERSION
from .cloudtilelayer import CloudTileLayer


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
