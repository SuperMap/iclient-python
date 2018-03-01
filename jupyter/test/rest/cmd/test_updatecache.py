from unittest import TestCase
from io import StringIO
from unittest.mock import MagicMock, patch
from iclientpy.rest.cmd.updatecache import main, interact


class TestUpdateCache(TestCase):
    def test(self):
        def fun(*arg, **kwargs):
            self.assertDictEqual(kwargs, {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                                          'password': 'iServer123', 'component_name': 'cache-World',
                                          'w_loc': '..\\..\\..\\data\\WorldNew\\World.sxwu', 'map_name': 'World',
                                          'original_point': (-180.0, 90.0), 'cache_bounds': (0.0, 0.0, 180.0, 90.0),
                                          'scale': [4000000.0, 8000000.0], 'remote_workspace': False, 'quite': True,
                                          'update': False})

        main(
            r"-l http://localhost:8090/iserver --user admin --password iServer123  --component-name cache-World -w ..\..\..\data\WorldNew\World.sxwu -m World -o '-180,90' -b 0,0,180,90 -s 4000000,8000000 --rw=False --quite"
                .split(' '),
            fun)

    @patch('builtins.input',
           side_effect=['http://192.168.20.158:8090/iserver', 'admin', 'iserver', 'cache-world', './World.zip', 'World',
                        '-180,90', '0,-90,180,90'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_interact(self, mock_out: StringIO, mock_in: StringIO):
        d = {}
        interact(d)
        field_and_desc = {
            'address': 'http://192.168.20.158:8090/iserver',
            'username': 'admin',
            'password': 'iserver',
            'component_name': 'cache-world',
            'w_loc': './World.zip',
            'map_name': 'World',
            'original_point': '-180,90',
            'cache_bounds': '0,-90,180,90'
        }
        for key, value in d.items():
            self.assertEqual(field_and_desc[key], value)
