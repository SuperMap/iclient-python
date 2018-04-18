from typing import Callable
class NamedObjects:

    def __repr__(self):
        return list(self.__dict__.keys()).__repr__()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]


class Option:
    _select_callback: Callable
    def __init__(self, select_callback: Callable):
        self._select_callback = select_callback

    def __call__(self, *args, **kwargs):
        return self.selected()

    def selected(self):
        return self._select_callback()