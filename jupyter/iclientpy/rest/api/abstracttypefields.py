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
