from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy import env
from iclientpy.env import *


class TestProfile(TestCase):

    def test_get_default_not_set(self):
        env._default_profile = None
        with self.assertRaises(Exception):
            env.get_profile()

    def test_add_then_get(self):
        env.add_server_username_password_profile(name='iserver8090',url='http://localhost:8090/iserver', username='admin',  passwd='iserver')
        profile = env.get_profile()
        u_p_authentication = profile.authentication #type: UsernamePasswdAuthentication
        self.assertEqual(u_p_authentication.username, 'admin')
        self.assertEqual(u_p_authentication.passwd, 'iserver')
        self.assertEqual(profile.url, 'http://localhost:8090/iserver')

        profile = env.get_profile(name='iserver8090')
        u_p_authentication = profile.authentication #type: UsernamePasswdAuthentication
        self.assertEqual(u_p_authentication.username, 'admin')
        self.assertEqual(u_p_authentication.passwd, 'iserver')
        self.assertEqual(profile.url, 'http://localhost:8090/iserver')

        env.add_server_token_profile('token8090', 'http://localhost:8091/iserver', 'tokenvalue')

        profile = env.get_profile(name='token8090')
        token_authentication = profile.authentication #type: TokenAuthentication
        self.assertEqual(token_authentication.token, 'tokenvalue')
        self.assertEqual(profile.url, 'http://localhost:8091/iserver')
