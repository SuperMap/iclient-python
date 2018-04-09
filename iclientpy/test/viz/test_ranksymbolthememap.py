from unittest import TestCase, mock
from iclientpy import RankSymbolThemeMap
from io import StringIO
from .common import MockMapView


class MockRankSymbolThemeLayer(object):
    def __init__(self, data):
        self.data = [[1, 1, 1, 1], [2, 2, 2, 2]]


class RankSymbolThemeTestCase(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('iclientpy.MapView', MockMapView)
    @mock.patch('iclientpy.RankSymbolThemeLayer', MockRankSymbolThemeLayer)
    def test_ipython_display(self, mockout: StringIO):
        data = [[1, 2, 3], [4, 5, 6]]
        rankmap = RankSymbolThemeMap(data)
        rankmap.compute_bounds = mock.Mock(return_value=[[1, 2], [3, 4]])
        rankmap._ipython_display_()
        self.assertEqual(mockout.getvalue(), 'python_display method\n')
        self.assertEqual(rankmap.map.fit_bounds, [[1, 2], [3, 4]])
        self.assertEqual(len(rankmap.map.layers), 1)
        self.assertIsInstance(rankmap.layer, MockRankSymbolThemeLayer)
