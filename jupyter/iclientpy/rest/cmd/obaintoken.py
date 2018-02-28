import sys
import argparse
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.model import PostTokenParameter, ClientType


def get_parser():
    parser = argparse.ArgumentParser(usage='%(prog)s [OPTIONS]',
                                     epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
            更新切片
        """)
    require_group = parser.add_argument_group('必选参数')
    require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    require_group.add_argument('-u', '--user', dest='username', help='用户名')
    require_group.add_argument('-p', '--password', dest='password', help='密码')
    require_group.add_argument('-c', '--client_type', dest='client_type',
                               choices=['IP', 'Referer', 'RequestIP', 'NONE'],
                               help='发放令牌的方式。支持以下四个取值，分别对应四种发放令牌的方式：IP，即指定的 IP 地址；Referer，即指定的 URL；RequestIP，即发送申请令牌请求的客户端 IP；NONE，即不做任何验证。')
    require_group.add_argument('-e', '--expiration', dest='expiration',
                               help='申请令牌的有效期，默认单位为分钟，支持单位m(分)，h(小时)，d(天)，w(周)，M(月)，y(年)')
    optional_group = parser.add_argument_group('可选参数')
    optional_group.add_argument('--ip', dest='ip', help='clientType=IP 时，必选。 如果按照指定 IP 的方式申请令牌，则传递相应的 IP 地址。')
    optional_group.add_argument('--referer', dest='referer',
                                help='clientType=Referer 时，必选。如果按照指定 URL 的方式申请令牌，则传递相应的 URL。')
    return parser


minutes_per_unit = {"m": 1, "h": 60, "d": 1440, "w": 10080, "M": 43200, 'y': 525600}


def convert_to_minutes(s):
    return int(s) if s[-1].isdigit() else int(s[:-1]) * minutes_per_unit[s[-1]]


def main(argv=sys.argv[1:]):
    parser = get_parser()
    try:
        args = parser.parse_known_args(argv)[0]
        d = vars(args)
        d = dict((k, v) for k, v in d.items() if not (v is None))
        # interact(d)
        api = APIFactory(d['address'], d['username'], d['password'])
        security = api.security_service()
        param = PostTokenParameter()
        param.userName = d['username']
        param.password = d['password']
        param.expiration = convert_to_minutes(d['expiration'])
        param.clientType = d['client_type']
        if 'ip' in d:
            param.ip = d['ip']
        if 'refer' in d:
            param.referer = d['refer']
        tokenstr = security.post_tokens(param)
        print(tokenstr)
    except SystemExit as err:
        return err.code
    return 0
