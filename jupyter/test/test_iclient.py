from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter.iclient import SuperMapMap
from iclientpy.jupyter.iclient import CloudTileLayer


class TestIClient(TestCase):
    @patch.object(Comm, 'send')
    def test_cloudTileLayer(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = CloudTileLayer();
        layer._map = SuperMapMap()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.mapName = 'quanguo'
        expected = {'method': 'update', 'state': {'mapName': 'quanguo'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        layer.type = 'web'
        expectedVisibility = {'method': 'update', 'state': {'type': 'web'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expectedVisibility, buffers=[])
        self.assertEqual(mock_send.call_count, 2)

    @patch.object(Comm, 'send')
    def test_SuperMapMap(self, mock_send):
        """
        :type mock_send:Mock
        :tpye map:SuperMapMap
        :param mock_send:
        :return:
        """
        map = SuperMapMap()
        comm = Comm()
        comm.kernel = Kernel()
        map.comm = comm
        map.mapName = 'quanguo'
        self.assertIsInstance(map.default_tiles, CloudTileLayer)
