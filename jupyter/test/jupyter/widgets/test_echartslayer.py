from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, EchartsLayer


class EchartsLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_heat_layer(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = EchartsLayer();
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.option = {"test": 1}
        expected = {'method': 'update', 'state': {'option': {"test": 1}}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
