from notebook.notebookapp import main as nbmain
from iclientpy.server import Server
from os.path import join as pjoin, abspath, dirname
import argparse
import sys

__all__ = ['server']

server = None


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
                iServer启动示范代码
            """)
    parser.add_argument('-l', '--uri', dest='address', help='服务地址，如：http://localhost:8090/iserver')
    parser.add_argument('-u', '--user', dest='username', help='用户名')
    parser.add_argument('-p', '--password', dest='password', help='密码')
    parser.add_argument('--dir', dest='notebook_dir', default='.', help='notebook目录')
    parser.add_argument('--ip', dest='ip', default='localhost', help='notebook服务ip')
    parser.add_argument('--port', dest='port', default=8888, type=int, help='notebook服务端口')

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
        notebook_dir = d['notebook_dir']
        ip = d['ip']
        port = d['port']
        param = [d["address"]]
        if "username" in d:
            param.append(d["username"])
        if "password" in d:
            param.append(d["password"])
        server = Server(*param)
        services = server.services
        first_map_service_name = 'map-world/rest'
        for index, name in services:
            service = services[index]
            if hasattr(service, 'maps'):
                first_map_service_name = name
                break
        map_service = services[first_map_service_name]
        maps = map_service.maps
        first_map_name = 'World'
        for map_index, map_name in maps:
            first_map_name = map_name
            break

        with open(pjoin(abspath(dirname(__file__)), 'server_template.ipynb'), mode='r', encoding='utf8') as src:
            with open(pjoin(notebook_dir, 'sample_server.ipynb'), mode='w+', encoding='utf8') as tar:
                for line in src.readlines():
                    line = line.replace('{param}', ','.join(["'" + p + "'" for p in param]))
                    line = line.replace('{map_service}', "'" + first_map_service_name + "'")
                    line = line.replace('{map_name}', first_map_name)
                    tar.write(line)
        sys.argv = sys.argv[:1]
        nbmain(notebook_dir=notebook_dir, ip=ip, port=port)
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
