import json
import typing
from enum import Enum

__all__ = [
    'from_json_str', 'to_json_str', 'deserializer', 'ByFieldValueParserSwitcher', 'parser', 'AbstractTypeParserSwitcher'
]
primitive_types = (int, str, bool, float)


def is_primitive(o) -> bool:
    return type(o) in primitive_types


def to_dict_or_list(obj):
    clz = type(obj)
    if clz is list:
        result = []
        for e in obj:
            result.append(to_dict_or_list(e))
        return result
    if is_primitive(obj):
        return obj
    if isinstance(obj, Enum):
        return obj.name
    if isinstance(obj, dict):
        tmp_dict = obj # type:dict
        result = {}
        for key, value in tmp_dict.items():
            result[key] = None if value is None else to_dict_or_list(value)
        return result
    annos = _get_all_annotations(clz)  # type:dict
    result = vars(obj).copy()  # type:dict
    for key in annos.keys():
        value = result.get(key, None)
        # TODO enum
        if value is not None:
            result[key] = to_dict_or_list(value)
    return result


def to_json_str(obj):

    """
    将json对象转为json字符串

    Args:
        obj: Python对象，用于转为json字符串

    Returns:
        字符串，Python对象转成的json字符串
    """
    return obj.name if isinstance(obj, Enum) else json.dumps(to_dict_or_list(obj))


def get_class(kls):
    try:
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
    except Exception:
        return eval(kls)


def _get_all_annotations(clz:type) -> dict:
    result = {}
    annos = clz.__dict__.get('__annotations__', None)  # type:dict
    if annos is not None:
        result.update(annos)
    for base_clz in clz.__bases__:
        result.update(_get_all_annotations(base_clz))
    return result


def from_json_str(jsonstr: str, clz: type):
    """
    从json字符串转向对应的Python对象

    Args:
        jsonstr: json字符串
        clz: Python对象类型
        abstract_type_fields: 类型为抽象类型的字段具体类型判断函数

    Returns:
        返回对象的Python对象实例
    """
    return deserializer(clz)(jsonstr)


class ObjectParser:
    _clz: type
    _parsers: typing.Dict[str, typing.Callable]

    def __init__(self, clz, deserializers):
        self._clz = clz
        self._parsers = deserializers

    def __call__(self, json_obj: dict, *args):
        if json_obj is None:
            return None
        result = self._clz()
        for field_name, deserializer in self._parsers.items():
            setattr(result, field_name, deserializer(json_obj.get(field_name, None), json_obj))
        return result


class EnumParser:
    _clz: type

    def __init__(self, clz):
        self._clz = clz

    def __call__(self, value, *args):
        return self._clz[value] if value is not None else None


class ReturnOriginalParser:
    def __call__(self, value, *args):
        return value


_return_original_parser = ReturnOriginalParser()

_primitive_parser = _return_original_parser

_dict_parser = _return_original_parser

class ListParser:
    _element_parser:typing.Callable

    def __init__(self, element_parser):
        self._element_parser = element_parser

    def __call__(self, json_array, *args):
        if json_array is None:
            return None
        result = []
        for e in json_array:
            result.append(self._element_parser(e))
        return result


def parser(clz:type, field_parser: typing.Dict[typing.Tuple[type, str], typing.Callable] = {}):
    if clz in primitive_types:
        return _primitive_parser
    if issubclass(clz, Enum):
        return EnumParser(clz)
    if clz == dict:
        return _dict_parser
    if issubclass(clz, list):
        if not isinstance(clz, typing.GenericMeta):
            raise NotImplemented()
        clzname = clz.__str__(clz)  # type:str
        start = clzname.find('[')
        end = clzname.rfind(']')
        elementclz = get_class(clzname[start + 1: end])
        return ListParser(parser(elementclz, field_parser))
    annos = _get_all_annotations(clz)
    deserializers = {}
    for field_name, field_type in annos.items():
        field = (clz, field_name)
        if field in field_parser:
            deserializers[field_name] = field_parser[field]
        else:
            deserializers[field_name] = parser(field_type, field_parser)
    return ObjectParser(clz, deserializers)


def _deserialize(parser:typing.Callable, json_str):
    try:
        json_obj = json.loads(json_str)
    except:
        return json_str
    return parser(json_obj)

def _null_function(*args, **kwargs):
    return None
from functools import partial


def deserializer(root_clz:type, field_parser: typing.Dict[typing.Tuple[type, str], typing.Callable] = {}):
    if root_clz is None:
        return _null_function
    return partial(_deserialize, parser(root_clz, field_parser))

class ByFieldValueParserSwitcher:
    _field_name: str
    _parsers: {}

    def __init__(self, field_name: str, parsers: dict):
        self._field_name = field_name
        self._parsers = parsers

    def __call__(self, json_obj: dict, parent_json_obj: dict):
        parser = self._parsers.get(parent_json_obj.get(self._field_name, None), None)
        return None if parser is None else parser(json_obj, parent_json_obj)


class AbstractTypeParserSwitcher:
    _field_name: str
    _parsers: {}

    def __init__(self, field_name: str, parsers: dict):
        self._field_name = field_name
        self._parsers = parsers

    def __call__(self, json_obj: dict, *args):
        parser = self._parsers.get(json_obj.get(self._field_name, None), None)
        return None if parser is None else parser(json_obj, *args)
