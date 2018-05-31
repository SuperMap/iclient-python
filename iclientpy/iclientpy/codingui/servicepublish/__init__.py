import json
from functools import partial
from typing import List, Callable, Any
from iclientpy.dtojson import to_json_str
from iclientpy.codingui.comon import NamedObjects
from iclientpy.rest.api.model import PostWorkspaceParameter, ServiceType
from iclientpy.rest.api.management import Management
from .remotefilebrowser import RemoteFileBrowser, File


class PrepareWorkspacePublish:
    _post_entity: PostWorkspaceParameter
    _service_types_options: NamedObjects
    _executor: Callable[[PostWorkspaceParameter], Any]
    _workspace_info: List[str]
    _mng: Management

    def __init__(self, post_workspace: Callable, mng: Management):
        self._post_entity = PostWorkspaceParameter()
        self._post_entity.servicesTypes = []
        self._service_types_options = NamedObjects()
        self._init_servicetype([ServiceType.RESTMAP, ServiceType.RESTDATA])
        self._executor = post_workspace
        self._workspace_info = []
        self._mng = mng

    def _attach_file_explorer(self, file_workspace):
        class SelectableFile(File):
            def select(self_file):
                file_workspace.set_path(self_file.path)
        file_workspace.get_file_explorer = lambda : RemoteFileBrowser(mng=self._mng,file_clz=SelectableFile)

    def use_file_workspace(self):
        self._clear_workspace_info()
        workspace = NamedObjects()
        workspace['set_path'] = partial(self._add_workspace_info)
        setattr(self, 'workspace', workspace)
        self._attach_file_explorer(workspace)
        return self

    def use_file_workspace_with_password(self):
        self._clear_workspace_info()
        file_workspace = NamedObjects()
        file_workspace['set_path'] = partial(self._add_workspace_info_kv, 'server')
        file_workspace['set_password'] = partial(self._add_workspace_info_kv, 'password')
        self._attach_file_explorer(file_workspace)
        setattr(self, 'workspace', file_workspace)
        return self

    def use_oracle_workspace(self):
        self._clear_workspace_info()
        workspace = NamedObjects()
        self._add_workspace_info_kv('type', 'ORACLE')
        workspace['set_server_name'] = partial(self._add_workspace_info_kv, 'server')
        workspace['set_workspace_name'] = partial(self._add_workspace_info_kv, 'name')
        workspace['set_database_name'] = partial(self._add_workspace_info_kv, 'database')
        workspace['set_username'] = partial(self._add_workspace_info_kv, 'username')
        workspace['set_password'] = partial(self._add_workspace_info_kv, 'password')
        setattr(self, 'workspace', workspace)
        return self

    def use_sql_workspace(self):
        self._clear_workspace_info()
        workspace = NamedObjects()
        self._add_workspace_info_kv('type', 'SQL')
        workspace['set_server_name'] = partial(self._add_workspace_info_kv, 'server')
        workspace['set_workspace_name'] = partial(self._add_workspace_info_kv, 'name')
        workspace['set_database_name'] = partial(self._add_workspace_info_kv, 'database')
        workspace['set_username'] = partial(self._add_workspace_info_kv, 'username')
        workspace['set_password'] = partial(self._add_workspace_info_kv, 'password')
        workspace['set_driver'] = partial(self._add_workspace_info_kv, 'driver')
        setattr(self, 'workspace', workspace)
        return self

    def use_pgsql_workspace(self):
        self._clear_workspace_info()
        workspace = NamedObjects()
        self._add_workspace_info_kv('type', 'PGSQL')
        workspace['set_server_name'] = partial(self._add_workspace_info_kv, 'server')
        workspace['set_workspace_name'] = partial(self._add_workspace_info_kv, 'name')
        workspace['set_database_name'] = partial(self._add_workspace_info_kv, 'database')
        workspace['set_username'] = partial(self._add_workspace_info_kv, 'username')
        workspace['set_password'] = partial(self._add_workspace_info_kv, 'password')
        workspace['set_driver'] = partial(self._add_workspace_info_kv, 'driver')
        setattr(self, 'workspace', workspace)
        return self

    def _add_workspace_info(self, info: str):
        self._workspace_info.append(info)
        return self

    def _add_workspace_info_kv(self, key, value):
        self._workspace_info.append(key + '=' + value)
        return self

    def _clear_workspace_info(self):
        self._workspace_info = []

    def allow_edit(self):
        self._post_entity.isDataEditable = True
        return self

    def disallow_edit(self):
        self._post_entity.isDataEditable = False
        return self

    def _service_type_select(self, type: ServiceType):
        if type not in self._post_entity.servicesTypes:
            self._post_entity.servicesTypes.append(type)
        return self

    def _service_type_remove(self, type: ServiceType):
        if type in self._post_entity.servicesTypes:
            self._post_entity.servicesTypes.remove(type)
        return self

    def _init_servicetype(self, servicestypes: List[ServiceType]):
        for type in servicestypes:
            type_name_objects = NamedObjects()
            type_name_objects["select"] = partial(self._service_type_select, type)
            type_name_objects["remove"] = partial(self._service_type_remove, type)
            self._service_types_options[type.value] = type_name_objects

    @property
    def avaliable_service_types(self):
        return self._service_types_options

    def __repr__(self):
        self._post_entity.workspaceConnectionInfo = ';'.join(self._workspace_info)
        return json.dumps(json.loads(to_json_str(self._post_entity)), indent=2, sort_keys=True)

    def execute(self):
        self._post_entity.workspaceConnectionInfo = ';'.join(self._workspace_info)
        return self._executor(self._post_entity)


from iclientpy.rest.api.management import Management, PostWorkspaceResultItem
from iclientpy.rest.apifactory import APIFactory
from ..servicespage import ui_class_register


class PostWorkspaceExecutor:
    _management: Management
    _api_factory: APIFactory

    def __init__(self, api_factory: APIFactory):
        self._management = api_factory.management()
        self._api_factory = api_factory

    def __call__(self, param: PostWorkspaceParameter):
        post_result = self._management.post_workspaces(param)  # type:List[PostWorkspaceResultItem]
        result = NamedObjects()
        for item in post_result:
            service_addr = item.serviceAddress
            service_name = service_addr[
                           service_addr.rfind('/services/') + len('/services/'):]
            result[service_name] = ui_class_register.new_service_ui_from_service_type(service_name=service_name, service_type=item.serviceType, api_factory=self._api_factory)
        return result
