from .abstractrest import AbstractRESTTestCase
import httpretty
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.mapsservice import MapsService
from iclientpy.rest.api.model import *


class MapsServiceTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls, 'http://www.supermapol.com', 'test', 'test')
        cls.init_online_apifactory(cls)
        cls.init_api(cls, "maps_service")

    def test_maps(self):
        get_body = '{"total":1,"totalPage":1,"pageSize":9,"searchParameter":{"orderType":"ASC","updateEnd":-1,"keywords":null,"sourceTypes":null,"orderBy":null,"pageSize":9,"dirIds":null,"filterFields":null,"departmentIds":null,"mapStatus":null,"checkStatus":null,"epsgCode":null,"createEnd":-1,"groupIds":null,"permitInstances":null,"resourceIds":null,"visitEnd":-1,"excludeIds":null,"returnSubDir":null,"isNotInDir":null,"suggest":null,"visitStart":-1,"createStart":-1,"tags":null,"updateStart":-1,"currentUser":null,"unique":null,"userNames":["admin"],"currentPage":1},"currentPage":1,"content":[{"extent":null,"controls":null,"extentString":"","description":"123","verifyReason":null,"units":null,"title":"test123","resolution":0,"checkStatus":"SUCCESSFUL","visitCount":3,"centerString":"{\"x\":1.2626762220726E7,\"y\":2619886.8435466}","epsgCode":3857,"nickname":"admin","layers":[{"wmtsOption":null,"styleString":"null","title":"天地图","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":null,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"BASE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":null,"scalesString":"null","scales":null,"name":null,"bounds":null,"mapId":null,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"天地图","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":null,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"OVERLAY_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":null,"scalesString":"null","scales":null,"name":null,"bounds":null,"mapId":null,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"test","type":null,"subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":null,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"FEATURE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://localhost:8090/iportal/services/../web/datas/18220636/content.json","zindex":null,"scalesString":"null","scales":null,"name":null,"bounds":null,"mapId":null,"style":null,"markersString":"null","opacity":1,"markers":null}],"id":283390367,"searchSetting":null,"thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","level":null,"center":{"x":1.2626762220726E7,"y":2619886.8435466},"authorizeSetting":[{"permissionType":"DELETE","aliasName":"admin","entityRoles":["ADMIN","SYSTEM"],"entityType":"USER","entityName":"admin","entityId":null}],"updateTime":1523950707525,"userName":"admin","tags":null,"checkUser":null,"checkUserNick":null,"checkTime":null,"sourceType":"MAPVIEWER","createTime":1523950707525,"controlsString":"","isDefaultBottomMap":false,"status":null}]}'
        self.check_api(MapsService.get_maps, self.baseuri + "/web/maps.json", HttpMethod.GET,
                       httpretty.Response(body=get_body, status=201))
        entity = PostMapsItem()
        entity.center = Point2D()
        entity.center.x = 12626762.220726
        entity.center.y = 2619886.8435466
        entity.epsgCode = 3857
        entity.description = '123'
        baseLayer = Layer()
        baseLayer.url = 'http://t1.tianditu.cn'
        baseLayer.title = '天地图'
        baseLayer.zindex = 0
        baseLayer.layerType = LayerType.BASE_LAYER
        baseLayer.name = 'tianditu'
        baseLayer.isVisible = True
        baseLayer.type = SourceType.TIANDITU_VEC
        base_Layer = Layer()
        base_Layer.url = 'http://t1.tianditu.cn'
        base_Layer.title = '天地图'
        base_Layer.zindex = 1
        base_Layer.layerType = LayerType.OVERLAY_LAYER
        base_Layer.name = 'tianditu'
        base_Layer.isVisible = True
        base_Layer.type = SourceType.TIANDITU_VEC
        layer = Layer()
        layer.prjCoordSys = PrjCoordSys()
        layer.prjCoordSys.epsgCode = 4326
        layer.name = 'test'
        layer.layerType = LayerType.FEATURE_LAYER
        layer.zindex = 2
        layer.isVisible = True
        layer.title = "test"
        layer.cartoCSS = '{"isAddFile":true,"needTransform":"needTransform"}'
        layer.url = 'http://localhost:8090/iportal/web/datas/18220636/content.json'
        entity.layers = [baseLayer, base_Layer, layer]
        entity.title = 'test123'
        self.check_api(MapsService.post_maps, self.baseuri + "/web/maps.json", HttpMethod.POST,
                       httpretty.Response(
                           body='{"succeed":true,"newResourceID":"24","newResourceLocation":"http://localhost:8090/iportal/web/maps/24"}',
                           status=201), entity=entity)
        self.check_api(MapsService.delete_maps, self.baseuri + "/web/maps.json", HttpMethod.DELETE,
                       httpretty.Response(body='{"succeed":true', status=201), ids=['283390367'])

    def test_map(self):
        map_id = '283390367'
        get_body = '{"extent":null,"controls":null,"extentString":"","description":"123","verifyReason":null,"units":null,"title":"test_liu123","resolution":0,"checkStatus":"SUCCESSFUL","visitCount":4,"centerString":"{\"x\":1.2626762220726E7,\"y\":2619886.8435466}","epsgCode":3857,"nickname":"admin","layers":[{"wmtsOption":null,"styleString":"null","title":"天地图","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":87,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"BASE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":0,"scalesString":"null","scales":null,"name":"tianditu","bounds":null,"mapId":283390367,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"天地图","type":"TIANDITU_VEC","subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":null,"id":88,"cartoCSS":null,"datasourceName":null,"prjCoordSysString":"null","identifier":null,"layerType":"OVERLAY_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://t1.tianditu.cn","zindex":1,"scalesString":"null","scales":null,"name":"tianditu","bounds":null,"mapId":283390367,"style":null,"markersString":"null","opacity":1,"markers":null},{"wmtsOption":null,"styleString":"null","title":"test_liu","type":null,"subLayersString":"null","WMTSOptionString":"null","features":null,"boundsString":"null","prjCoordSys":{"distanceUnit":null,"projectionParam":null,"epsgCode":4326,"coordUnit":null,"name":null,"projection":null,"type":"PCS_USER_DEFINED","coordSystem":null},"id":89,"cartoCSS":"{\"isAddFile\":true,\"needTransform\":\"needTransform\"}","datasourceName":null,"prjCoordSysString":"{\"distanceUnit\":null,\"projectionParam\":null,\"epsgCode\":4326,\"coordUnit\":null,\"name\":null,\"projection\":null,\"type\":\"PCS_USER_DEFINED\",\"coordSystem\":null}","identifier":null,"layerType":"FEATURE_LAYER","featuresString":"null","WMTSOption":null,"themeSettings":null,"isVisible":true,"subLayers":null,"url":"http://localhost:8090/iportal/services/../web/datas/18220636/content.json","zindex":2,"scalesString":"null","scales":null,"name":"test_liu","bounds":null,"mapId":283390367,"style":null,"markersString":"null","opacity":1,"markers":null}],"id":283390367,"searchSetting":null,"thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","level":null,"center":{"x":1.2626762220726E7,"y":2619886.8435466},"authorizeSetting":[{"permissionType":"DELETE","aliasName":"admin","entityRoles":["ADMIN","SYSTEM"],"entityType":"USER","entityName":"admin","entityId":null}],"updateTime":1523950707525,"userName":"admin","tags":[],"checkUser":null,"checkUserNick":null,"checkTime":null,"sourceType":"MAPVIEWER","createTime":1523950707525,"controlsString":"","isDefaultBottomMap":false,"status":null}'
        self.check_api(MapsService.get_map, self.baseuri + "/web/maps/283390367.json", HttpMethod.GET,
                       httpretty.Response(body=get_body, status=201), map_id=map_id)
