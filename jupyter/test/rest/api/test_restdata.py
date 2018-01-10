import httpretty
from typing import List
from iclientpy.rest.api.model import Feature
from iclientpy.dtojson import from_json_str
from iclientpy.rest.decorator import HttpMethod
from .abstractrest import AbstractRESTTestCase


class RESTDataTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, "data_service", "data-World/rest")

    def test_dataservice(self):
        jsonstr = '[{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["22","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都a","示例国家a","47067.0","亚洲"],"geometry":{"id":22,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION"}},{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["23","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都b","示例国家b","47067.0","亚洲"],"geometry":{"id":23,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION","prjCoordSys":null}}]'
        features = from_json_str(jsonstr, List[Feature])
        self.check_api('post_features',
                       self.baseuri + "/services/data-World/rest/data/datasources/World/datasets/Countries/features.json",
                       HttpMethod.POST, httpretty.Response(status=200, body='{"succeed": true}'),
                       datasourceName='World', datasetName='Countries', entity=features, isUseBatch=True)

        self.check_api('get_features',
                       self.baseuri + "/services/data-World/rest/data/datasources/World/datasets/Countries/features.json",
                       HttpMethod.GET, httpretty.Response(status=200,
                                                          body='{"startIndex": 0,"childUriList": ["http://192.168.20.158:8090/iserver/services/data-World/rest/data/feature/0-13-0", "http://192.168.20.158:8090/iserver/services/data-World/rest/data/feature/0-13-1"], "geometryType":"REGION","featureCount": 247}'),
                       datasourceName='World', datasetName='Countries', fromIndex=3, toIndex=5)
