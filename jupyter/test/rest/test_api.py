from unittest import TestCase
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.management import *
import httpretty
from sure import expect
from typing import List
from iclientpy.rest.api.model import Feature
from iclientpy.dtojson import *


class TestAPI(TestCase):
    @httpretty.activate
    def test_post_workspace(self):
        httpretty.register_uri(httpretty.POST,
                               'http://192.168.20.158:8090/iserver/services/security/login.json',
                               status=201,
                               set_cookie='JSESSIONID=958322873908FF9CA99B5CB443ADDD5C')
        httpretty.register_uri(httpretty.POST,
                               'http://192.168.20.158:8090/iserver/manager/workspaces.json',
                               status=201,
                               body='[{"serviceType": "RESTMAP", "serviceAddress": "123"}]'
                               )

        facctory = APIFactory('http://192.168.20.158:8090/iserver', 'admin', 'iserver')
        expect(httpretty.last_request()).to.have.property("body").being.equal(
            b'{"username": "admin", "password": "iserver"}'
        )
        mng = facctory.management()
        param = PostWorkspaceParameter()
        param.workspaceConnectionInfo = 'World.sxwu'
        param.servicesTypes = [ServiceType.RESTMAP]
        result = mng.postWorkspace(param=param)
        self.assertEqual(len(result), 1)

    @httpretty.activate
    def test_post_feature(self):
        httpretty.register_uri(httpretty.POST,
                               'http://192.168.20.158:8090/iserver/services/security/login.json',
                               status=201,
                               set_cookie='JSESSIONID=958322873908FF9CA99B5CB443ADDD5C')

        httpretty.register_uri(httpretty.POST,
                               'http://192.168.20.158:8090/iserver/services/data-World/rest/data/datasources/World/datasets/Countries/features.json',
                               status=200,
                               body='{"succeed": true}'
                               )

        facctory = APIFactory('http://192.168.20.158:8090/iserver', 'admin', 'iserver')
        expect(httpretty.last_request()).to.have.property("body").being.equal(
            b'{"username": "admin", "password": "iserver"}'
        )
        data_service = facctory.data_service('data-World/rest')
        jsonstr = '[{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["22","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都a","示例国家a","47067.0","亚洲"],"geometry":{"id":22,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION"}},{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["23","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都b","示例国家b","47067.0","亚洲"],"geometry":{"id":23,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION","prjCoordSys":null}}]'
        features = from_json_str(jsonstr, List[Feature])
        result = data_service.postFeatures('World', 'Countries', features)
        self.assertTrue(result.succeed)
