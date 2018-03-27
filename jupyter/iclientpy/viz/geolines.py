from .abstractmap import AbstractMap
import iclientpy as icp


class GeoLines(AbstractMap):
    def __init__(self, data, **kwargs):
        self._data = data
        self._layer_option = kwargs
        self._geojsondata = icp.load_geojson_data()
        self._all_feature = []

    def compute_coords(self, datas):
        coordses = []
        for data in datas:
            from_pos = icp.get_geojson_data(self._geojsondata, data[0][self._layer_option["address_key"]])
            to_pos = icp.get_geojson_data(self._geojsondata, data[1][self._layer_option["address_key"]])
            self._all_feature.append(from_pos)
            self._all_feature.append(to_pos)
            coordses.append({"coords": [
                [from_pos["properties"]["cp"][0], from_pos["properties"]["cp"][1]],
                [to_pos["properties"]["cp"][0], to_pos["properties"]["cp"][1]]
            ]})
        return coordses

    def compute_pos(self, datas):
        result = []
        for data in datas:
            geo_json = icp.get_geojson_data(self._geojsondata, data[1][self._layer_option["address_key"]])
            result.append({
                "name": data[1][self._layer_option["address_key"]],
                "value": [geo_json["properties"]["cp"][0], geo_json["properties"]["cp"][1],
                          data[1][self._layer_option["value_key"]]]
            })
        return result

    def _ipython_display_(self, **kwargs):
        series = []
        i = 0
        while i < len(self._data):
            data = self._data[i]
            coords = self.compute_coords(data)
            datas = self.compute_pos(data)
            line_series = {
                "name": self._layer_option["names"][i],
                "type": 'lines',
                "coordinateSystem": 'leaflet',
                "zlevel": 2,
                "symbol": ['none', 'arrow'],
                "symbolSize": self._layer_option["symbol_size"],
                "effect": {
                    "show": True,
                    "period": 6,
                    "trailLength": 0,
                    "symbol": self._layer_option["symbol"],
                    "symbolSize": 15
                },
                "lineStyle": {
                    "normal": {
                        "color": self._layer_option["colors"][i] if "colors" in self._layer_option else '',
                        "width": 1,
                        "opacity": 0.6,
                        "curveness": 0.2
                    }
                },
                "data": coords
            }
            if line_series['effect']['symbol'] == 'plane':
                line_series['effect']['symbol'] = icp.SYMBOL['plane']
            scatter_series = {
                "name": self._layer_option["names"][i],
                "type": 'effectScatter',
                'coordinateSystem': 'leaflet',
                'zlevel': 2,
                'rippleEffect': {
                    'brushType': 'stroke'
                },
                'label': {
                    'normal': {
                        'show': True,
                        'position': 'right',
                        'formatter': '{b}'
                    }
                },
                'symbolSize': self._layer_option["symbol_size"],
                'itemStyle': {
                    'normal': {
                        'color': self._layer_option["colors"][i] if "colors" in self._layer_option else ''
                    }
                },
                'data': datas
            }
            series.append(line_series)
            series.append(scatter_series)
            i = i + 1

        option = {
            "tooltip": {
                "trigger": 'item'
            },
            "legend": {
                "orient": 'vertical',
                "left": 'right',
                "data": self._layer_option["names"]
            },
            "series": series
        }
        map = icp.MapView()
        map.fit_bounds = self.compute_bounds(self._all_feature, lat_key=lambda d: d["properties"]["cp"][1],
                                             lng_key=lambda d: d["properties"]["cp"][0])
        layer = icp.EchartsLayer(option=option)
        map.add_layer(layer)
        self.map = map
        self.layer = layer
        map._ipython_display_(**kwargs)
