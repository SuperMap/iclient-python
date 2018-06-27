import sys
import argparse
from iclientpy.rest.api.cache import cache_localworkspace, cache_remoteworkspace


def cache_local(**args):
    del args['func']
    cache_localworkspace(**args)


def cache_remote(**args):
    del args['func']
    cache_remoteworkspace(**args)


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
            切图
        """)
    sub_parsers = parser.add_subparsers()
    cache_local_parser = sub_parsers.add_parser('cache_local')  # type: argparse.ArgumentParser
    cache_local_parser.set_defaults(func=cache_local)
    cache_local_require_group = cache_local_parser.add_argument_group('必选参数')
    cache_local_require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    cache_local_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    cache_local_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    cache_local_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    cache_local_require_group.add_argument('-w', '--w-loc', dest='w_loc', help='工作空间路径')
    cache_local_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    cache_local_require_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺分母，如：8000000,4000000,2000000')
    cache_local_require_group.add_argument('-o', '--original-point', dest='original_point',
                                           help='切图原点，需以单引号开始和结束，如：\'-180,90\'')
    cache_local_require_group.add_argument('-b', '--bounds', dest='cache_bounds',
                                           help='缓存范围，需以单引号开始和结束，如：\'-180,-90,0,0\'')
    cache_local_optional_group = cache_local_parser.add_argument_group('可选参数')
    cache_local_optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    cache_local_optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    cache_local_optional_group.add_argument('--format', dest='format', help='切片输出格式')
    cache_local_optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    cache_local_optional_group.add_argument('--storageid', dest='storageid', help='存储的id')
    cache_local_optional_group.add_argument('--quite', dest='quite', action='store_true', help='不需要确认，直接运行')
    cache_local_optional_group.add_argument('--jobtilesourcetype', dest='job_tile_source_type',
                                            choices=['SMTiles', 'MBTiles', 'UGCV5', 'GeoPackage'], default='SMTiles',
                                            help='存储类型，仅在输出到本地存储路径时生效，Mongo，OTS与FastDFS时不生效，Mongo，OTS与FastDFS应直接设置storageid')

    cache_remote_parser = sub_parsers.add_parser('cache_remote')  # type: argparse.ArgumentParser
    cache_remote_parser.set_defaults(func=cache_remote)
    cache_remote_require_group = cache_remote_parser.add_argument_group('必选参数')
    cache_remote_require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    cache_remote_require_group.add_argument('-u', '--user', dest='username', help='用户名', default=None)
    cache_remote_require_group.add_argument('-p', '--password', dest='password', help='密码', default=None)
    cache_remote_require_group.add_argument('-t', '--token', dest='token', help='用于身份验证的token')
    cache_remote_require_group.add_argument('-c', '--component-name', dest='component_name', help='服务名称')
    cache_remote_require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    cache_remote_require_group.add_argument('-o', '--original-point', dest='original_point',
                                            help='切图原点，需以单引号开始和结束，如：\'-180,90\'')
    cache_remote_require_group.add_argument('-b', '--bounds', dest='cache_bounds',
                                            help='缓存范围，需以单引号开始和结束，如：\'-180,-90,0,0\'')
    cache_remote_require_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺分母，如：8000000,4000000,2000000')
    cache_remote_optional_group = cache_remote_parser.add_argument_group('可选参数')
    cache_remote_optional_group.add_argument('--service-type', dest='w_servicetype', help='工作空间服务类型')
    cache_remote_optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    cache_remote_optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    cache_remote_optional_group.add_argument('--format', dest='format', help='切片输出格式')
    cache_remote_optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    cache_remote_optional_group.add_argument('--storageid', dest='storageid', help='存储id')
    cache_remote_optional_group.add_argument('--quite', dest='quite', action='store_true', help='不需要确认，直接运行')
    cache_remote_optional_group.add_argument('--jobtilesourcetype', dest='job_tile_source_type',
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
        d = vars(args)
        d = dict((k, v) for k, v in d.items() if k in ('username', 'password') or not (v is None))
        d['original_point'] = tuple(float(item) for item in d['original_point'].strip("'").strip('"').split(','))
        d['cache_bounds'] = tuple(float(item) for item in d['cache_bounds'].strip("'").strip('"').split(','))
        if 'scale' in d:
            d['scale'] = [float(item) for item in d['scale'].strip("'").strip('"').split(',')]
        args.func(**d)
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
