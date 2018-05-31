from typing import List, Callable
from functools import partial
from iclientpy.codingui.distributedanalyst import get_datas_with_optionms
from .rest.apifactory import APIFactory
from .rest.api.servicespage import ServicesPage, ServiceComponentType
from .codingui.servicespage import get_services_by_component_type
from .rest.api.model import ServiceMetaInfo
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
