from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.server import Server
from iclientpy.rest.api.servicespage import ServiceComponentType, ServiceMetaInfo


class ServerTest(TestCase):

    def test_no_bigdata_services(self):
        services_page = MagicMock()
        services_page.list_services = MagicMock(return_value=[])
        api_factory = MagicMock()
        api_factory.servicespage = MagicMock(return_value=services_page)
        mocked_factory_clz = MagicMock(return_value=api_factory)
        Server(api_factory_clz=mocked_factory_clz, base_url='http://localhost:8090/iserver')  # 不抛出异常就算过

        meta_info = ServiceMetaInfo()
        meta_info.componentType = ServiceComponentType.datacatalog.value
        services_page.list_services.return_value = [meta_info]
        Server(api_factory_clz=mocked_factory_clz, base_url='http://localhost:8090/iserver')  # 不抛出异常就算过

