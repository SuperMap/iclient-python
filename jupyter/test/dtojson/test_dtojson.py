from unittest import TestCase
import  json
from iclientpy.dtojson import *
import typing
import inspect
from iclientpy.rest.api.model import ProviderSetting,SMTilesMapProviderSetting,MngServiceInfo

from enum import  Enum

class C(Enum):
    CA = 'CA'
    CB = 'CB'
    CC = 'CC'

class B:
    b1: str

class A:
    a1: str
    a2: B
    a3: C
    a4: int
    a5: typing.List[C]

a = A()
a.a1 = '1'
a.a2 = B()
a.a2.b1 = 'b1'
a.a4 = 1
a.a3 = C.CA
a.a5 = [C.CA, C.CB]
class TestDTOJson(TestCase):

    def test(self):
        jsonstr = to_json_str(a)
        parseresult = deserializer(A)(jsonstr)#from_json_str(jsonstr, A) # type:A
        self.assertEqual(parseresult.a1, '1')
        self.assertEqual(parseresult.a2.b1, 'b1')
        self.assertEqual(parseresult.a3, C.CA)
        self.assertEqual(parseresult.a4, 1)
        self.assertIn(C.CA, parseresult.a5)
        self.assertIn(C.CB, parseresult.a5)
        self.assertNotIn(C.CC, parseresult.a5)


    def testArray(self) -> typing.List[C]:
        annos = inspect.getfullargspec(self.testArray).annotations
        list = deserializer(typing.List[C])('["CA","CB"]')
        self.assertEqual(len(list), 2)

    def testDictProperty(self):
        class WithDictProp:
            dictProp: dict
        parseresult = deserializer(WithDictProp)('{"dictProp":{"key":"value"}}') # type:WithDictProp
        self.assertEqual(parseresult.dictProp['key'], 'value')

        to_parse = WithDictProp()
        to_parse.dictProp = {"key":"value"}
        jsonstr = to_json_str(to_parse)
        self.assertIn('{"key":"value"}', jsonstr.replace(' ', '', 3))

    def test_abstract_type_field(self):
        jsonstr = '{"isStreamingService":false,"interfaceTypes":"com.supermap.services.rest.RestServlet","isSet":false,"instances":[{"interfaceType":"com.supermap.services.rest.RestServlet","componentType":"com.supermap.services.components.impl.MapImpl","name":"map-smtiles-World2/rest","componentSetName":null,"authorizeSetting":{"permittedRoles":[],"deniedRoles":[],"type":"PUBLIC"},"id":null,"componentName":"map-smtiles-World2","interfaceName":"rest","enabled":true,"status":"OK"}],"isClusterService":false,"type":"com.supermap.services.components.impl.MapImpl","interfaceNames":"rest","clusterInterfaceNames":"","isDataflowService":false,"component":{"isScSet":false,"scSetSetting":null,"scSetting":{"disabledInterfaceNames":"","instanceCount":0,"name":"map-smtiles-World2","alias":"","interfaceNames":"rest","type":"com.supermap.services.components.impl.MapImpl","config":{"cacheReadOnly":false,"cacheConfigs":null,"useVectorTileCache":false,"utfGridCacheConfig":null,"tileCacheConfig":null,"vectorTileCacheConfig":null,"expired":0,"logLevel":"info","outputPath":"","useCache":false,"outputSite":"","useUTFGridCache":false,"clip":false},"providers":"smtiles-World2","enabled":true}},"providerNames":"smtiles-World2","name":"map-smtiles-World2","alias":"","providers":[{"spsetSetting":null,"isSPSet":false,"spSetting":{"name":"smtiles-World2","alias":null,"innerProviders":null,"type":"com.supermap.services.providers.SMTilesMapProvider","config":{"dataPrjCoordSysType":null,"watermark":null,"cacheVersion":"4.0","outputPath":"./output","filePath":"C:/supermappackages/supermap-iserver-9.0.1-win64-deploy/bin/output/World_-452220655_256X256_PNG.smtiles","cacheMode":null,"name":null,"outputSite":"http://{ip}:{port}/iserver/output/"},"enabled":true}}]}'
        def fun(json_obj):
            return SMTilesMapProviderSetting
        clz_deserializer = deserializer(MngServiceInfo, {(ProviderSetting, 'config') : ByFieldValueParserSwitcher('type', {'com.supermap.services.providers.SMTilesMapProvider': parser(SMTilesMapProviderSetting)})})
        mng_serviceSetting = clz_deserializer(jsonstr) # type:MngServiceInfo
        self.assertIsInstance(mng_serviceSetting.providers[0].spSetting.config, SMTilesMapProviderSetting)
        config = mng_serviceSetting.providers[0].spSetting.config # type:SMTilesMapProviderSetting
        self.assertIn('World_-452220655_256X256_PNG.smtiles', config.filePath)

    def test_dict_with_object_value(self):
        obj_value_dict = {'key1': A(), 'key2': None}
        to_json_str(obj_value_dict)  # 不抛出异常就算过

    def test_base_fields(self):
        class FieldType:
            a:str
            def __init__(self, a = None):
                self.a = a

            def __eq__(self, other):
                return self.a == other.a


        class Base1:
            base1:FieldType


        class Base2(Base1):
            base2:FieldType


        class Kls(Base2):
            kls:FieldType


        kls = Kls()
        kls.kls = FieldType('kls')
        kls.base1 = FieldType('base1')
        kls.base2 = FieldType('base2')
        jsonstr = to_json_str(kls)
        json_dict = json.loads(jsonstr)  #type:dict
        self.assertSetEqual(set(json_dict.keys()), set(['base1', 'base2', 'kls']))
        parse_result = deserializer(Kls)(jsonstr)
        self.assertDictEqual(vars(kls), vars(parse_result))