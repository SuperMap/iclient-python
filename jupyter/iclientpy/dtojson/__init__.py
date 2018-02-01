import json
import typing
from enum import Enum

__all__ = [
    'from_json_str', 'to_json_str'
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
        obj: python对象，用于转为json字符串

    Returns:
        字符串，python对象转成的json字符串
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


def parse_jsonobj(jsonobj, clz: type, abstract_type_fields: typing.Dict[typing.Tuple[type, str], typing.Callable[[dict], type]] = {}):
    if isinstance(jsonobj, list):
        return from_list(jsonobj, clz, abstract_type_fields)
    if clz in primitive_types:
        return jsonobj
    if Enum in clz.__bases__:
        return clz[jsonobj]
    if clz is dict:
        return jsonobj
    return from_dict(jsonobj, clz, abstract_type_fields)


def from_list(jsonobjarray, clz: type, abstract_type_fields: typing.Dict[typing.Tuple[type, str], typing.Callable[[dict], type]]):
    result = []
    clzname = clz.__str__(clz)  # type:str
    start = clzname.find('[')
    end = clzname.find(']')
    elementclz = get_class(clzname[start + 1: end])
    for e in jsonobjarray:
        result.append(parse_jsonobj(e, elementclz, abstract_type_fields))
    return result

def _get_all_annotations(clz:type):
    annos = clz.__dict__.get('__annotations__', None)  # type:dict
    assert annos is not None
    annos = annos.copy()
    for base_clz in clz.__bases__:
        if hasattr(base_clz, '__annotations__'):
            annos.update(base_clz.__annotations__)
    return annos


def from_dict(jsonobj: dict, clz: type, abstract_type_fields: typing.Dict[typing.Tuple[type, str], typing.Callable[[dict], type]] = {}):
    test = clz.__dict__
    annos = _get_all_annotations(clz)  # type:dict
    result = clz()
    for (key, valuetype) in annos.items():
        field = (clz, key)
        value = jsonobj.get(key, None)
        if value is not None:
            if field in abstract_type_fields:
                field_type = abstract_type_fields[field](jsonobj)
                setattr(result, key, parse_jsonobj(value, field_type, abstract_type_fields))
            else:
                if Enum in valuetype.__bases__:
                    setattr(result, key, valuetype[value])
                else:
                    if valuetype in primitive_types:
                        setattr(result, key, value)
                    else:
                        setattr(result, key, parse_jsonobj(value, valuetype, abstract_type_fields))
    return result


def from_json_str(jsonstr: str, clz: type, abstract_type_fields: typing.Dict[typing.Tuple[type, str], typing.Callable[[dict], type]] = {}):
    """
    从json字符串转向对应的python对象

    Args:
        jsonstr: json字符串
        clz: python对象类型
        abstract_type_fields: 类型为抽象类型的字段具体类型判断函数

    Returns:
        返回对象的python对象实例
    """
    jsonobj = json.loads(jsonstr)
    return parse_jsonobj(jsonobj, clz, abstract_type_fields)
