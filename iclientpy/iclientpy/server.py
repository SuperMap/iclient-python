from typing import List, Callable
from functools import partial
from iclientpy.codingui.distributedanalyst import get_datas_with_optionms
from .rest.api.datacatalog import Datacatalog
from .rest.apifactory import APIFactory
from .rest.api.servicespage import ServicesPage,ServiceComponentType
from .codingui.servicespage import get_services_by_component_type
from .rest.api.model import ServiceMetaInfo
from .rest.api.distributedanalyst import DistributedAnalyst
from iclientpy.codingui.comon import NamedObjects
from iclientpy.codingui.servicespage import ui_class_register

class Server:
    _apifactory: APIFactory
    _services_page: ServicesPage
    _get_bigdatas: Callable

    def __init__(self, base_url: str, username: str = None, passwd: str = None, token: str = None, proxy: str = None):
        parms = (lambda ldict:{key:ldict[key] for key in ['base_url', 'username', 'passwd', 'token']})(locals())
        parms['proxies'] = None if proxy is None else dict.fromkeys(['http', 'https'], proxy)
        self._apifactory = APIFactory(**parms)
        self._services_page = self._apifactory.servicespage()
        servicelist = self._services_page.list_services()# type: List[ServiceMetaInfo]
        bigdata_services = get_services_by_component_type(servicelist, ServiceComponentType.datacatalog, ServiceComponentType.distributedanalysis)
        datacatalog = self._apifactory.datacatalog_service(bigdata_services[ServiceComponentType.datacatalog].name)
        distributedanalysis = self._apifactory.distributedanalyst_service(bigdata_services[ServiceComponentType.distributedanalysis].name)
        self._get_bigdatas = partial(get_datas_with_optionms, distributedanalysis, datacatalog, self._apifactory.map_service)

    @property
    def bigdatas(self):
        return self._get_bigdatas()

    @property
    def services(self):
        servicelist = self._services_page.list_services()  # type: List[ServiceMetaInfo]
        result = NamedObjects()
        for meta_info in servicelist:
            ui = ui_class_register.new_service_ui(meta_info, self._apifactory)
            if ui is not None:
                result[meta_info.name.replace('/', '_')] = ui
        return result
