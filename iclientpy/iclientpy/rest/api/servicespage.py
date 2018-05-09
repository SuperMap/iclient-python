from typing import List
from enum import Enum
from .model import ServiceMetaInfo
from ..decorator import get


class ServiceComponentType(Enum):
    map = 'com.supermap.services.components.impl.MapImpl'
    data='com.supermap.services.components.impl.DataImpl'
    datacatalog='com.supermap.services.components.impl.DataCatalogImpl'
    distributedanalysis='com.supermap.processing.jobserver.ProcessingServer'


class ServiceInterfaceType(Enum):
    rest = 'com.supermap.services.rest.RestServlet'
    restjsr = 'com.supermap.services.rest.JaxrsServletForJersey'
    handler = 'com.supermap.services.handler.HandlerServlet'
    wcs = 'com.supermap.services.wcs.WCSServlet'


class ServicesPage:

    @get('/services')
    def list_services(self) -> List[ServiceMetaInfo]:
        pass