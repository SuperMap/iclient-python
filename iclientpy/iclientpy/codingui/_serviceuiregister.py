from typing import Callable, Dict, Tuple
from iclientpy.rest.api.servicespage import ServiceMetaInfo
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.servicespage import ServiceComponentType, ServiceInterfaceType
from iclientpy.rest.api.model import ServiceType


_service_types_to_registed_key = {
    ServiceType.RESTMAP:(ServiceComponentType.map.value, ServiceInterfaceType.rest.value),
    ServiceType.RESTDATA:(ServiceComponentType.data.value, ServiceInterfaceType.rest.value)
}


class ServiceUIRegister:
    _registed: Dict[Tuple[str, str], Tuple[str, type]]

    def __init__(self):
        self._registed = {}

    def __call__(self, component_type: ServiceComponentType, interface_type: ServiceInterfaceType, service_api_method: Callable):
        def wrapper(clz: type):
            self._registed[(component_type.value, interface_type.value)] = (service_api_method.__name__, clz)
            return clz
        return wrapper

    def _new_service_ui(self, key: Tuple[str, str], service_name:str, api_factory: APIFactory, default_value = None):
        value =  self._registed.get(key, None)
        if value is None:
            return default_value
        service_api_method_name, ui_clz = value
        service_api = getattr(api_factory, service_api_method_name)(service_name)
        return ui_clz(service_api)

    def new_service_ui_from_meta_info(self, service_meta_info: ServiceMetaInfo, api_factory: APIFactory, default_value = None):
        return self._new_service_ui((service_meta_info.componentType, service_meta_info.interfaceType), service_meta_info.name, api_factory, default_value)

    def new_service_ui_from_service_type(self, service_type: ServiceType, service_name:str, api_factory: APIFactory, default_value = None):
        key = _service_types_to_registed_key[service_type]
        return self._new_service_ui(key, service_name, api_factory, default_value)