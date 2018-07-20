import sys
import argparse
from iclientpy.rest.api.updatetileset import update_smtilestileset, recache_tileset
from iclientpy.rest.api.cache import cache_workspace, cache_service


def cache_local_workspace(args):
    d = vars(args)
    d = dict((k, v) for k, v in d.items() if k in ('username', 'password') or not (v is None))
    d['original_point'] = tuple(float(item) for item in d['original_point'].strip("'").strip('"').split(','))
    d['cache_bounds'] = tuple(float(item) for item in d['cache_bounds'].strip("'").strip('"').split(','))
    if 'scale' in d:
        d['scale'] = [float(item) for item in d['scale'].strip("'").strip('"').split(',')]
    del d['func']
    cache_workspace(**d)


def cache_remote_service(args):
    d = vars(args)
    d = dict((k, v) for k, v in d.items() if k in ('username', 'password') or not (v is None))
    d['original_point'] = tuple(float(item) for item in d['original_point'].strip("'").strip('"').split(','))
    d['cache_bounds'] = tuple(float(item) for item in d['cache_bounds'].strip("'").strip('"').split(','))
    if 'scale' in d:
        d['scale'] = [float(item) for item in d['scale'].strip("'").strip('"').split(',')]
    del d['func']
    cache_service(**d)


def recache(args):
    d = vars(args)
    d = dict((k, v) for k, v in d.items() if k in ('username', 'password') or not (v is None))
    del d['func']
    recache_tileset(**d)


def update_cache(args):
    d = vars(args)
    d = dict((k, v) for k, v in d.items() if k in ('username', 'password') or not (v is None))
    d['original_point'] = tuple(float(item) for item in d['original_point'].strip("'").strip('"').split(','))
    d['cache_bounds'] = tuple(float(item) for item in d['cache_bounds'].strip("'").strip('"').split(','))
    if 'scale' in d:
        d['scale'] = [float(item) for item in d['scale'].strip("'").strip('"').split(',')]
    del d['func']
    update_smtilestileset(**d)


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
            切图，更新切片命令行工具
        """)
    sub_parsers = parser.add_subparsers()
    recache_parser = sub_parsers.add_parser('recache')  # type: argparse.ArgumentParser
    recache_parser.set_defaults(func=recache)
    recache_require_group = recache_parser.add_argument_group('必选参数')
    recache_require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    recache_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    recache_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    recache_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    recache_require_group.add_argument('-c', '--component-name', dest='component_name', help='待更新缓存服务名称')
    recache_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    recache_require_group.add_argument('-s', '--storageid', dest='storageid', help='存储的id')
    recache_optional_group = recache_parser.add_argument_group('可选参数')
    recache_optional_group.add_argument('-n', '--tileset_name', dest='tileset_name', help='存储切片集名称')

    updatecache_parser = sub_parsers.add_parser('updatecache')  # type: argparse.ArgumentParser
    updatecache_parser.set_defaults(func=update_cache)
    updatecache_require_group = updatecache_parser.add_argument_group('必选参数')
    updatecache_require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    updatecache_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    updatecache_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    updatecache_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    updatecache_require_group.add_argument('-c', '--component-name', dest='component_name', help='待更新缓存服务名称')
    updatecache_require_group.add_argument('-w', '--w-loc', dest='w_loc', help='工作空间路径')
    updatecache_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    updatecache_require_group.add_argument('-o', '--original-point', dest='original_point',
                                           help='切图原点，需以单引号开始和结束，如：\'-180,90\'')
    updatecache_require_group.add_argument('-b', '--bounds', dest='cache_bounds',
                                           help='缓存范围，需以单引号开始和结束，如：\'-180,-90,0,0\'')
    updatecache_optional_group = updatecache_parser.add_argument_group('可选参数')
    updatecache_optional_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺分母，如：8000000,4000000,2000000')
    updatecache_optional_group.add_argument('--service-type', dest='w_servicetype', help='工作空间服务类型')
    updatecache_optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    updatecache_optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    updatecache_optional_group.add_argument('--format', dest='format', help='切片输出格式')
    updatecache_optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    updatecache_optional_group.add_argument('--storageid', dest='storageid', help='存储id')
    updatecache_optional_group.add_argument('-rw', dest='remote_workspace', action='store_true',
                                            help='输入的工作空间地址是远程iServer所在服务器上的地址，不需要上传工作空间。')
    updatecache_optional_group.add_argument('--quiet', dest='quiet', action='store_true', help='不需要确认，直接运行')
    updatecache_optional_group.add_argument('--source-component', dest='source_component_name', help='缓存更新数据来源服务')
    updatecache_optional_group.add_argument('--update', dest='update', action='store_true', help='更新服务缓存')

    cache_workspace_parser = sub_parsers.add_parser('cacheworkspace')  # type: argparse.ArgumentParser
    cache_workspace_parser.set_defaults(func=cache_local_workspace)
    cache_workspace_require_group = cache_workspace_parser.add_argument_group('必选参数')
    cache_workspace_require_group.add_argument('-l', '--uri', dest='address',
                                               help='服务地址，如：http://localhost:8090/iserver')
    cache_workspace_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    cache_workspace_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    cache_workspace_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    cache_workspace_require_group.add_argument('-w', '--w-loc', dest='w_loc', help='工作空间路径')
    cache_workspace_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    cache_workspace_require_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺分母，如：8000000,4000000,2000000')
    cache_workspace_require_group.add_argument('-o', '--original-point', dest='original_point',
                                               help='切图原点，需以单引号开始和结束，如：\'-180,90\'')
    cache_workspace_require_group.add_argument('-b', '--bounds', dest='cache_bounds',
                                               help='缓存范围，需以单引号开始和结束，如：\'-180,-90,0,0\'')
    cache_workspace_optional_group = cache_workspace_parser.add_argument_group('可选参数')
    cache_workspace_optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    cache_workspace_optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    cache_workspace_optional_group.add_argument('--format', dest='format', help='切片输出格式')
    cache_workspace_optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    cache_workspace_optional_group.add_argument('--storageid', dest='storageid', help='存储的id')
    cache_workspace_optional_group.add_argument('--output', dest='output', help='结果输出路径')
    cache_workspace_optional_group.add_argument('--remote-workspace', dest='remote_workspace', action='store_true',
                                                help='是否是远程工作空间路径')
    cache_workspace_optional_group.add_argument('--quiet', dest='quiet', action='store_true', help='不需要确认，直接运行')
    cache_workspace_optional_group.add_argument('--jobtilesourcetype', dest='job_tile_source_type',
                                                choices=['SMTiles', 'MBTiles', 'UGCV5', 'GeoPackage'],
                                                default='SMTiles',
                                                help='存储类型，仅在输出到本地存储路径时生效，Mongo，OTS与FastDFS时不生效，Mongo，OTS与FastDFS应直接设置storageid')

    cache_service_parser = sub_parsers.add_parser('cacheservice')  # type: argparse.ArgumentParser
    cache_service_parser.set_defaults(func=cache_remote_service)
    cache_service_require_group = cache_service_parser.add_argument_group('必选参数')
    cache_service_require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    cache_service_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    cache_service_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    cache_service_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    cache_service_require_group.add_argument('-c', '--component-name', dest='component_name', help='服务名称')
    cache_service_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    cache_service_require_group.add_argument('-o', '--original-point', dest='original_point',
                                             help='切图原点，需以单引号开始和结束，如：\'-180,90\'')
    cache_service_require_group.add_argument('-b', '--bounds', dest='cache_bounds',
                                             help='缓存范围，需以单引号开始和结束，如：\'-180,-90,0,0\'')
    cache_service_require_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺分母，如：8000000,4000000,2000000')
    cache_service_optional_group = cache_service_parser.add_argument_group('可选参数')
    cache_service_optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    cache_service_optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    cache_service_optional_group.add_argument('--format', dest='format', help='切片输出格式')
    cache_service_optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    cache_service_optional_group.add_argument('--storageid', dest='storageid', help='存储id')
    cache_service_optional_group.add_argument('--output', dest='output', help='结果输出路径')
    cache_service_optional_group.add_argument('--quiet', dest='quiet', action='store_true', help='不需要确认，直接运行')
    cache_service_optional_group.add_argument('--jobtilesourcetype', dest='job_tile_source_type',
                                              choices=['SMTiles', 'MBTiles', 'UGCV5', 'GeoPackage'], default='SMTiles',
                                              help='存储类型，仅在输出到本地存储路径时生效，Mongo，OTS与FastDFS时不生效，Mongo，OTS与FastDFS应直接设置storageid')

    return parser


def main(argv=sys.argv[1:]):
    parser = get_parser()
    try:
        if not argv:
            parser.print_usage()
            parser.exit(1)
        args = parser.parse_known_args(argv)[0]
        args.func(args)
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
