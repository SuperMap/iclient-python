# 尝试匹配语言对应模块，比如zh_CN 匹配顺序一次为 '_zh_CN' -> '_zh' -> '' 为后缀的模块
import os
from os.path import dirname, abspath, join as pjoin, exists
import locale

default_translate_filename = 'iclientpy'
translate_file_suffix = '.json'

language_all = locale.getdefaultlocale()[0]
language_short = language_all.split('_')[0]
for l_path in [language_all, language_short, '']:
    if exists(pjoin(dirname(abspath(__file__)), default_translate_filename + '_' + l_path + translate_file_suffix)):
        translate_file_path = pjoin(dirname(abspath(__file__)),
                                    default_translate_filename + '_' + l_path + translate_file_suffix)
        break

# 判断环境变量DISABLEICLIENTPYI18N是否存在，存在则不启用国际化翻译的docstrings，不存在则使用国际化翻译的dostrings


hook = os.environ.get('DISABLEICLIENTPYI18N') is None

# 在语言模块内字典名称
locale_member_name = 'iclientpy_locale'
