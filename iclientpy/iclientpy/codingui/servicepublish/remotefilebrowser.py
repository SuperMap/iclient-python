from functools import partial
from typing import List
from iclientpy.rest.api.management import Management
from IPython.core.display import display


class _RemoteItem:
    _path: str
    _name: str

    def __init__(self, path: str, name: str):
        self._path = path
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path


class Directory(_RemoteItem):

    def enter(self):
        pass

    def __repr__(self):
        return 'DIR:' + self.name


class File(_RemoteItem):
    pass

    def __repr__(self):
        return 'FILE:' + self.name


class RemoteItemCollection:
    _list: List[_RemoteItem]

    def __init__(self):
        self._list = []

    def _add(self, e: _RemoteItem):
        self._list.append(e)

    def __repr__(self):
        array = ['{index}:{name}'.format(index=str(index), name=item.__repr__()) for index, item in enumerate(self._list)]
        return '\n'.join(array)

    def __getitem__(self, key):
        return self._list[key]


class RemoteFileBrowser:
    _mng: Management
    _collection: RemoteItemCollection
    _default_filters: List[str]
    _dir_clz: type
    _file_clz: type
    _path: str
    _home_path: str

    def __init__(self, mng: Management, default_filters:List[str] = ['*.sxwu', '*.smwu', '*.sxw', '*.smw'], dir_clz: type = Directory, file_clz: type = File):
        self._mng = mng
        self._dir_clz = dir_clz
        self._file_clz = file_clz
        self._default_filters = [] if default_filters is None else list(default_filters)
        self._path = ''
        self._home_path = mng.get_home_path().get('Path')
        self.goto_home()

    def _goto_dir(self, path: str):
        list = self._mng.get_file_list(path, self._default_filters)
        collection = RemoteItemCollection()
        new_dir = self._new_dir
        new_file = self._new_file
        for e in list:
            fun = new_dir if e.isDirectory else new_file
            collection._add(fun(e.filePath, e.fileName))
        self._collection = collection
        self._path = path
        display(self)

    def _new_file(self, path, name):
        return self._file_clz(path= path, name= name)

    def _new_dir(self, path, name):
        result = self._dir_clz(path= path, name= name)
        result.enter = partial(self._goto_dir, path)
        return result

    def goto_home(self):
        return self._goto_dir(self._home_path)

    def goto_parent(self):
        linux_index = self._path.rfind('/')
        windows_index = self._path.rfind('\\')
        path = self._path[0:max(linux_index, windows_index)]
        return self._goto_dir(path)

    @property
    def files(self):
        return self._collection

    def __repr__(self):
        return self._path + '\n' + self._collection.__repr__()

    def __getitem__(self, key):
        return self._collection[key]