from unittest import TestCase, mock
from iclientpy import AbstractMap


class AbstractMapTestCase(TestCase):
    def test_compute_bounds(self):
        data = [[1, 2, 3], [4, 5, 6]]
        lat_key = lambda d: d[0]
        lng_key = lambda d: d[1]
        map = AbstractMap()
        result = map.compute_bounds(data, lat_key, lng_key)
        self.assertEqual(result, [[1, 2], [4, 5]])

    def test_interact(self):
        with mock.patch('iclientpy.Layer') as mock_layer:
            rankmap = AbstractMap()
            rankmap.layer = mock_layer
            method = mock.MagicMock()
            mock_layer.interact = method
            rankmap.interact()
            method.assert_called_once()
