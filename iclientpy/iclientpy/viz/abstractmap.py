from iclientpy import Layer, Map


class AbstractMap:
    layer: Layer = None
    map: Map = None
    _url: str = None
    _crs: str = None

    def set_base_map_options(self, url: str, crs: str = 'EPSG3857'):
        self._url = url
        self._crs = crs

    def compute_bounds(self, data, lat_key, lng_key):
        return [[lat_key(min(data, key=lat_key)), lng_key(min(data, key=lng_key))],
                [lat_key(max(data, key=lat_key)), lng_key(max(data, key=lng_key))]]

    def interact(self):
        return self.layer.interact()
