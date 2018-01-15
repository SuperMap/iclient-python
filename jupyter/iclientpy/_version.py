import os

version_info = (9, 0, 0)

_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': ''}

__version__ = '%s.%s.%s%s' % (version_info[0], version_info[1], version_info[2],
                              '.' + os.environ.get('build.number') if os.environ.get('build.number') else '')

EXTENSION_VERSION = '^9.0.0'
