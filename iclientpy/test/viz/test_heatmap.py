from unittest import TestCase, mock
from iclientpy import HeatMap
from io import StringIO
from .common import MockMapView


class MockHeatLayer(object):
    def __init__(self, heat_points):
        self.heat_point = heat_points


class HeatMapTestCase(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('iclientpy.MapView', MockMapView)
    @mock.patch('iclientpy.HeatLayer', MockHeatLayer)
    def test_ipython_display(self, mockout: StringIO):
        data = [[1, 2, 3], [4, 5, 6]]
        heatmap = HeatMap(data)
        heatmap.compute_bounds = mock.Mock(return_value=[[1, 2], [3, 4]])
        heatmap._ipython_display_()
        self.assertEqual(mockout.getvalue(), 'python_display method\n')
        self.assertEqual(heatmap.map.fit_bounds, [[1, 2], [3, 4]])
        self.assertEqual(len(heatmap.map.layers), 1)
        self.assertIsInstance(heatmap.layer, MockHeatLayer)
