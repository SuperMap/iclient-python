import httpretty
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.model import PostTokenParameter, ClientType
from iclientpy.rest.api.securityservice import SecurityService
from .abstractrest import AbstractRESTTestCase


class SecurityServiceTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, APIFactory.security_service)

    def test_post_tokens(self):
        param = PostTokenParameter()
        param.userName = 'admin'
        param.password = 'iserver'
        param.clientType = ClientType.RequestIP
        param.expiration = 60
        self.check_api(SecurityService.post_tokens, self.baseuri + "/services/security/tokens.json", HttpMethod.POST,
                       httpretty.Response(status=200, body="tokenstrtokenstr"), entity=param)
