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
                 fixed_queryKWs: dict = {}, splice_url: bool = True, json_deserializer=None, fileKW: str = None, content_type: str = None):
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
        self._uri = uri if uri.startswith('/') or (not splice_url) else ('/' + uri)
        self._entityKW = entityKW
        self._queryKWs = queryKWs
        self._fileKW = fileKW
        self._splice_url = splice_url
        self._fixed_querKWs = fixed_queryKWs
        self._json_deserializer = json_deserializer if json_deserializer is not None else deserializer(
            inspect.getfullargspec(self._original).annotations.get('return', None))
        self._content_type = content_type

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

    def get_splice_url(self) -> bool:
        """
        获取url是否拼接标识

        Returns:
            返回url是否拼接标识
        """
        return self._splice_url

    def get_fixed_queryKWs(self):
        """
        获取固定的查询参数

        Returns:
            返回固定查询参数
        """
        return self._fixed_querKWs

    def get_content_type(self):
        return self._content_type


def rest(method: HttpMethod, uri, entityKW: str = None, queryKWs: List[str] = None, splice_url: bool = True,
         fixed_queryKWs: dict = {}, json_deserializer=None, fileKW: str = None, content_type: str='application/json'):
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
            super().__init__(func, method, uri, entityKW=entityKW, queryKWs=queryKWs, fixed_queryKWs=fixed_queryKWs,
                             splice_url=splice_url, json_deserializer=json_deserializer, fileKW=fileKW, content_type = content_type);

    return RESTWrapper

from functools import partial


head = partial(rest, HttpMethod.HEAD)

post = partial(rest, HttpMethod.POST)

get = partial(rest, HttpMethod.GET)

put = partial(rest, HttpMethod.PUT)

delete = partial(rest, HttpMethod.DELETE)
