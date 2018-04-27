from typing import Iterable,Dict
from ..rest.api.model import ServiceMetaInfo
from ..rest.api.servicespage import ServiceComponentType


def get_services_by_component_type(services: Iterable[ServiceMetaInfo], *args):
    result = {} #type: Dict[ServiceComponentType, ServiceMetaInfo]
    for com_type in args:
        type_name = com_type.value #type: str
        for service in services:
            if type_name == service.componentType:
                result[com_type] = service
                break
        else:
            result[com_type] = None
    return result