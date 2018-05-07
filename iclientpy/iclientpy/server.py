from typing import List
from iclientpy.codingui.distributedanalyst import get_datas_with_optionms
from .rest.api.datacatalog import Datacatalog
from .rest.apifactory import APIFactory
from .rest.api.servicespage import ServicesPage,ServiceComponentType
from .codingui.servicespage import get_services_by_component_type
from .rest.api.model import ServiceMetaInfo
from .rest.api.distributedanalyst import DistributedAnalyst

class Server:
    _datacatalog: Datacatalog
    _apifactory: APIFactory
    _services_page: ServicesPage
    _distributedanalysis: DistributedAnalyst
    def __init__(self, base_url: str, username: str = None, passwd: str = None, token: str = None, proxy: str = None):
        parms = (lambda ldict:{key:ldict[key] for key in ['base_url', 'username', 'passwd', 'token']})(locals())
        parms['proxies'] = None if proxy is None else dict.fromkeys(['http', 'https'], proxy)
        self._apifactory = APIFactory(**parms)
        self._services_page = self._apifactory.servicespage()
        servicelist = self._services_page.list_services()# type: List[ServiceMetaInfo]
        bigdata_services = get_services_by_component_type(servicelist, ServiceComponentType.datacatalog, ServiceComponentType.distributedanalysis)
        self._datacatalog = self._apifactory.datacatalog_service(bigdata_services[ServiceComponentType.datacatalog].name)
        self._distributedanalysis = self._apifactory.distributedanalyst_service(bigdata_services[ServiceComponentType.distributedanalysis].name)


    @property
    def bigdatas(self):
        return get_datas_with_optionms(self._distributedanalysis, self._datacatalog, self._apifactory.map_service)
