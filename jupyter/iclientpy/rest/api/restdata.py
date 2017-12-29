from typing import List
from enum import  Enum
from ..decorator import post
from .model import Feature,MethodResult

class DataService:

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/features', 'entity')
    def postFeatures(self, datasourceName: str, datasetName: str, entity: List[Feature]) -> MethodResult:
        pass
