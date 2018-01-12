from typing import List
from enum import Enum
from ..decorator import post, get
from .model import Point2D, Rectangle2D, Geometry


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


class TileSize(Enum):
    SIZE_1024 = 'SIZE_1024'
    SIZE_256 = 'SIZE_256'
    SIZE_512 = 'SIZE_512'


class OutputFormat(Enum):
    BIL = 'BIL'
    BINARY = 'BINARY'
    BMP = 'BMP'
    DEFAULT = 'DEFAULT'
    DXTZ = 'DXTZ'
    EMF = 'EMF'
    EPS = 'EPS'
    GEOTIFF = 'GEOTIFF'
    GIF = 'GIF'
    JPG = 'JPG'
    JPG_PNG = 'JPG_PNG'
    PBF = 'PBF'
    PDF = 'PDF'
    PNG = 'PNG'
    PNG8 = 'PNG8'
    TIFF = 'TIFF'


class TileSourceInfo:
    type: str
    outputPath: str


class TileType(Enum):
    Image = 'Image'
    OSGB = 'OSGB'
    RealspaceImage = 'RealspaceImage'
    Terrain = 'Terrain'
    UTFGrid = 'UTFGrid'
    Vector = 'Vector'


class UTFGridJobParameter:
    layerName: str
    pixCell: int


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    BYTE = 'BYTE'
    CHAR = 'CHAR'
    DATETIME = 'DATETIME'
    DOUBLE = 'DOUBLE'
    INT16 = 'INT16'
    INT32 = 'INT32'
    INT64 = 'INT64'
    LONGBINARY = 'LONGBINARY'
    SINGLE = 'SINGLE'
    TEXT = 'TEXT'
    WTEXT = 'WTEXT'


class VectorTileLayer:
    expandPixels: int
    fields: List[str]
    fieldTypes: List[FieldType]
    maxScale: float
    minScale: float
    name: str
    searchFields: List[str]


class VectorJobParameter:
    compressTolerance: int
    containAttributes: bool
    expands: str
    layers = List[VectorTileLayer]


class PostTileJobItem:
    dataConnectionString: str
    mapName: str
    tileSize: TileSize
    format: OutputFormat
    transparent: bool
    scaleDenominators: List[float]
    originalPoint: Point2D
    epsgCode: int
    cacheBounds: Rectangle2D
    storageID: str
    storeConfig: TileSourceInfo
    createNewTileVersion: bool
    parentTileVersion: str
    tileType: TileType
    utfGridParameter: UTFGridJobParameter
    vectorParameter: VectorJobParameter


class CacheVersion(Enum):
    DEFAULT = 'DEFAULT'
    VERSION_31 = 'VERSION_31'
    VERSION_40 = 'VERSION_40'
    VERSION_50 = 'VERSION_50'


class DataPreProcessInfo:
    columnCount: int
    rowCount: int


class FileVerificationMode(Enum):
    FILESIZE = 'FILESIZE'
    MD5 = 'MD5'


class RealspaceJobParameter:
    isDataFloat: bool
    layerName: str
    sceneName: str


class StorageType(Enum):
    Compact = 'Compact'
    Original = 'Original'


class TaskAssignmentType(Enum):
    CLOUD = 'CLOUD'
    DEFAULT = 'DEFAULT'
    GDP = 'GDP'


class UTFGridJobParameter:
    layerName: str
    pixCell: int


class JobInfo:
    actualTileVersion: str
    autoAvoidEffectEnabled: bool
    cacheBounds: Rectangle2D
    # cacheRegions:
    cacheVersion: CacheVersion
    compressionQuality: float
    convertToPng8: bool
    createNewTileVersion: bool
    createStandardMBTiles: bool
    dataConnectionString: str
    dataPreProcessInfo: DataPreProcessInfo
    epsgCode: int
    fileVerificationMode: FileVerificationMode
    format: OutputFormat
    mapName: str
    originalPoint: Point2D
    parentTileVersion: str
    realspaceParameter: RealspaceJobParameter
    refMapRestAdress: str
    resolutions: List[float]
    scaleDenominators: List[float]
    storageType: StorageType
    # storeConfig:
    taskAssignmentType: TaskAssignmentType
    tileSize: TileSize
    tileType: TileType
    tileVersionDescription: str
    transparent: bool
    useLocal: bool
    utfGridParameter: UTFGridJobParameter
    vectorBounds: str
    vectorParameter: VectorJobParameter


class TileIndex:
    columnIndex: int
    rowIndex: int


class BuildingScaleInfo:
    nextIndex: TileIndex


class TileMatrix:
    columnCount: int
    novalueFlags: List[List[bool]]
    rowCount: int
    startingIndex: TileIndex


class WorkerBuildingInfo:
    completed: int
    lastTileRegion: Geometry


class TileScaleInfo:
    completed: int
    completedBytes: int
    completedRegion: Geometry
    failedRegion: Geometry
    matrixes: List[TileMatrix]
    scaleDenominator: float
    total: int
    totalMatrix: TileMatrix
    workerBuildingInfos: List[WorkerBuildingInfo]


class ScaleBuildConfig:
    cacheRegions: List[Geometry]
    excludeRegions: List[Geometry]
    resolution: float
    scaleDenominator: float
    tileBoundsHeight: float
    tileBoundsWidth: float


class TileWorkerInfo:
    address: str
    controllable: bool
    hostName: str
    id: str
    ip: str
    local: bool
    masterAddress: str
    name: str
    port: int
    token: str


class DeployingStatus(Enum):
    DEPLOYING_DATA = 'DEPLOYING_DATA',
    DEPLOYING_JOB_CONFIG = 'DEPLOYING_JOB_CONFIG'
    NONE = 'NONE'
    PREPARE = 'PREPARE',
    RETRYING = 'RETRYING'
    WAITING_DEPLOYING_DATA = 'WAITING_DEPLOYING_DATA'


class ErrorStatus(Enum):
    DEPLOYING_DATA = 'DEPLOYING_DATA'
    DEPLOYING_JOB_CONFIG = 'DEPLOYING_JOB_CONFIG'
    NONE = 'NONE'
    PREPARE = 'PREPARE'
    UNKNOWN = 'UNKNOWN'
    WAITING_DEPLOYING_DATA = 'WAITING_DEPLOYING_DATA'


class JobDeployingInfo:
    deployingStatus: DeployingStatus
    errorStatus: ErrorStatus
    fileVerificationMode: FileVerificationMode
    retryDelay: int
    retryTime: int
    total: int
    uploaded: int


class BuildState(Enum):
    ANALYSTBLANK = 'ANALYSTBLANK'
    BUILDING = 'BUILDING'
    COMPLETED = 'COMPLETED'
    DATAPREPROCESS = 'DATAPREPROCESS'
    STOPPED = 'STOPPED'
    WAITTING = 'WAITTING'


class RunState(Enum):
    PRE_RUN = 'PRE_RUN'
    RUNNING = 'RUNNING'
    STOPED = 'STOPED'


class TileTaskState:
    completed: int
    lastIndex: TileIndex
    runState: RunState
    workerId: str


class TaskType(Enum):
    DATAPREPROCESSTASK = 'DATAPREPROCESSTASK'
    TILETASK = 'TILETASK'


class TileTask:
    dataPreProcessInfo: DataPreProcessInfo
    deployTime: int
    id: str
    isRetile: bool
    jobId: str
    masterAddress: str
    originalPoint: Point2D
    scaleConfigs: List[ScaleBuildConfig]
    state: TileTaskState
    taskType: TaskType
    tileMatrixToBuilds: List[TileMatrix]
    totalTileCount: int


class JobState:
    analystBlankPercentage: int
    buildingScale: BuildingScaleInfo
    completed: int
    completedBytes: int
    completedScale: List[TileScaleInfo]
    dataPreProcessBuildConfig: ScaleBuildConfig
    dataPreProcessState: BuildingScaleInfo
    deployedCompleted: int
    deployedTotal: int
    deployedWorkerInfo: List[TileWorkerInfo]
    eployingDataWorkerInfo: List[JobDeployingInfo]
    elapsedTime: int
    masterAddress: str
    noFeaturesTileCount: int
    pureColorTileCount: int
    remainTime: int
    runState: BuildState
    scaleConfigs: List[ScaleBuildConfig]
    scaleInfos: List[TileScaleInfo]
    speedPerSecond: int
    startTime: int
    tasks: List[TileTask]
    tasksToRetry: List[TileTask]
    tileMatrixEdgeCount: int
    total: int


class TilesetDesc:
    name: str
    filePath: str


class TileJob:
    id: str
    info: JobInfo
    state: JobState
    targetTilesetInfo: TilesetDesc


class PostTileJobResultItem:
    succeed: str
    newResourceID: str
    customResult: TileJob
    newResourceLocation: str
    postResultType: str


class GetTileJobResultItem:
    id: str
    info: JobInfo
    state: JobState


class Management:
    @post('/manager/workspaces', 'param')
    def post_workspaces(self, param: PostWorkspaceParameter) -> List[PostWorkspaceResultItem]:
        pass

    @get('/manager/workspaces')
    def get_workspaces(self) -> List[GetWorkspaceResultItem]:
        pass

    @post('/manager/tileservice/jobs', entityKW='entity')
    def post_tilejobs(self, entity: PostTileJobItem) -> PostTileJobResultItem:
        pass

    @get('/manager/tileservice/jobs')
    def get_tilejobs(self) -> List[GetTileJobResultItem]:
        pass
