from ipyleaflet import TileLayer
from traitlets import Unicode
from iclientpy._version import EXTENSION_VERSION


class CloudTileLayer(TileLayer):
    """
    超图云图层
    """
    _view_name = Unicode("SuperMapCloudTileLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapCloudTileLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    url = Unicode('').tag(sync=True) #:地址
    attribution = Unicode('').tag(sync=True, o=True)#:版权信息
    map_name = Unicode('').tag(sync=True, o=True)#:地图名称
    type = Unicode('').tag(sync=True, o=True)#:地图类型
