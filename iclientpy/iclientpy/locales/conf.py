# 语言默认模块
default_language_module = 'iclientpy.locales.iclientpy'

# 尝试匹配语言对应模块，比如zh_CN 匹配顺序一次为 '_zh_CN' -> '_zh' -> '' 为后缀的模块
import importlib
import locale

language_all = locale.getdefaultlocale()[0]
language_short = language_all.split('_')[0]
try:
    importlib.import_module(default_language_module + '_' + language_all)
    language_module = default_language_module + '_' + language_all
except Exception:
    try:
        importlib.import_module(default_language_module + '_' + language_short)
        language_module = default_language_module + '_' + language_short
    except Exception:
        language_module = default_language_module

# 判断环境变量DISABLEICLIENTPYI18N是否存在，存在则不启用国际化翻译的docstrings，不存在则使用国际化翻译的dostrings
import os

hook = os.environ.get('DISABLEICLIENTPYI18N') is None

# 在语言模块内字典名称
locale_member_name = 'iclientpy_locale'
