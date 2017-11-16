from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from ipyiclient.iclient import Layer
from ipyiclient.iclient import Map
from ipyiclient.iclient import Markers
from ipyiclient.iclient import Marker
from ipyiclient.iclient import Icon
from ipykernel.comm import Comm
from ipykernel.kernelbase import Kernel


class TestIClient(TestCase):
    @patch.object(Comm, 'send')
    def test_layer(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        layer = Layer();
        layer._map = Map()
        comm = Comm()
        comm.kernel = Kernel()
        layer.comm = comm
        layer.options = ['pan']
        expected = {'method': 'update', 'state': {'options': ['pan']}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        layer.visibility = True
        expectedVisibility = {'method': 'update', 'state': {'visibility': True}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expectedVisibility, buffers=[])
        self.assertEqual(mock_send.call_count, 2)

    @patch.object(Comm, 'send')
    def test_icon(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        icon = Icon()
        comm = Comm()
        comm.kernel = Kernel()
        icon.comm = comm
        icon.url = 'test/url/test.png'
        expected = {'method': 'update', 'state': {'url': 'test/url/test.png'}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        icon.size = (25, 24)
        expected = {'method': 'update', 'state': {'size': (25, 24)}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        icon.offset = (1, 2)
        expected = {'method': 'update', 'state': {'offset': (1, 2)}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        self.assertEqual(mock_send.call_count, 3)

    @patch.object(Comm, 'send')
    def test_marker(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        marker = Marker()
        comm = Comm()
        comm.kernel = Kernel()
        marker.comm = comm
        icon = Icon()
        marker.icon = icon
        expected = {'method': 'update', 'state': {'icon': 'IPY_MODEL_' + icon.model_id}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        marker.lonlat = (12345, 45678)
        expected = {'method': 'update', 'state': {'lonlat': (12345, 45678)}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        self.assertEqual(mock_send.call_count, 2)

    @patch.object(Comm, 'send')
    def test_markers(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        markers = Markers()
        comm = Comm()
        comm.kernel = Kernel()
        markers.comm = comm
        marker = Marker()
        markers.add_marker(marker)
        expected = {'method': 'update', 'state': {'markers': ['IPY_MODEL_' + marker.model_id]}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        markers.opacity = 0.5
        expected = {'method': 'update', 'state': {'opacity': 0.5}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        markers.is_base_layer = True
        expected = {'method': 'update', 'state': {'is_base_layer': True}, 'buffer_paths': []}
        mock_send.assert_called_with(data=expected, buffers=[])
        self.assertEqual(mock_send.call_count, 3)

    @patch.object(Comm, 'send')
    def test_map(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:
        """
        map = Map()
        comm = Comm()
        comm.kernel = Kernel()
        map.comm = comm
        markers = Markers()
        map.add_layer(markers)
        expected = {'method': 'update', 'state': {'layers': ['IPY_MODEL_' + markers.model_id]}, 'buffer_paths': []}
        mock_send.assert_called_once_with(data=expected, buffers=[])

    @patch.object(Comm, 'send')
    def test_map_add(self, mock_send):
        """
        :type mock_send:Mock
        :param mock_send:
        :return:        """
        map = Map()
        comm = Comm()
        comm.kernel = Kernel()
        map.comm = comm
        markers = Markers()
        map += markers
        expected = {'method': 'update', 'state': {'layers': ['IPY_MODEL_' + markers.model_id]}, 'buffer_paths': []}
        mock_send.assert_called_once_with(data=expected, buffers=[])
