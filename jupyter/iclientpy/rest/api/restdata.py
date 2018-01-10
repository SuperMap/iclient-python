from typing import List
from ..decorator import post, get
from .model import Feature, MethodResult, GeometryType


class Features:
    startIndex: int
    childUriList: List[str]
    geometryType: GeometryType
    featureCount: int


class DataService:
    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/features', entityKW='entity',
          queryKWs=['isUseBatch', 'returnContent', '_method'])
    def post_features(self, datasourceName: str, datasetName: str, entity: List[Feature], isUseBatch: bool = None,
                      returnContent: bool = None, _method: str = None) -> MethodResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/features', queryKWs=['fromIndex', 'toIndex'])
    def get_features(self, datasourceName: str, datasetName: str, fromIndex: int = None,
                     toIndex: int = None) -> Features:
        pass
