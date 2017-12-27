import json
from enum import Enum
primitive_types = (int, str, bool, float)


def is_primitive(o) -> bool:
    return type(o) in primitive_types


def to_dict(obj):
    clz = type(obj)
    annos = clz.__dict__['__annotations__']# type:dict
    result = vars(obj).copy() # type:dict
    for key in annos.keys():
        value = result.get(key, None)
        # TODO enum
        if value is not None:
            if isinstance(value, Enum):
                result[key] = value.name
            else:
                if not is_primitive(value):
                    result[key] = to_dict(value)
    return result


def to_json_str(obj):
    return json.dumps(to_dict(obj))


def from_dict(jsonobj: dict, clz:type):
    annos = clz.__dict__['__annotations__']  # type:dict
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
                    setattr(result, key, from_dict(value, valuetype))
    return result


def from_json_str(jsonstr: str, clz: type):
    jsonobj = json.loads(jsonstr)
    return from_dict(jsonobj, clz)