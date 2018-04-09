from ipywidgets import Widget
from iclientpy import Layer, Map


class AbstractMap(Widget):
    layer: Layer = None
    map: Map = None

    def __init__(self, **kwargs):
        super(AbstractMap, self).__init__(**kwargs)

    def compute_bounds(self, data, lat_key, lng_key):
        return [[lat_key(min(data, key=lat_key)), lng_key(min(data, key=lng_key))],
                [lat_key(max(data, key=lat_key)), lng_key(max(data, key=lng_key))]]

    def interact(self):
        return self.layer.interact()
