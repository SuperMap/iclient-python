from unittest import TestCase, mock
from iclientpy.rest.cmd.updatecache import main, cache, recache
import argparse


class TestUpdateCache(TestCase):
    @mock.patch('iclientpy.rest.cmd.updatecache.cache')
    def test_main_cache(self, mock_method: mock.MagicMock):
        main(
            r"cache -l http://localhost:8090/iserver --user admin --password iServer123  --component-name cache-World -w ..\..\..\data\WorldNew\World.sxwu -m World -o '-180,90' -b 0,0,180,90 -s 4000000,8000000 --rw=False --quite"
                .split(' '))

        args = mock_method.call_args[0][0]  # type:   argparse.Namespace

        kwargs = args._get_kwargs()
        del kwargs[5]  # 删除func
        self.assertEqual(kwargs, [('address', 'http://localhost:8090/iserver'), ('cache_bounds', '0,0,180,90'),
                                  ('component_name', 'cache-World'), ('epsg_code', None), ('format', None),
                                  ('map_name', 'World'), ('original_point', "'-180,90'"), ('password', 'iServer123'),
                                  ('quite', True), ('remote_workspace', False), ('scale', '4000000,8000000'),
                                  ('source_component_name', None), ('storageid', None), ('tile_size', None),
                                  ('tile_type', None), ('token', None), ('update', False), ('username', 'admin'),
                                  ('w_loc', '..\\..\\..\\data\\WorldNew\\World.sxwu'), ('w_servicetype', None)])

    @mock.patch('iclientpy.rest.cmd.updatecache.update_smtilestileset')
    def test_cache(self, mock_method: mock.MagicMock):
        param = {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                 'password': 'iServer123', 'component_name': 'cache-World',
                 'w_loc': '..\\..\\..\\data\\WorldNew\\World.sxwu', 'map_name': 'World',
                 'original_point': "'-180.0, 90.0'", 'cache_bounds': "'0.0, 0.0, 180.0, 90.0'",
                 'scale': '4000000.0, 8000000.0', 'remote_workspace': False, 'quite': True,
                 'update': False, 'func': 'f'}
        ns = argparse.Namespace(**param)
        cache(ns)
        args = mock_method.call_args[1]
        self.assertEqual(args, {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                                'password': 'iServer123', 'component_name': 'cache-World',
                                'w_loc': '..\\..\\..\\data\\WorldNew\\World.sxwu', 'map_name': 'World',
                                'original_point': (-180.0, 90.0), 'cache_bounds': (0.0, 0.0, 180.0, 90.0),
                                'scale': [4000000.0, 8000000.0], 'remote_workspace': False, 'quite': True,
                                'update': False})

    @mock.patch('iclientpy.rest.cmd.updatecache.recache')
    def test_main_recache(self, mock_method: mock.MagicMock):
        main(r"recache -l http://localhost:8090/iserver".split(' '))
        mock_method.assert_called_once()

    @mock.patch('iclientpy.rest.cmd.updatecache.recache_tileset')
    def test_reache(self, mock_method: mock.MagicMock):
        param = {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                 'password': 'iServer123', 'component_name': 'cache-World',
                 'map_name': 'World', 'func': 'f'}
        ns = argparse.Namespace(**param)
        recache(ns)
        args = mock_method.call_args[1]
        self.assertEqual(args, {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                                'password': 'iServer123', 'component_name': 'cache-World',
                                'map_name': 'World'})
