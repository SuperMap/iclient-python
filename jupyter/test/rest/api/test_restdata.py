import httpretty
from typing import List
from iclientpy.rest.api.model import Feature
from iclientpy.dtojson import from_json_str
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.apifactory import APIFactory
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

    def test_getmap(self):
        jsonstr = '{"viewBounds":{"top":76.05736072192,"left":-76.05736072192,"bottom":-76.05736072192,"leftBottom":{"x":-76.05736072192,"y":-76.05736072192},"right":76.05736072192,"rightTop":{"x":76.05736072192,"y":76.05736072192}},"viewer":{"leftTop":{"x":0,"y":0},"top":0,"left":0,"bottom":256,"rightBottom":{"x":256,"y":256},"width":256,"right":256,"height":256},"distanceUnit":null,"minVisibleTextSize":0,"coordUnit":"DEGREE","scale":4.0000000000104906E-9,"description":"","paintBackground":false,"maxVisibleTextSize":0,"maxVisibleVertex":0,"clipRegionEnabled":false,"antialias":false,"textOrientationFixed":false,"angle":0,"prjCoordSys":{"distanceUnit":"METER","projectionParam":null,"epsgCode":4326,"coordUnit":"DEGREE","name":"Longitude / Latitude Coordinate System---GCS_WGS_1984","projection":null,"type":"PCS_EARTH_LONGITUDE_LATITUDE","coordSystem":{"datum":{"name":"D_WGS_1984","type":"DATUM_WGS_1984","spheroid":{"flatten":0.00335281066474748,"name":"WGS_1984","axis":6378137,"type":"SPHEROID_WGS_1984"}},"unit":"DEGREE","spatialRefType":"SPATIALREF_EARTH_LONGITUDE_LATITUDE","name":"GCS_WGS_1984","type":"GCS_WGS_1984","primeMeridian":{"longitudeValue":0,"name":"Greenwich","type":"PRIMEMERIDIAN_GREENWICH"}}},"minScale":0,"markerAngleFixed":false,"overlapDisplayedOptions":null,"visibleScales":[4.0000000000104906E-9,8.000000000020981E-9,1.5625000000435417E-8,3.125000000004909E-8,6.250000000009817E-8,1.2499999999690936E-7,2.499999999990779E-7],"visibleScalesEnabled":true,"customEntireBoundsEnabled":false,"clipRegion":null,"maxScale":0,"customParams":"","center":{"x":0,"y":0},"dynamicPrjCoordSyses":[{"distanceUnit":"METER","projectionParam":null,"epsgCode":4326,"coordUnit":"DEGREE","name":"Longitude / Latitude Coordinate System---GCS_WGS_1984","projection":null,"type":"PCS_EARTH_LONGITUDE_LATITUDE","coordSystem":{"datum":{"name":"D_WGS_1984","type":"DATUM_WGS_1984","spheroid":{"flatten":0.00335281066474748,"name":"WGS_1984","axis":6378137,"type":"SPHEROID_WGS_1984"}},"unit":"DEGREE","spatialRefType":"SPATIALREF_EARTH_LONGITUDE_LATITUDE","name":"GCS_WGS_1984","type":"GCS_WGS_1984","primeMeridian":{"longitudeValue":0,"name":"Greenwich","type":"PRIMEMERIDIAN_GREENWICH"}}}],"colorMode":null,"textAngleFixed":false,"overlapDisplayed":false,"userToken":{"userID":""},"cacheEnabled":true,"dynamicProjection":false,"autoAvoidEffectEnabled":true,"customEntireBounds":null,"name":"World","bounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"backgroundStyle":{"fillGradientOffsetRatioX":0,"markerSize":0,"fillForeColor":{"red":255,"green":0,"blue":0,"alpha":255},"fillGradientOffsetRatioY":0,"markerWidth":0,"markerAngle":0,"fillSymbolID":0,"lineColor":{"red":0,"green":0,"blue":0,"alpha":255},"markerSymbolID":0,"lineWidth":0.01,"markerHeight":0,"fillOpaqueRate":100,"fillBackOpaque":false,"fillBackColor":{"red":255,"green":255,"blue":255,"alpha":255},"fillGradientMode":"NONE","lineSymbolID":0,"fillGradientAngle":0}}'
        self.check_api('get_map', self.baseuri + "/services/data-World/rest/maps/World.json",
                       HttpMethod.GET, httpretty.Response(status=200, body=jsonstr), map='World')
