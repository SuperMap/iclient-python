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


class Named:
    name: str


class NamedSetting:
    alias: str


class AbstractServiceSetting(NamedSetting):
    config: object
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


class CommaJoinedStr(List[str]):  # iServer管理里面有很多那种把字符串数组通过逗号分隔变成一个字符串的表达形式，反复split很烦。
    pass


class ComponentSetting(AbstractServiceSetting):
    providers: CommaJoinedStr
    enabled: bool
    interfaceNames: CommaJoinedStr
    disabledInterfaceNames: CommaJoinedStr
    instanceCount: int


class SCAndSCSetSetting:
    isScSet: bool
    scSetting: ComponentSetting
    # todo scSetSetting


class MngServiceInfo:
    alias: str
    clusterInterfaceNames: str
    component: SCAndSCSetSetting
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

    def __init__(self, datastoreType):
        self.datastoreType = datastoreType


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

    def __init__(self, type: TileSourceType = None):
        super().__init__(DataStoreType.TILES)
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
    fdhtGroups: List[List[str]]

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


class Type(Enum):
    NOTSET = 'NOTSET'
    KMLFILE = 'KMLFILE'


class CacheRegionsInfo:
    type: Type


class KMLFile(CacheRegionsInfo):
    filePath: str


class PostTileJobsItem:
    dataConnectionString: str
    mapName: str
    scaleDenominators: List[float]
    resolutions: List[float]
    originalPoint: Point2D
    cacheBounds: Rectangle2D
    tileSize: TileSize
    format: OutputFormat
    compressionQuality: float
    transparent: bool
    epsgCode: int
    storeConfig: TileSourceInfo
    createNewTileVersion: bool
    tileVersionDescription: str
    parentTileVersion: str
    actualTileVersion: str
    refMapRestAdress: str
    # taskAssignmentType: TaskAssignmentType
    # cacheVersion: CacheVersion
    # storageType: StorageType
    vectorBounds: str
    tileType: TileType
    utfGridParameter: UTFGridJobParameter
    vectorParameter: VectorJobParameter
    # realspaceParameter: RealspaceJobParameter
    createStandardMBTiles: bool
    # dataPreProcessInfo: DataPreProcessInfo
    convertToPng8: bool
    # fileVerificationMode: FileVerificationMode
    autoAvoidEffectEnabled: bool
    cacheRegions: CacheRegionsInfo
    useLocal: bool


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
    tileFormat: OutputFormat


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


class RestMngTileStorageInfo:
    id: str
    tileSourceInfo: TileSourceInfo
    tilesetInfos: List[TilesetInfo]
    totalCount: int
    currentCount: int
    connct: bool


class ContextSetting:
    driver_memory: str
    executor_memory: str
    executor_cores: int


class TargetSericeType(Enum):
    RESTDATA = 'RESTDATA'
    RESTMAP = 'RESTMAP'
    RESTSPATIALANALYST = 'RESTSPATIALANALYST'


class TargetServiceInfo:
    serviceAddress: str
    serviceType: TargetSericeType


class PublishServiceResult:
    targetServiceInfos: List[TargetServiceInfo]
    targetDataPath: str


class OutputType(Enum):
    INDEXEDHDFS = 'INDEXEDHDFS'
    UDB = 'UDB'
    MONGODB = 'MONGODB'
    PG = 'PG'
    RDD = 'RDD'


class OutputSetting:
    outputPath: str
    datasetName: str
    type: OutputType


class EngineType(Enum):
    IMAGEPLUGINS = 'IMAGEPLUGINS'
    OGC = 'OGC'
    ORACLEPLUS = 'ORACLEPLUS'
    SDBPLUS = 'SDBPLUS'
    SQLPLUS = 'SQLPLUS'
    UDB = 'UDB'
    ES = 'ES'
    GOOGLEMAPS = 'GOOGLEMAPS'
    SUPERMAPCLOUD = 'SUPERMAPCLOUD'
    POSTGRESQL = 'POSTGRESQL'
    KINGBASE = 'KINGBASE'
    DB2 = 'DB2'
    NetCDF = 'NetCDF'
    ISERVERREST = 'ISERVERREST'
    MAPWORLD = 'MAPWORLD'
    ORACLESPATIAL = 'ORACLESPATIAL'
    MYSQL = 'MYSQL'
    MONGDB = 'MONGDB'


class DatasourceConnectionInfo:
    alias: str
    dataBase: str
    driver: str
    engienType: EngineType
    password: str
    server: str
    user: str
    connect: bool
    exclusive: bool
    openLinkTable: bool
    readOnly: bool


class FileSystemOutputSetting(OutputSetting):
    datasourcePath: str


class DatabaseOutputSetting(OutputSetting):
    datasourceInfo: DatasourceConnectionInfo


class SparkJobSetting:
    contextSetting: ContextSetting
    appName: str
    mainClass: str
    args: List[str]
    serviceInfo: PublishServiceResult


class InputDataSetting:
    pass


class CSVInputDataSetting(InputDataSetting):
    xIndex: int
    yIndex: int
    separator: str


class FileCSVInputDataSetting(CSVInputDataSetting):
    filePath: str


class Named:
    name: str


class BigDataFileShareDatasetInfoType(Enum):
    CSV = 'CSV'
    UDB = 'UDB'
    INDEXEDHDFS = 'INDEXEDHDFS'


class BigDataFileShareDataSetInfo(Named):
    avilable: bool
    url: str
    type: BigDataFileShareDatasetInfoType


class CSVFieldType(Enum):
    INT32 = 'INT32'
    DOUBLE = 'DOUBLE'
    DATETIME = 'DATETIME'
    WTEXT = 'WTEXT'


class CSVFieldInfo:
    name: str
    typ: CSVFieldType


class CSVDatasetInfo(BigDataFileShareDataSetInfo):
    xIndex: int
    yIndex: int
    separator: str
    firstRowIsHead: bool
    prjCoordsys: int
    filedInfo: List[CSVFieldInfo]


class IndexedHdfsDatasetInfo(BigDataFileShareDataSetInfo):
    datasetType: str


class FieldInfo:
    name: str
    caption: str
    type: FieldType
    defaultValue: str
    maxLength: int
    isRequired: bool
    isZeroLengthAllowed: bool
    isSystemField: bool


class UDBDatasetInfo(BigDataFileShareDataSetInfo):
    datsetType: str
    datasetName: str
    bounds: str
    epsgCode: int
    readOnly: bool
    fieldInfos = List[FieldInfo]


class EncodeType(Enum):
    BYTE = 'BYTE'
    DCT = 'DCT'
    INT16 = 'INT16'
    INT24 = 'INT24'
    INT32 = 'INT32'
    LZW = 'LZW'
    NONE = 'NONE'
    PNG = 'PNG'
    SGL = 'SGL'


class DatasetType(Enum):
    UNDEFINED = 'UNDEFINED'
    POINT = 'POINT'
    LINE = 'LINE'
    REGION = 'REGION'
    TEXT = 'TEXT'
    NETWORK = 'NETWORK'
    GRID = 'GRID'
    IMAGE = 'IMAGE'
    CAD = 'CAD'
    LINEM = 'LINEM'
    TABULAR = 'TABULAR'
    NETWORKPOINT = 'NETWORKPOINT'
    LINKTABLE = 'LINKTABLE'
    WCS = 'WCS'
    WMS = 'WMS'
    POINT3D = 'POINT3D'
    LINE3D = 'LINE3D'
    REGION3D = 'REGION3D'
    NETWORK3D = 'NETWORK3D'
    MODEL = 'MODEL'
    POINTEPS = 'POINTEPS'
    LINEEPS = 'LINEEPS'
    REGIONEPS = 'REGIONEPS'
    TEXTEPS = 'TEXTEPS'
    VECTORCOLLECTION = 'VECTORCOLLECTION'


class DatasetInfo(Named):
    description: str
    prjCoordSys: PrjCoordSys
    isReadOnly: bool
    tableName: str
    encodeType: EncodeType
    type: DatasetType
    dataSourceName: str
    bounds: Rectangle2D
    datasourceConnectionInfo: DatasourceConnectionInfo


class PixelFormat(Enum):
    BIT8 = 'BIT8'
    BIT16 = 'BIT16'
    BIT32 = 'BIT32'
    BIT64 = 'BIT64'
    DOUBLE = 'DOUBLE'
    SINGLE = 'SINGLE'
    UBIT1 = 'UBIT1'
    UBIT4 = 'UBIT4'
    UBIT8 = 'UBIT8'
    UBIT16 = 'UBIT16'
    RGB = 'RGB'
    RGBA = 'RGBA'
    UBIT32 = 'UBIT32'
    UNKNOWN = 'UNKNOWN'


class DatasetGridInfo(DatasetInfo):
    blockSize: int
    height: int
    weight: int
    minValue: float
    maxValue: float
    noValue: float
    pixelFormat: PixelFormat


class Color:
    red: int
    green: int
    blue: int
    alpha: int


class ColorSpaceType(Enum):
    CMYK = 'CMYK'
    RGB = 'RGB'


class DatasetImageInfo(DatasetInfo):
    blockSize: int
    height: int
    width: int
    palettes: List[Color]
    pixelFormat: PixelFormat
    bandCount: int
    bandNames: List[str]
    colorSpace: ColorSpaceType


class Charset(Enum):
    ANSI = 'ANSI'
    ARABIC = 'ARABIC'
    BALTIC = 'BALTIC'
    CHINESEBIG5 = 'CHINESEBIG5'
    CYRILLIC = 'CYRILLIC'
    DEFAULT = 'DEFAULT'
    EASTEUPOPE = 'EASTEUPOPE'
    GB18030 = 'GB18030'
    GREEK = 'GREEK'
    HEBREW = 'HEBREW'
    JOHAB = 'JOHAB'
    KOREAN = 'KPREAN'
    MAC = 'MAC'
    OEM = 'OEM'
    RUSSIAN = 'RUSSIAN'
    SHIFTJIS = 'SHIFTJIS'
    SYMBOL = 'SYMBOL'
    THAI = 'THAI'
    TURKISH = 'TURKISH'
    UNICODE = 'UNICODE'
    UTF32 = 'UTF32'
    UTF7 = 'UTF7'
    URF8 = 'UTF8'
    VIETNAMESE = 'VIETNAMESE'
    WINDOWS1252 = 'WINDOWS1252'
    XIA5 = 'XIA5'
    XIA5GREMAN = 'XIA5GERMAN'
    XIA5nORWEGIAN = 'XIA5NORWEGIAN'
    XIA5SWEDISH = 'XIA5SWEDISH'


class DatasetVectorInfo(DatasetInfo):
    isFileCache: bool
    charset: Charset
    recordCount: int


class ArcGISDatasetVectorInfo(DatasetVectorInfo):
    id: int


class WFSDatasetInfo(DatasetVectorInfo):
    crsCode: str


class SpatialDatasetInfo(DatasetInfo):
    datasetName: str


class DatasetInputSetting(InputDataSetting):
    datasetInfo: Named
    datasetName: str
    numSlices: int
    specField: str


class DistributeAnalysisSetting(SparkJobSetting):
    referServicesAddress: str
    referToken: str
    # input: InputDataSetting
    output: OutputSetting


class SummaryAnalystType(Enum):
    SUMMARYMESH = 'SUMMARYMESH'
    SUMMARYREGION = 'SUMMARYREGION'


class AggregatePointsJobSetting(DistributeAnalysisSetting):
    type: SummaryAnalystType


class DistanceUnit(Enum):
    Meter = 'Meter'
    Kilometer = 'Kilometer'
    Yard = 'Yard'
    Foot = 'Foot'
    Mile = 'Mile'


class MappingParameters:
    numericPrecision: int


class SummaryAnalystSetting:
    pass


# TODO: SummaryAnalystSetting为标记类，实际不存在
class SummaryMeshAnalystSetting(SummaryAnalystSetting):
    query: str
    resolution: str
    fields: str
    meshType: int
    statisticModes: str
    resultFieldNames: str
    meshSizeUnit: DistanceUnit
    mappingParameters: MappingParameters


class SummaryMeshJobSetting(AggregatePointsJobSetting):
    analyst: SummaryMeshAnalystSetting


class SummaryRegionAnalystSettingBase:
    regionDatasource: str
    regionDataset: str
    fields: str
    statisticModes: str
    resultFidleNames: str
    mappingParameters: MappingParameters


# TODO: SummaryAnalystSetting为标记类，实际不存在
class SummaryRegionAnalystSetting(SummaryAnalystSetting, SummaryRegionAnalystSettingBase):
    attributeFilter: str


class SummaryRegionJobSetting(AggregatePointsJobSetting):
    analyst: SummaryRegionAnalystSetting


class BuffersAnalystSetting:
    distance: str
    distanceField: str
    distanceUnit: DistanceUnit
    bounds: str
    dissolveField: str


class BuffersAnalystJobSetting(DistributeAnalysisSetting):
    analyst: BuffersAnalystSetting


class ImageType(Enum):
    basic = 'basic'
    heatmap = 'heatmap'


class BuildCacheDrawingSetting:
    bounds: str
    level: int
    imageType: ImageType


class BuildCacheJobSetting(DistributeAnalysisSetting):
    drawing: BuildCacheDrawingSetting


class BuildGridIndexAnalystSetting:
    indexFile: str
    isSer: bool
    bounds: str
    rows: str
    cols: str
    interval: str


class BuidlGridIndexJobSetting(DistributeAnalysisSetting):
    analyst: BuildGridIndexAnalystSetting


class JoinOperation(Enum):
    JOINONETOONE = 'JOINONETOONE'
    JOINONETOMANY = 'JOINONETOMANY'


class SpatialRelationShip(Enum):
    CONTAIN = 'CONTAIN'
    CROSS = 'CROSS'
    DISJOINT = 'DISJOINT'
    IDENTITY = 'IDENTITY'
    INTERSECT = 'INTERSECT'
    OVERLAP = 'OVERLAP'
    TOUCH = 'TOUCH'
    WITHIN = 'WITHIN'
    NEAR = 'NEAR'


class Unit(Enum):
    METER = 'METER'
    KILOMETER = 'KILOMETER'
    MILE = 'MILE'
    YARD = 'YARD'
    DEGREE = 'DEGREE'
    MILIMETER = 'MILIMETER'
    CENTIMETER = 'CENTIMETER'
    INCH = 'INCH'
    DECIMETER = 'DECIMETER'
    FOOT = 'FOOT'
    SECOND = 'SECOND'
    MINUTE = 'MINUTE'
    RADIAN = 'RADIAN'


class TemporalRelationShip(Enum):
    AFTER = 'AFTER'
    BEFORE = 'BEGPRE'
    CONTAINS = 'CONTAINS'
    DURING = 'DURING'
    FINISHES = 'FINISHES'
    MEETS = 'MEETS'
    NEAR = 'NEAR'
    FINISHEDBY = 'FINISHEDBY'
    METBY = 'METBY'
    OVERLAPS = 'OVERLAPS'
    OVERLAPPEDBY = 'OVERLAPPEDBY'
    STARTS = 'STARTS'
    STARTEDBY = 'STARTEDBY'
    EQUALS = 'EQUALS'


class TemporalNearDistanceUnit(Enum):
    MILLISECOND = 'MILLISECOND'
    SECOND = 'SECOND'
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


class AttributeStatisticalMode(Enum):
    EQUAL = 'EQUAL'
    NOTEQUAL = 'NOTEQUAL'


class FeatureJoinAnalystSetting:
    inputJoin: str
    datasetFeatureJoin: str
    joinOperation: JoinOperation
    joinFields: str
    spatialRelationship: SpatialRelationShip
    spatialNearDistance: float
    spatialNearDistanceUnit: Unit
    tolerance: float
    temporalRelationship: TemporalRelationShip
    temporalNearDistance: int
    temporalNearDistanceUnit: TemporalNearDistanceUnit
    attributeRelationship: str
    summaryFields: str
    summaryMode: str
    attributeMode: AttributeStatisticalMode
    specFields: str
    resultFieldNames: str
    mappingParameters: MappingParameters


class FeatureJoinJobSettting(DistributeAnalysisSetting):
    analyst: FeatureJoinAnalystSetting


class AreaUnit(Enum):
    SquareMeter = 'SquareMeter'
    SquareKileMeter = 'SquareKileMeter'
    Hectare = 'Hectare'
    Are = 'Are'
    Acre = 'Acre'
    SquareFoot = 'SquareFoot'
    SquareYard = 'SquareYard'
    SquareMile = 'SquareMile'


class KernelDensityAnalystSetting:
    query: str
    resolution: str
    radius: str
    fields: str
    method: int
    meshType: int
    meshSizeUnit: DistanceUnit
    radiusUnit: DistanceUnit
    areaUnit: AreaUnit


class KernelDensityJobSetting(DistributeAnalysisSetting):
    analyst: KernelDensityAnalystSetting


class OverlayMode(Enum):
    clip = 'clip'
    erase = 'erase'
    update = 'update'
    union = 'union'
    identity = 'identity'
    xor = 'xor'
    intersect = 'intersect'


class BufferEndType(Enum):
    FLAT = 'FLAT'
    ROUND = 'ROUND'


class BufferDistance:
    value: float
    exp: str


class BufferRadiusUnit(Enum):
    METER = 'METER'
    KILOMETER = 'KILOMETER'
    MILE = 'MILE'
    YARD = 'YARD'
    MILLIMETER = 'MILLIMETER'
    CENTIMETER = 'CENTIMETER'
    INCH = 'INCH'
    DECIMETER = 'DECIMETER'
    FOOT = 'FOOT'


class BufferAnalystParameter:
    endType: BufferEndType
    leftDistance: BufferDistance
    rightDistance: BufferDistance
    semicircleLineSegment: int
    radiusUnit: BufferRadiusUnit


class OverlayAnalystGeoSetting:
    inputVectorClip: str
    datasetVectorClip: str
    mode: OverlayMode
    attributeFilter: str
    geometryClip: Geometry
    bufferAnalystParameter: BufferAnalystParameter


class OverlayAnalystGeoJobSetting(DistributeAnalysisSetting):
    analyst: OverlayAnalystGeoSetting


class OverlayAanalystSetting:
    inputOverlay: str
    datasetOverlay: str
    srcFields: str
    overlayFields: str
    mode: OverlayMode


class OverlayAnalystJobSetting(DistributeAnalysisSetting):
    analyst: OverlayAanalystSetting


class SpatialQueryMode(Enum):
    NONE = 'NONE'
    IDENTITY = 'IDENTITY'
    DISJOINT = 'DISJOINT'
    INTERSECT = 'INTERSECT'
    TOUCH = 'TOUCH'
    OVERLAP = 'OVERLAP'
    CROSS = 'CROSS'
    WITHIN = 'WITHIN'
    CONTAIN = 'CONTAIN'


class SpatialQueryGeoAnalystSetting:
    inputQuery: str
    datasetQuery: str
    mode: SpatialQueryMode
    attributeFilter: str
    geometryQuery: Geometry
    bufferAnalystPatameter: BufferAnalystParameter


class SpatialQueryGeoJobSetting(DistributeAnalysisSetting):
    analyst: SpatialQueryGeoAnalystSetting


class SummaryAttributesAnalystSetting:
    groupField: str
    attributeField: str
    statisticModes: str
    resultField: str


class SummaryAttributesJobSetting(DistributeAnalysisSetting):
    analyst: SummaryAttributesAnalystSetting


class SummaryWithInJobSettingBase(DistributeAnalysisSetting):
    type: SummaryAnalystType


# 解决区域汇总分析analyst多个类型
class SummaryWithInRegionAnalystBaseSetting:
    pass


class SummaryWithinMeshAnalystSetting(SummaryWithInRegionAnalystBaseSetting, SummaryMeshAnalystSetting):
    standardSummaryFields: bool
    weightedSummaryFields: bool
    sumShape: bool
    weightedFields: str
    standardFields: str
    standardStatisticModes: str
    weightedStatisticModes: str


class SummaryWithinMeshJobSetting(SummaryWithInJobSettingBase):
    analyst: SummaryWithinMeshAnalystSetting


class SummaryWithinRegionAnalystSettting(SummaryWithInRegionAnalystBaseSetting, SummaryRegionAnalystSettingBase):
    standardSummaryFields: bool
    weightedSummaryFields: bool
    sumShape: bool
    query: str
    weightedFields: str
    standardFields: str
    standardStatisticModes: str
    weightedStatisticModes: str


class SummaryWithinRegionJobSetting(SummaryWithInJobSettingBase):
    analyst: SummaryWithinRegionAnalystSettting


class TopologyValidatorRuleType(Enum):
    REGIONNOOVERLAP = 'REGIONNOOVERLAP'
    REGIONNOOVERLAPWITH = 'REGIONNOOVERLAPWITH'
    REGIONCONTAINEDBYREGION = 'REGIONCONTAINEDBYREGION'
    REGIONCOVEREDBYREGION = 'REGIONCOVEREDBYREGION'
    LINENOOVERLAP = 'LINENOOVERLAP'
    LINENOOVERLAPWITH = 'LINENOOVERLAPWITH'
    POINTNOIDENTICAL = 'POINTNOIDENTICAL'


class TopologyvalidatorAnalystSetting:
    inputValidating: str
    datasetTopology: str
    rule: TopologyValidatorRuleType
    tolerance: str


class TopologyValidatorJobSettting(DistributeAnalysisSetting):
    analyst: TopologyvalidatorAnalystSetting


class SparkRunState(Enum):
    UNKNOWN = 'UNKNOWN'
    CONNECTED = 'CONNECTED'
    SUBMITTED = 'SUBMITTED'
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'
    KILLED = 'KILLED'
    LOST = 'LOST'


class SparkJobState:
    runState: SparkRunState
    endState: bool
    errorMsg: str
    startTime: int
    endTime: int
    elapsedTime: int
    publisherelapsedTime: int


class GetAggregatePointsResultItem:
    id: str
    state: SparkJobState
    setting: AggregatePointsJobSetting


class PostAgggregatePointsEntity:
    input: InputDataSetting
    analyst: SummaryAnalystSetting
    type: SummaryAnalystType
    output: OutputSetting


class GetFeatureJoinResultItem:
    id: str
    state: SparkJobState
    setting: FeatureJoinJobSettting


class PostFeatureJoinEntity:
    input: InputDataSetting
    analyst: FeatureJoinAnalystSetting
    output: OutputSetting


class GetBuffersResultItem:
    id: str
    state: SparkJobState
    setting: BuffersAnalystJobSetting


class PostBuffersEntity:
    input: InputDataSetting
    analyst: BuffersAnalystSetting
    output: OutputSetting


class GetDensityResultItem:
    id: str
    state: SparkJobState
    setting: KernelDensityJobSetting


class PostDensityEntity:
    input: InputDataSetting
    analyst: KernelDensityAnalystSetting
    output: OutputSetting


class GetOverlayResultItem:
    id: str
    state: SparkJobState
    setting: OverlayAnalystJobSetting


class OverlayAnalystSetting:
    inputOverlay: str
    datasetOverlay: str
    srcFields: str
    overFields: str
    mode: OverlayMode


class PostOverlayEntity:
    input: InputDataSetting
    analyst: OverlayAnalystSetting
    output: OutputSetting


class GetQueryResultItem:
    id: str
    state: SparkJobState
    setting: SpatialQueryGeoJobSetting


class PostQueryEntity:
    input: InputDataSetting
    analyst: SpatialQueryGeoAnalystSetting
    output: OutputSetting


class GetSummaryAttributesResultItem:
    id: str
    state: SparkJobState
    setting: SummaryAttributesJobSetting


class PostSummaryAttributesEntity:
    input: InputDataSetting
    analyst: SummaryAnalystSetting
    output: OutputSetting


class GetSummaryRegionResultItem:
    id: str
    state: SparkJobState
    setting: SummaryWithInJobSettingBase


class PostSummaryRegionEntity:
    input: InputDataSetting
    analyst: SummaryWithInRegionAnalystBaseSetting
    type: SummaryAnalystType
    output: OutputSetting


class GetTopologyValidatorResultItem:
    id: str
    state: SparkJobState
    setting: TopologyValidatorJobSettting


class PostTopologyValidatorEntity:
    input: InputDataSetting
    analyst: TopologyvalidatorAnalystSetting
    output: OutputSetting


class GetVectorClipResultItem:
    id: str
    state: SparkJobState
    setting: OverlayAnalystGeoJobSetting


class PostVectorClipEntity:
    input: InputDataSetting
    analyst: OverlayAnalystGeoSetting
    output: OutputSetting


class DatasetsContent:
    datasetNames: List[str]
    datasetCount: int
    childUriList: List[str]


class DatasetContent:
    childUriList: List[str]
    supportAttachments: bool
    supportFeatureMetadatas: bool


class RelationShipDatasetContent(DatasetContent):
    datasetInfo: DatasetInfo


class BigDataFileShareDatasetContent(DatasetContent):
    datasetInfo: BigDataFileShareDataSetInfo


class FieldsContent:
    fieldNames: List[str]
    childUriList: List[str]


class FieldContent:
    fieldInfo: FieldInfo
    childUriList: List[str]


class CacheConfig:
    mapName: str
    scales: List[float]


class MapConfig:
    outputPath: str
    outputSite: str
    useCache: bool
    tileCacheConfig: TileSourceInfo
    utfGridCacheConfig: TileSourceInfo
    vectorTileCacheConfig: TileSourceInfo
    useUTFGridCache: bool
    useVectorTileCache: bool
    cacheConfigs: List[CacheConfig]
    expired: int
    cacheReadOnly: bool
