from .proxyfactory import RestInvocationHandler
from .decorator import  REST,HttpMethod
from .api.management import Management
from .proxyfactory import create
from ..dtojson import from_json_str,to_json_str
import inspect
import requests
from requests.auth import AuthBase
default_session_cookie_name = 'JSESSIONID'
class CookieAuth(AuthBase):
    def __init__(self, cookieValue : str, cookieName : str=default_session_cookie_name):
        self._value = cookieValue
        self._name = cookieName

    def __call__(self, r: requests.PreparedRequest):
        r.prepare_cookies({self._name: self._value})
        return r


class RestInvocationHandlerImpl(RestInvocationHandler):
    def __init__(self, base_url: str, auth : AuthBase, proxies = None):
        self._base_url = base_url
        self._auth = auth
        self._proxies = proxies if proxies is not None else {}

    def get(self, rest, uri, args, kwargs):
        pass

    def post(self, rest, uri, args, kwargs):
        response = requests.post(self._base_url + uri + '.json', data=to_json_str(kwargs[rest.getEntityKW()]), proxies = self._proxies, auth = self._auth) # type:requests.Response
        response.raise_for_status()
        return from_json_str(response.text, inspect.getfullargspec(rest.get_original_func()).annotations['return'])

    def put(self, rest, uri, args, kwargs):
        pass

    def delete(self, rest, uri, args, kwargs):
        pass

    def head(self, rest, uri, args, kwargs):
        pass

    def handle_rest_invocation(self, rest, func, args, kwargs):
        methods = {
            HttpMethod.POST: self.post,
            HttpMethod.GET: self.get,
            HttpMethod.PUT: self.put,
            HttpMethod.DELETE: self.delete,
            HttpMethod.HEAD: self.head
        }
        uri = rest.getUri() # type:str
        uri = uri.format(**kwargs)
        return methods[rest.getMethod()](rest, uri, args, kwargs)

def createAuth(base_url: str, username: str, passwd: str, token: str, proxies = None) -> AuthBase:
    if username is not None and passwd is not None:
        # TODO iPortal和online，iServer CAS登录后续考虑
        # TODO session超时处理，定时刷新保证不超时，以及超时检测重新登录
        response = requests.post(base_url + '/services/security/login.json', json={'username': username, 'password': passwd}, proxies=proxies)
        response.raise_for_status()
        value = response.cookies[default_session_cookie_name]
        return CookieAuth(value)

class APIFactory:
    def __init__(self, base_url: str, username: str = None, passwd: str = None, token: str = None, proxies = None):
        base_url = base_url if not base_url.endswith('/') else base_url[:-1]
        _proxies = proxies if proxies is not  None else {}
        auth = createAuth(base_url, username, passwd, token, proxies = proxies)
        self._handler = RestInvocationHandlerImpl(base_url, auth, proxies = proxies)

    def management(self) -> Management:
        return create(Management, self._handler);


