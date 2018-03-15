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
    # TODO
    pass


class MongoDBTileProviderSetting(MapProviderSetting):
    # TODO
    pass


class OTSTileProviderSetting(MapProviderSetting):
    # TODO
    pass


class UGCV5TileProviderSetting(MapProviderSetting):
    # todo
    pass


class GeoPackageMapProviderSetting(MapProviderSetting):
    # todo
    pass


class PostFileUploadTaskResult:
    fileNames: str
    filePath: str
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


class ClientType(Enum):
    IP = 'IP'
    Referer = 'Referer'
    RequestIP = 'RequestIP'
    NONE = 'NONE'


class PostTokenParameter:
    userName: str
    password: str
    clientType: ClientType
    ip: str
    referer: str
    expiration: int


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


class DataStoreType(Enum):
    RELATIONSHIP = 'RELATIONSHIP'
    SPATIOTEMPORAL = 'SPATIOTEMPORAL'
    TILES = 'TILES'
    BIGDATAFILESHARE = 'BIGDATAFILESHARE'
    BINARY = 'BINARY'
    SPATIAL = 'SPATIAL'


class DataStoreInfo:
    datastoreType: DataStoreType


class TileSourceType(Enum):
    SMTiles = 'SMTiles'
    FastDFS = 'FastDFS'
    Hazelcast = 'Hazelcast'
    UTFGrid = 'UTFGrid'
    SVTiles = 'SVTiles'
    Remote = 'Remote'
    UGCV5 = 'UGCV5'
    MongoDB = 'MongoDB'
    UserDefined = 'UserDefined'
    GeoPackage = 'GeoPackage'
    GDP = 'GDP'
    OTS = 'OTS'
    ZXY = 'ZXY'

class TileSourceType(Enum):
    SMTiles = 'SMTiles'
    FastDFS = 'FastDFS'
    Hazelcast = 'Hazelcast'
    UTFGrid = 'UTFGrid'
    SVTiles = 'SVTiles'
    Remote = 'Remote'
    UGCV5 = 'UGCV5'
    MongoDB = 'MongoDB'
    UserDefined = 'UserDefined'
    GeoPackage = 'GeoPackage'
    MBTiles = 'MBTiles'
    GDP = 'GDP'
    OTS = 'OTS'
    ZXY = 'ZXY'

class TileSourceInfo(DataStoreInfo):
    type: str

    def __init__(self, type:TileSourceType = None):
        self.type = type


class SMTilesTileSourceInfo(TileSourceInfo):
    outputPath: str

    def __init__(self):
        super().__init__(TileSourceType.SMTiles)


class MongoDBTilesourceInfo(TileSourceInfo):
    serverAdresses: List[str]
    database: str
    username: str
    password: str

    def __init__(self):
        super().__init__(TileSourceType.MongoDB)


class FastDFSTileSourceInfo(TileSourceInfo):
    fdfsTrackers: List[str]
    fdhtGroups: List[str]

    def __init__(self):
        super().__init__(TileSourceType.FastDFS)


class OTSTileSourceInfo(TileSourceInfo):
    instanceName: str
    nodeName: str
    fromPublic: bool
    accessKeyId: str
    accessKeySecret: str



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


class PostTileJobsItem:
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


class PostTileJobsResultItem:
    succeed: str
    newResourceID: str
    customResult: TileJob
    newResourceLocation: str
    postResultType: str


class CompletedTilesetInfo:
    name: str
    filePath: str


class GetTileJobResultItem:
    id: str
    info: JobInfo
    state: JobState
    targetTilesetInfo: CompletedTilesetInfo


class MethodResult:
    succeed: bool


class PostTilesetUpdateJobs:
    sourceTileSourceInfo: TileSourceInfo
    sourceTilesetIdentifier: str
    targetTileSourceInfo: TileSourceInfo
    targetTilesetIdentifier: str
    scaleDenominators: List[float]
    bounds: Rectangle2D
    tileVersions: List[str]
    targetInfo: str
    relatedObject: str


class PostTilesetUpdateJobsResultItem:
    succeed: bool
    newResourceID: str
    newResourceLocation: str
    postResultType: str


class Projection:
    name: str
    type: str


class CoordSys:
    # TODO
    unit: str
    # datum:Datum
    name: str


class PrjCoordSys:
    # TODO
    epsgCode: int
    # enum
    distanceUnit: str
    type: str
    projection: Projection
    coordUnit: str
    name: str
    coordSystem: CoordSys


class MetaData:
    mapName: str
    tileWidth: int
    tileHeight: int
    resolutions: List[float]
    scaleDenominators: List[float]
    originalPoint: Point2D
    prjCoordSys: PrjCoordSys
    bounds: Rectangle2D
    tileRuleVersion: str
    tileType: TileType


class VersionUpdate:
    bounds: Rectangle2D
    scaleDenominators: List[float]
    resolutions: List[float]


class TileVersion:
    name: str
    desc: str
    parent: str
    update: VersionUpdate
    timestamp: int


class TilesetInfo:
    name: str
    metaData: MetaData
    tileVersions: List[TileVersion]


class TilesetExportJobInfo:
    sourceTilesetInfo: TilesetInfo
    targetTilesetInfo: TilesetInfo
    sourceTilesetDesc: TilesetDesc
    targetTilesetDesc: TilesetDesc
    sourceTileSourceInfo: TileSourceInfo
    sourceTilesetIdentifier: str
    targetTileSourceInfo: TileSourceInfo
    targetTilesetIdentifier: str
    scaleDenominators: List[float]
    bounds: Rectangle2D
    tileVersions: List[str]
    targetInfo: str
    relatedObject: str


class TilesetExportJobRunState(Enum):
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'
    COMPLETED = 'COMPLETED'


class TilesetExportScaleState:
    total: int
    completed: int
    resolution: float
    scaleDenominator: float
    tileMatrix: TileMatrix


class ExporttingScaleState(TilesetExportScaleState):
    nextIndex: TileIndex


class TilesetExportJobState:
    runState: TilesetExportJobRunState
    total: int
    completed: int
    actualCompleted: int
    startTime: int
    elapsedTime: int
    remainTime: int
    speedPerSecond: int
    toExportScaleState: List[TilesetExportScaleState]
    exporttingScale: ExporttingScaleState
    completedScales: List[TilesetExportScaleState]


class GetTilesetExportJobResultItem:
    id: str
    info: TilesetExportJobInfo
    state: TilesetExportJobState

class DataStoreSetting:
    id: str
    dataStoreInfo: DataStoreInfo
