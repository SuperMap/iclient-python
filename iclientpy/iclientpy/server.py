from typing import List, Callable
from functools import partial
from iclientpy.codingui.distributedanalyst import get_datas_with_optionms
from .rest.apifactory import APIFactory
from .rest.api.servicespage import ServicesPage, ServiceComponentType
from .codingui.servicespage import get_services_by_component_type
from .rest.api.model import ServiceMetaInfo, UserEntity, RoleEntity, RolePermissions, UserInfo, AuthorizeSetting, \
    PostAuthorizeEntity, AuthorizeType, ServiceInstance
from iclientpy.codingui.comon import NamedObjects
from iclientpy.codingui.servicepublish import PrepareWorkspacePublish, PostWorkspaceExecutor
from iclientpy.codingui.servicespage import ui_class_register


class Server:
    _apifactory: APIFactory
    _services_page: ServicesPage
    _get_bigdatas: Callable

    def __init__(self, base_url: str, username: str = None, passwd: str = None, token: str = None, proxy: str = None,
                 api_factory_clz=APIFactory):
        parms = (lambda ldict: {key: ldict[key] for key in ['base_url', 'username', 'passwd', 'token']})(locals())
        parms['proxies'] = None if proxy is None else dict.fromkeys(['http', 'https'], proxy)
        self._apifactory = api_factory_clz(**parms)
        self._services_page = self._apifactory.servicespage()
        servicelist = self._services_page.list_services()  # type: List[ServiceMetaInfo]
        bigdata_services = get_services_by_component_type(servicelist, ServiceComponentType.datacatalog,
                                                          ServiceComponentType.distributedanalysis)
        if bigdata_services[ServiceComponentType.datacatalog] is not None and bigdata_services[
            ServiceComponentType.distributedanalysis] is not None:
            datacatalog = self._apifactory.datacatalog_service(bigdata_services[ServiceComponentType.datacatalog].name)
            distributedanalysis = self._apifactory.distributedanalyst_service(
                bigdata_services[ServiceComponentType.distributedanalysis].name)
            self._get_bigdatas = partial(get_datas_with_optionms, distributedanalysis, datacatalog,
                                         self._apifactory.map_service)
        else:
            self._get_bigdatas = lambda: '服务不可用'

    @property
    def bigdatas(self):
        return self._get_bigdatas()

    @property
    def services(self):
        servicelist = self._services_page.list_services()  # type: List[ServiceMetaInfo]
        result = NamedObjects()
        for meta_info in servicelist:
            ui = ui_class_register.new_service_ui_from_meta_info(meta_info, self._apifactory)
            if ui is not None:
                result[meta_info.name] = ui
        return result

    @property
    def service_names(self) -> List[str]:
        return [meta_info.name for meta_info in self._services_page.list_services()]

    def prepare_workspace_for_publish(self):
        return PrepareWorkspacePublish(PostWorkspaceExecutor(self._apifactory), self._apifactory.management())

    def get_users(self) -> List[List[str]]:
        """
            获取用户列表

        Returns:
            用户简略信息列表
        """
        mng = self._apifactory.security_management()
        return mng.get_users()

    def get_user(self, name: str) -> UserInfo:
        """
            获取用户信息

        Args:
            name: 用户名

        Returns:
            用户详细信息
        """
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
        result = mng.put_users(names)
        if not result.succeed:
            raise Exception('删除用户失败')

    def delete_user(self, name: str):
        """
            删除用户

        Args:
            name: 用户名
        """
        mng = self._apifactory.security_management()
        result = mng.delete_user(name)
        if not result.succeed:
            raise Exception('删除用户失败')

    def get_roles(self) -> List[RoleEntity]:
        """
            获取所有角色信息

        Returns:
            角色信息列表
        """
        mng = self._apifactory.security_management()
        return mng.get_roles()

    def get_role(self, name: str) -> RoleEntity:
        """
            获取角色信息

        Args:
            name: 角色名

        Returns:
            角色信息
        """
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
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
        mng = self._apifactory.security_management()
        result = mng.delete_role(name)
        if not result.succeed:
            raise Exception('删除角色失败')

    def delete_roles(self, names: List[str]):
        """
            批量删除角色

        Args:
            names: 角色名列表
        """
        mng = self._apifactory.security_management()
        result = mng.put_roles(names)
        if not result.succeed:
            raise Exception('删除角色失败')

    def get_instances(self) -> List[ServiceInstance]:
        """
            获取所有服务实例

        Returns:
            服务实例信息列表
        """
        mng = self._apifactory.management()
        return mng.get_instances()

    def get_instance(self, instance_name: str) -> ServiceInstance:
        """
            获取服务实例

        Args:
            instance_name: 实例名称

        Returns:
            服务实例信息
        """
        mng = self._apifactory.management()
        return mng.get_instance(instance_name)

    def grant_privileges_instances(self, instances_name: List[str], authorize_type: AuthorizeType,
                                   denied_roles: List[str] = None, permitted_roles: List[str] = None):
        """
            为服务示例授权

        Args:
            instances_name: 服务实例名称列表
            authorize_type: 验证类型
            denied_roles: 禁止访问的角色列表
            permitted_roles: 允许访问的角色列表
        """
        mng = self._apifactory.management()
        entity = PostAuthorizeEntity()
        entity.instances = instances_name
        entity.authorizeSetting = AuthorizeSetting()
        entity.authorizeSetting.type = authorize_type
        entity.authorizeSetting.deniedRoles = denied_roles
        entity.authorizeSetting.permittedRoles = permitted_roles
        result = mng.post_authorize(entity)
        if not result.succeed:
            raise Exception('授权失败')

    def create_users_from_csv(self, path: str, name_key: str = 'name', password_key: str = 'password',
                              roles_key: List[str] = 'roles', description_key: str = 'description',
                              user_groups_key: List[str] = 'usergroups', sep=',', encoding: str = 'utf8'):
        """
            从csv文件里面读取用户信息，并在iServer上创建用户

        Args:
            path: csv文件路径
            name_key: 名称的列名
            password_key: 密码的列名
            roles_key: 角色的列名
            description_key: 描述的列名
            user_groups_key: 用户组的列名
            sep: csv文件的分隔符
            encoding: csv文件编码
        """
        with open(path, encoding=encoding) as csvfile:
            import csv
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get(name_key)
                password = row.get(password_key)
                roles = row.get(roles_key).split(sep)
                description = row.get(description_key)
                user_groups = row.get(user_groups_key).split(sep)
                self.create_user(name=name, password=password, roles=roles, description=description,
                                 user_groups=user_groups)
