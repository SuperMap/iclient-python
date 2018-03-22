from unittest import TestCase
from iclientpy.rest.api.model import DataStoreSetting, MongoDBTilesourceInfo
from iclientpy.dtojson import *
from typing import List


class CustomDeserializerTest(TestCase):
    def test_data_store_setting_deserializer(self):
        result = deserializer(List[DataStoreSetting])(
            '[{"id":"mongodb","dataStoreInfo":{"serverAdresses":["127.0.0.1:88"],"database":"mongodb","password":"mongodb","type":"MongoDB","datastoreType":"TILES","username":"mongodb"}}]')  # type:list[DataStoreSetting]
        self.assertIsInstance(result[0].dataStoreInfo, MongoDBTilesourceInfo)
        info = result[0].dataStoreInfo  # type:MongoDBTilesourceInfo
        self.assertEqual(info.serverAdresses, ['127.0.0.1:88'])
