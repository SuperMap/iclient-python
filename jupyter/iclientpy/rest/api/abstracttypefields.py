from .model import SMTilesMapProviderSetting

_provider_type_name_to_setting_type = {
    'com.supermap.services.providers.SMTilesMapProvider': SMTilesMapProviderSetting
}


def get_provider_setting_type_from_provider_type_name(jsonobj) -> type:
    return _provider_type_name_to_setting_type[jsonobj['type']]