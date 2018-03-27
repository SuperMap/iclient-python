from unittest import TestCase, mock
from iclientpy import GeoLines
from io import StringIO
from .common import MockMapView


class MockEchatsLayer(object):
    def __init__(self, option):
        self.option = option


class GeoLinesTestCase(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('iclientpy.MapView', MockMapView)
    @mock.patch('iclientpy.EchartsLayer', MockEchatsLayer)
    def test_ipython_display(self, mockout: StringIO):
        data = [
            [[{'name': '北京'}, {'name': '上海', 'value': 95}], [{'name': '北京'}, {'name': '广州', 'value': 90}],
             [{'name': '北京'}, {'name': '大连', 'value': 80}], [{'name': '北京'}, {'name': '南宁', 'value': 70}],
             [{'name': '北京'}, {'name': '南昌', 'value': 60}], [{'name': '北京'}, {'name': '拉萨', 'value': 50}],
             [{'name': '北京'}, {'name': '长春', 'value': 40}], [{'name': '北京'}, {'name': '包头', 'value': 30}],
             [{'name': '北京'}, {'name': '重庆', 'value': 20}], [{'name': '北京'}, {'name': '常州', 'value': 10}]],
            [[{'name': '上海'}, {'name': '包头', 'value': 95}], [{'name': '上海'}, {'name': '昆明', 'value': 90}],
             [{'name': '上海'}, {'name': '广州', 'value': 80}], [{'name': '上海'}, {'name': '郑州', 'value': 70}],
             [{'name': '上海'}, {'name': '长春', 'value': 60}], [{'name': '上海'}, {'name': '重庆', 'value': 50}],
             [{'name': '上海'}, {'name': '长沙', 'value': 40}], [{'name': '上海'}, {'name': '北京', 'value': 30}],
             [{'name': '上海'}, {'name': '丹东', 'value': 20}], [{'name': '上海'}, {'name': '大连', 'value': 10}]],
            [[{'name': '广州'}, {'name': '福州', 'value': 95}], [{'name': '广州'}, {'name': '太原', 'value': 90}],
             [{'name': '广州'}, {'name': '长春', 'value': 80}], [{'name': '广州'}, {'name': '重庆', 'value': 70}],
             [{'name': '广州'}, {'name': '西安', 'value': 60}], [{'name': '广州'}, {'name': '成都', 'value': 50}],
             [{'name': '广州'}, {'name': '常州', 'value': 40}], [{'name': '广州'}, {'name': '北京', 'value': 30}],
             [{'name': '广州'}, {'name': '北海', 'value': 20}], [{'name': '广州'}, {'name': '海口', 'value': 10}]]
        ]
        chart = GeoLines(data, address_key='name', value_key='value', names=['北京', '上海', '广州'], symbol_size=15,
                         symbol='plane', selected_mode='multiple')
        chart.compute_bounds = mock.Mock(return_value=[[1, 2], [3, 4]])
        chart.compute_pos = mock.Mock(return_value=[[1, 2], [3, 4]])
        chart.compute_coords = mock.Mock(return_value=[[1, 2], [3, 4]])
        chart._ipython_display_()
        self.assertEqual(mockout.getvalue(), 'python_display method\n')
        self.assertEqual(chart.map.fit_bounds, [[1, 2], [3, 4]])
        self.assertEqual(len(chart.map.layers), 1)
        self.assertIsInstance(chart.layer, MockEchatsLayer)

    def test_compute_pos(self):
        chart = GeoLines([], address_key='name', value_key='value', names=['北京', '上海', '广州'], symbol_size=15,
                         symbol='plane', selected_mode='multiple')
        result = chart.compute_pos([[{'name': '北京'}, {'name': '上海', 'value': 95}]])
        self.assertEqual(result, [{"name": "上海", 'value': [121.47398, 31.230075, 95]}])

    def test_compute_coords(self):
        chart = GeoLines([], address_key='name', value_key='value', names=['北京', '上海', '广州'], symbol_size=15,
                         symbol='plane', selected_mode='multiple')
        result = chart.compute_coords([[{'name': '北京'}, {'name': '上海', 'value': 95}]])
        self.assertEqual(result, [{'coords': [[116.407283, 39.904557], [121.47398, 31.230075]]}])
