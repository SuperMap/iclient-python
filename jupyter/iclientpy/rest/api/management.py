from typing import List
from enum import Enum
from ..decorator import post, get


class ServiceType(Enum):
    AGSRESTDATA = 'AGSRESTDATA'
    AGSRESTMAP = 'AGSRESTMAP'
    AGSRESTNETWORKANALYST = 'AGSRESTNETWORKANALYST'
    BAIDUREST = 'BAIDUREST'
    DATAFLOW = 'DATAFLOW'
    GOOGLEREST = 'GOOGLEREST'
    REST_NETWORKANALYST3D = 'REST_NETWORKANALYST3D'
    RESTADDRESSMATCH = 'RESTADDRESSMATCH'
    RESTDATA = 'RESTDATA'
    RESTMAP = 'RESTMAP'
    RESTREALSPACE = 'RESTREALSPACE'
    RESTSPATIALANALYST = 'RESTSPATIALANALYST'
    RESTTRAFFICTRANSFERANALYST = 'RESTTRAFFICTRANSFERANALYST'
    RESTTRANSPORTATIONANALYST = 'RESTTRANSPORTATIONANALYST'
    STREAMING = 'STREAMING'
    WCS111 = 'WCS111'
    WCS112 = 'WCS112'
    WFS100 = 'WFS100'
    WFS200 = 'WFS200'
    WMS111 = 'WMS111'
    WMS130 = 'WMS130'
    WMTS100 = 'WMTS100'
    WMTSCHINA = 'WMTSCHINA'
    WPS100 = 'WPS100'


class PostWorkspaceParameter:
    workspaceConnectionInfo: str
    servicesTypes: List[ServiceType] = []
    isDataEditable: bool = False


class PostWorkspaceResultItem:
    serviceAddress: str
    serviceType: ServiceType


class GetWorkspaceResultItem:
    address: str
    enabled: bool
    message: str
    name: str
    serviceName: str
    serviceType: str


class Management:
    @post('/manager/workspaces', 'param')
    def post_workspaces(self, param: PostWorkspaceParameter) -> List[PostWorkspaceResultItem]:
        pass

    @get('/manager/workspaces')
    def get_workspaces(self) -> List[GetWorkspaceResultItem]:
        pass
