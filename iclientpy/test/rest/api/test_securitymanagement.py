import httpretty
from iclientpy.rest.api.management import *
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.model import UserEntity
from .abstractrest import AbstractRESTTestCase


class SecurityManagementTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, "security_management")

    def test_users(self):
        get_users_body = '[["admin","","ADMIN"],["guest1","","ADMIN"]]'
        self.check_api('get_users', self.baseuri + '/manager/security/users.json', HttpMethod.GET,
                       httpretty.Response(body=get_users_body, status=200))
        post_users_body = '{"newResourceID":"guest1","newResourceLocation":"http://localhost:8090/iserver/manager/security/users/guest1.rjson","postResultType":"CreateChild","succeed":true}'
        entity = UserEntity()
        self.check_api('post_users', self.baseuri + '/manager/security/users.json', HttpMethod.POST,
                       httpretty.Response(body=post_users_body, status=200), entity=entity)
        self.check_api('put_users', self.baseuri + '/manager/security/users.json', HttpMethod.PUT,
                       httpretty.Response(body='{"succeed":true}', status=200), entity=['admin'])

    def test_user(self):
        get_user_body = '{"description":"","email":null,"name":"guest1","ownRoles":["PUBLISHER"],"password":"$shiro1$SHA-256$500000$3FK4ExWiZ35PFfr/NqfMGg==$R5Gwtq4bIgXywfnGKCHYGzOO59CnMSZme69D8H18GvI=","roles":["PUBLISHER"],"userGroups":[]}'
        self.check_api('get_user', self.baseuri + '/manager/security/users/admin.json', HttpMethod.GET,
                       httpretty.Response(body=get_user_body, status=200), username='admin')
        entity = UserEntity()
        self.check_api('put_user', self.baseuri + '/manager/security/users/admin.json', HttpMethod.PUT,
                       httpretty.Response(body='{"succeed":true}', status=200), username='admin', entity=entity)
        self.check_api('delete_user', self.baseuri + '/manager/security/users/admin.json', HttpMethod.DELETE,
                       httpretty.Response(body='{"succeed":true}', status=200), username='admin', entity=['admin'])

    def test_roles(self):
        get_roles_body = '[{"description":"内置的系统管理员角色，此角色默认拥有整个iServer的管理权限。","name":"ADMIN","permissions":{"componentManagerPermissions":{"denied":[],"permitted":[]},"instanceAccessPermissions":{"denied":[],"permitted":[]},"publishEnabled":false},"userGroups":[],"users":["admin"]},{"description":"","name":"UNAUTHORIZED","permissions":{"componentManagerPermissions":{"denied":[],"permitted":[]},"instanceAccessPermissions":{"denied":[],"permitted":[]},"publishEnabled":false},"userGroups":["THIRD_PART_AUTHORIZED"],"users":[]},{"description":"内置的服务发布者角色，此角色默认拥有服务发布和服务实例管理的权限。","name":"PUBLISHER","permissions":{"componentManagerPermissions":{"denied":[],"permitted":[]},"instanceAccessPermissions":{"denied":[],"permitted":[]},"publishEnabled":true},"userGroups":[],"users":[]},{"description":"","name":"NOPASSWORD","permissions":{"componentManagerPermissions":{"denied":[],"permitted":[]},"instanceAccessPermissions":{"denied":[],"permitted":[]},"publishEnabled":false},"userGroups":["THIRD_PART_AUTHORIZED"],"users":[]},{"description":"内置的iPortal用户角色。","name":"PORTAL_USER","permissions":{"componentManagerPermissions":{"denied":[],"permitted":[]},"instanceAccessPermissions":{"denied":[],"permitted":[]},"publishEnabled":false},"userGroups":[],"users":[]}]'
        self.check_api('get_roles', self.baseuri + '/manager/security/roles.json', HttpMethod.GET,
                       httpretty.Response(body=get_roles_body, status=200))
        post_users_body = '{"newResourceID":"ROLE1","newResourceLocation":"http://localhost:8090/iserver/manager/security/roles/ROLE1.rjson","postResultType":"CreateChild","succeed":true}'
        entity = RoleEntity()
        self.check_api('post_roles', self.baseuri + '/manager/security/roles.json', HttpMethod.POST,
                       httpretty.Response(body=post_users_body, status=200), entity=entity)
        self.check_api('put_roles', self.baseuri + '/manager/security/roles.json', HttpMethod.PUT,
                       httpretty.Response(body='{"succeed":true}', status=200), entity=['admin'])

    def test_role(self):
        get_role_body = '{"newResourceID":"ROLE1","newResourceLocation":"http://localhost:8090/iserver/manager/security/roles/ROLE1.rjson","postResultType":"CreateChild","succeed":true}'
        self.check_api('get_role', self.baseuri + '/manager/security/roles/admin.json', HttpMethod.GET,
                       httpretty.Response(body=get_role_body, status=200), role='admin')
        entity = RoleEntity()
        self.check_api('put_role', self.baseuri + '/manager/security/roles/admin.json', HttpMethod.PUT,
                       httpretty.Response(body='{"succeed":true}', status=200), role='admin', entity=entity)
        self.check_api('delete_role', self.baseuri + '/manager/security/roles/admin.json', HttpMethod.DELETE,
                       httpretty.Response(body='{"succeed":true}', status=200), role='admin', entity=['admin'])


class PortalSecurityManagementTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_iportal_apifactory(cls)
        cls.init_api(cls, "security_management")

    def test_users(self):
        get_users_body = '[{"description":"","email":null,"name":"guest1","ownRoles":["PUBLISHER"],"password":"$shiro1$SHA-256$500000$3FK4ExWiZ35PFfr/NqfMGg==$R5Gwtq4bIgXywfnGKCHYGzOO59CnMSZme69D8H18GvI=","roles":["PUBLISHER"],"userGroups":[]}]'
        self.check_api('get_users', self.baseuri + '/manager/security/portalusers.json', HttpMethod.GET,
                       httpretty.Response(body=get_users_body, status=200))
