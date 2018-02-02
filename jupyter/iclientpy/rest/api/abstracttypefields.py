from .model import SMTilesMapProviderSetting, FastDFSTileProviderSetting, MongoDBTileProviderSetting, OTSTileProviderSetting, UGCV5TileProviderSetting, GeoPackageMapProviderSetting

_provider_type_name_to_setting_type = {
    'com.supermap.services.providers.SMTilesMapProvider': SMTilesMapProviderSetting,
    'com.supermap.services.providers.FastDFSTileProvider': FastDFSTileProviderSetting,
    'com.supermap.services.providers.MongoDBTileProvider': MongoDBTileProviderSetting,
    'com.supermap.services.providers.OTSTileProvider': OTSTileProviderSetting,
    'com.supermap.services.providers.UGCV5TileProvider': UGCV5TileProviderSetting,
    'com.supermap.services.providers.GeoPackageMapProvider': GeoPackageMapProviderSetting
}


def get_provider_setting_type_from_provider_type_name(jsonobj) -> type:
    return _provider_type_name_to_setting_type[jsonobj['type']]