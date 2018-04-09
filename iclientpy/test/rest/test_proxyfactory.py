from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.rest.proxyfactory import *
from iclientpy.rest.decorator import rest,HttpMethod

class SomeService:
    @rest(HttpMethod.GET, "someapi")
    def someapi(self):
        pass

class TestProxyFactory(TestCase):

    def test(self):
        handler = RestInvocationHandler();
        handler.handle_rest_invocation = MagicMock(unsafe=True)
        instance = create(SomeService, handler) # type SomeService
        instance.someapi()
        handler.handle_rest_invocation.assert_called()