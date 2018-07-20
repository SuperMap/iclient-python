from notebook.notebookapp import main as nbmain
from os.path import join as pjoin, abspath, dirname, exists
from os import listdir
import argparse
import sys
import shutil


def get_parser():
    parser = argparse.ArgumentParser(epilog='for more information , visit<http://iclientpy.supermap.io/>.', description="""
                iclientpy使用引导
            """)
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
        if notebook_dir == '.':
            notebook_dir = '.\iclientpy'
        if not exists(notebook_dir):
            current_path = abspath(dirname(__file__))
            sample_path = pjoin(current_path, '..', 'sample')
            shutil.copytree(sample_path, notebook_dir)
        sys.argv = sys.argv[:1]
        nbmain(notebook_dir=notebook_dir, ip=ip, port=port, token='', password='')
    except SystemExit as err:
        return err.code
    return 0


if __name__ == '__main__':
    main()
