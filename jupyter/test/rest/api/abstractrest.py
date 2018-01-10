import inspect
import httpretty
from sure import expect
from unittest import TestCase
from iclientpy.dtojson import to_json_str, from_json_str
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.apifactory import APIFactory


class AbstractREST(object):
    def init_rest(self, baseuri="http://192.168.20.158:8090/iserver", username="admin", password="iserver", **kwargs):
        self.baseuri = baseuri
        self.username = username
        self.password = password
        for k, v in kwargs.items():
            setattr(self, k, v)

    @httpretty.activate
    def init_apifactory(self):
        if not hasattr(self, 'factory'):
            loginuri = self.loginuri if hasattr(self, 'loginuri') else self.baseuri + '/services/security/login.json'
            httpretty.register_uri(httpretty.POST, loginuri, status=201,
                                   set_cookie='JSESSIONID=958322873908FF9CA99B5CB443ADDD5C')
            self.factory = APIFactory(self.baseuri, self.username, self.password)

    def init_api(self, method_name, *args, **kwargs):
        if not hasattr(self, 'api'):
            method = getattr(self.factory, method_name)
            self.api = method(*args, **kwargs)

    @httpretty.activate
    def check_api(self, method_name, uri, http_method: HttpMethod, response: httpretty.Response, *args, **kwargs):
        methods = {
            HttpMethod.POST: httpretty.POST,
            HttpMethod.GET: httpretty.GET,
            HttpMethod.PUT: httpretty.PUT,
            HttpMethod.DELETE: httpretty.DELETE,
            HttpMethod.HEAD: httpretty.HEAD
        }
        httpretty.register_uri(methods[http_method], uri, responses=[response])
        method = getattr(self.api, method_name)
        result = method(*args, **kwargs)
        if http_method != HttpMethod.HEAD:
            expect(to_json_str(result)).should.within(
                to_json_str(from_json_str(
                    str(response.body, encoding='utf-8'),
                    inspect.getfullargspec(method).annotations['return']
                ))
            )
        else:
            expect(result).should.equal(response.status)


class AbstractRESTTestCase(TestCase, AbstractREST):
    pass
