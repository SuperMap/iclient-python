import types
from typing import List
from enum import Enum
from functools import wraps


class HttpMethod(Enum):
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE',
    HEAD = 'HEAD'


class REST:
    def __init__(self, func, method, uri: str, entityKW: str = None, queryKWs: List[str] = None):
        """
        :type func:function
        :type uri:str
        :type method:HttpMethod
        """
        wraps(func)(self)
        self._original = func
        while hasattr(self._original, '__wrapped__'):
            # TODO 处理多个装饰器并且装饰器中有类实例装饰器的情况
            self._original = self._original.__wrapped__
        self._method = method
        self._uri = uri if uri.startswith('/') else ('/' + uri)
        self._entityKW = entityKW
        self._queryKWs = queryKWs

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def get_original_func(self):
        return self._original

    def get_method(self) -> HttpMethod:
        return self._method

    def get_uri(self) -> str:
        return self._uri

    def get_entityKW(self) -> str:
        return self._entityKW

    def get_queryKWs(self) -> str:
        return self._queryKWs


def rest(method: HttpMethod, uri, entityKW: str = None, queryKWs: List[str] = None):
    """
    :type uri:str
    :type method:HttpMethod
    """

    class RESTWrapper(REST):
        def __init__(self, func):
            super().__init__(func, method, uri, entityKW, queryKWs);

    return RESTWrapper


def head(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    return rest(HttpMethod.HEAD, uri, entityKW, queryKWs)


def post(uri: str, entityKW: str, queryKWs: List[str] = None):
    return rest(HttpMethod.POST, uri, entityKW, queryKWs)


def get(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    return rest(HttpMethod.GET, uri, entityKW, queryKWs)


def put(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    return rest(HttpMethod.PUT, uri, entityKW, queryKWs)


def delete(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    return rest(HttpMethod.DELETE, uri, entityKW, queryKWs)
