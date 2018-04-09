from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, CloudTileLayer


class CloudTileLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_cloud_tile_layer(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = CloudTileLayer();
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.map_name = 'quanguo'
        expected = {'method': 'update', 'state': {'map_name': 'quanguo'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        layer.type = 'web'
        expectedVisibility = {'method': 'update', 'state': {'type': 'web'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expectedVisibility, buffers=[])
        self.assertEqual(mock_send.call_count, 2)
