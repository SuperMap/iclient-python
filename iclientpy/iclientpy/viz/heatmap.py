import iclientpy as icp
from .abstractmap import AbstractMap


class HeatMap(AbstractMap):
    def __init__(self, data, **kwargs):
        self._data = data
        self._layer_kwargs = kwargs
        super(HeatMap, self).__init__(**kwargs)

    def _ipython_display_(self, **kwargs):
        map = icp.MapView()
        layer = icp.HeatLayer(heat_points=self._data, **self._layer_kwargs)
        map.add_layer(layer)
        map.fit_bounds = self.compute_bounds(self._data, lat_key=lambda d: d[0], lng_key=lambda d: d[1])
        self.map = map
        self.layer = layer
        map._ipython_display_(**kwargs)
