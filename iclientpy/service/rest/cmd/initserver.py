import sys
import json
import time
import requests
import argparse
from typing import List


class _InitServer:
    def __init__(self, url: str):
        self._base_url = url if not url.endswith('/') else url[:-1]
        self._session = requests.session()

    def wait_server(self, timeout: int):
        deadline = time.time() + timeout * 60
        while (True):
            if time.time() > deadline:
                return False
            time.sleep(5)
            try:
                response = self._session.get(self._base_url + '/')
                if response.status_code == 200:
                    return True
            except requests.exceptions.ConnectionError as e:
                continue

    def registry_admin_account(self, username: str, password: str):
        entity = {'username': username, 'password': password, 'passwrod2': password}
        response = self._session.put(self._base_url + '/_setup.json', data=json.dumps(entity))
        response.raise_for_status()

    def get_all_license_module(self):
        response = self._session.get(self._base_url + '/manager/license.json')
        modules = [key for key, value in json.loads(response.text).items() if value is True]
        license_modules = []
        for l_module in modules:
            l_module = l_module[7:]
            tmp = ''
            for letter in l_module:
                tmp += letter.upper() if letter.islower() else (letter if tmp == '' else '_' + letter)
            license_modules.append(tmp)
        return license_modules

    def enable_license_module(self, modules: List[str]):
        response = self._session.put(self._base_url + '/_setup/enabledmodules.json', data=json.dumps(modules))
        response.raise_for_status()

    def init_server(self):
        response = self._session.get(self._base_url + '/_initServer')
        response.raise_for_status()


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
                iServer初始化工具
            """)
    require_group = parser.add_argument_group('必选参数')
    require_group.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    require_group.add_argument('-u', '--user', dest='username', help='用户名')
    require_group.add_argument('-p', '--password', dest='password', help='密码')
    require_group.add_argument('-t', '--timeout', dest='timeout', default=1, type=int,
                               help='超时时间，等待iServer启动的超时时间，单位为分钟')
    return parser


def main(argv=sys.argv[1:]):
    parser = get_parser()
    try:
        if not argv:
            parser.print_usage()
            parser.exit(1)
        args = parser.parse_known_args(argv)[0]
        d = vars(args)
        d = dict((k, v) for k, v in d.items() if not (v is None))
        _init = _InitServer(d['address'])
        if not _init.wait_server(d['timeout']):
            raise Exception('等待iServer服务启动超时')
        _init.registry_admin_account(d['username'], d['password'])
        license_modules = _init.get_all_license_module()
        _init.enable_license_module(license_modules)
        _init.init_server()
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
