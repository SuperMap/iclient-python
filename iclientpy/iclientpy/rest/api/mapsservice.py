from typing import List
from ..decorator import get, post, put, delete
from iclientpy.rest.api.model import GetMapsResult, PostMapsItem, MethodResult, ViewerMap, MapShareSetting


class MapsService:
    @get('/maps',
         queryKWs=['userNames', 'tags', 'suggest', 'sourceTypes', 'keywords', 'epsgCode', 'orderBy', 'currentPage',
                   'pageSize', 'dirIds', 'isNotInDir', 'updateStart', 'updateEnd', 'visitStart', 'visitEnd',
                   'filterFields', 'checkStatus', 'createStart', 'createEnd'])
    def get_maps(self, userNames: List[str], tags: List[str], suggest: bool, sourceTypes: List[str],
                 keywords: List[str], epsgCode: int, orderBy: List[str], currentPage: int, pageSize: int,
                 dirIds: List[int], isNotInDir: bool, updateStart: int, updateEnd: int, visitStart: int, visitEnd: int,
                 filterFields: List[str], checkStatus: str, createStart: int, createEnd: int) -> GetMapsResult:
        pass

    @post('/maps', entityKW='entity')
    def post_maps(self, entity: PostMapsItem) -> MethodResult:
        pass

    @delete('/maps', queryKWs=['ids'])
    def delete_maps(self, ids: List[str]) -> MethodResult:
        pass

    @get('/maps/{map_id}')
    def get_map(self, map_id: str) -> ViewerMap:
        pass

    @get('/maps/{map_id}/sharesetting')
    def get_map_sharesetting(self, map_id: str) -> List[MapShareSetting]:
        pass

    @put('/maps/{map_id}/sharesetting', entityKW='entity')
    def put_map_sharesetting(self, map_id: str, entity: List[MapShareSetting]) -> MethodResult:
        pass
