from unittest import TestCase
from iclientpy.rest.api.cacheutils import provider_setting_to_tile_source_info
from iclientpy.rest.api.model import FastDFSTileProviderSetting

class ProviderSettingToTileSourceInfoTest(TestCase):
    def test_unknown(self):
        class Kls:
            pass
        with self.assertRaises(Exception):
            provider_setting_to_tile_source_info(Kls())

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            provider_setting_to_tile_source_info(FastDFSTileProviderSetting())