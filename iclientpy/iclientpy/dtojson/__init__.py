import json
import typing
from enum import Enum
import importlib

__all__ = [
    'to_json_str', 'deserializer', 'ByFieldValueParserSwitcher', 'parser', 'AbstractTypeParserSwitcher', 'register'
]
primitive_types = (int, str, bool, float)

type_parser_map = {}


def register(clz: type, parser_clz, force: bool = False):
    if clz in type_parser_map and (not force):
        raise Exception('已经存在')
    else:
        type_parser_map[clz] = parser_clz


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
        tmp_dict = obj  # type:dict
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
        else:
            if key in result:
                del result[key]
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


def import_root_module_to_local(kls, local_dict = None):
    if local_dict is None:
        local_dict = {}
    generic_start = kls.find('[')
    generic_end = kls.rfind(']')
    kls_no_generic = kls
    if generic_start != -1 and generic_end != -1 and generic_end > generic_start:
        import_root_module_to_local(kls[generic_start + 1: generic_end], local_dict)
        kls_no_generic = kls[generic_start]
    last_dot = kls_no_generic.rfind('.')
    if last_dot == -1:
        return local_dict
    pkg_name_end = last_dot if generic_start == -1 else min(last_dot, generic_start)
    pkg_name = kls[:pkg_name_end] #type:str
    parts = pkg_name.split('.')
    cur_module_name = parts[0]
    cur_module = importlib.import_module(parts[0])
    local_dict[parts[0]] = cur_module
    for name in parts[1:]:
        cur_module_name = cur_module_name + '.' + name
        imported = importlib.import_module(cur_module_name)
        setattr(cur_module, name, imported)
        cur_module = imported
    return local_dict


def get_class(kls):
    try:
        if kls.find('[') == -1:
            last_dot = kls.rfind('.')
            if last_dot == -1:
                return eval(kls, globals())
            pkg_name = kls[:last_dot]
            return getattr(importlib.import_module(pkg_name), kls[last_dot + 1:])
        local_dict = import_root_module_to_local(kls)
        return eval(kls, globals(), local_dict)
    except Exception as err:
        raise Exception('get class ' + kls + ' exception')


def _get_all_annotations(clz: type) -> dict:
    result = {}
    annos = clz.__dict__.get('__annotations__', None)  # type:dict
    if annos is not None:
        result.update(annos)
    for base_clz in clz.__bases__:
        result.update(_get_all_annotations(base_clz))
    return result


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
    _element_parser: typing.Callable

    def __init__(self, element_parser):
        self._element_parser = element_parser

    def __call__(self, json_array, *args):
        if json_array is None:
            return None
        result = []
        for e in json_array:
            result.append(self._element_parser(e))
        return result


def parser(clz: type, field_parser: typing.Dict[typing.Tuple[type, str], typing.Callable] = {},
           type_parser: typing.Dict[type, typing.Callable] = {}):
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
        if start == -1 and end == -1:
            elementclz = get_class(clzname)
        elif start != -1 and end != -1 and end > start:
            elementclz = get_class(clzname[start + 1: end])
        else:
            raise Exception('unknown ' + clz.__name__)
        return ListParser(parser(elementclz, field_parser, type_parser))
    annos = _get_all_annotations(clz)
    deserializers = {}
    for field_name, field_type in annos.items():
        field = (clz, field_name)
        if field in field_parser:
            deserializers[field_name] = field_parser[field]
        elif field_type in type_parser:
            deserializers[field_name] = type_parser[field_type]
        elif field_type in type_parser_map:
            deserializers[field_name] = type_parser_map[field_type]
        else:
            deserializers[field_name] = parser(field_type, field_parser, type_parser)
    return ObjectParser(clz, deserializers)


def _deserialize(parser: typing.Callable, json_str):
    try:
        json_obj = json.loads(json_str)
    except:
        return json_str
    return parser(json_obj)


def _null_function(*args, **kwargs):
    return None


from functools import partial


def deserializer(clz: type, field_parser: typing.Dict[typing.Tuple[type, str], typing.Callable] = {},
                 abstract_type_parser: typing.Dict[typing.Tuple[type, str], typing.Callable] = {}):
    """
    创建指定类型的json字符串反序列化函数。

    Args:
        clz: 需要反序列化的类型
        field_parser: 需要特殊处理的字段的反序列化函数

    Returns:
        反序列化函数，该函数接受一个json字符串为参数，返回指定类型的对象
    """
    if clz is None:
        return _null_function
    return partial(_deserialize, parser(clz, field_parser, abstract_type_parser))


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
        if json_obj is None:
            return None
        parser = self._parsers.get(json_obj.get(self._field_name, None), None)
        return None if parser is None else parser(json_obj, *args)
