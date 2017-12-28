import json
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
        return  obj.name
    annos = clz.__dict__['__annotations__']# type:dict
    result = vars(obj).copy() # type:dict
    for key in annos.keys():
        value = result.get(key, None)
        # TODO enum
        if value is not None:
            result[key] = to_dict_or_list(value)
    return result


def to_json_str(obj):
    return json.dumps(to_dict_or_list(obj))


def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def parse_jsonobj(jsonobj, clz:type):
    if isinstance(jsonobj, list):
        return from_list(jsonobj, clz)
    if clz in primitive_types:
        return jsonobj
    if Enum in clz.__bases__:
        return clz[jsonobj]
    return from_dict(jsonobj, clz)

def from_list(jsonobjarray, clz:type):
    result = []
    clzname = clz.__str__(clz) # type:str
    start = clzname.find('[')
    end = clzname.find(']')
    elementclz = get_class(clzname[start + 1: end])
    for e in jsonobjarray:
        result.append(parse_jsonobj(e, elementclz))
    return result

def from_dict(jsonobj: dict, clz:type):
    annos = clz.__dict__.get('__annotations__', None)  # type:dict
    assert annos is not None
    result = clz()
    for (key, valuetype) in annos.items():
        value = jsonobj.get(key, None)
        if value is not None:
            if Enum in valuetype.__bases__:
                setattr(result, key, valuetype[value])
            else:
                if valuetype in primitive_types:
                    setattr(result, key, value)
                else:
                    setattr(result, key, parse_jsonobj(value, valuetype))
    return result


def from_json_str(jsonstr: str, clz: type):
    jsonobj = json.loads(jsonstr)
    return parse_jsonobj(jsonobj, clz)