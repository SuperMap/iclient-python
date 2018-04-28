from .jupyter import *
from .viz import *
from ._version import version_info, __version__
from .rest import *
from .portal import *
from ipyleaflet import *


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'iclientpy',
        'require': 'iclientpy/extension'
    }]
