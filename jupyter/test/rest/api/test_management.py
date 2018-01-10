import httpretty
from iclientpy.rest.api.management import *
from iclientpy.rest.decorator import HttpMethod
from .abstractrest import AbstractRESTTestCase


class ManagementTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, "management")

    def test_workspace(self):
        param = PostWorkspaceParameter()
        param.workspaceConnectionInfo = 'World.sxwu'
        param.servicesTypes = [ServiceType.RESTMAP]
        self.check_api('post_workspaces', self.baseuri + "/manager/workspaces.json", HttpMethod.POST,
                       httpretty.Response(body='[{"serviceType": "RESTMAP", "serviceAddress": "123"}]', status=201),
                       param=param)

        self.check_api('get_workspaces', self.baseuri + "/manager/workspaces.json", HttpMethod.GET,
                       httpretty.Response(
                           body='[{"address": "/etc/icloud/World/World.sxwu","enabled": true,"name": "World.sxwu","serviceName": "map-World/rest","serviceType": "MapService"}]',
                           status=201),
                       param=param)
