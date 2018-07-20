from typing import List
from io import FileIO

from .model import Feature, MethodResult, GeometryType, GetDataSourcesResult, GetDataSourceResult, PutDatasourceItem, \
    GetDatasetsResult, CopyDatasetItem, GetDatasetResult, CreateDatasetItem, PutDatasetItem, \
    GetFeatureResult, PutFeatureItem, GetAttachmentsResult, GetMetadataResult, FieldInfo, GetFieldResult, \
    GetStatisticResult, StatisticMode, GetDomainResult, GetGridValuesResult, DefaultValuesItem, GetGridValueResult, \
    GetImageValuesResult, GetImageValueResult, GetFeatureResults, PostFeatureResultsItem, GetFeatureResultResult, \
    PostCoordtransferItem, Geometry, PostFeatureResultsResult, PostGridValuesResult, PostImageValuesResult
from ..decorator import post, get, put, delete


class Features:
    startIndex: int
    childUriList: List[str]
    geometryType: GeometryType
    featureCount: int


class DataService:
    @get('/data/datasources')
    def get_datasources(self) -> GetDataSourcesResult:
        pass

    @get('/data/datasources/{datasource}')
    def get_datasource(self, datasource: str) -> GetDataSourceResult:
        pass

    @put('/data/datasources/{datasource}', entityKW='entity')
    def put_datasource(self, datasource: str, entity: PutDatasourceItem) -> MethodResult:
        pass

    @get('/data/datasources/{datasource}/datasets')
    def get_datasets(self, datasource: str) -> GetDatasetsResult:
        pass

    @post('/data/datasources/{datasource}/datasets', entityKW='entity')
    def copy_dataset(self, datasource: str, entity: CopyDatasetItem) -> MethodResult:
        pass

    @put('/data/datasources/{datasource}/datasets/{dataset}', entityKW='entity')
    def create_dataset(self, datasource: str, dataset: str, entity: CreateDatasetItem) -> MethodResult:
        pass

    @get('/data/datasources/{datasource}/datasets/{dataset}')
    def get_dataset(self, datasource: str, dataset: str) -> GetDatasetResult:
        pass

    @put('/data/datasources/{datasource}/datasets/{dataset}', entityKW='entity')
    def put_dataset(self, datasource: str, dataset: str, entity: PutDatasetItem) -> MethodResult:
        pass

    @delete('/data/datasources/{datasource}/datasets/{dataset}')
    def delete_dataset(self, datasource: str, dataset: str) -> MethodResult:
        pass

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/features', entityKW='entity',
          queryKWs=['isUseBatch', 'returnContent'])
    def post_features(self, datasourceName: str, datasetName: str, entity: List[Feature], isUseBatch: bool = None,
                      returnContent: bool = None) -> MethodResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/features', queryKWs=['fromIndex', 'toIndex'])
    def get_features(self, datasourceName: str, datasetName: str, fromIndex: int = None,
                     toIndex: int = None) -> Features:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}',
         fixed_queryKWs={'hasGeometry': True})
    def get_feature(self, datasourceName: str, datasetName: str, featureId: str) -> GetFeatureResult:
        pass

    @put('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}', entityKW='entity')
    def put_feature(self, datasourceName: str, datasetName: str, featureId: str,
                    entity: PutFeatureItem) -> MethodResult:
        pass

    @delete('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}')
    def delete_feature(self, datasourceName: str, datasetName: str, featureId: str) -> MethodResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}/attachments')
    def get_attachments(self, datasourceName: str, datasetName: str, featureId: str) -> List[GetAttachmentsResult]:
        pass

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}/attachments', fileKW='file')
    def post_attachments(self, datasourceName: str, datasetName: str, featureId: str, file: FileIO) -> str:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/features/{featureId}/metadata')
    def get_metadata(self, datasourceName: str, datasetName: str, featureId: str) -> GetMetadataResult:
        pass

    @get('{feature_url}', splice_url=False, fixed_queryKWs={'hasGeometry': True})
    def get_feature_by_url(self, feature_url: str) -> GetFeatureResult:
        pass

    @put('{feature_url}', entityKW='entity', splice_url=False)
    def put_feature_by_url(self, feature_url: str, entity: PutFeatureItem) -> MethodResult:
        pass

    @delete('{feature_url}', splice_url=False)
    def delete_feature_by_url(self, feature_url: str) -> MethodResult:
        pass

    @get('{feature_url}/attachments', splice_url=False)
    def get_attachments_by_url(self, feature_url: str) -> List[GetAttachmentsResult]:
        pass

    @post('{feature_url}/attachments', fileKW='file', splice_url=False)
    def post_attachments_by_url(self, feature_url: str, file: FileIO) -> str:
        pass

    @get('{feature_url}/metadata', splice_url=False)
    def get_metadata_by_url(self, feature_url: str) -> GetMetadataResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/fields', fixed_queryKWs={'returnAll': True})
    def get_fields(self, datasourceName: str, datasetName: str) -> List[FieldInfo]:
        pass

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/fields', entityKW='entity')
    def post_fields(self, datasourceName: str, datasetName: str, entity: FieldInfo) -> MethodResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/fields/{field}')
    def get_field(self, datasourceName: str, datasetName: str, field: str) -> GetFieldResult:
        pass

    @put('/data/datasources/{datasourceName}/datasets/{datasetName}/fields/{field}', entityKW='entity')
    def put_field(self, datasourceName: str, datasetName: str, field: str, entity: FieldInfo) -> MethodResult:
        pass

    @delete('/data/datasources/{datasourceName}/datasets/{datasetName}/fields/{field}')
    def delete_field(self, datasourceName: str, datasetName: str, field: str) -> MethodResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/fields/{field}/{statisticMode}')
    def get_statistic(self, datasourceName: str, datasetName: str, field: str,
                      statisticMode: str) -> GetStatisticResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/domain')
    def get_domain(self, datasourceName: str, datasetName: str) -> List[GetDomainResult]:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/gridValues', queryKWs=['bounds'])
    def get_gridvalues(self, datasourceName: str, datasetName: str, bounds: DefaultValuesItem) -> GetGridValuesResult:
        pass

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/gridValues', entityKW='entity')
    def post_gridvalues(self, datasourceName: str, datasetName: str,
                        entity: List[DefaultValuesItem]) -> PostGridValuesResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/gridValue', queryKWs=['x', 'y'])
    def get_gridvalue(self, datasourceName: str, datasetName: str, x: float, y: float) -> GetGridValueResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/imageValues', queryKWs=['bounds'])
    def get_imagevalues(self, datasourceName: str, datasetName: str, bounds: DefaultValuesItem) -> GetImageValuesResult:
        pass

    @post('/data/datasources/{datasourceName}/datasets/{datasetName}/imageValues', entityKW='entity')
    def post_imagevalues(self, datasourceName: str, datasetName: str,
                         entity: List[DefaultValuesItem]) -> PostImageValuesResult:
        pass

    @get('/data/datasources/{datasourceName}/datasets/{datasetName}/imageValue', queryKWs=['x', 'y'])
    def get_imagevalue(self, datasourceName: str, datasetName: str, x: float, y: float) -> GetImageValueResult:
        pass

    @get('/data/featureResults')
    def get_featureResults(self) -> List[GetFeatureResults]:
        pass

    @post('/data/featureResults', queryKWs=['returnContent', 'formIndex', 'toIndex'], entityKW='entity',
          fixed_queryKWs={'returnContent': True})
    def post_featureResults(self, entity: PostFeatureResultsItem, formIndex: int,
                            toIndex: int) -> PostFeatureResultsResult:
        pass

    @get('/data/featureResults/{featureResultId}')
    def get_featureResult(self, featureResultId: str) -> GetFeatureResultResult:
        pass

    @post('/data/coordtransfer', entityKW='entity')
    def post_coordtransfer(self, entity: PostCoordtransferItem) -> MethodResult:
        pass

    @get('/data/coordtransfer/{coordtransferResult}')
    def get_coordtransfer(self, coordtransferResult: str) -> List[Geometry]:
        pass
