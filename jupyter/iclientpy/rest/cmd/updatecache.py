import sys
import argparse
from iclientpy.rest.api.updatetileset import update_smtilestileset


#
# def run(argv):
#     print(argv)


def get_parser():
    parser = argparse.ArgumentParser(usage='%(prog)s [OPTIONS]',
                                     epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
            更新切片
        """)
    require_group = parser.add_argument_group('必选参数')
    require_group.add_argument('-l', '--uri', dest='address', help='服务地址')
    require_group.add_argument('-u', '--user', dest='username', help='用户名')
    require_group.add_argument('-p', '--password', dest='password', help='密码')
    require_group.add_argument('-w', '--w-loc', dest='w_loc', help='工作空间路径')
    require_group.add_argument('-m', '--map-name', dest='map_name', help='切图地图名称')
    require_group.add_argument('-o', '--origin-point', dest='original_point', help='切图原点')
    require_group.add_argument('-b', '--bounds', dest='cache_bounds', help='缓存范围')
    require_group.add_argument('-s', '--scale', dest='scale', help='缓存比例尺')
    require_group.add_argument('--u-loc', dest='u_loc', help='待更新切图文件位置')
    optional_group = parser.add_argument_group('可选参数')
    optional_group.add_argument('--service-type', dest='w_servicetype', help='工作空间服务类型')
    optional_group.add_argument('--tile-size', dest='tile_size', help='切片大小')
    optional_group.add_argument('--tile-type', dest='tile_type', help='切片类型')
    optional_group.add_argument('--format', dest='format', help='切片输出格式')
    optional_group.add_argument('--epsgcode', dest='epsg_code', help='投影')
    optional_group.add_argument('--storageid', dest='storageid', help='存储id')
    return parser


def ask_value(tip: str):
    print(tip, end=' ')
    return input('')


def interact(d):
    if 'address' not in d:
        d['address'] = ask_value('请输入地址：')
    if 'username' not in d:
        d['username'] = ask_value('请输入用户名：')
    if 'password' not in d:
        d['password'] = ask_value('请输入密码：')
    if 'w_loc' not in d:
        d['w_loc'] = ask_value('请输入工作空间路径：')
    if 'map_name' not in d:
        d['map_name'] = ask_value('请输入切图地图名称：')
    if 'original_point' not in d:
        d['original_point'] = ask_value('请输入切图原点：')
    if 'cache_bounds' not in d:
        d['cache_bounds'] = ask_value('请输入缓存范围：')
    if 'scale' not in d:
        d['scale'] = ask_value('请输入切图比例尺：')
    if 'u_loc' not in d:
        d['u_loc'] = ask_value('请输入待更新切图文件位置：')


def main(argv=sys.argv[1:]):
    parser = get_parser()
    try:
        args = parser.parse_args(argv)
        d = vars(args)
        d = dict((k, v) for k, v in d.items() if not (v is None))
        interact(d)
        d['original_point'] = tuple(float(item) for item in d['original_point'].strip("'").strip('"').split(','))
        d['cache_bounds'] = tuple(float(item) for item in d['cache_bounds'].strip("'").strip('"').split(','))
        d['scale'] = [float(item) for item in d['scale'].strip("'").strip('"').split(',')]
        update_smtilestileset(**d)
        # run(d)
    except SystemExit as err:
        return err.code
    return 0
