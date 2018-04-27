from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.codingui.comon import Option


class TestCommon(TestCase):
    def test_option(self):
        callback = MagicMock()
        option = Option(callback, 'add')
        option.add()
        callback.assert_called()
        option()
        self.assertEqual(callback.call_count, 2)