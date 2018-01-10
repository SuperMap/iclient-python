from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.rest.decorator import *



class TestREST(TestCase):

    def test(self):
        rest = REST(TestREST.test, HttpMethod.POST, 'uri/abc')
        self.assertEqual(rest.get_uri(), '/uri/abc')