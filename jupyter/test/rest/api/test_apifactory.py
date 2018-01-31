import unittest
from iclientpy.rest.apifactory import TokenAuth
from requests import PreparedRequest


class TokenAuthCase(unittest.TestCase):
    def test_token(self):
        token = TokenAuth('tokenvalue')
        req = PreparedRequest()
        req.url = 'http://test.com/'
        req.method='GET'
        req.prepare_auth(token)
        self.assertEqual(req.url, 'http://test.com/?token=tokenvalue')
