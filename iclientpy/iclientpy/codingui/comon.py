from typing import Callable,Dict


class NamedObjects:
    _key_index: Dict[str, int]
    _index_key: Dict[int, str]
    _index: int

    def __init__(self):
        self._key_index = {}
        self._index_key = {}
        self._index = 0

    def __repr__(self):
        array = ['{index}:{key}'.format(index= str(index), key=key) for index, key in self._index_key.items()]
        return '\n'.join(array)

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        if not key in self._key_index:
            self._key_index[key] = self._index
            self._index_key[self._index] = key
            self._index += 1

    def __getitem__(self, key):
        return self.__dict__[self._index_key[key]] if isinstance(key, int) else self.__dict__[key]


class Option:
    _select_callback: Callable

    def __init__(self, select_callback: Callable, confirm_method_name: str = None):
        self._select_callback = select_callback
        if confirm_method_name is not None:
            setattr(self, confirm_method_name, lambda :self())

    def __call__(self, *args, **kwargs):
        return self._select_callback()