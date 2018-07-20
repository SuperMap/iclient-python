from ..decorator import get, post, put, delete
from typing import List
from io import FileIO
from iclientpy.rest.api.model import GetMyDatasResult, PostMyDatasItem, MyDatasMethodResult, DataItem, MethodResult, \
    PutMyDataItem, MyDataUploadProcess, IportalDataAuthorizeEntity


class DatasService:
    @get('/web/datas',
         queryKWs=['userNames', 'types', 'fileName', 'serviceStatus', 'serviceId', 'ids', 'keywords', 'orderBy',
                   'orderType', 'tags', 'filterFields'])
    def get_datas(self, userNames: List[str], types: List[str], fileName: str, serviceStatus: List[str],
                  serviceId: str, ids: List[int], keywords: List[str], orderBy: str, orderType: str, tags: List[str],
                  filterFields: List[str]) -> GetMyDatasResult:
        pass

    @post('/web/mycontent/datas', entityKW='entity')
    def post_datas(self, entity: PostMyDatasItem) -> MyDatasMethodResult:
        pass

    @get('/web/datas/{data_id}')
    def get_data(self, data_id: str) -> DataItem:
        pass

    @put('/web/mycontent/datas/{data_id}', entityKW='entity')
    def put_data(self, data_id: str, entity: PutMyDataItem) -> MethodResult:
        pass

    @delete('/web/mycontent/datas/{data_id}')
    def delete_data(self, data_id: str) -> MethodResult:
        pass

    @post('/web/mycontent/datas/{data_id}/upload', fileKW='file')
    def upload_data(self, data_id: str, file: FileIO) -> MyDatasMethodResult:
        pass

    @get('/web/mycontent/datas/{data_id}/progress')
    def get_upload_process(self, data_id: str) -> MyDataUploadProcess:
        pass

    @get('/web/mycontent/datas/{data_id}/sharesetting')
    def get_data_sharesetting(self, data_id: str) -> List[IportalDataAuthorizeEntity]:
        pass

    @put('/web/mycontent/datas/{data_id}/sharesetting', entityKW='entity')
    def put_data_sharesetting(self, data_id: str, entity: List[IportalDataAuthorizeEntity]) -> MethodResult:
        pass
