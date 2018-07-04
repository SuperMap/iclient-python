from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.server import Server
from iclientpy.rest.api.servicespage import ServiceComponentType, ServiceMetaInfo
from iclientpy.rest.api.model import UserInfo, RoleEntity, MethodResult, AuthorizeType, ServiceInstance


class ServerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        services_page = MagicMock()
        services_page.list_services = MagicMock(return_value=[])
        api_factory = MagicMock()
        api_factory.servicespage = MagicMock(return_value=services_page)
        mocked_factory_clz = MagicMock(return_value=api_factory)
        cls.server = Server(api_factory_clz=mocked_factory_clz, base_url='http://localhost:8090/iserver',
                            username='admin',
                            passwd='Supermap123')

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

    def test_getusers(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        users = []
        managment.get_users = MagicMock(return_value=users)
        result = server.get_users()
        self.assertEqual(result, users)

    def test_getuser(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        user = UserInfo()
        managment.get_users = MagicMock(return_value=user)
        result = server.get_users()
        self.assertEqual(result, user)

    def test_createuser(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.post_users = MagicMock(return_value=re)
        server.create_user('test', 'test')
        managment.post_users.assert_called_once()

    def test_updateuser(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.put_user = MagicMock(return_value=re)
        server.update_user('test', 'test')
        managment.put_user.assert_called_once()

    def test_deleteusers(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.put_users = MagicMock(return_value=re)
        server.delete_users(['test'])
        managment.put_users.assert_called_once()

    def test_deleteuser(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.delete_user = MagicMock(return_value=re)
        server.delete_user('test')
        managment.delete_user.assert_called_once()

    def test_createuser_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.post_users = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.create_user('test', 'test')
        managment.post_users.assert_called_once()

    def test_updateuser_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.put_user = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.update_user('test', 'test')
        managment.put_user.assert_called_once()

    def test_deleteusers_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.put_users = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.delete_users(['test'])
        managment.put_users.assert_called_once()

    def test_deleteuser_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.delete_user = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.delete_user('test')
        managment.delete_user.assert_called_once()

    def test_getroles(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        roles = []
        managment.get_roles = MagicMock(return_value=roles)
        result = server.get_roles()
        self.assertEqual(result, roles)

    def test_getrole(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        role = RoleEntity()
        managment.get_role = MagicMock(return_value=role)
        result = server.get_role('test')
        self.assertEqual(result, role)

    def test_createrole(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.post_roles = MagicMock(return_value=re)
        server.create_role('test')
        managment.post_roles.assert_called_once()

    def test_updaterole(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.put_role = MagicMock(return_value=re)
        server.update_role('test', description='test')
        managment.put_role.assert_called_once()

    def test_deleterole(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.delete_role = MagicMock(return_value=re)
        server.delete_role('test')
        managment.delete_role.assert_called_once()

    def test_deleteroles(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.put_roles = MagicMock(return_value=re)
        server.delete_roles(['test'])
        managment.put_roles.assert_called_once()

    def test_createrole_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.post_roles = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.create_role('test')
        managment.post_roles.assert_called_once()

    def test_updaterole_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.put_role = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.update_role('test', description='test')
        managment.put_role.assert_called_once()

    def test_deleterole_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.delete_role = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.delete_role('test')
        managment.delete_role.assert_called_once()

    def test_deleteroles_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.security_management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.put_roles = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.delete_roles(['test'])
        managment.put_roles.assert_called_once()

    def test_get_instances(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.management = MagicMock(return_value=managment)
        instances = []
        managment.get_instances = MagicMock(return_value=instances)
        result = server.get_instances()
        self.assertEqual(result, instances)

    def test_get_instance(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.management = MagicMock(return_value=managment)
        instance = ServiceInstance()
        managment.get_instance = MagicMock(return_value=instance)
        result = server.get_instance('map-World/rest')
        self.assertEqual(result, instance)

    def test_grant_privileges_instances(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.management = MagicMock(return_value=managment)
        re = MethodResult()
        re.succeed = True
        managment.post_authorize = MagicMock(return_value=re)
        server.grant_privileges_instances(['test'], authorize_type=AuthorizeType.AUTHENTICATED)
        managment.post_authorize.assert_called_once()

    def test_grant_privileges_instances_exception(self):
        server = self.server
        server._apifactory = MagicMock()
        managment = MagicMock()
        server._apifactory.management = MagicMock(return_value=managment)
        re = MethodResult()
        managment.post_authorize = MagicMock(return_value=re)
        with self.assertRaises(Exception):
            server.grant_privileges_instances(['test'], authorize_type=AuthorizeType.AUTHENTICATED)
        managment.post_authorize.assert_called_once()
