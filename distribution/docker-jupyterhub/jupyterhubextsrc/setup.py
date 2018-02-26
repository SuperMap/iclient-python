from __future__ import print_function
import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, 'js')
is_repo = os.path.exists(os.path.join(here, '.git'))

from distutils import log

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'iclientpy ext jupyterhub'

version_ns = {}
with open(os.path.join(here, 'iclientpyjupyterhubext', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    'name': 'iclientpy.jupyterhub.ext',
    'version': version_ns['__version__'],
    'description': 'iclientpy for jupyterhub',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'install_requires': [
        'pamela>=0.3.0',
        'python_dateutil>=2.6.1',
        'tornado>=4.5.3',
        'jupyterhub>=0.8.1'
    ],
    'packages': find_packages(exclude=("*.test", "*.test.*", "test.*", "test")),
    'zip_safe': False,
    'author': 'supermap',
    'author_email': 'guyongquan@supermap.com',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.6',
    ],
}

setup(**setup_args)
