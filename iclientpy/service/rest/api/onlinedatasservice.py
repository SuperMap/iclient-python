from ..decorator import get, post, put, delete
from typing import List
from io import FileIO
from iclientpy.rest.api.model import GetMyDatasResult, PostMyDatasItem, MyDatasMethodResult, DataItem, MethodResult, \
    PutMyDataItem, MyDataUploadProcess, IportalDataAuthorizeEntity, OnlineDataShareSetting


class OnlineDatasService:
    @get('/datas',
         queryKWs=['userNames', 'types', 'fileName', 'serviceStatus', 'serviceId', 'ids', 'keywords', 'orderBy',
                   'orderType', 'tags', 'filterFields'])
    def get_datas(self, userNames: List[str], types: List[str], fileName: str, serviceStatus: List[str],
                  serviceId: str, ids: List[int], keywords: List[str], orderBy: str, orderType: str, tags: List[str],
                  filterFields: List[str]) -> GetMyDatasResult:
        pass

    @post('/mycontent/datas', entityKW='entity')
    def post_datas(self, entity: PostMyDatasItem) -> MyDatasMethodResult:
        pass

    @get('/datas/{data_id}')
    def get_data(self, data_id: str) -> DataItem:
        pass

    @put('/mycontent/datas/sharesetting', entityKW='entity')
    def put_sharesetting(self, entity: OnlineDataShareSetting) -> MethodResult:
        pass

    @put('/mycontent/datas/{data_id}', entityKW='entity')
    def put_data(self, data_id: str, entity: PutMyDataItem) -> MethodResult:
        pass

    @delete('/mycontent/datas/{data_id}')
    def delete_data(self, data_id: str) -> MethodResult:
        pass

    @post('/mycontent/datas/{data_id}/upload', fileKW='file')
    def upload_data(self, data_id: str, file: FileIO) -> MyDatasMethodResult:
        pass

    @get('/mycontent/datas/{data_id}/progress')
    def get_upload_process(self, data_id: str) -> MyDataUploadProcess:
        pass

    @put('/mycontent/datas/{data_id}/sharesetting', entityKW='entity')
    def put_data_sharesetting(self, data_id: str, entity: List[IportalDataAuthorizeEntity]) -> MethodResult:
        pass
