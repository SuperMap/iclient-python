import httpretty
from .abstractrest import AbstractRESTTestCase
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.node_service import NodeService
from iclientpy.rest.api.model import CreateServerEntity


class NodeServiceTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls, 'http://localhost:8090/imanager', 'admin', 'Supermap123')
        cls.init_imanager_apifactory(cls)
        cls.init_api(cls, "node_service")

    def test_api(self):
        entity = CreateServerEntity()
        self.check_api(NodeService.create_server, self.baseuri + "/cloud/web/nodes/server.json",
                       HttpMethod.POST,
                       httpretty.Response(body='{"isSucceed":true,"msg":"","resultId":"35660","taskId":"1683"}',
                                          status=201), entity=entity)
        node_ids = [123]
        self.check_api(NodeService.stop_nodes, self.baseuri + "/web/api/service/stopped.json",
                       HttpMethod.POST,
                       httpretty.Response(
                           body='{"failures":[],"isSucceed":true,"msg":"","success":[{"id":"35662","name":"test123"}]}',
                           status=201), node_ids=node_ids)
        self.check_api(NodeService.start_nodes, self.baseuri + "/web/api/service/started.json",
                       HttpMethod.POST,
                       httpretty.Response(
                           body='{"failures":[],"isSucceed":true,"msg":"","success":[{"id":"35662","name":"test123"}]}',
                           status=201), node_ids=node_ids)
        self.check_api(NodeService.delete_nodes, self.baseuri + "/web/api/service/deleted.json",
                       HttpMethod.POST,
                       httpretty.Response(
                           body='{"failures":[],"isSucceed":true,"msg":"","success":[{"id":"35662","name":"test123"}]}',
                           status=201), node_ids=node_ids)
        self.check_api(NodeService.restart_nodes, self.baseuri + "/web/api/service/restarted.json",
                       HttpMethod.POST,
                       httpretty.Response(
                           body='{"failures":[],"isSucceed":true,"msg":"","success":[{"id":"35662","name":"test123"}]}',
                           status=201), node_ids=node_ids)
        self.check_api(NodeService.get_servers, self.baseuri + "/web/api/service.json",
                       HttpMethod.GET,
                       httpretty.Response(
                           body='{"list":[{"address":"http://192.168.22.127:8090/iserver","dbs":[],"hasAgent":false,"id":35336,"isCreate":true,"isMonitored":true,"name":"不要删用来跑VT","owner":"admin","status":[],"type":"iServer"},{"address":"http://192.168.22.127:8091/iserver","dbs":[],"hasAgent":false,"id":35558,"isCreate":false,"isMonitored":true,"name":"aaa","owner":"admin","status":["INSTALLING_AGENT"],"type":"iServer"},{"address":"http://192.168.22.133:8090/iserver","dbs":[],"hasAgent":false,"id":35616,"isCreate":true,"isMonitored":true,"name":"test","owner":"admin","status":[],"type":"iServer"},{"address":"http://192.168.22.136:8090/iserver","dbs":[],"hasAgent":false,"id":35668,"isCreate":true,"isMonitored":true,"name":"test123","owner":"admin","status":[],"type":"iServer"}],"total":4}',
                           status=201), node_ids=node_ids)
