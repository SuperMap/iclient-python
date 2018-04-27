from typing import List
from enum import Enum
from .model import ServiceMetaInfo
from ..decorator import get


class ServiceComponentType(Enum):
    map = 'com.supermap.services.components.impl.MapImpl'
    data='com.supermap.services.components.impl.DataImpl'
    datacatalog='com.supermap.services.components.impl.DataCatalogImpl'
    distributedanalysis='com.supermap.processing.jobserver.ProcessingServer'


class ServicesPage:

    @get('/services')
    def list_services(self) -> List[ServiceMetaInfo]:
        pass