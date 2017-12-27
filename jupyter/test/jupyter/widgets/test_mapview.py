from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, CloudTileLayer


class MapViewTest(TestCase):
    @patch.object(Comm, 'send')
    def test_map_view(self, mock_send):
        """
        :type mock_send:Mock
        :tpye map:SuperMapMap
        :param mock_send:
        :return:
        """
        map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        map.comm = comm
        map.mapName = 'quanguo'
        self.assertIsInstance(map.default_tiles, CloudTileLayer)
