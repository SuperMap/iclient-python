from ..decorator import get, post
from typing import List
from iclientpy.rest.api.model import CreateNodeResult, CreateServerEntity, BatchMethodResult, NodeInfo, NodeInfoList


class NodeService:

    @post('/cloud/web/nodes/server', entityKW='entity')
    def create_server(self, entity: CreateServerEntity) -> CreateNodeResult:
        pass

    @post('/web/api/service/stopped', entityKW='node_ids')
    def stop_nodes(self, node_ids: List[str]) -> BatchMethodResult:
        pass

    @post('/web/api/service/started', entityKW='node_ids')
    def start_nodes(self, node_ids: List[str]) -> BatchMethodResult:
        pass

    @post('/web/api/service/deleted', entityKW='node_ids')
    def delete_nodes(self, node_ids: List[str]) -> BatchMethodResult:
        pass

    @post('/web/api/service/restarted', entityKW='node_ids')
    def restart_nodes(self, node_ids: List[str]) -> BatchMethodResult:
        pass

    @get('/web/api/service', fixed_queryKWs={'type': 'iServer'})
    def get_servers(self) -> NodeInfoList:
        pass
