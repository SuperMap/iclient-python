import os
import sys
import subprocess
from notebook.nbextensions import install_nbextension_python, uninstall_nbextension_python, enable_nbextension_python, \
    disable_nbextension_python
from notebook.notebookapp import main as nbmain
from os.path import dirname, abspath, join as pjoin


def uninstall_develop():
    rootdir = pjoin(dirname(abspath(__file__)), '..', '..')
    develop_cmd = [
        sys.executable,
        'setup.py',
        'develop',
        '-u'
    ]
    subprocess.check_call(develop_cmd, cwd=rootdir)


def uninstall_nbextension():
    disable_nbextension_python('iclientpy', sys_prefix=True)
    uninstall_nbextension_python('iclientpy', sys_prefix=True)


def clear_dir():
    static_dir = pjoin(dirname(abspath(__file__)), '..', '..', 'iclientpy', 'static')
    build_dir = pjoin(dirname(abspath(__file__)), '..', '..', 'build')
    os.removedirs(static_dir)
    os.removedirs(build_dir)


def install_develop():
    rootdir = pjoin(dirname(abspath(__file__)), '..', '..')
    develop_cmd = [
        sys.executable,
        'setup.py',
        'develop'
    ]
    subprocess.check_call(develop_cmd, cwd=rootdir)


def install_nbextension():
    install_nbextension_python('iclientpy', overwrite=True, symlink=True, sys_prefix=True)
    enable_nbextension_python('iclientpy', sys_prefix=True)


def run():
    rootdir = pjoin(dirname(abspath(__file__)), '..', '..')
    uninstall_nbextension()
    uninstall_develop()
    install_develop()
    install_nbextension()
    nbmain(notebook_dir=rootdir)


if __name__ == '__main__':
    run()
