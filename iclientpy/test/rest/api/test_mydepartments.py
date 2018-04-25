from .abstractrest import AbstractRESTTestCase
import httpretty
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.mydepartments import MyDepartments
from iclientpy.rest.api.model import *
from unittest import mock


class MyDatasTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls, 'http://localhost:8090/iportal', 'admin', 'Supermap123')
        cls.init_iportal_apifactory(cls)
        cls.init_api(cls, "mydepartments_service")

    def test_departments(self):
        self.check_api(MyDepartments.get_mydepartments, self.baseuri + "/web/mycontent/departments.json",
                       HttpMethod.GET,
                       httpretty.Response(
                           body='[{"createTime":1481681711688,"id":3,"name":"研发1","upperDepartmentNames":["研发部","xx公司"]},{"createTime":1481681703250,"id":2,"name":"研发部","upperDepartmentNames":["xx公司"]}]',
                           status=201))
        self.check_api(MyDepartments.get_mydepartments_members,
                       self.baseuri + "/web/mycontent/departments/members.json", HttpMethod.GET, httpretty.Response(
                body='[{"departmentId":3,"id":1,"nickname":"user1","userName":"user1"},{"departmentId":3,"id":2,"nickname":"user3","userName":"user3"},{"departmentId":3,"id":3,"nickname":"user2","userName":"user2"},{"departmentId":2,"id":4,"nickname":"user5","userName":"user5"},{"departmentId":2,"id":5,"nickname":"user4","userName":"user4"}]',
                status=201))
