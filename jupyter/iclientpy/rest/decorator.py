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
    def __init__(self, func, method, uri):
        """
        :type func:function
        :type uri:str
        :type method:HttpMethod
        """
        wraps(func)(self)
        self._method = method
        self._uri = uri if uri.startswith('/') else ('/' + uri)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def getMethod(self):
        return self._method

    def getUri(self):
        return self._uri


def rest(method, uri):
    """
    :type uri:str
    :type method:HttpMethod
    """
    class RESTWrapper(REST):
        def __init__(self, func):
            super().__init__(func, method, uri);

    return RESTWrapper