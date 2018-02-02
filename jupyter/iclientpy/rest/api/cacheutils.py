from .management import TileSourceInfo, SMTilesTileSourceInfo
from .model import SMTilesMapProviderSetting, FastDFSTileProviderSetting, MongoDBTileProviderSetting, OTSTileProviderSetting, UGCV5TileProviderSetting, GeoPackageMapProviderSetting
from os import path as ospath

def _smtiles_provider_setting_to_tilesourceinfo(setting: SMTilesMapProviderSetting) -> SMTilesTileSourceInfo:
    result = SMTilesTileSourceInfo()
    result.outputPath = ospath.dirname(setting.filePath)
    return result

def _provider_setting_to_tilesourceinfo_todo(setting):
    raise NotImplementedError('type ' + type(setting).__name__)

_provider_setting_to_tile_source_info_functions = {
    SMTilesMapProviderSetting : _smtiles_provider_setting_to_tilesourceinfo,
    FastDFSTileProviderSetting : _provider_setting_to_tilesourceinfo_todo,
    MongoDBTileProviderSetting : _provider_setting_to_tilesourceinfo_todo,
    OTSTileProviderSetting : _provider_setting_to_tilesourceinfo_todo,
    UGCV5TileProviderSetting : _provider_setting_to_tilesourceinfo_todo,
    GeoPackageMapProviderSetting : _provider_setting_to_tilesourceinfo_todo
}
def _unknown_provider_setting_type(setting):
    raise Exception('unknown type ' + type(setting))


def provider_setting_to_tile_source_info(provider_setting) -> TileSourceInfo:
    return _provider_setting_to_tile_source_info_functions.get(type(provider_setting), _unknown_provider_setting_type)(provider_setting)