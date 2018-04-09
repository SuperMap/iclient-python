import abc
from .decorator import *


class RestInvocationHandler:
    def __call__(self, rest: REST, args, kwargs):
        """
        :type rest: REST
        :return:
        """
        return self.handle_rest_invocation(rest, args, kwargs)

    @abc.abstractmethod
    def handle_rest_invocation(self, rest, args, kwargs):
        """
        :type rest: REST
        :return:
        """
        pass


def init(self, resthandler):
    self._resthandler = resthandler
    self._handlers = {}


def getattribute(self, name):
    """
    :type name:str
    :return:
    """
    value = object.__getattribute__(self, name)
    rest = value  # type: REST
    while rest is not None:
        if (hasattr(rest, '__func__') and isinstance(rest.__func__, REST)) or isinstance(rest, REST):
            break
        if hasattr(rest, '__wrapped__'):
            rest = rest.__wrapped__
        else:
            rest = None
    if rest is None:
        return value
    handlers = self._handlers  # type:dict
    existshandler = handlers.get(name, None)
    if existshandler is not None:
        return existshandler

    @wraps(value)
    def sendrest(*args, **kwargs):
        return self._resthandler(rest, args, kwargs)

    handlers[name] = sendrest
    return sendrest


cls_dict = {
    '__init__': init,
    '__getattribute__': getattribute
}

_proxyclasses = {}  # type: dict[str, type]


def _create_proxy_class(clz):
    return types.new_class("Proxy" + clz.__name__, (clz,), {}, lambda ns: ns.update(cls_dict))


def create(clz, handler: RestInvocationHandler):
    """
    type clz:type
    type handler:RestInvocationHandler
    """
    name = clz.__name__
    proxy_clz = _proxyclasses.get(name, None)
    if proxy_clz is None:
        proxy_clz = _create_proxy_class(clz)
        _proxyclasses[name] = proxy_clz
    return proxy_clz(handler)
