import iclientpy as icp
from .abstractmap import AbstractMap


class MapvMap(AbstractMap):
    def __init__(self, data, **kwargs):
        self._data = data
        self._layer_kwargs = kwargs

    def _ipython_display_(self, **kwargs):
        if self._url is None:
            self.map = icp.MapView()
        else:
            default_tile = icp.TileMapLayer(url=self._url)
            self.map = icp.MapView(default_tiles=default_tile, crs=self._crs)
        self.layer = icp.MapVLayer(data_set=self._data, **self._layer_kwargs)
        self.map.add_layer(self.layer)
        self.map.fit_bounds = self.compute_bounds(self._data, lat_key=lambda d: d['geometry']['coordinates'][1],
                                                  lng_key=lambda d: d['geometry']['coordinates'][0])
        self.map._ipython_display_(**kwargs)
