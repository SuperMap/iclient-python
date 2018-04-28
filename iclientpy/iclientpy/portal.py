from typing import List, Callable
from enum import Enum
from io import FileIO, StringIO
from pandas import DataFrame
from iclientpy.rest.apifactory import iPortalAPIFactory
from iclientpy.rest.api.model import DataItemType, PostMyDatasItem, Layer, LayerType, SourceType, PostMapsItem, Point2D, \
    Rectangle2D, PrjCoordSys, MapShareSetting, PermissionType, EntityType, IportalDataAuthorizeEntity, \
    DataPermissionType, Status


class BaseLayerType(Enum):
    DEFAULT = 'DEFAULT'
    TIANDITU = 'TIANDITU'


class Portal:
    def __init__(self, url, username: str = None, password: str = None, token: str = None):
        self._portal = iPortalAPIFactory(url, username, password, token)

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
        ms = self._portal.maps_service()
        return ms.get_maps(userNames=owners, tags=tags, keywords=keywords).content

    def get_map(self, map_id: str):
        """
        获取指定id的地图的详细信息
        Args:
            map_id: 地图的id

        Returns:
            地图信息
        """
        ms = self._portal.maps_service()
        return ms.get_map(map_id)

    def _monitor_upload_progress(self, data_id: str, callback: Callable = None):
        item = self.get_data(data_id)
        while (item.status != Status.OK):
            read, total = self.get_data_upload_progress(data_id)
            item = self.get_data(data_id)
            if (item.status == Status.OK and read == -1 and total == -1):
                total = 100
                read = 100
            callback(read, total)

    def upload_data(self, data_name: str, data_content: FileIO, type: DataItemType, callback: Callable = None):
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
        ds = self._portal.datas_service()
        entity = PostMyDatasItem()
        entity.type = type
        entity.fileName = data_name
        data_id = ds.post_my_datas(entity).childID
        if not callback is None:
            import threading
            threading.Thread(target=self._monitor_upload_progress, args=(data_id, callback)).start()
        ds.upload_my_data(data_id, data_content)
        return data_id

    def upload_dataframe_as_json(self, data_name: str, df: DataFrame, callback: Callable = None):
        """
        上传DataFrame为JSON类型数据
        Args:
            data_name: 上传后数据名称
            df: DataFrame数据

        Returns:

        """
        with StringIO(df.to_json()) as dff:
            return self.upload_data(data_name, dff, DataItemType.JSON, callback)

    def get_data(self, data_id: str):
        """
        获取数据详细信息
        Args:
            data_id: 数据的id

        Returns:
            数据的信息
        """
        return self._portal.datas_service().get_my_data(data_id)

    def get_data_upload_progress(self, data_id: str):
        """
        获取数据上传进度
        Args:
            data_id: 数据的id

        Returns:

        """
        process = self._portal.datas_service().get_upload_process(data_id)
        return process.read, process.total

    def __prepare_base_layer(self, type: BaseLayerType):
        base_layers = []
        if type in (BaseLayerType.DEFAULT, BaseLayerType.TIANDITU):
            base_layer = Layer()
            base_layer.url = 'http://t1.tianditu.cn'
            base_layer.title = '天地图'
            base_layer.zindex = 0
            base_layer.layerType = LayerType.BASE_LAYER
            base_layer.name = '天地图'
            base_layer.isVisible = True
            base_layer.type = SourceType.TIANDITU_VEC
            base_layer_label = Layer()
            base_layer_label.url = 'http://t1.tianditu.cn'
            base_layer_label.title = '天地图-标签'
            base_layer_label.zindex = 1
            base_layer_label.layerType = LayerType.OVERLAY_LAYER
            base_layer_label.name = '天地图-标签'
            base_layer_label.isVisible = True
            base_layer_label.type = SourceType.TIANDITU_VEC
            base_layers = base_layers + [base_layer, base_layer_label]
        return base_layers

    def create_map(self, layers: List[Layer], epsgCode: int, map_title: str, center: tuple = None, extend: tuple = None,
                   base_layer_type: BaseLayerType = BaseLayerType.DEFAULT, tags: List[str] = None):
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
        return self._portal.maps_service().post_maps(entity).newResourceID

    def prepare_geojson_layer(self, data_id: str, layer_name: str):
        """
        根据上传到iportal的geojson数据，生成Layer
        Args:
            data_id: 数据在iPortal中的id
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
        layer.url = self._portal._base_url + '/datas/' + str(data_id) + '/content.json'
        layer.themeSettings = '{"filter" : "", "vectorType": "REGION", "type" : "VECTOR"}'
        return layer

    def search_group(self, owners: List[str] = None, tags: List[str] = None, keywords: List[str] = None):
        """
        查找群组
        Args:
            owners: 群组创建者
            tags: 群组标签
            keywords: 群组关键字

        Returns:
            群组基本信息
        """
        return self._portal.groups_service().get_groups(tags=tags, userNames=owners, keywords=keywords).content;

    def get_data_sharesetting(self, data_id: str):
        """
        获取数据的共享权限
        Args:
            data_id: 数据的id

        Returns:
            数据的共享权限
        """
        ds = self._portal.datas_service()
        return ds.get_my_data_sharesetting(data_id)

    def config_data_sharesetting(self, data_id, entities: List[IportalDataAuthorizeEntity]):
        """
        设置数据的共享权限
        Args:
            data_id: 数据的id
            entities: 共享权限的列表

        Returns:

        """
        ds = self._portal.datas_service()
        if not ds.put_my_data_sharesetting(data_id, entities).succeed:
            raise Exception('更新权限失败')

    def get_map_sharesetting(self, map_id: str):
        """
        返回地图的共享权限
        Args:
            map_id: 地图的id

        Returns:
            地图的共享权限
        """
        maps = self._portal.maps_service()
        return maps.get_map_sharesetting(map_id)

    def config_map_sharesetting(self, map_id: str, entities: List[MapShareSetting]):
        """
        设置地图的共享权限
        Args:
            map_id: 地图的id
            entities: 共享权限的列表

        Returns:

        """
        maps = self._portal.maps_service()
        if not maps.put_map_sharesetting(map_id, entities).succeed:
            raise Exception('更新权限失败')


class MapShareSettingBuilder:
    def __init__(self, settings: List[MapShareSetting] = None):
        self._settings = [] if settings is None else settings

    def share_to_user(self, user_name: str, type: PermissionType):
        """
        共享地图给指定用户
        Args:
            user_name: 用户名
            type: 共享权限

        Returns:

        """
        entity = MapShareSetting()
        entity.permissionType = type.value
        entity.entityType = EntityType.USER
        entity.entityName = user_name
        self._settings.append(entity)
        return self

    def share_to_users(self, user_names: List[str], type: PermissionType):
        """
        共享地图给多个用户
        Args:
            user_names: 用户名列表
            type: 共享权限

        Returns:

        """
        for user_name in user_names:
            self.share_to_user(user_name, type)
        return self

    def share_to_group(self, group_id: str, type: PermissionType):
        """
        共享地图给群组
        Args:
            group_id: 群组的id
            type: 共享权限

        Returns:

        """
        entity = MapShareSetting()
        entity.permissionType = type.value
        entity.entityType = EntityType.IPORTALGROUP
        entity.entityId = group_id
        self._settings.append(entity)
        return self

    def share_to_department(self, department_id: str, type: PermissionType):
        """
        共享地图给指定组织
        Args:
            department_id: 组织的id
            type: 共享权限

        Returns:

        """
        entity = MapShareSetting()
        entity.permissionType = type.value
        entity.entityType = EntityType.DEPARTMENT
        entity.entityId = department_id
        self._settings.append(entity)
        return self

    def share_to_everyone(self, type: PermissionType):
        """
        共享地图给所有人
        Args:
            type: 共享权限

        Returns:

        """
        entity = MapShareSetting()
        entity.permissionType = type.value
        entity.entityType = EntityType.USER
        entity.entityName = 'GUEST'
        entity.aliasName = 'GUEST'
        self._settings.append(entity)
        return self

    def build(self):
        """
        获得共享信息列表
        Returns:
            共享信息列表
        """
        return self._settings


class DataShareSettingBuilder:
    def __init__(self, settings: List[IportalDataAuthorizeEntity] = None):
        self._settings = [] if settings is None else settings

    def share_to_user(self, user_name: str, type: DataPermissionType):
        """
        共享数据给指定用户
        Args:
            user_name: 用户名
            type: 共享权限

        Returns:

        """
        entity = IportalDataAuthorizeEntity()
        entity.dataPermissionType = type.value
        entity.entityType = EntityType.USER
        entity.entityName = user_name
        self._settings.append(entity)
        return self

    def share_to_users(self, user_names: List[str], type: DataPermissionType):
        """
        共享数据给多个用户
        Args:
            user_names: 用户列表
            type: 共享权限

        Returns:

        """
        for user_name in user_names:
            self.share_to_user(user_name, type)
        return self

    def share_to_group(self, group_id: str, type: DataPermissionType):
        """
        共享数据给群组
        Args:
            group_id: 群组的id
            type: 共享权限

        Returns:

        """
        entity = IportalDataAuthorizeEntity()
        entity.dataPermissionType = type.value
        entity.entityType = EntityType.IPORTALGROUP
        entity.entityId = group_id
        self._settings.append(entity)
        return self

    def share_to_everyone(self, type: DataPermissionType):
        """
        共享数据给所有人
        Args:
            type: 共享权限

        Returns:

        """
        entity = IportalDataAuthorizeEntity()
        entity.dataPermissionType = type.value
        entity.entityType = EntityType.USER
        entity.entityName = 'GUEST'
        entity.aliasName = 'GUEST'
        self._settings.append(entity)
        return self

    def build(self):
        """
        获得共享信息列表
        Returns:
            共享信息列表
        """
        return self._settings
