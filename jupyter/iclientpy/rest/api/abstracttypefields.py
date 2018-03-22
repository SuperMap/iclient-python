from typing import List
from .model import SMTilesMapProviderSetting, FastDFSTileProviderSetting, MongoDBTileProviderSetting, \
    OTSTileProviderSetting, UGCV5TileProviderSetting, GeoPackageMapProviderSetting, MngServiceInfo, ProviderSetting
from iclientpy.dtojson import *

_provider_setting_parsers = {
    'com.supermap.services.providers.SMTilesMapProvider': parser(SMTilesMapProviderSetting),
    'com.supermap.services.providers.FastDFSTileProvider': parser(FastDFSTileProviderSetting),
    'com.supermap.services.providers.MongoDBTileProvider': parser(MongoDBTileProviderSetting),
    'com.supermap.services.providers.OTSTileProvider': parser(OTSTileProviderSetting),
    'com.supermap.services.providers.UGCV5TileProvider': parser(UGCV5TileProviderSetting),
    'com.supermap.services.providers.GeoPackageMapProvider': parser(GeoPackageMapProviderSetting)
}

provider_setting_parser_switcher = ByFieldValueParserSwitcher('type', _provider_setting_parsers)
mng_service_info_deserializer = deserializer(MngServiceInfo,
                                             {(ProviderSetting, 'config'): provider_setting_parser_switcher})

from .model import TileSourceType, MongoDBTilesourceInfo, FastDFSTileSourceInfo, OTSTileSourceInfo, DataStoreSetting, \
    TileSourceInfo, DataStoreInfo

_data_source_info_parser_switcher = AbstractTypeParserSwitcher('type', {
    TileSourceType.MongoDB.value: parser(MongoDBTilesourceInfo),
    TileSourceType.FastDFS.value: parser(FastDFSTileSourceInfo),
    TileSourceType.OTS.value: parser(OTSTileSourceInfo)
})

data_store_setting_array_deserializer = deserializer(List[DataStoreSetting], abstract_type_parser={
    DataStoreInfo: _data_source_info_parser_switcher})

from .model import RestMngTileStorageInfo

rest_mng_tile_storage_info_deserializer = deserializer(RestMngTileStorageInfo, abstract_type_parser={
    TileSourceInfo: _data_source_info_parser_switcher})

from .model import OutputSetting, DatabaseOutputSetting, FileSystemOutputSetting, OutputType

_output_setting_parser_switcher = AbstractTypeParserSwitcher('type', {
    OutputType.PG.value: parser(DatabaseOutputSetting),
    OutputType.MONGODB.value: parser(DatabaseOutputSetting),
    OutputType.INDEXEDHDFS.value: parser(FileSystemOutputSetting),
    OutputType.UDB.value: parser(FileSystemOutputSetting)
    # OutputType.UDB.RDD
    # TODO: 暂未对接RDD，rest api文档中没有
})

from .model import AggregatePointsJobSetting, SummaryMeshJobSetting, SummaryRegionJobSetting, SummaryAnalystType, \
    GetAggregatePointsResultItem, GetFeatureJoinResultItem

_aggregate_point_job_setting_parser_switcher = AbstractTypeParserSwitcher('type', {
    SummaryAnalystType.SUMMARYMESH.value: parser(SummaryMeshJobSetting),
    SummaryAnalystType.SUMMARYREGION.value: parser(SummaryRegionJobSetting)
})

aggregate_points_job_settting_list_deserializer = deserializer(List[GetAggregatePointsResultItem],
                                                               abstract_type_parser={
                                                                   AggregatePointsJobSetting: _aggregate_point_job_setting_parser_switcher,
                                                                   OutputSetting: _output_setting_parser_switcher})

aggregate_point_job_settting_deserializer = deserializer(GetAggregatePointsResultItem, abstract_type_parser={
    AggregatePointsJobSetting: _aggregate_point_job_setting_parser_switcher,
    OutputSetting: _output_setting_parser_switcher})

feature_join_list_deserializer = deserializer(List[GetFeatureJoinResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

feature_join_deserializer = deserializer(GetFeatureJoinResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})
from .model import GetBuffersResultItem

buffers_list_deserializer = deserializer(List[GetBuffersResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

buffers_deserializer = deserializer(GetBuffersResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetDensityResultItem

density_list_deserializer = deserializer(List[GetDensityResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

density_deserializer = deserializer(GetDensityResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetOverlayResultItem

overlay_list_deserializer = deserializer(List[GetOverlayResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

overlay_deserializer = deserializer(GetOverlayResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetQueryResultItem

query_list_deserializer = deserializer(List[GetQueryResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

query_deserializer = deserializer(GetQueryResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetSummaryAttributesResultItem

summary_attributes_list_deserializer = deserializer(List[GetSummaryAttributesResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

summary_attributes_deserializer = deserializer(GetSummaryAttributesResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetSummaryRegionResultItem

summary_region_list_deserializer = deserializer(List[GetSummaryRegionResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

summary_region_deserializer = deserializer(GetSummaryRegionResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetTopologyValidatorResultItem

topologyvalidator_list_deserializer = deserializer(List[GetTopologyValidatorResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

topologyvalidator_deserializer = deserializer(GetTopologyValidatorResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

from .model import GetVectorClipResultItem

vector_clip_list_deserializer = deserializer(List[GetVectorClipResultItem], abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})

vector_clip_deserializer = deserializer(GetVectorClipResultItem, abstract_type_parser={
    OutputSetting: _output_setting_parser_switcher
})
