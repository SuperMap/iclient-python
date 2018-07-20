from functools import wraps
import inspect
import typing


def typeassert(func):
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_values = sig.bind(*args, **kwargs)
        func_annotations = inspect.getfullargspec(func).annotations
        for name, value in bound_values.arguments.items():
            if name in func_annotations:
                clz = _get_expect_type(func_annotations[name])
                if value is not None and not isinstance(value, clz):
                    raise TypeError(
                        'Argument {} must be {}'.format(name, func_annotations[name])
                    )
        return func(*args, **kwargs)

    return wrapper


def _get_expect_type(wrapped_type):
    types_matcher = {
        typing.List: list,
        typing.Dict: dict,
        typing.Tuple: tuple,
        typing.Text: str
    }
    for key, value in types_matcher.items():
        if issubclass(wrapped_type, key):
            return value
    else:
        return wrapped_type
