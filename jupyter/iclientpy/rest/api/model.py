from enum import Enum
from typing import List


def default_init(cls: type):
    def _get_all_annotations(clz):
        result = {}
        annos = clz.__dict__.get('__annotations__', None)  # type:dict
        if annos is not None:
            result.update(annos)
        for base_clz in clz.__bases__:
            result.update(_get_all_annotations(base_clz))
        return result

    fileds = _get_all_annotations(cls)

    def init_method(self, *args, **kwargs):
        for field_name, field_type in fileds.items():
            setattr(self, field_name, None)

    cls.__init__ = init_method
    return cls


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


@default_init
class Point2D:
    x: float
    y: float


@default_init
class Rectangle2D:
    leftBottom: Point2D
    rightTop: Point2D


@default_init
class Geometry:
    id: int
    parts: List[int]
    partTopo: List[int]
    points: List[Point2D]
    type: GeometryType
    # TODO prjCoordSys style


@default_init
class Feature:
    fieldNames: List[str]
    fieldValues: List[str]
    geometry: Geometry


@default_init
class HttpError:
    code: int
    errorMsg: str


class PostResultType(Enum):
    AddContent = 'AddContent'
    createAsynchronizedResource = 'createAsynchronizedResource'
    CreateChild = 'CreateChild'
    CreateChildAndReturnContent = 'CreateChildAndReturnContent'


@default_init
class MethodResult:
    customResult: dict
    error: HttpError
    newResourceID: str
    newResourceLocation: str
    postResultType: PostResultType
    succeed: bool


@default_init
class Named:
    name: str


@default_init
class NamedSetting:
    alias: str


@default_init
class AbstractServiceSetting(NamedSetting):
    config: object
    type: str


@default_init
class ProviderSetting(AbstractServiceSetting):
    enabled: bool
    innerProviders: List[str]


@default_init
class MapProviderSetting:
    cacheMode: str
    cacheVersion: str
    name: str
    outputPath: str
    outputSite: str
    # TODO watermarker


@default_init
class MngProvider:
    isSPSet: bool
    spSetting: ProviderSetting
    spsetSetting: List[ProviderSetting]


@default_init
class CommaJoinedStr(List[str]):  # iServer管理里面有很多那种把字符串数组通过逗号分隔变成一个字符串的表达形式，反复split很烦。
    pass


@default_init
class ComponentSetting(AbstractServiceSetting):
    providers: CommaJoinedStr
    enabled: bool
    interfaceNames: CommaJoinedStr
    disabledInterfaceNames: CommaJoinedStr
    instanceCount: int


@default_init
class SCAndSCSetSetting:
    isScSet: bool
    scSetting: ComponentSetting
    # todo scSetSetting


@default_init
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


@default_init
class SMTilesMapProviderSetting(MapProviderSetting):
    filePath: str


@default_init
class FastDFSTileProviderSetting(MapProviderSetting):
    # TODO
    pass


@default_init
class MongoDBTileProviderSetting(MapProviderSetting):
    # TODO
    pass


@default_init
class OTSTileProviderSetting(MapProviderSetting):
    # TODO
    pass


@default_init
class UGCV5TileProviderSetting(MapProviderSetting):
    # todo
    pass


@default_init
class GeoPackageMapProviderSetting(MapProviderSetting):
    # todo
    pass


@default_init
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


@default_init
class GetFileUploadTaskResult:
    path: str
    progress: float
    md5: str
    uploadedDataMD5: str
    state: FileUploadState
    uploadedByteCount: int


@default_init
class PostFileUploadTasksParam:
    md5: str
    fileSize: int
    path: str


@default_init
class PostUploadTasksResult:
    newResourceID: str
    newResourceLocation: str
    postResultType: str
    succeed: bool


@default_init
class GetFileUploadResult:
    path: str
    progress: float
    taskID: str


class ClientType(Enum):
    IP = 'IP'
    Referer = 'Referer'
    RequestIP = 'RequestIP'
    NONE = 'NONE'


@default_init
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


@default_init
class PostWorkspaceParameter:
    workspaceConnectionInfo: str
    servicesTypes: List[ServiceType] = []
    isDataEditable: bool = False


@default_init
class PostWorkspaceResultItem:
    serviceAddress: str
    serviceType: ServiceType


@default_init
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
        self.outputPath = None


class MongoDBTilesourceInfo(TileSourceInfo):
    serverAdresses: List[str]
    database: str
    username: str
    password: str

    def __init__(self):
        super().__init__(TileSourceType.MongoDB)
        self.serverAdresses = None
        self.database = None
        self.username = None
        self.password = None


class FastDFSTileSourceInfo(TileSourceInfo):
    fdfsTrackers: List[str]
    fdhtGroups: List[List[str]]

    def __init__(self):
        super().__init__(TileSourceType.FastDFS)
        self.fdhtGroups = None
        self.fdfsTrackers = None


@default_init
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


@default_init
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


@default_init
class VectorTileLayer:
    expandPixels: int
    fields: List[str]
    fieldTypes: List[FieldType]
    maxScale: float
    minScale: float
    name: str
    searchFields: List[str]


@default_init
class VectorJobParameter:
    compressTolerance: int
    containAttributes: bool
    expands: str
    layers = List[VectorTileLayer]


class Type(Enum):
    NOTSET = 'NOTSET'
    KMLFILE = 'KMLFILE'


@default_init
class CacheRegionsInfo:
    type: Type


@default_init
class KMLFile(CacheRegionsInfo):
    filePath: str


@default_init
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


@default_init
class DataPreProcessInfo:
    columnCount: int
    rowCount: int


class FileVerificationMode(Enum):
    FILESIZE = 'FILESIZE'
    MD5 = 'MD5'


@default_init
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


@default_init
class UTFGridJobParameter:
    layerName: str
    pixCell: int


@default_init
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


@default_init
class TileIndex:
    columnIndex: int
    rowIndex: int


@default_init
class BuildingScaleInfo:
    nextIndex: TileIndex


@default_init
class TileMatrix:
    columnCount: int
    novalueFlags: List[List[bool]]
    rowCount: int
    startingIndex: TileIndex


@default_init
class WorkerBuildingInfo:
    completed: int
    lastTileRegion: Geometry


@default_init
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


@default_init
class ScaleBuildConfig:
    cacheRegions: List[Geometry]
    excludeRegions: List[Geometry]
    resolution: float
    scaleDenominator: float
    tileBoundsHeight: float
    tileBoundsWidth: float


@default_init
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


@default_init
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


@default_init
class TileTaskState:
    completed: int
    lastIndex: TileIndex
    runState: RunState
    workerId: str


class TaskType(Enum):
    DATAPREPROCESSTASK = 'DATAPREPROCESSTASK'
    TILETASK = 'TILETASK'


@default_init
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


@default_init
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


@default_init
class TilesetDesc:
    name: str
    filePath: str


@default_init
class TileJob:
    id: str
    info: JobInfo
    state: JobState
    targetTilesetInfo: TilesetDesc


@default_init
class PostTileJobsResultItem:
    succeed: str
    newResourceID: str
    customResult: TileJob
    newResourceLocation: str
    postResultType: str


@default_init
class CompletedTilesetInfo:
    name: str
    filePath: str


@default_init
class GetTileJobResultItem:
    id: str
    info: JobInfo
    state: JobState
    targetTilesetInfo: CompletedTilesetInfo


@default_init
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


@default_init
class PostTilesetUpdateJobsResultItem:
    succeed: bool
    newResourceID: str
    newResourceLocation: str
    postResultType: str


@default_init
class Projection:
    name: str
    type: str


@default_init
class CoordSys:
    # TODO
    unit: str
    # datum:Datum
    name: str


@default_init
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


@default_init
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


@default_init
class VersionUpdate:
    bounds: Rectangle2D
    scaleDenominators: List[float]
    resolutions: List[float]


@default_init
class TileVersion:
    name: str
    desc: str
    parent: str
    update: VersionUpdate
    timestamp: int


@default_init
class TilesetInfo:
    name: str
    metaData: MetaData
    tileVersions: List[TileVersion]


@default_init
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


@default_init
class TilesetExportScaleState:
    total: int
    completed: int
    resolution: float
    scaleDenominator: float
    tileMatrix: TileMatrix


@default_init
class ExporttingScaleState(TilesetExportScaleState):
    nextIndex: TileIndex


@default_init
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


@default_init
class GetTilesetExportJobResultItem:
    id: str
    info: TilesetExportJobInfo
    state: TilesetExportJobState


@default_init
class DataStoreSetting:
    id: str
    dataStoreInfo: DataStoreInfo


@default_init
class RestMngTileStorageInfo:
    id: str
    tileSourceInfo: TileSourceInfo
    tilesetInfos: List[TilesetInfo]
    totalCount: int
    currentCount: int
    connct: bool


@default_init
class ContextSetting:
    driver_memory: str
    executor_memory: str
    executor_cores: int


class TargetSericeType(Enum):
    RESTDATA = 'RESTDATA'
    RESTMAP = 'RESTMAP'
    RESTSPATIALANALYST = 'RESTSPATIALANALYST'


@default_init
class TargetServiceInfo:
    serviceAddress: str
    serviceType: TargetSericeType


@default_init
class PublishServiceResult:
    targetServiceInfos: List[TargetServiceInfo]
    targetDataPath: str


class OutputType(Enum):
    INDEXEDHDFS = 'INDEXEDHDFS'
    UDB = 'UDB'
    MONGODB = 'MONGODB'
    PG = 'PG'
    RDD = 'RDD'


@default_init
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


@default_init
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


@default_init
class FileSystemOutputSetting(OutputSetting):
    datasourcePath: str


@default_init
class DatabaseOutputSetting(OutputSetting):
    datasourceInfo: DatasourceConnectionInfo


@default_init
class SparkJobSetting:
    contextSetting: ContextSetting
    appName: str
    mainClass: str
    args: List[str]
    serviceInfo: PublishServiceResult


@default_init
class InputDataSetting:
    pass


@default_init
class CSVInputDataSetting(InputDataSetting):
    xIndex: int
    yIndex: int
    separator: str


@default_init
class FileCSVInputDataSetting(CSVInputDataSetting):
    filePath: str


@default_init
class Named:
    name: str


class BigDataFileShareDatasetInfoType(Enum):
    CSV = 'CSV'
    UDB = 'UDB'
    INDEXEDHDFS = 'INDEXEDHDFS'


@default_init
class BigDataFileShareDataSetInfo(Named):
    avilable: bool
    url: str
    type: BigDataFileShareDatasetInfoType


class CSVFieldType(Enum):
    INT32 = 'INT32'
    DOUBLE = 'DOUBLE'
    DATETIME = 'DATETIME'
    WTEXT = 'WTEXT'


@default_init
class CSVFieldInfo:
    name: str
    typ: CSVFieldType


@default_init
class CSVDatasetInfo(BigDataFileShareDataSetInfo):
    xIndex: int
    yIndex: int
    separator: str
    firstRowIsHead: bool
    prjCoordsys: int
    filedInfo: List[CSVFieldInfo]


@default_init
class IndexedHdfsDatasetInfo(BigDataFileShareDataSetInfo):
    datasetType: str


@default_init
class FieldInfo:
    name: str
    caption: str
    type: FieldType
    defaultValue: str
    maxLength: int
    isRequired: bool
    isZeroLengthAllowed: bool
    isSystemField: bool


@default_init
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


@default_init
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


@default_init
class DatasetGridInfo(DatasetInfo):
    blockSize: int
    height: int
    weight: int
    minValue: float
    maxValue: float
    noValue: float
    pixelFormat: PixelFormat


@default_init
class Color:
    red: int
    green: int
    blue: int
    alpha: int


class ColorSpaceType(Enum):
    CMYK = 'CMYK'
    RGB = 'RGB'


@default_init
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


@default_init
class DatasetVectorInfo(DatasetInfo):
    isFileCache: bool
    charset: Charset
    recordCount: int


@default_init
class ArcGISDatasetVectorInfo(DatasetVectorInfo):
    id: int


@default_init
class WFSDatasetInfo(DatasetVectorInfo):
    crsCode: str


@default_init
class SpatialDatasetInfo(DatasetInfo):
    datasetName: str


@default_init
class DatasetInputSetting(InputDataSetting):
    datasetInfo: Named
    datasetName: str
    numSlices: int
    specField: str


@default_init
class DistributeAnalysisSetting(SparkJobSetting):
    referServicesAddress: str
    referToken: str
    # input: InputDataSetting
    output: OutputSetting


class SummaryAnalystType(Enum):
    SUMMARYMESH = 'SUMMARYMESH'
    SUMMARYREGION = 'SUMMARYREGION'


@default_init
class AggregatePointsJobSetting(DistributeAnalysisSetting):
    type: SummaryAnalystType


class DistanceUnit(Enum):
    Meter = 'Meter'
    Kilometer = 'Kilometer'
    Yard = 'Yard'
    Foot = 'Foot'
    Mile = 'Mile'


@default_init
class MappingParameters:
    numericPrecision: int


@default_init
class SummaryAnalystSetting:
    pass


@default_init
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


@default_init
class SummaryMeshJobSetting(AggregatePointsJobSetting):
    analyst: SummaryMeshAnalystSetting


@default_init
class SummaryRegionAnalystSettingBase:
    regionDatasource: str
    regionDataset: str
    fields: str
    statisticModes: str
    resultFidleNames: str
    mappingParameters: MappingParameters


@default_init
# TODO: SummaryAnalystSetting为标记类，实际不存在
class SummaryRegionAnalystSetting(SummaryAnalystSetting, SummaryRegionAnalystSettingBase):
    attributeFilter: str


@default_init
class SummaryRegionJobSetting(AggregatePointsJobSetting):
    analyst: SummaryRegionAnalystSetting


@default_init
class BuffersAnalystSetting:
    distance: str
    distanceField: str
    distanceUnit: DistanceUnit
    bounds: str
    dissolveField: str


@default_init
class BuffersAnalystJobSetting(DistributeAnalysisSetting):
    analyst: BuffersAnalystSetting


class ImageType(Enum):
    basic = 'basic'
    heatmap = 'heatmap'


@default_init
class BuildCacheDrawingSetting:
    bounds: str
    level: int
    imageType: ImageType


@default_init
class BuildCacheJobSetting(DistributeAnalysisSetting):
    drawing: BuildCacheDrawingSetting


@default_init
class BuildGridIndexAnalystSetting:
    indexFile: str
    isSer: bool
    bounds: str
    rows: str
    cols: str
    interval: str


@default_init
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


@default_init
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


@default_init
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


@default_init
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


@default_init
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


@default_init
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


@default_init
class BufferAnalystParameter:
    endType: BufferEndType
    leftDistance: BufferDistance
    rightDistance: BufferDistance
    semicircleLineSegment: int
    radiusUnit: BufferRadiusUnit


@default_init
class OverlayAnalystGeoSetting:
    inputVectorClip: str
    datasetVectorClip: str
    mode: OverlayMode
    attributeFilter: str
    geometryClip: Geometry
    bufferAnalystParameter: BufferAnalystParameter


@default_init
class OverlayAnalystGeoJobSetting(DistributeAnalysisSetting):
    analyst: OverlayAnalystGeoSetting


@default_init
class OverlayAanalystSetting:
    inputOverlay: str
    datasetOverlay: str
    srcFields: str
    overlayFields: str
    mode: OverlayMode


@default_init
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


@default_init
class SpatialQueryGeoAnalystSetting:
    inputQuery: str
    datasetQuery: str
    mode: SpatialQueryMode
    attributeFilter: str
    geometryQuery: Geometry
    bufferAnalystPatameter: BufferAnalystParameter


@default_init
class SpatialQueryGeoJobSetting(DistributeAnalysisSetting):
    analyst: SpatialQueryGeoAnalystSetting


@default_init
class SummaryAttributesAnalystSetting:
    groupField: str
    attributeField: str
    statisticModes: str
    resultField: str


@default_init
class SummaryAttributesJobSetting(DistributeAnalysisSetting):
    analyst: SummaryAttributesAnalystSetting


@default_init
class SummaryWithInJobSettingBase(DistributeAnalysisSetting):
    type: SummaryAnalystType


@default_init
# 解决区域汇总分析analyst多个类型
class SummaryWithInRegionAnalystBaseSetting:
    pass


@default_init
class SummaryWithinMeshAnalystSetting(SummaryWithInRegionAnalystBaseSetting, SummaryMeshAnalystSetting):
    standardSummaryFields: bool
    weightedSummaryFields: bool
    sumShape: bool
    weightedFields: str
    standardFields: str
    standardStatisticModes: str
    weightedStatisticModes: str


@default_init
class SummaryWithinMeshJobSetting(SummaryWithInJobSettingBase):
    analyst: SummaryWithinMeshAnalystSetting


@default_init
class SummaryWithinRegionAnalystSettting(SummaryWithInRegionAnalystBaseSetting, SummaryRegionAnalystSettingBase):
    standardSummaryFields: bool
    weightedSummaryFields: bool
    sumShape: bool
    query: str
    weightedFields: str
    standardFields: str
    standardStatisticModes: str
    weightedStatisticModes: str


@default_init
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


@default_init
class TopologyvalidatorAnalystSetting:
    inputValidating: str
    datasetTopology: str
    rule: TopologyValidatorRuleType
    tolerance: str


@default_init
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


@default_init
class SparkJobState:
    runState: SparkRunState
    endState: bool
    errorMsg: str
    startTime: int
    endTime: int
    elapsedTime: int
    publisherelapsedTime: int


@default_init
class GetAggregatePointsResultItem:
    id: str
    state: SparkJobState
    setting: AggregatePointsJobSetting


@default_init
class PostAgggregatePointsEntity:
    input: InputDataSetting
    analyst: SummaryAnalystSetting
    type: SummaryAnalystType
    output: OutputSetting


@default_init
class GetFeatureJoinResultItem:
    id: str
    state: SparkJobState
    setting: FeatureJoinJobSettting


@default_init
class PostFeatureJoinEntity:
    input: InputDataSetting
    analyst: FeatureJoinAnalystSetting
    output: OutputSetting


@default_init
class GetBuffersResultItem:
    id: str
    state: SparkJobState
    setting: BuffersAnalystJobSetting


@default_init
class PostBuffersEntity:
    input: InputDataSetting
    analyst: BuffersAnalystSetting
    output: OutputSetting


@default_init
class GetDensityResultItem:
    id: str
    state: SparkJobState
    setting: KernelDensityJobSetting


@default_init
class PostDensityEntity:
    input: InputDataSetting
    analyst: KernelDensityAnalystSetting
    output: OutputSetting


@default_init
class GetOverlayResultItem:
    id: str
    state: SparkJobState
    setting: OverlayAnalystJobSetting


@default_init
class OverlayAnalystSetting:
    inputOverlay: str
    datasetOverlay: str
    srcFields: str
    overFields: str
    mode: OverlayMode


@default_init
class PostOverlayEntity:
    input: InputDataSetting
    analyst: OverlayAnalystSetting
    output: OutputSetting


@default_init
class GetQueryResultItem:
    id: str
    state: SparkJobState
    setting: SpatialQueryGeoJobSetting


@default_init
class PostQueryEntity:
    input: InputDataSetting
    analyst: SpatialQueryGeoAnalystSetting
    output: OutputSetting


@default_init
class GetSummaryAttributesResultItem:
    id: str
    state: SparkJobState
    setting: SummaryAttributesJobSetting


@default_init
class PostSummaryAttributesEntity:
    input: InputDataSetting
    analyst: SummaryAnalystSetting
    output: OutputSetting


@default_init
class GetSummaryRegionResultItem:
    id: str
    state: SparkJobState
    setting: SummaryWithInJobSettingBase


@default_init
class PostSummaryRegionEntity:
    input: InputDataSetting
    analyst: SummaryWithInRegionAnalystBaseSetting
    type: SummaryAnalystType
    output: OutputSetting


@default_init
class GetTopologyValidatorResultItem:
    id: str
    state: SparkJobState
    setting: TopologyValidatorJobSettting


@default_init
class PostTopologyValidatorEntity:
    input: InputDataSetting
    analyst: TopologyvalidatorAnalystSetting
    output: OutputSetting


@default_init
class GetVectorClipResultItem:
    id: str
    state: SparkJobState
    setting: OverlayAnalystGeoJobSetting


@default_init
class PostVectorClipEntity:
    input: InputDataSetting
    analyst: OverlayAnalystGeoSetting
    output: OutputSetting


@default_init
class DatasetsContent:
    datasetNames: List[str]
    datasetCount: int
    childUriList: List[str]


@default_init
class DatasetContent:
    childUriList: List[str]
    supportAttachments: bool
    supportFeatureMetadatas: bool


@default_init
class RelationShipDatasetContent(DatasetContent):
    datasetInfo: DatasetInfo


@default_init
class BigDataFileShareDatasetContent(DatasetContent):
    datasetInfo: BigDataFileShareDataSetInfo


@default_init
class FieldsContent:
    fieldNames: List[str]
    childUriList: List[str]


@default_init
class FieldContent:
    fieldInfo: FieldInfo
    childUriList: List[str]


@default_init
class CacheConfig:
    mapName: str
    scales: List[float]


@default_init
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
