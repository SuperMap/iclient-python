from ..decorator import post, get, put, delete, head
from .model import *
from .abstracttypefields import mng_service_info_deserializer
from io import FileIO


class Management:
    @post('/manager/workspaces', 'param')
    def post_workspaces(self, param: PostWorkspaceParameter) -> List[PostWorkspaceResultItem]:
        pass

    @get('/manager/workspaces')
    def get_workspaces(self) -> List[GetWorkspaceResultItem]:
        pass

    @delete('/manager/services/{name}')
    def delete_mapcomponent(self, name: str) -> MethodResult:
        pass

    @post('/manager/tileservice/jobs', entityKW='entity')
    def post_tilejobs(self, entity: PostTileJobsItem) -> PostTileJobsResultItem:
        pass

    @get('/manager/tileservice/jobs')
    def get_tilejobs(self) -> List[GetTileJobResultItem]:
        pass

    @head('/manager/tileservice/jobs')
    def head_tilejobs(self) -> int:
        pass

    @get('/manager/tileservice/jobs/{id}')
    def get_tilejob(self, id: str) -> GetTileJobResultItem:
        pass

    @put('/manager/tileservice/jobs/{id}', entityKW='entity')
    def put_tilejob(self, id: str, entity: BuildState) -> MethodResult:
        pass

    @delete('/manager/tileservice/jobs/{id}')
    def delete_tilejob(self, id: str) -> MethodResult:
        pass

    @head('/manager/tileservice/jobs/{id}')
    def head_tilejob(self, id: str) -> int:
        pass

    @post('/manager/tilesetupdatejobs', entityKW='entity')
    def post_tilesetupdatejobs(self, entity: PostTilesetUpdateJobs) -> PostTilesetUpdateJobsResultItem:
        pass

    @get('/manager/tilesetupdatejobs')
    def get_tilesetupdatejobs(self) -> List[GetTilesetExportJobResultItem]:
        pass

    @get('/manager/tilesetupdatejobs/{id}')
    def get_tilesetupdatejob(self, id: str) -> GetTilesetExportJobResultItem:
        pass

    @get('/manager/services/{service_name}', json_deserializer=mng_service_info_deserializer)
    def get_service(self, service_name: str) -> MngServiceInfo:
        pass

    @get('/manager/filemanager/uploadtasks')
    def get_fileuploadtasks(self) -> List[GetFileUploadResult]:
        pass

    @post('/manager/filemanager/uploadtasks', entityKW='entity')
    def post_fileuploadtasks(self, entity: PostFileUploadTasksParam) -> PostUploadTasksResult:
        pass

    @post('/manager/filemanager/uploadtasks/{id}', queryKWs=['toFile', 'overwrite', 'unzip'], fileKW='file')
    def post_fileuploadtask(self, id: str, file: FileIO, toFile: str, overwrite: bool = False,
                            unzip: bool = False) -> PostFileUploadTaskResult:
        pass

    @get('/manager/filemanager/uploadtasks/{id}')
    def get_fileuploadtask(self, id: str) -> GetFileUploadTaskResult:
        pass

    @get('/manager/datastores')
    def get_datastores(self) -> List[DataStoreSetting]:
        pass

    @get('/manager/datastores/{id}')
    def get_datastore(self, id:str) -> RestMngTileStorageInfo:
        pass
