from ipyleaflet import TileLayer
from traitlets import Unicode
from iclientpy._version import EXTENSION_VERSION


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
