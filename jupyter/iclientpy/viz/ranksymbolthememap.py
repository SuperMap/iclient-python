from .abstractmap import AbstractMap
import iclientpy as icp


class RankSymbolThemeMap(AbstractMap):
    def __init__(self, data, **kwargs):
        self._data = data
        self._layer_kwargs = kwargs
        super(RankSymbolThemeMap, self).__init__(**kwargs)

    def _ipython_display_(self, **kwargs):
        map = icp.MapView()
        layer = icp.RankSymbolThemeLayer(data=self._data, **self._layer_kwargs)
        map.add_layer(layer)
        map.fit_bounds = self.compute_bounds(layer.data, lat_key=lambda d: d[3], lng_key=lambda d: d[2])
        self.map = map
        self.layer = layer
        map._ipython_display_(**kwargs)
