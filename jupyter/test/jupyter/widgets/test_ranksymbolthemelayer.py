from unittest import TestCase
from unittest.mock import Mock, patch
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel
from iclientpy.jupyter import MapView, RankSymbolThemeLayer, SymbolSetting


class RankSymbolThemeLayerTest(TestCase):
    @patch.object(Comm, 'send')
    def test_rank_symbol_theme_layer(self, mock_send):
        """
        :type mock_send:Mock
        :type layer:RankSymbolThemeLayer
        :param mock_send:
        :return:
        """
        layer = RankSymbolThemeLayer(name='test1',
                                     data=[{'name': '北京市', 'value': 23014.59},
                                           {'name': '天津市', 'value': 16538.189999999999},
                                           {'name': '河北省', 'value': 29806.110000000001}],
                                     address_key='name',
                                     value_key='value');
        layer._map = MapView()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.name = "test"
        expected = {'method': 'update', 'state': {'name': 'test'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])

    def test_symbol_setting(self):
        setting = SymbolSetting(codomain=(0, 40000), fill_opacity=0.5)
        setting_dict = setting.get_settings()
        self.assertEqual(setting_dict['codomain'], (0, 40000))
        self.assertEqual(setting_dict['circleStyle']['fillOpacity'], 0.5)
