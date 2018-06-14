from notebook.notebookapp import main as nbmain
from os.path import join as pjoin, abspath, dirname, exists
from os import mkdir
import argparse
import sys


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
                Online启动示范代码
            """)
    parser.add_argument('-u', '--user', dest='username', help='用户名')
    parser.add_argument('-p', '--password', dest='password', help='密码')
    parser.add_argument('--dir', dest='notebook_dir', default='.', help='notebook目录')
    parser.add_argument('--ip', dest='ip', default='localhost', help='notebook服务ip')
    parser.add_argument('--port', dest='port', default=8888, type=int, help='notebook服务端口')

    return parser


def main(argv=sys.argv[1:]):
    parser = get_parser()
    try:
        args = parser.parse_known_args(argv)[0]
        d = vars(args)
        d = dict((k, v) for k, v in d.items() if not (v is None))
        notebook_dir = d['notebook_dir']
        ip = d['ip']
        port = d['port']
        param = []
        if "username" in d:
            param.append(d["username"])
        if "password" in d:
            param.append(d["password"])

        if notebook_dir == '.':
            if not exists(pjoin(notebook_dir, "iclientpy")):
                notebook_dir = '.\iclientpy'
            else:
                i = 1
                while exists(pjoin(notebook_dir, "iclientpy-%s" % i)):
                    i += 1
                notebook_dir = ".\iclientpy-%s" % i
        if not exists(notebook_dir):
            mkdir(notebook_dir)
        with open(pjoin(abspath(dirname(__file__)), 'online_template.ipynb'), mode='r', encoding='utf8') as src:
            with open(pjoin(notebook_dir, 'preliminary_online.ipynb'), mode='w+', encoding='utf8') as tar:
                for line in src.readlines():
                    line = line.replace('{param}', ','.join(["'" + p + "'" for p in param]))
                    tar.write(line)
        sys.argv = sys.argv[:1]
        nbmain(notebook_dir=notebook_dir, ip=ip, port=port)
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
