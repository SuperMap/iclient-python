from .abstractrest import AbstractRESTTestCase
import httpretty
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.groupsservice import GroupsService


class GroupsServiceTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls, 'http://localhost:8090/iportal', 'admin', 'Supermap123')
        cls.init_iportal_apifactory(cls)
        cls.init_api(cls, "groups_service")

    def test_groups(self):
        self.check_api(GroupsService.get_groups, self.baseuri + "/web/groups.json", HttpMethod.GET,
                       httpretty.Response(
                           body='{"content":[{"createTime":1461721285156,"creator":"admin","description":"","groupName":"FA","icon":null,"id":1,"isEnabled":true,"isNeedCheck":true,"isPublic":true,"nickname":"admin","resourceSharer":"MEMBER","tags":["iPortal"],"updateTime":1461721285156},{"createTime":1461721383744,"creator":"user1","description":"","groupName":"FB","icon":null,"id":2,"isEnabled":true,"isNeedCheck":true,"isPublic":true,"nickname":"user1","resourceSharer":"MEMBER","tags":["iserver"],"updateTime":1461721383744}],"currentPage":1,"pageSize":9,"searchParameter":{"currentPage":1,"currentUser":null,"filterFields":null,"isEnabled":true,"isPublic":null,"joinTypes":null,"keywords":null,"orderBy":null,"orderType":"ASC","pageSize":9,"returnCanJoin":false,"returnCreate":false,"returnJoined":false,"tags":null,"userNames":null},"total":2,"totalPage":1}',
                           status=201))
