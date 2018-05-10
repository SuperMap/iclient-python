from typing import Callable, Dict, Tuple
from iclientpy.rest.api.servicespage import ServiceMetaInfo
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.servicespage import ServiceComponentType, ServiceInterfaceType


class ServiceUIRegister:
    _registed: Dict[Tuple[str, str], Tuple[str, type]]

    def __init__(self):
        self._registed = {}

    def __call__(self, component_type: ServiceComponentType, interface_type: ServiceInterfaceType, service_api_method: Callable):
        def wrapper(clz: type):
            self._registed[(component_type.value, interface_type.value)] = (service_api_method.__name__, clz)
            return clz
        return wrapper

    def new_service_ui(self, service_meta_info: ServiceMetaInfo, api_factory: APIFactory, default_value = None):
        key = (service_meta_info.componentType, service_meta_info.interfaceType)
        value =  self._registed.get(key, None)
        if value is None:
            return default_value
        service_api_method_name, ui_clz = value
        service_api = getattr(api_factory, service_api_method_name)(service_meta_info.name)
        return ui_clz(service_api)