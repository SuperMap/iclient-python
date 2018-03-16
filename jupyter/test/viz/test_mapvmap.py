from unittest import TestCase, mock
from iclientpy import MapvMap
from io import StringIO
from .common import MockMapView


class MockMapVLayer(object):
    def __init__(self, data_set):
        self.data_set = data_set


class HeatMapTestCase(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('iclientpy.MapView', MockMapView)
    @mock.patch('iclientpy.MapVLayer', MockMapVLayer)
    def test_ipython_display(self, mockout: StringIO):
        data = [[1, 2, 3], [4, 5, 6]]
        mapvmap = MapvMap(data)
        mapvmap.compute_bounds = mock.Mock(return_value=[[1, 2], [3, 4]])
        mapvmap._ipython_display_()
        self.assertEqual(mockout.getvalue(), 'python_display method\n')
        self.assertEqual(mapvmap.map.fit_bounds, [[1, 2], [3, 4]])
        self.assertEqual(len(mapvmap.map.layers), 1)
        self.assertIsInstance(mapvmap.layer, MockMapVLayer)
