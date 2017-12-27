from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, TileMapLayer


class TileMapLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_tile_map_layer(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = TileMapLayer();
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.url = "http://test.com"
        expected = {'method': 'update', 'state': {'url': 'http://test.com'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
