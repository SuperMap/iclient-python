from enum import Enum
from typing import List


class GeometryType(Enum):
    ARC = 'ARC'
    BSPLINE = 'BSPLINE'
    CARDINAL = 'CARDINAL'
    CHORD = 'CHORD'
    CIRCLE = 'CIRCLE'
    CURVE = 'CURVE'
    ELLIPSE = 'ELLIPSE'
    ELLIPTICARC = 'ELLIPTICARC'
    GEOCOMPOUND = 'GEOCOMPOUND'
    GEOMODEL = 'GEOMODEL'
    GEOMODEL3D = 'GEOMODEL3D'
    GRAPHICOBJECT = 'GRAPHICOBJECT'
    LINE = 'LINE'
    LINE3D = 'LINE3D'
    LINEEPS = 'LINEEPS'
    LINEM = 'LINEM'
    PIE = 'PIE'
    POINT = 'POINT'
    POINT3D = 'POINT3D'
    POINTEPS = 'POINTEPS'
    RECTANGLE = 'RECTANGLE'
    REGION = 'REGION'
    REGION3D = 'REGION3D'
    REGIONEPS = 'REGIONEPS'
    ROUNDRECTANGLE = 'ROUNDRECTANGLE'
    TEXT = 'TEXT'
    TEXTEPS = 'TEXTEPS'
    UNKNOWN = 'UNKNOWN'


class Point2D:
    x: float
    y: float


class Rectangle2D:
    leftBottom: Point2D
    rightTop: Point2D


class Geometry:
    id: int
    parts: List[int]
    partTopo: List[int]
    points: List[Point2D]
    type: GeometryType
    # TODO prjCoordSys style


class Feature:
    fieldNames: List[str]
    fieldValues: List[str]
    geometry: Geometry


class HttpError:
    code: int
    errorMsg: str


class PostResultType(Enum):
    AddContent = 'AddContent'
    createAsynchronizedResource = 'createAsynchronizedResource'
    CreateChild = 'CreateChild'
    CreateChildAndReturnContent = 'CreateChildAndReturnContent'


class MethodResult:
    customResult: dict
    error: HttpError
    newResourceID: str
    newResourceLocation: str
    postResultType: PostResultType
    succeed: bool


class AbstractServiceSetting:
    alias: str
    config: object
    name: str
    type: str


class ProviderSetting(AbstractServiceSetting):
    enabled: bool
    innerProviders: List[str]


class MapProviderSetting:
    cacheMode: str
    cacheVersion: str
    name: str
    outputPath: str
    outputSite: str
    # TODO watermarker


class MngProvider:
    isSPSet: bool
    spSetting: ProviderSetting
    spsetSetting: List[ProviderSetting]


class MngServiceInfo:
    alias: str
    clusterInterfaceNames: str
    # todo component
    # todo instances
    interfaceNames: str
    interfaceTypes: str
    isClusterService: bool
    isDataflowService: bool
    isSet: bool
    isStreamingService: bool
    name: str
    providerNames: str
    providers: List[MngProvider]
    type: str


class SMTilesMapProviderSetting(MapProviderSetting):
    filePath: str


class FastDFSTileProviderSetting(MapProviderSetting):
    #TODO
    pass


class MongoDBTileProviderSetting(MapProviderSetting):
    #TODO
    pass


class  OTSTileProviderSetting(MapProviderSetting):
    #TODO
    pass


class UGCV5TileProviderSetting(MapProviderSetting):
    #todo
    pass


class  GeoPackageMapProviderSetting(MapProviderSetting):
    #todo
    pass



class PostFileUploadTaskResult:
    fileNames: str
    fielPath: str
    fileSize: int
    isDirectory: bool


class FileUploadState(Enum):
    NEW = 'NEW'
    UPLOADING = 'UPLOADING'
    COMPLETED = 'COMPLETED'
    UPLOADING_ERROR = 'UPLOADING_ERROR'
    ERROR = 'ERROR'


class GetFileUploadTaskResult:
    path: str
    progress: float
    md5: str
    uploadedDataMD5: str
    state: FileUploadState
    uploadedByteCount: int


class PostFileUploadTasksParam:
    md5: str
    fileSize: int
    path: str


class PostUploadTasksResult:
    newResourceID: str
    newResourceLocation: str
    postResultType: str
    succeed: bool


class GetFileUploadResult:
    path: str
    progress: float
    taskID: str
