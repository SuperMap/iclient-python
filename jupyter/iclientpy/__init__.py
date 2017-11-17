from ._version import version_info, __version__

from .iclient import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'iclientpy',
        'require': 'iclientpy/extension'
    }]
