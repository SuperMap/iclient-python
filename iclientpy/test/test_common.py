from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.codingui.comon import Option, NamedObjects


class TestCommon(TestCase):
    def test_option(self):
        callback = MagicMock()
        option = Option(callback, 'add')
        option.add()
        callback.assert_called()
        option()
        self.assertEqual(callback.call_count, 2)

    def test_NamedObjects(self):
        named = NamedObjects()
        named['a'] = object()
        named['b'] = object()
        original_a = named.a
        self.assertIs(named[0], named.a)
        self.assertIs(named[1], named.b)

        named['a'] = object()
        self.assertIsNot(original_a, named.a)
        self.assertIs(named[0], named.a)