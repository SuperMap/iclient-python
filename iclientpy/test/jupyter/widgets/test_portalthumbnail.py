from io import StringIO
from unittest import TestCase, mock
from iclientpy.jupyter import PortalThumbnail
from iclientpy.rest.api.model import ViewerMap


class MockHTML:
    def __init__(self, *args, **kwargs):
        pass

    def _ipython_display_(self, **kwargs):
        print('python_display method')


class PortalThumbnailTestCase(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('iclientpy.jupyter.portalthumbnail.HTML', MockHTML)
    def test_ipytion_display(self, mockout: StringIO):
        map = ViewerMap()
        widget = PortalThumbnail(map)
        widget._ipython_display_()
        self.assertEqual(mockout.getvalue(), 'python_display method\n')
