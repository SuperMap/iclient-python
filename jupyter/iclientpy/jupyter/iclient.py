from ipyleaflet import Map, TileLayer
from traitlets import Unicode, List, Int, default
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


class SuperMapMap(Map):
    _view_name = Unicode("SuperMapMapView").tag(sync=True)
    _model_name = Unicode("SuperMapMapModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    center = List([30.656483307485072, 104.06917333602907]).tag(sync=True, o=True)
    zoom = Int(15).tag(sync=True, o=True)

    @default('default_tiles')
    def _default_tiles(self):
        return CloudTileLayer()
