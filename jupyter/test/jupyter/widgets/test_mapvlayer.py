from unittest import TestCase
from unittest.mock import Mock, patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, MapVLayer, MapvOptions


class MapVLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_map_v_layer(self, mock_send):
        """
        :type mock_send:Mock
        :type layer:MapVLayer
        :param mock_send:
        :return:
        """
        layer = MapVLayer(
            data_set=[{"geometry": {"type": "Point", "coordinates": [117.6516476632447, 24.79141797359827]},
                       "count": 14.491465292723886},
                      {"geometry": {"type": "Point", "coordinates": [115.40463990328632, 29.776387718326674]},
                       "count": 14.067846279906583},
                      {"geometry": {"type": "Point", "coordinates": [114.3864486463097, 28.931467637939697]},
                       "count": 8.496995944766768}])
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.shadow_blur = 50
        sb_expected = {'method': 'update', 'state': {'shadow_blur': 50}, 'buffer_paths': []}
        mock_send.assert_called_with(data=sb_expected, buffers=[])

    def test_map_v_options(self):
        options = MapvOptions(fill_style="#3732FA", shadow_blur=20, label_show=True)
        options_dict = options.get_settings()
        self.assertEqual(options_dict['fillStyle'], "#3732FA")
        self.assertEqual(options_dict['shadowBlur'], 20)
        self.assertTrue(options_dict['label']['show'])
        self.assertEqual(options_dict['draw'], "honeycomb")
