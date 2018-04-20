import os
import httpretty
import requests_mock
from time import sleep
from unittest import TestCase, mock
from geopandas import GeoDataFrame
from iclientpy.rest.apifactory import OnlineAPIFactory
from iclientpy.data.portal import from_geodataframe_pubilsh
from iclientpy.rest.api.model import ViewerMap


class test_portal(TestCase):
    @httpretty.activate
    def test_from_geodataframe_publish(self):
        base_uri = "http://www.supermapol.com"
        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://sso.supermap.com/login',
                           text='{"lt":"LT-11506-wDwBEJsE2dWoVoKOfIDBZyRt0qk35k-sso.supermap.com","execution":"e1s1","_eventId":"submit"}',
                           cookies={'JSESSIONID': '958322873908FF9CA99B5CB443ADDD5C'})
            m.register_uri('POST', 'https://sso.supermap.com/login',
                           headers={'location': 'https://www.supermapol.com/shiro-cas'}, status_code=302)
            m.register_uri('GET', 'https://www.supermapol.com/shiro-cas',
                           cookies={'JSESSIONID': '958322873908FF9CA99B5CB443ADDD5C'})
            api = OnlineAPIFactory('http://www.supermapol.com', 'admin', 'Supermap123')
        httpretty.register_uri(httpretty.POST, base_uri + '/web/mycontent/datas.json',
                               body='{"childID":"2","isAsynchronizedReturn":false,"childContent":null,"childUrl":null,"customResult":null}',
                               status=201)
        httpretty.register_uri(httpretty.POST, base_uri + '/web/mycontent/datas/2/upload.json',
                               body='{"childContent":null,"childID":"2","childUrl":null,"customResult":null,"isAsynchronizedReturn":false}',
                               status=200)
        httpretty.register_uri(httpretty.GET, base_uri + '/web/mycontent/datas/2/progress.json',
                               body='{"id":"null","read":100,"total":100}', status=200)
        httpretty.register_uri(httpretty.GET, base_uri + '/web/mycontent/datas/2.json',
                               responses=[httpretty.Response(
                                   body='{"dataMetaInfo":null,"lastModfiedTime":1523946252375,"fileName":"test.json","thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","dataItemServices":[],"dataCheckResult":{"serviceCheckInfos":null,"dataCheckInfo":null},"publishInfo":null,"authorizeSetting":[],"description":null,"userName":"admin","type":"JSON","tags":[],"coordType":null,"size":1006096,"createTime":1523946252375,"serviceStatus":"DOES_NOT_INVOLVE","nickname":"admin","id":18220636,"serviceId":null,"downloadCount":0,"storageId":"wdosrwih_pdb9lxhq_d7485aae_cd3d_413b_99f8_5e72930d2f53","status":"CREATED","MD5":"67492951f6d694e45d26278dc1a7d40d"}',
                                   status=200),
                                   httpretty.Response(
                                       body='{"dataMetaInfo":null,"lastModfiedTime":1523946252375,"fileName":"test.json","thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","dataItemServices":[],"dataCheckResult":{"serviceCheckInfos":null,"dataCheckInfo":null},"publishInfo":null,"authorizeSetting":[],"description":null,"userName":"admin","type":"JSON","tags":[],"coordType":null,"size":1006096,"createTime":1523946252375,"serviceStatus":"DOES_NOT_INVOLVE","nickname":"admin","id":18220636,"serviceId":null,"downloadCount":0,"storageId":"wdosrwih_pdb9lxhq_d7485aae_cd3d_413b_99f8_5e72930d2f53","status":"OK","MD5":"67492951f6d694e45d26278dc1a7d40d"}',
                                       status=200)])
        httpretty.register_uri(httpretty.POST, base_uri + "/web/maps.json",
                               body='{"succeed":true,"newResourceID":"24","newResourceLocation":"http://localhost:8090/iportal/web/maps/24"}',
                               status=200)
        httpretty.register_uri(httpretty.GET, base_uri + '/web/maps/24.json',
                               body='''
                               {"extent":null,"controls":null,"extentString":"","description":null,"verifyReason":null,"units":null,"title":"map","resolution":0,"checkStatus":"SUCCESSFUL","visitCount":2,"centerString":"{'x':1.2626762220726E7,'y':2619886.8435466}","epsgCode":3857,"nickname":"admin","layers":[{"wmtsOption":null,"styleString":"null","title":"天地图","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":191,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"BASE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":0,"scalesString":"null","scales":null,"name":"天地图","bounds":null,"mapId":2128139851,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"天地图-标签","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":192,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"OVERLAY_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":1,"scalesString":"null","scales":null,"name":"天地图-标签","bounds":null,"mapId":2128139851,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"layer_liu","type":null,"subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":{"distanceUnit":null,"projectionParam":null,"epsgCode":4326,"coordUnit":null,"name":null,"projection":null,"type":"PCS_USER_DEFINED","coordSystem":null},"id":193,"cartoCSS":"{'isAddFile':true,'needTransform':'needTransform'}","datasourceName":null,"prjCoordSysString":"{'distanceUnit':null,'projectionParam':null,'epsgCode':4326,'coordUnit':null,'name':null,'projection':null,'type':'PCS_USER_DEFINED','coordSystem':null}","identifier":null,"layerType":"FEATURE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://localhost:8090/iportal/services/../web/datas/522725056/content.json","zindex":2,"scalesString":"null","scales":null,"name":"layer_liu","bounds":null,"mapId":2128139851,"style":null,"markersString":"null","opacity":1,"markers":null}],"id":2128139851,"searchSetting":null,"thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","level":null,"center":{"x":1.2626762220726E7,"y":2619886.8435466},"authorizeSetting":[{"permissionType":"DELETE","aliasName":"admin","entityRoles":["ADMIN","SYSTEM"],"entityType":"USER","entityName":"admin","entityId":null}],"updateTime":1524048663059,"userName":"admin","tags":[],"checkUser":null,"checkUserNick":null,"checkTime":null,"sourceType":"MAPVIEWER","createTime":1524048663059,"controlsString":"","isDefaultBottomMap":false,"status":null}
                               ''',
                               status=200)

        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
        gdf = GeoDataFrame.from_file(json_path)
        gdf['geometry'] = gdf.buffer(1)
        result = from_geodataframe_pubilsh(api, gdf, 'data', 'map', 'layer')  # type: ViewerMap
        sleep(2)
        self.assertEqual(result.title, 'map')
