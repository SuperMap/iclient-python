from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter.widget import MapView
from iclientpy.jupyter.widget import CloudTileLayer
from iclientpy.jupyter.widget import RankSymbolThemeLayer
import iclientpy.jupyter.widget as widget


class TestIClient(TestCase):
    @patch.object(Comm, 'send')
    def test_CloudTileLayer(self, mock_send):
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
        layer.mapName = 'quanguo'
        expected = {'method': 'update', 'state': {'mapName': 'quanguo'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        layer.type = 'web'
        expectedVisibility = {'method': 'update', 'state': {'type': 'web'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expectedVisibility, buffers=[])
        self.assertEqual(mock_send.call_count, 2)

    @patch.object(Comm, 'send')
    def test_MapView(self, mock_send):
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

    def test_GetPrivinceGeoJSON(self):
        privName = '天津'
        feature = widget.get_privince_geojson_data(privName)
        self.assertEqual('天津市', feature["properties"]["name"])
        self.assertEqual([117.30463831663721, 39.288494853279495], feature["properties"]["cp"])

    @patch.object(Comm, 'send')
    def test_RankSymbolThemeLayer(self, mock_send):
        """
        :type mock_send:Mock
        :type layer:RankSymbolThemeLayer
        :param mock_send:
        :return:
        """
        layer = RankSymbolThemeLayer(name='test1', data=[]);
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.name = "test"
        expected = {'method': 'update', 'state': {'name': 'test'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
