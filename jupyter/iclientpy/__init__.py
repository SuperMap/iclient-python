from .jupyter import *
from ._version import version_info, __version__
from .rest import *
from ipyleaflet import *


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'iclientpy',
        'require': 'iclientpy/extension'
    }]
