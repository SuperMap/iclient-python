from .management import TileSourceInfo, SMTilesTileSourceInfo
from .model import SMTilesMapProviderSetting, FastDFSTileProviderSetting, MongoDBTileProviderSetting, OTSTileProviderSetting, UGCV5TileProviderSetting, GeoPackageMapProviderSetting
from os import path as ospath
from io import BufferedIOBase
import requests

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


def download_file_from_output_directory(base_url:str, relative_path:str, output:BufferedIOBase):
    url = (base_url if base_url.endswith('/') else base_url + '/') + relative_path.replace('\\', '/').replace('//', '/')
    resp = requests.get(url, stream = True)
    for chunk in resp.iter_content(1024):
        if chunk:
            output.write(chunk)
