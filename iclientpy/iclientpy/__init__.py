# 优先从locales模块导入，并执行方法i18n，进行docstrigns的国际化，避免先import的模块的docstrings没有正确国际化
from .locales import *

i18n()

from .jupyter import *
from .viz import *
from ._version import version_info, __version__
from .rest import *
from .portal import *
from .online import *
from ipyleaflet import *


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'iclientpy',
        'require': 'iclientpy/extension'
    }]
