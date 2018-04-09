from unittest import TestCase
from iclientpy.rest.api.cacheutils import provider_setting_to_tile_source_info, download_file_from_output_directory
from iclientpy.rest.api.model import FastDFSTileProviderSetting
import httpretty
import io

class ProviderSettingToTileSourceInfoTest(TestCase):
    def test_unknown(self):
        class Kls:
            pass
        with self.assertRaises(Exception):
            provider_setting_to_tile_source_info(Kls())

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            provider_setting_to_tile_source_info(FastDFSTileProviderSetting())

    @httpretty.activate
    def test_download_file(self):
        with io.BytesIO() as output:
            content = 'content'
            httpretty.register_uri(httpretty.GET, 'http://localhost:8090/iserver/./output/b.smtiles', content)
            download_file_from_output_directory('http://localhost:8090/iserver', r'.\output\b.smtiles', output)
            self.assertIn(content, str(output.getvalue()))