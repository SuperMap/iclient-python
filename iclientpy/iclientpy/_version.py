import os

version_info = (9, 0, 0)

_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': ''}

__version__ = '%s.%s.%s%s' % (version_info[0], version_info[1], version_info[2],
                              '.' + os.environ.get('BUILD_NUMBER') if os.environ.get('BUILD_NUMBER') else '')

EXTENSION_VERSION = '^9.0.0'
