from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, HeatLayer


class HeatLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_heat_layer(self, mock_send):


        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = HeatLayer(heat_points=[[39.86369678193944, 116.25519414479928, 33.46073333534289],
                                       [39.85730998494624, 116.21477193093531, 20.440150687928877]]);
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.radius = 30
        expected = {'method': 'update', 'state': {'radius': 30}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        layer.blur = 50
        expected_blur = {'method': 'update', 'state': {'blur': 50}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected_blur, buffers=[])
        self.assertEqual(mock_send.call_count, 2)
