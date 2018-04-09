from .model import SMTilesMapProviderSetting, FastDFSTileProviderSetting, MongoDBTileProviderSetting, \
    OTSTileProviderSetting, UGCV5TileProviderSetting, GeoPackageMapProviderSetting, MngServiceInfo, ProviderSetting
from iclientpy.dtojson import *


def _comma_joined_str_parser(text:str, *args, **kwargs):
    return text.split(',')


from .model import CommaJoinedStr
register(CommaJoinedStr, _comma_joined_str_parser)

from .model import TileSourceType, MongoDBTilesourceInfo, FastDFSTileSourceInfo, OTSTileSourceInfo, DataStoreSetting, \
    TileSourceInfo, DataStoreInfo

_data_source_info_parser_switcher = AbstractTypeParserSwitcher('type', {
    TileSourceType.MongoDB.value: parser(MongoDBTilesourceInfo),
    TileSourceType.FastDFS.value: parser(FastDFSTileSourceInfo),
    TileSourceType.OTS.value: parser(OTSTileSourceInfo)
})
register(DataStoreInfo, _data_source_info_parser_switcher)
register(TileSourceInfo, _data_source_info_parser_switcher)

from .model import OutputSetting, DatabaseOutputSetting, FileSystemOutputSetting, OutputType

_output_setting_parser_switcher = AbstractTypeParserSwitcher('type', {
    OutputType.PG.value: parser(DatabaseOutputSetting),
    OutputType.MONGODB.value: parser(DatabaseOutputSetting),
    OutputType.INDEXEDHDFS.value: parser(FileSystemOutputSetting),
    OutputType.UDB.value: parser(FileSystemOutputSetting)
    # OutputType.UDB.RDD
    # TODO: 暂未对接RDD，rest api文档中没有
})
register(OutputSetting, _output_setting_parser_switcher)

from .model import AggregatePointsJobSetting, SummaryMeshJobSetting, SummaryRegionJobSetting, SummaryAnalystType, \
    GetAggregatePointsResultItem, GetFeatureJoinResultItem

_aggregate_point_job_setting_parser_switcher = AbstractTypeParserSwitcher('type', {
    SummaryAnalystType.SUMMARYMESH.value: parser(SummaryMeshJobSetting),
    SummaryAnalystType.SUMMARYREGION.value: parser(SummaryRegionJobSetting)
})

register(AggregatePointsJobSetting, _aggregate_point_job_setting_parser_switcher)

from .model import BigDataFileShareDataSetInfo, UDBDatasetInfo, CSVDatasetInfo, IndexedHdfsDatasetInfo, \
    BigDataFileShareDatasetInfoType

_bigdata_fileshare_dataset_info_parser_switcher = AbstractTypeParserSwitcher('type', {
    BigDataFileShareDatasetInfoType.UDB.value: parser(UDBDatasetInfo),
    BigDataFileShareDatasetInfoType.INDEXEDHDFS.value: parser(IndexedHdfsDatasetInfo),
    BigDataFileShareDatasetInfoType.CSV.value: parser(CSVDatasetInfo)
})
register(BigDataFileShareDataSetInfo, _bigdata_fileshare_dataset_info_parser_switcher)


from .model import MapConfig
_component_config_parser = ByFieldValueParserSwitcher('type', {
    'com.supermap.services.components.impl.MapImpl': parser(MapConfig)
})
from .model import ComponentSetting
_component_setting_parser = parser(ComponentSetting, field_parser={(ComponentSetting, 'config'):_component_config_parser})
register(ComponentSetting, _component_setting_parser)

