from enum import Enum
import typing


class AuthenticationType(Enum):
    Token = 'Token'
    Password = 'Password'
    CAS = 'CAS'


class Authentication:
    type: AuthenticationType
    def __init__(self, authentication_type):
        self.type = authentication_type


class UsernamePasswdAuthentication(Authentication):
    username: str
    passwd: str
    def __init__(self, username:str, passwd: str):
        super().__init__(AuthenticationType.Password)
        self.username = username
        self.passwd = passwd


class TokenAuthentication(Authentication):
    token: str
    def __init__(self, token:str):
        super().__init__(AuthenticationType.Token)
        self.token = token

class ProfileTargetType(Enum):
    Portal = 'Portal'
    Server = 'Server'
    Online = 'Online'


class Profile:
    targetType: ProfileTargetType
    url: str
    authentication: Authentication
    def __init__(self, targetType: ProfileTargetType, url: str, authentication:Authentication):
        self.targetType = targetType
        self.url = url
        self.authentication = authentication


_default_profile = None

_profiles = {} #type:typing.Dict[str, Profile]

def get_profile(name:str = None):
    if name is None :
        if _default_profile is None:
            raise Exception('not set')
        else:
            return _default_profile
    return _profiles[name]

def set_default_profile(profile: Profile):
    global _default_profile
    _default_profile = profile

def add_profile(*, name:str, type:ProfileTargetType, url:str, username_password: typing.Tuple[str, str] = None,token:str = None, authentication_type: AuthenticationType = None, update_default:bool = False):
    if username_password is None and token is None:
        raise Exception('必须设置用户名/密码或者token')
    if username_password is not None and token is not None:
        raise Exception('用户名/密码或者token只能设置其中一个')

    if type != ProfileTargetType.Server:
        raise Exception('暂时只支持iServer')

    if authentication_type is None:
        authentication_type = AuthenticationType.Password if username_password is not None else AuthenticationType.Token
    if authentication_type != AuthenticationType.Password and authentication_type != AuthenticationType.Token:
        raise Exception('暂时只支持用户名密码和Token验证')

    authentication = None #type: Authentication
    if username_password is not None:
        authentication = UsernamePasswdAuthentication(username_password[0], username_password[1])
    elif token is not None:
        authentication = TokenAuthentication(token)
    profile = Profile(targetType=type, url=url,authentication=authentication)

    if update_default or _default_profile is None:
        set_default_profile(profile)
    _profiles[name] = profile


def add_server_username_password_profile(name: str, url:str, username: str, passwd: str, **kwargs):
    add_profile(name=name,type=ProfileTargetType.Server, url=url, username_password=(username, passwd),authentication_type=AuthenticationType.Password, **kwargs)

def add_server_token_profile(name: str, url:str, token: str, **kwargs):
    add_profile(name=name,type=ProfileTargetType.Server, url=url, token=token ,authentication_type=AuthenticationType.Password, **kwargs)