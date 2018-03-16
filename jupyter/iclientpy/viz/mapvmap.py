import iclientpy as icp
from .abstractmap import AbstractMap


class MapvMap(AbstractMap):
    def __init__(self, data, **kwargs):
        self._data = data
        self._layer_kwargs = kwargs
        super(MapvMap, self).__init__(**kwargs)

    def _ipython_display_(self, **kwargs):
        map = icp.MapView()
        layer = icp.MapVLayer(data_set=self._data, **self._layer_kwargs)
        map.add_layer(layer)
        map.fit_bounds = self.compute_bounds(self._data, lat_key=lambda d: d['geometry']['coordinates'][1],
                                             lng_key=lambda d: d['geometry']['coordinates'][0])
        self.map = map
        self.layer = layer
        map._ipython_display_(**kwargs)
