from .proxyfactory import RestInvocationHandler
from .decorator import HttpMethod
from .api.management import Management
from .api.restdata import DataService
from .proxyfactory import create
from ..dtojson import from_json_str, to_json_str
import inspect
import requests
from requests.auth import AuthBase

default_session_cookie_name = 'JSESSIONID'


class CookieAuth(AuthBase):
    def __init__(self, cookie_value: str, cookie_name: str = default_session_cookie_name):
        self._value = cookie_value
        self._name = cookie_name

    def __call__(self, r: requests.PreparedRequest):
        r.prepare_cookies({self._name: self._value})
        return r


class RestInvocationHandlerImpl(RestInvocationHandler):
    def __init__(self, base_url: str, auth: AuthBase = None, proxies=None):
        self._base_url = base_url
        self._auth = auth
        self._proxies = proxies if proxies is not None else {}

    def _get_query_params(self, kwages, queryKWs):
        query_params = {}
        if queryKWs:
            for name in queryKWs:
                if name in kwages:
                    if type(kwages[name]) in (int, str, bool, float):
                        query_params[name] = kwages[name]
                    else:
                        query_params[name] = to_json_str(kwages[name])
        return query_params

    def _send_request(self, rest, *args, **kwargs):
        requests_methods = {
            HttpMethod.POST: requests.post,
            HttpMethod.GET: requests.get,
            HttpMethod.PUT: requests.put,
            HttpMethod.DELETE: requests.delete
        }
        response = requests_methods[rest.get_method()](*args, **kwargs)
        response.raise_for_status()
        return from_json_str(response.text, inspect.getfullargspec(rest.get_original_func()).annotations['return'])

    def get(self, rest, uri, args, kwargs):
        return self._send_request(rest, self._base_url + uri + '.json',
                                  params=self._get_query_params(kwargs, rest.get_queryKWs()), proxies=self._proxies,
                                  auth=self._auth)

    def post(self, rest, uri, args, kwargs):
        return self._send_request(rest, self._base_url + uri + '.json', data=to_json_str(kwargs[rest.get_entityKW()]),
                                  params=self._get_query_params(kwargs, rest.get_queryKWs()), proxies=self._proxies,
                                  auth=self._auth)

    def put(self, rest, uri, args, kwargs):
        return self._send_request(rest, self._base_url + uri + '.json', data=to_json_str(kwargs[rest.get_entityKW()]),
                                  params=self._get_query_params(kwargs, rest.get_queryKWs()), proxies=self._proxies,
                                  auth=self._auth)

    def delete(self, rest, uri, args, kwargs):
        return self._send_request(rest, self._base_url + uri + '.json',
                                  params=self._get_query_params(kwargs, rest.get_queryKWs()),
                                  proxies=self._proxies, auth=self._auth)

    def head(self, rest, uri, args, kwargs):
        response = requests.head(self._base_url + uri + '.json',
                                 params=self._get_query_params(kwargs, rest.get_queryKWs()),
                                 proxies=self._proxies, auth=self._auth)
        response.raise_for_status()
        return response.status_code

    def handle_rest_invocation(self, rest, args, kwargs: dict):
        methods = {
            HttpMethod.POST: self.post,
            HttpMethod.GET: self.get,
            HttpMethod.PUT: self.put,
            HttpMethod.DELETE: self.delete,
            HttpMethod.HEAD: self.head
        }
        uri = rest.get_uri()  # type:str
        argspec = inspect.getfullargspec(rest.get_original_func())
        kwargs = kwargs.copy()
        names = argspec[0]
        for index in range(len(args)):
            kwargs[names[index + 1]] = args[index]
        uri = uri.format(**kwargs)
        return methods[rest.get_method()](rest, uri, args, kwargs)


def create_auth(base_url: str, username: str, passwd: str, token: str, proxies=None) -> AuthBase:
    if username is not None and passwd is not None:
        # TODO iPortal和online，iServer CAS登录后续考虑
        # TODO session超时处理，定时刷新保证不超时，以及超时检测重新登录
        response = requests.post(base_url + '/services/security/login.json',
                                 json={'username': username, 'password': passwd}, proxies=proxies)
        response.raise_for_status()
        value = response.cookies[default_session_cookie_name]
        return CookieAuth(value)


class APIFactory:
    def __init__(self, base_url: str, username: str = None, passwd: str = None, token: str = None, proxies=None):
        self._base_url = base_url if not base_url.endswith('/') else base_url[:-1]
        self._services_url = self._base_url + '/services'
        self._proxies = proxies if proxies is not None else {}
        auth = create_auth(self._base_url, username, passwd, token, proxies=self._proxies)
        self._handler = RestInvocationHandlerImpl(self._base_url, auth, proxies=self._proxies)

    def management(self) -> Management:
        return create(Management, self._handler);

    def data_service(self, service_name: str) -> DataService:
        handler = RestInvocationHandlerImpl(self._services_url + '/' + service_name, proxies=self._proxies)
        return create(DataService, handler)
