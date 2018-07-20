import types
from typing import List, Callable
from enum import Enum
from io import IOBase, StringIO
from pandas import DataFrame
from iclientpy.rest.apifactory import iPortalAPIFactory
from iclientpy.rest.api.model import DataItemType, PostMyDatasItem, Layer, LayerType, SourceType, PostMapsItem, Point2D, \
    Rectangle2D, PrjCoordSys, MapShareSetting, PermissionType, EntityType, IportalDataAuthorizeEntity, \
    DataPermissionType, Status, RoleEntity, UserInfo, UserEntity, RolePermissions
from iclientpy.typeassert import typeassert


class BaseLayerType(Enum):
    DEFAULT = 'DEFAULT'
    TIANDITU = 'TIANDITU'


class Portal:
    def __init__(self, url, username: str = None, password: str = None, token: str = None):
        self._portal = iPortalAPIFactory(url, username, password, token)

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
        ms = self._portal.maps_service()
        contents = ms.get_maps(userNames=owners, tags=tags, keywords=keywords).content

        _url = self._portal._base_url + "/../apps/viewer/"
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
        ms = self._portal.maps_service()
        content = ms.get_map(map_id)

        _url = self._portal._base_url + "/../apps/viewer/"

        def _repr_html_(self, **kwargs):
            return "<iframe src='" + _url + str(self.id) + "' style='width: 100%; height: 600px;'/>"

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
        ds = self._portal.datas_service()
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
        ds = self._portal.datas_service()
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
        return self._portal.datas_service().get_data(data_id)

    @typeassert
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

    @typeassert
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

    @typeassert
    def delete_map(self, map_id: str):
        """
        删除一个地图

        Args:
            map_id:地图id
        """
        self._portal.maps_service().delete_maps([map_id])

    @typeassert
    def delete_maps(self, map_ids: List[str]):
        """
        删除多个地图
        Args:
            map_ids: 地图的id列表
        """
        self._portal.maps_service().delete_maps(map_ids)

    @typeassert
    def delete_data(self, data_id: str):
        """
        删除一个数据

        Args:
            data_id: 数据的id
        """
        self._portal.datas_service().delete_data(data_id)

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

    @typeassert
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

    @typeassert
    def get_data_sharesetting(self, data_id: str):
        """
        获取数据的共享权限

        Args:
            data_id: 数据的id

        Returns:
            数据的共享权限
        """
        ds = self._portal.datas_service()
        return ds.get_data_sharesetting(data_id)

    @typeassert
    def config_data_sharesetting(self, data_id, entities: List[IportalDataAuthorizeEntity]):
        """
        设置数据的共享权限

        Args:
            data_id: 数据的id
            entities: 共享权限的列表

        Returns:

        """
        ds = self._portal.datas_service()
        if not ds.put_data_sharesetting(data_id, entities).succeed:
            raise Exception('更新权限失败')

    @typeassert
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

    @typeassert
    def config_map_sharesetting(self, map_id: str, entities: List[MapShareSetting]):
        """
        设置地图的共享权限

        Args:
            map_id: 地图的id
            entities: 共享权限的列表

        """
        maps = self._portal.maps_service()
        if not maps.put_map_sharesetting(map_id, entities).succeed:
            raise Exception('更新权限失败')

    def get_users(self) -> List[List[str]]:
        """
            获取用户列表

        Returns:
            用户简略信息列表
        """
        mng = self._portal.security_management()
        return mng.get_users()

    def get_user(self, name: str) -> UserInfo:
        """
            获取用户信息

        Args:
            name: 用户名

        Returns:
            用户详细信息
        """
        mng = self._portal.security_management()
        return mng.get_user(name)

    def create_user(self, name: str, password: str, roles: List[str] = None, description: str = None,
                    user_groups: List[str] = None):
        """
            创建用户

        Args:
            name: 用户名
            password: 密码
            roles: 角色
            description: 描述信息
            user_groups: 用户组
        """
        mng = self._portal.security_management()
        entity = UserEntity()
        entity.name = name
        entity.password = password
        entity.roles = roles
        entity.description = description
        entity.userGroups = user_groups
        result = mng.post_users(entity)
        if not result.succeed:
            raise Exception('创建用户失败')

    def update_user(self, name: str, password: str = None, roles: List[str] = None, description: str = None,
                    user_groups: List[str] = None):
        """
            更新用户信息

        Args:
            name: 用户名
            password: 密码
            roles: 角色
            description: 描述信息
            user_groups: 用户组
        """
        mng = self._portal.security_management()
        entity = mng.get_user(name)
        entity.password = password if password is not None else entity.password
        entity.roles = roles if roles is not None else entity.roles
        entity.description = description if description is not None else entity.description
        entity.userGroups = user_groups if user_groups is not None else entity.userGroups
        result = mng.put_user(name, entity)
        if not result.succeed:
            raise Exception('更新用户失败')

    def delete_users(self, names: List[str]):
        """
            批量删除用户

        Args:
            names: 用户名列表
        """
        mng = self._portal.security_management()
        result = mng.put_users(names)
        if not result.succeed:
            raise Exception('删除用户失败')

    def delete_user(self, name: str):
        """
            删除用户

        Args:
            name: 用户名
        """
        mng = self._portal.security_management()
        result = mng.delete_user(name)
        if not result.succeed:
            raise Exception('删除用户失败')

    def get_roles(self) -> List[RoleEntity]:
        """
            获取所有角色信息

        Returns:
            角色信息列表
        """
        mng = self._portal.security_management()
        return mng.get_roles()

    def get_role(self, name: str) -> RoleEntity:
        """
            获取角色信息

        Args:
            name: 角色名

        Returns:
            角色信息
        """
        mng = self._portal.security_management()
        return mng.get_role(name)

    def create_role(self, name: str, users: List[str] = None, description: str = None, user_groups: List[str] = None,
                    permissions: RolePermissions = None):
        """
            创建角色

        Args:
            name: 角色名
            users: 用户
            description: 描述信息
            user_groups: 用户组
            permissions: 权限
        """
        mng = self._portal.security_management()
        entity = RoleEntity()
        entity.name = name
        entity.userGroups = user_groups
        entity.description = description
        entity.premissions = permissions
        entity.users = users
        result = mng.post_roles(entity)
        if not result.succeed:
            raise Exception('创建角色失败')

    def update_role(self, name: str, users: List[str] = None, description: str = None, user_groups: List[str] = None,
                    permissions: RolePermissions = None):
        """
            更新角色

        Args:
            name: 角色名
            users: 用户
            description: 描述信息
            user_groups: 用户组
            permissions: 权限
        """
        mng = self._portal.security_management()
        entity = mng.get_role(name)
        entity.userGroups = user_groups if user_groups is not None else entity.userGroups
        entity.description = description if description is not None else entity.description
        entity.premissions = permissions if permissions is not None else entity.premissions
        entity.users = users if users is not None else entity.users
        result = mng.put_role(name, entity)
        if not result.succeed:
            raise Exception('更新角色失败')

    def delete_role(self, name: str):
        """
            删除角色

        Args:
            name: 角色名
        """
        mng = self._portal.security_management()
        result = mng.delete_role(name)
        if not result.succeed:
            raise Exception('删除角色失败')

    def delete_roles(self, names: List[str]):
        """
            批量删除角色

        Args:
            names: 角色名列表
        """
        mng = self._portal.security_management()
        result = mng.put_roles(names)
        if not result.succeed:
            raise Exception('删除角色失败')


class MapShareSettingBuilder:
    def __init__(self, settings: List[MapShareSetting] = None):
        self._settings = [] if settings is None else settings

    @typeassert
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

    @typeassert
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

    @typeassert
    def share_to_group(self, group_id: int, type: PermissionType):
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

    @typeassert
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

    @typeassert
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

    @typeassert
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

    @typeassert
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

    @typeassert
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

    @typeassert
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

    @typeassert
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

    @typeassert
    def build(self):
        """
        获得共享信息列表

        Returns:
            共享信息列表
        """
        return self._settings
