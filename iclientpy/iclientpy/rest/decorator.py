import types
from typing import List, Dict, Callable, Tuple
from enum import Enum
from functools import wraps
from ..dtojson import deserializer
import inspect


class HttpMethod(Enum):
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE',
    HEAD = 'HEAD'


class REST:
    """
    REST请求的封装，用于封装Python API参数与rest请求之间的对应关系，比如：查询字符串，请求体之类
    """

    def __init__(self, func, method, uri: str, entityKW: str = None, queryKWs: List[str] = None,
                 json_deserializer = None, fileKW: str = None):
        """
        初始化REST类，存放实际调用的rest请求的相关信息

        Args:
            func: 调用请求的实际方法
            method: http请求的方法
            uri: 请求地址
            entityKW: 请求体的key
            queryKWs: 查询字符串的key
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
        self._fileKW = fileKW
        self._json_deserializer = json_deserializer if json_deserializer is not None else deserializer(inspect.getfullargspec(self._original).annotations.get('return', None))

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def get_json_deserializer(self):
        return self._json_deserializer

    def get_original_func(self):
        """
        获取原始的请求发起方法，可用于获取请求的参数以及返回类型

        Returns:
            返回请求的发起方法
        """
        return self._original

    def get_method(self) -> HttpMethod:
        """
        获取http方法

        Returns:
            返回http方法
        """
        return self._method

    def get_uri(self) -> str:
        """
        获取请求的uri

        Returns:
            返回请求的uri
        """
        return self._uri

    def get_entityKW(self) -> str:
        """
        获取请求的请求体的key，用于从原始方法参数中找到请求体的Python对象

        Returns:
            返回请求体的key
        """
        return self._entityKW

    def get_queryKWs(self) -> str:
        """
        获取请求的查询字符串的key，用于从原始方法参数中找到请求的查询参数

        Returns:
            返回查询字符串的key
        """
        return self._queryKWs

    def get_fileKW(self) -> str:
        """
        获取请求的文件的key，用于post请求发送文件
        Returns:
            返回文件的key
        """
        return self._fileKW


def rest(method: HttpMethod, uri, entityKW: str = None, queryKWs: List[str] = None, json_deserializer = None, fileKW: str = None):
    """
    rest请求的封装方法

    Args:
        method: http方法
        uri: 请求uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询参数的key

    Returns:
        请求的封装类
    """

    class RESTWrapper(REST):
        def __init__(self, func):
            super().__init__(func, method, uri, entityKW, queryKWs, json_deserializer, fileKW);

    return RESTWrapper


def head(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    """
    head请求的装饰器，可以在方法上直接通过@head方式使用

    Args:
        uri: 请求的uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询字符串的key

    Returns:
        封装了请求的REST类
    """
    return rest(HttpMethod.HEAD, uri, entityKW, queryKWs)


def post(uri: str, entityKW: str = None, queryKWs: List[str] = None, fileKW: str = None):
    """
    post请求的装饰器，可以在方法上直接通过@post方式使用

    Args:
        uri: 请求的uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询字符串的key
        fileKW: 请求的文件的key

    Returns:
        封装了请求的REST类
    """
    return rest(HttpMethod.POST, uri, entityKW, queryKWs, fileKW=fileKW)


def get(uri: str, entityKW: str = None, queryKWs: List[str] = None, *args, **kwargs):
    """
    get请求的装饰器，可以在方法上直接通过@get方式使用

    Args:
        uri: 请求的uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询字符串的key

    Returns:
        封装了请求的REST类
    """
    return rest(HttpMethod.GET, uri, entityKW, queryKWs, *args, **kwargs)


def put(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    """
    put请求的装饰器，可以在方法上直接通过@put方式使用

    Args:
        uri: 请求的uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询字符串的key

    Returns:
        封装了请求的REST类
    """
    return rest(HttpMethod.PUT, uri, entityKW, queryKWs)


def delete(uri: str, entityKW: str = None, queryKWs: List[str] = None):
    """
    delete请求的装饰器，可以在方法上直接通过@delete方式使用

    Args:
        uri: 请求的uri
        entityKW: 请求的请求体的key
        queryKWs: 请求的查询字符串的key

    Returns:
        封装了请求的REST类
    """
    return rest(HttpMethod.DELETE, uri, entityKW, queryKWs)
