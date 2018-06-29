from unittest import TestCase, mock
from iclientpy.rest.cmd.updatecache import main, update_cache, recache, cache_local_workspace, cache_remote_service
import argparse


class TestUpdateCache(TestCase):
    @mock.patch('iclientpy.rest.cmd.updatecache.update_cache')
    def test_main_updatecache(self, mock_method: mock.MagicMock):
        main(
            r"updatecache -l http://localhost:8090/iserver --user admin --password iServer123  --component-name cache-World -w ..\..\..\data\WorldNew\World.sxwu -m World -o '-180,90' -b 0,0,180,90 -s 4000000,8000000 --rw=False --quiet"
                .split(' '))

        args = mock_method.call_args[0][0]  # type:   argparse.Namespace

        kwargs = args._get_kwargs()
        del kwargs[5]  # 删除func
        self.assertEqual(kwargs, [('address', 'http://localhost:8090/iserver'), ('cache_bounds', '0,0,180,90'),
                                  ('component_name', 'cache-World'), ('epsg_code', None), ('format', None),
                                  ('map_name', 'World'), ('original_point', "'-180,90'"), ('password', 'iServer123'),
                                  ('quiet', True), ('remote_workspace', False), ('scale', '4000000,8000000'),
                                  ('source_component_name', None), ('storageid', None), ('tile_size', None),
                                  ('tile_type', None), ('token', None), ('update', False), ('username', 'admin'),
                                  ('w_loc', '..\\..\\..\\data\\WorldNew\\World.sxwu'), ('w_servicetype', None)])

    @mock.patch('iclientpy.rest.cmd.updatecache.update_smtilestileset')
    def test_cache(self, mock_method: mock.MagicMock):
        param = {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                 'password': 'iServer123', 'component_name': 'cache-World',
                 'w_loc': '..\\..\\..\\data\\WorldNew\\World.sxwu', 'map_name': 'World',
                 'original_point': "'-180.0, 90.0'", 'cache_bounds': "'0.0, 0.0, 180.0, 90.0'",
                 'scale': '4000000.0, 8000000.0', 'remote_workspace': False, 'quiet': True,
                 'update': False, 'func': 'f'}
        ns = argparse.Namespace(**param)
        update_cache(ns)
        args = mock_method.call_args[1]
        self.assertEqual(args, {'address': 'http://localhost:8090/iserver', 'username': 'admin',
                                'password': 'iServer123', 'component_name': 'cache-World',
                                'w_loc': '..\\..\\..\\data\\WorldNew\\World.sxwu', 'map_name': 'World',
                                'original_point': (-180.0, 90.0), 'cache_bounds': (0.0, 0.0, 180.0, 90.0),
                                'scale': [4000000.0, 8000000.0], 'remote_workspace': False, 'quiet': True,
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

    @mock.patch('iclientpy.rest.cmd.updatecache.cache_local_workspace')
    def test_main_cache_workspace(self, mock_method: mock.MagicMock):
        main(
            r"cacheworkspace -l http://192.168.20.182:8090/iserver -u admin -p Supermap123 -w C:/Users/liu/Desktop/World.zip -m World -o '-180,90' -b '-180,-90,180,90' -s 4000000,8000000,16000000,32000000,64000000,125000000,250000000 --quiet --jobtilesourcetype UGCV5"
                .split(' '))

        args = mock_method.call_args[0][0]  # type:   argparse.Namespace

        kwargs = args._get_kwargs()
        del kwargs[4]  # 删除func
        self.assertEqual(kwargs,
                         [('address', 'http://192.168.20.182:8090/iserver'), ('cache_bounds', "'-180,-90,180,90'"),
                          ('epsg_code', None), ('format', None), ('job_tile_source_type', 'UGCV5'),
                          ('map_name', 'World'), ('original_point', "'-180,90'"), ('output', None),
                          ('password', 'Supermap123'), ('quiet', True), ('remote_workspace', False),
                          ('scale', '4000000,8000000,16000000,32000000,64000000,125000000,250000000'),
                          ('storageid', None), ('tile_size', None), ('tile_type', None), ('token', None),
                          ('username', 'admin'), ('w_loc', 'C:/Users/liu/Desktop/World.zip')])

    @mock.patch('iclientpy.rest.cmd.updatecache.cache_workspace')
    def test_cache_workspace(self, mock_method: mock.MagicMock):
        param = {'address': 'http://192.168.20.182:8090/iserver', 'username': 'admin', 'password': 'Supermap123',
                 'w_loc': 'C:/Users/liu/Desktop/World.zip', 'map_name': 'World',
                 'scale': "4000000.0, 8000000.0, 16000000.0, 32000000.0, 64000000.0, 125000000.0, 250000000.0",
                 'original_point': "-180.0, 90.0", 'cache_bounds': "-180.0, -90.0, 180.0, 90.0", 'quiet': True,
                 'job_tile_source_type': 'SMTiles', 'func': 'f'}
        ns = argparse.Namespace(**param)
        cache_local_workspace(ns)
        args = mock_method.call_args[1]
        self.assertEqual(args, {'address': 'http://192.168.20.182:8090/iserver', 'username': 'admin',
                                'password': 'Supermap123', 'w_loc': 'C:/Users/liu/Desktop/World.zip',
                                'map_name': 'World',
                                'scale': [4000000.0, 8000000.0, 16000000.0, 32000000.0, 64000000.0, 125000000.0,
                                          250000000.0], 'original_point': (-180.0, 90.0),
                                'cache_bounds': (-180.0, -90.0, 180.0, 90.0), 'quiet': True,
                                'job_tile_source_type': 'SMTiles'})

    @mock.patch('iclientpy.rest.cmd.updatecache.cache_remote_service')
    def test_main_cache_service(self, mock_method: mock.MagicMock):
        main(
            r"cacheservice -l http://192.168.20.182:8090/iserver -u admin -p Supermap123 -c map-World -m World -o '-180,90' -b '-180,-90,180,90' -s 4000000,8000000,16000000,32000000,64000000,125000000,250000000 --quiet".split(
                ' '))
        mock_method.assert_called_once()
        args = mock_method.call_args[0][0]  # type:   argparse.Namespace

        kwargs = args._get_kwargs()
        del kwargs[5]  # 删除func
        self.assertEqual(kwargs,
                         [('address', 'http://192.168.20.182:8090/iserver'), ('cache_bounds', "'-180,-90,180,90'"),
                          ('component_name', 'map-World'), ('epsg_code', None), ('format', None),
                          ('job_tile_source_type', 'SMTiles'), ('map_name', 'World'), ('original_point', "'-180,90'"),
                          ('output', None), ('password', 'Supermap123'), ('quiet', True),
                          ('scale', '4000000,8000000,16000000,32000000,64000000,125000000,250000000'),
                          ('storageid', None), ('tile_size', None), ('tile_type', None), ('token', None),
                          ('username', 'admin')])

    @mock.patch('iclientpy.rest.cmd.updatecache.cache_service')
    def test_cache_service(self, mock_method: mock.MagicMock):
        param = {'address': 'http://192.168.20.182:8090/iserver', 'username': 'admin', 'password': 'Supermap123',
                 'component_name': 'map-World', 'map_name': 'World', 'original_point': "-180.0, 90.0",
                 'cache_bounds': "-180.0, -90.0, 180.0, 90.0",
                 'scale': "4000000.0, 8000000.0, 16000000.0, 32000000.0, 64000000.0, 125000000.0, 250000000.0",
                 'quiet': True, 'job_tile_source_type': 'UGCV5', 'func': 'f'}
        ns = argparse.Namespace(**param)
        cache_remote_service(ns)
        args = mock_method.call_args[1]
        self.assertEqual(args, {'address': 'http://192.168.20.182:8090/iserver', 'username': 'admin',
                                'password': 'Supermap123',
                                'component_name': 'map-World', 'map_name': 'World', 'original_point': (-180.0, 90.0),
                                'cache_bounds': (-180.0, -90.0, 180.0, 90.0),
                                'scale': [4000000.0, 8000000.0, 16000000.0, 32000000.0, 64000000.0, 125000000.0,
                                          250000000.0],
                                'quiet': True, 'job_tile_source_type': 'UGCV5'})
