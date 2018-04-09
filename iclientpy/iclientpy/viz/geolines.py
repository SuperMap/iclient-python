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

    def prepare_total(self, datas):
        total_array = []
        for data in datas:
            sum = 0
            for d in data:
                sum = sum + float(d[1][self._layer_option["value_key"]])
            total_array.append(sum)
        self.total_array = total_array
        self.max_size = self._layer_option["max_symbolsize"]
        self.min_size = self._layer_option["min_symbolsize"]
        self.size_sub = self.max_size - self.min_size
        self.max_total = max(self.total_array)
        self.min_total = min(self.total_array)

    def compute_size(self, index):
        val_div = (self.total_array[index] - self.min_total) / (
        self.max_total - self.min_total if self.max_total - self.min_total > 0 else 1)
        return int(self.size_sub * val_div + self.min_size)

    def _ipython_display_(self, **kwargs):
        series = []
        i = 0
        self.prepare_total(self._data)
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
                "symbolSize": 10,
                "effect": {
                    "show": True,
                    "period": 6,
                    "trailLength": 0,
                    "symbol": self._layer_option["symbol"],
                    "symbolSize": self.compute_size(i)
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
                'symbolSize': 5,
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
                "data": self._layer_option["names"],
                "selectedMode": self._layer_option["selected_mode"],
                "selected": {
                    k: "selected_legend" not in self._layer_option or k in self._layer_option["selected_legend"] for k
                    in self._layer_option["names"]}
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
