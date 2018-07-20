import types
from typing import List, Callable
from enum import Enum
from io import IOBase, StringIO
from pandas import DataFrame
from iclientpy.rest.apifactory import OnlineAPIFactory
from iclientpy.rest.api.model import DataItemType, PostMyDatasItem, Layer, LayerType, SourceType, PostMapsItem, Point2D, \
    Rectangle2D, PrjCoordSys, Status, OnlineMapShareSetting, OnlineDataShareSetting, MapShareSetting, PermissionType, \
    EntityType, IportalDataAuthorizeEntity, DataPermissionType
from iclientpy.typeassert import typeassert
from IPython.display import display


class OnlineBaseLayerType(Enum):
    DEFAULT = 'DEFAULT'
    TIANDITU = 'TIANDITU'
    CHINADARK = 'CHINADARK'
    CHINALIGHT = 'CHINALIGHT'
    CHINABLUEDRAK = 'CHINABLUEDRAK'
    GOOGLE = 'GOOGLE'
    GAODE = 'GAODE'
    BING = 'BING'
    OPENSTREET = 'OPENSTREET'
    TIANDITUIMAGE = 'TIANDITUIMAGE'
    TIANDITUTERRAIN = 'TIANDITUTERRAIN'
    BAIDU = 'BAIDU'


def _online_notebook_login(username, passwd):
    import requests
    import json
    from ipywidgets import HTML, Layout
    if username is not None and passwd is not None:
        SSO_URL = 'https://sso.supermap.com/login'
        params = {'format': 'json'}
        params.update({'service': 'https://www.supermapol.com/shiro-cas'})
        session = requests.session()
        lt_res = session.get(SSO_URL, params=params, allow_redirects=False)
        params.update(json.loads(lt_res.content))
        params.update({"username": username, "password": passwd})
        ticket_res = session.post(SSO_URL, params=params, allow_redirects=False)
        if ticket_res.status_code != 302:
            raise Exception("登录失败，请确保用户名和密码输入正确")
        url = ticket_res.headers["location"]
        layout = Layout()
        layout.visibility = 'hidden'
        layout.width = '0px'
        layout.height = '0px'
        return HTML(value='<iframe src="' + url + '">', layout=layout)


class Online:
    def __init__(self, username: str = None, password: str = None):
        self._online = OnlineAPIFactory('https://www.supermapol.com', username, password)
        display(_online_notebook_login(username, password))

    @typeassert
    def search_map(self, owners: List[str] = None, tags: List[str] = None, keywords: List[str] = None):
        """
        查找地图

        Args:
            owners: 地图所有者
            tags: 地图标签
            keywords: 关键字

        Returns:
            简略的地图信息列表
        """
        ms = self._online.maps_service()
        contents = ms.get_maps(userNames=owners, tags=tags, keywords=keywords).content
        _url = self._online._base_url + "/../apps/viewer/"
        for content in contents:
            def _repr_html_(self, **kwargs):
                return "<iframe src='" + _url + str(self.id) + "' style='width: 100%; height: 600px;'/>"

            content._repr_html_ = types.MethodType(_repr_html_, content)

        return contents

    @typeassert
    def get_map(self, map_id: str):
        """
        获取指定id的地图的详细信息

        Args:
            map_id: 地图的id

        Returns:
            地图信息
        """
        ms = self._online.maps_service()
        content = ms.get_map(map_id)
        _url = self._online._base_url + "/../apps/viewer/"

        def _repr_html_(self, **kwargs):
            return "<a href='{url}' target='_blank'>到SuperMap Online查看</a><iframe src='{url}' style='width: 100%; height: 600px;'/>".format(url = _url + str(self.id))

        content._repr_html_ = types.MethodType(_repr_html_, content)
        return content

    def _monitor_upload_progress(self, data_id: str, callback: Callable = None):
        item = self.get_data(data_id)
        while (item.status != Status.OK):
            read, total = self.get_data_upload_progress(data_id)
            item = self.get_data(data_id)
            if (item.status == Status.OK and read == -1 and total == -1):
                total = 100
                read = 100
            callback(read, total)

    @typeassert
    def upload_data(self, data_name: str, data_content: IOBase, type: DataItemType, callback: Callable = None):
        """
        上传数据

        Args:
            data_name: 数据名称
            data_content: 数据流
            type: 数据类型
            callback: 上传进度回调方法

        Returns:
            数据的id
        """
        ds = self._online.datas_service()
        entity = PostMyDatasItem()
        entity.type = type
        entity.fileName = data_name
        data_id = ds.post_datas(entity).childID
        if not callback is None:
            import threading
            threading.Thread(target=self._monitor_upload_progress, args=(data_id, callback)).start()
        ds.upload_data(data_id, data_content)
        return data_id

    @typeassert
    def upload_dataframe_as_json(self, data_name: str, df: DataFrame, callback: Callable = None):
        """
        上传DataFrame为JSON类型数据

        Args:
            data_name: 上传后数据名称
            df: DataFrame数据

        """
        with StringIO(df.to_json()) as dff:
            return self.upload_data(data_name, dff, DataItemType.JSON, callback)

    @typeassert
    def search_data(self, owners: List[str] = None, tags: List[str] = None, keywords: List[str] = None):
        """
        查找数据

        Args:
            owners: 数据所有者
            tags: 数据标签
            keywords: 数据关键字

        Returns:
            数据信息的列表
        """
        ds = self._online.datas_service()
        return ds.get_datas(userNames=owners, tags=tags, keywords=keywords).content

    @typeassert
    def get_data(self, data_id: str):
        """
        获取数据详细信息

        Args:
            data_id: 数据的id

        Returns:
            数据的信息
        """
        return self._online.datas_service().get_data(data_id)

    @typeassert
    def get_data_upload_progress(self, data_id: str):
        """
        获取数据上传进度

        Args:
            data_id: 数据的id

        Returns:

        """
        process = self._online.datas_service().get_upload_process(data_id)
        return process.read, process.total

    def __prepare_base_layer(self, type: OnlineBaseLayerType):
        base_layers = []
        if type in (OnlineBaseLayerType.DEFAULT, OnlineBaseLayerType.TIANDITU):
            base_layer = Layer()
            base_layer.url = 'http://t1.tianditu.cn'
            base_layer.title = '天地图'
            base_layer.zindex = 0
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.name = '天地图'
            base_layer.isVisible = True
            base_layer.type = SourceType.TIANDITU_VEC
            base_layer_text = Layer()
            base_layer_text.url = 'http://t1.tianditu.cn'
            base_layer_text.title = '天地图-标签'
            base_layer_text.zindex = 1
            base_layer_text.layerType = LayerType.OVERLAY_LAYER
            base_layer_text.name = '天地图-标签'
            base_layer_text.isVisible = True
            base_layer_text.type = SourceType.TIANDITU_VEC
            base_layers = base_layers + [base_layer, base_layer_text]
        elif type is OnlineBaseLayerType.CHINADARK:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.prjCoordSys = PrjCoordSys()
            base_layer.prjCoordSys.epsgCode = 3857
            base_layer.type = SourceType.SUPERMAP_REST
            base_layer.title = 'China_Dark'
            base_layer.url = 'https://www.supermapol.com/proxy/iserver/services/map_China/rest/maps/China_Dark'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.CHINALIGHT:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.prjCoordSys = PrjCoordSys()
            base_layer.prjCoordSys.epsgCode = 3857
            base_layer.type = SourceType.SUPERMAP_REST
            base_layer.title = 'China_Light'
            base_layer.url = 'https://www.supermapol.com/iserver/services/map_China/rest/maps/China_Light'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.CHINABLUEDRAK:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.prjCoordSys = PrjCoordSys()
            base_layer.prjCoordSys.epsgCode = 3857
            base_layer.type = SourceType.CLOUD
            base_layer.identifier = 'blue-black'
            base_layer.title = '中国_蓝黑'
            base_layer.name = 'cloud_layername'
            base_layer.url = 'http://t3.supermapcloud.com/MapService/getGdp?&x=${x}&y=${y}&z=${z}'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.GOOGLE:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.GOOGLE
            base_layer.title = '谷歌地图'
            base_layer.name = 'google_layername'
            base_layer.identifier = 'china'
            base_layer.url = 'http://mt3.google.cn/vt/lyrs=m&hl=zh-CN&gl=cn&x=${x}&y=${y}&z=${z}&scale=${z}'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.GAODE:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.CLOUD
            base_layer.title = '高德地图'
            base_layer.name = 'cloud_layername'
            base_layer.url = 'http://t2.supermapcloud.com/FileService/image'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.BING:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.BING
            base_layer.title = '必应地图'
            base_layer.name = 'bing_layername'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.OPENSTREET:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.OSM
            base_layer.title = 'OpenStreet'
            base_layer.name = 'osm_layername'
            base_layers = base_layers + [base_layer]
        elif type is OnlineBaseLayerType.TIANDITUIMAGE:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.TIANDITU_IMG
            base_layer.title = '天地图影像'
            base_layer.name = 'tianditu_layername'
            base_layer.url = 'http://t1.tianditu.cn'
            base_layer_text = Layer()
            base_layer_text.url = 'http://t1.tianditu.cn'
            base_layer_text.title = '天地图影像_路网'
            base_layer_text.name = 'tianditu_text_name'
            base_layer_text.zindex = 1
            base_layer_text.layerType = LayerType.OVERLAY_LAYER
            base_layer_text.name = '天地图影像_路网'
            base_layer_text.isVisible = True
            base_layer_text.type = SourceType.TIANDITU_VEC
            base_layers = base_layers + [base_layer, base_layer_text]
        elif type is OnlineBaseLayerType.TIANDITUTERRAIN:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.TIANDITU_TER
            base_layer.title = '天地图地形'
            base_layer.name = 'tianditu_layername'
            base_layer.url = 'http://t1.tianditu.cn'
            base_layer_text = Layer()
            base_layer_text.url = 'http://t1.tianditu.cn'
            base_layer_text.title = '天地图地形_路网'
            base_layer_text.name = 'tianditu_text_name'
            base_layer_text.zindex = 1
            base_layer_text.layerType = LayerType.OVERLAY_LAYER
            base_layer_text.name = '天地图地形_路网'
            base_layer_text.isVisible = True
            base_layer_text.type = SourceType.TIANDITU_VEC
            base_layers = base_layers + [base_layer, base_layer_text]
        elif type is OnlineBaseLayerType.BAIDU:
            base_layer = Layer()
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.isVisible = True
            base_layer.type = SourceType.BAIDU
            base_layer.title = '百度地图'
            base_layer.name = '百度图层'
            base_layer.url = 'http://online1.map.bdimg.com'
            base_layers = base_layers + [base_layer]
        return base_layers

    @typeassert
    def create_map(self, layers: List[Layer], epsgCode: int, map_title: str, center: tuple = None, extend: tuple = None,
                   base_layer_type: OnlineBaseLayerType = OnlineBaseLayerType.DEFAULT, tags: List[str] = None):
        """
        创建地图

        Args:
            layers: 地图图层
            epsgCode: 投影编码
            map_title: 地图名称
            center: 地图中心点
            extend: 地图缩放范围
            base_layer_type: 默认底图类型
            tags: 地图标签

        Returns:
            地图的id
        """
        entity = PostMapsItem()
        if not center is None:
            entity.center = Point2D()
            entity.center.x = center[0]
            entity.center.y = center[1]
        if not extend is None:
            entity.extent = Rectangle2D()
            entity.extent.leftBottom = Point2D()
            entity.extent.leftBottom.x = extend[0]
            entity.extent.leftBottom.y = extend[1]
            entity.extent.rightTop = Point2D()
            entity.extent.rightTop.x = extend[2]
            entity.extent.rightTop.y = extend[3]
        entity.epsgCode = epsgCode
        entity.title = map_title
        entity.layers = self.__prepare_base_layer(base_layer_type) + layers
        entity.tags = tags
        return self._online.maps_service().post_maps(entity).newResourceID

    @typeassert
    def delete_map(self, map_id: str):
        """
        删除一个地图

        Args:
            map_id:地图id
        """
        self._online.maps_service().delete_maps([map_id])

    @typeassert
    def delete_maps(self, map_ids: List[str]):
        """
        删除多个地图
        Args:
            map_ids: 地图的id列表
        """
        self._online.maps_service().delete_maps(map_ids)

    @typeassert
    def delete_data(self, data_id: str):
        """
        删除一个数据

        Args:
            data_id: 数据的id
        """
        self._online.datas_service().delete_data(data_id)

    @typeassert
    def delete_datas(self, data_ids: List[str]):
        """
        批量删除多个数据
        Args:
            data_ids: 数据的id列表
        """
        for data_id in data_ids:
            self.delete_data(data_id)

    @typeassert
    def prepare_geojson_layer(self, data_id: str, layer_name: str):
        """
        根据上传到Online的geojson数据，生成Layer

        Args:
            data_id: 数据在Online中的id
            layer_name: 图层名称

        Returns:
            Layer信息
        """
        layer = Layer()
        layer.prjCoordSys = PrjCoordSys()
        layer.prjCoordSys.epsgCode = 4326
        layer.name = layer_name
        layer.layerType = LayerType.FEATURE_LAYER
        layer.isVisible = True
        layer.title = layer_name
        layer.identifier = 'THEME'
        layer.datasourceName = 'true'
        layer.cartoCSS = '{"isAddFile":true,"needTransform":"needTransform"}'
        layer.url = self._online._base_url + '/datas/' + str(data_id) + '/content.json'
        layer.themeSettings = '{"filter" : "", "vectorType": "REGION", "type" : "VECTOR"}'
        return layer

    @typeassert
    def share_data(self, data_id: str, is_public: bool):
        """
        共享数据

        Args:
            data_id: 数据id
            is_public: 是否公开
        """
        setting = OnlineDataShareSetting()
        setting.ids = [data_id]
        if is_public:
            entity = IportalDataAuthorizeEntity()
            entity.dataPermissionType = DataPermissionType.DOWNLOAD
            entity.entityType = EntityType.USER
            entity.entityName = 'GUEST'
            entity.aliasName = 'GUEST'
            setting.entities = [entity]
        else:
            setting.entities = []
        self._online.datas_service().put_sharesetting(entity=setting)

    @typeassert
    def share_map(self, map_id: str, is_public: bool):
        """
        共享地图

        Args:
            map_id: 地图id
            is_public: 是否公开
        """
        setting = OnlineMapShareSetting()
        setting.ids = [map_id]
        if is_public:
            entity = MapShareSetting()
            entity.permissionType = PermissionType.READ
            entity.entityType = EntityType.USER
            entity.entityName = 'GUEST'
            entity.aliasName = 'GUEST'
            setting.entities = [entity]
        else:
            setting.entities = []
        self._online.maps_service().put_map_sharesetting(entity=setting)
