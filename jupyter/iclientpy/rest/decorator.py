import types
from enum import Enum
from functools import wraps


class HttpMethod(Enum):
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE',
    HEAD = 'HEAD'


class REST:
    def __init__(self, func, method, uri: str, entityKW: str = None):
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

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def get_original_func(self):
        return self._original

    def getMethod(self) -> HttpMethod:
        return self._method

    def getUri(self) -> str:
        return self._uri

    def getEntityKW(self) -> str:
        return self._entityKW


def rest(method: HttpMethod, uri, entityKW: str = None):
    """
    :type uri:str
    :type method:HttpMethod
    """
    class RESTWrapper(REST):
        def __init__(self, func):
            super().__init__(func, method, uri, entityKW);

    return RESTWrapper

def post(uri: str, entityKW: str):
    return rest(HttpMethod.POST, uri, entityKW)