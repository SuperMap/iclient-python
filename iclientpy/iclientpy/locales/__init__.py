from .conf import *

import inspect

__all__ = ['i18n']


class _Translater:
    def __init__(self):
        import importlib
        l_module = importlib.import_module(language_module)
        self._translate = getattr(l_module, locale_member_name)

    def translate(self, key: str, default_value):
        return self._translate.get(key, default_value)


class _TranslateKeyBuilder:
    def module_name(self, module_name: str):
        self._module_name = module_name
        self._clz_name = None
        self._method_name = None

    def clz_name(self, clz_name: str):
        self._clz_name = clz_name
        self._method_name = None

    def method_name(self, method_name: str):
        self._method_name = method_name

    def get_key(self):
        key = self._module_name
        if hasattr(self, '_clz_name') and self._clz_name != None:
            key = key + '.' + self._clz_name
        if hasattr(self, '_method_name') and self._method_name != None:
            key = key + '.' + self._method_name
        return key


_t_builder = _TranslateKeyBuilder()
_t = _Translater()


def _translate(default_value):
    return _t.translate(_t_builder.get_key(), default_value)


def _is_current_module_member(current_module, member):
    member_module = inspect.getmodule(member)
    return hasattr(member_module, '__name__') and inspect.getmodule(current_module).__name__ == member_module.__name__


def _is_iclientpy_module(mo):
    mo_module = inspect.getmodule(mo)
    return hasattr(mo_module, '__name__') and 'iclientpy' in mo_module.__name__


def _is_private(obj):
    return obj.__name__.startswith("_") if hasattr(obj, '__name__') else obj.startswith("_")


def _translate_method_docstrings(method):
    _t_builder.method_name(method.__name__)
    if not _is_private(method):
        method.__doc__ = _translate(method.__doc__)


def _filter_translate_member(parent):
    def verify(item):
        name, member = item
        return not _is_private(name) and _is_iclientpy_module(member) and _is_current_module_member(parent, member)

    return verify


def _translate_class_docstrings(clz):
    _t_builder.clz_name(clz.__name__)
    clz.__doc__ = _translate(clz.__doc__)
    for name, member in list(filter(_filter_translate_member(clz), inspect.getmembers(clz))):
        if inspect.isfunction(member) or inspect.ismethod(member):
            _translate_method_docstrings(member)


def _translate_module_docstrings(mo):
    _t_builder.module_name(mo.__name__)
    mo.__doc__ = _translate(mo.__doc__)
    for name, member in list(filter(_filter_translate_member(mo), inspect.getmembers(mo))):
        if inspect.isclass(member):
            _translate_class_docstrings(member)
        elif inspect.ismethod(member) or inspect.isfunction(member):
            _t_builder.clz_name(None)
            _translate_method_docstrings(member)


def i18n():
    if hook:
        import builtins

        old_import = builtins.__import__

        def _new_import(*args, **kwargs):
            result = old_import(*args, **kwargs)
            if _is_iclientpy_module(result):
                if inspect.ismodule(result):
                    _translate_module_docstrings(result)
                elif inspect.isclass(result):
                    _translate_class_docstrings(result)
                elif inspect.ismethod(result):
                    _translate_method_docstrings(result)
            return result

        builtins.__import__ = _new_import
