from .abstractrest import AbstractRESTTestCase
import httpretty
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.datasservice import DatasService
from iclientpy.rest.api.model import *
from unittest import mock


class DatasServiceTestCase(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls, 'http://www.supermapol.com', 'test', 'test')
        cls.init_online_apifactory(cls)
        cls.init_api(cls, "datas_service")

    def test_datas(self):
        get_body = '{"total":2,"totalPage":1,"pageSize":9,"searchParameter":{"serviceStatuses":null,"orderType":"ASC","fileName":null,"keywords":null,"md5s":null,"orderBy":null,"pageSize":9,"dirIds":null,"filterFields":null,"departmentIds":null,"type":null,"createEnd":null,"groupIds":null,"isPublic":false,"serviceId":null,"resourceIds":null,"types":null,"returnSubDir":null,"isNotInDir":false,"userName":null,"createStart":null,"tags":null,"currentUser":null,"ids":null,"userNames":["admin"],"currentPage":1,"status":null},"currentPage":1,"content":[{"dataMetaInfo":null,"lastModfiedTime":1523257742447,"fileName":"World.zip","thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","dataItemServices":[],"dataCheckResult":{"serviceCheckInfos":[{"serviceType":"RESTDATA","checkStatus":"SUCCESS","checkMsg":null,"dataType":"WORKSPACE","id":2,"MD5":"1ba8ffea81ec660c81898cbe4d9cfbbf"},{"serviceType":"RESTMAP","checkStatus":"SUCCESS","checkMsg":null,"dataType":"WORKSPACE","id":1,"MD5":"1ba8ffea81ec660c81898cbe4d9cfbbf"}],"dataCheckInfo":{"checkStatus":"SUCCESS","checkMsg":null,"dataType":"WORKSPACE","id":1,"MD5":"1ba8ffea81ec660c81898cbe4d9cfbbf"}},"publishInfo":null,"authorizeSetting":[{"aliasName":"admin","entityRoles":null,"entityType":"USER","entityName":"admin","dataPermissionType":"DELETE","entityId":null}],"description":null,"userName":"admin","type":"WORKSPACE","tags":null,"coordType":null,"size":131516686,"createTime":1523257742448,"serviceStatus":"UNPUBLISHED","nickname":"admin","id":696479938,"serviceId":null,"downloadCount":1,"storageId":"wdosrwih_pdb9lxhq_b4c7a7a3_1523_4463_a815_678b0453a2cd","status":"OK","MD5":"1ba8ffea81ec660c81898cbe4d9cfbbf"},{"dataMetaInfo":null,"lastModfiedTime":1523946252375,"fileName":"test.json","thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","dataItemServices":[],"dataCheckResult":{"serviceCheckInfos":null,"dataCheckInfo":null},"publishInfo":null,"authorizeSetting":[{"aliasName":"admin","entityRoles":null,"entityType":"USER","entityName":"admin","dataPermissionType":"DELETE","entityId":null}],"description":null,"userName":"admin","type":"JSON","tags":null,"coordType":null,"size":1006096,"createTime":1523946252375,"serviceStatus":"DOES_NOT_INVOLVE","nickname":"admin","id":18220636,"serviceId":null,"downloadCount":0,"storageId":"wdosrwih_pdb9lxhq_d7485aae_cd3d_413b_99f8_5e72930d2f53","status":"OK","MD5":"67492951f6d694e45d26278dc1a7d40d"}]}'
        self.check_api(DatasService.get_my_datas, self.baseuri + "/web/datas.json", HttpMethod.GET,
                       httpretty.Response(body=get_body, status=201))
        entity = PostMyDatasItem()
        entity.type = DataItemType.JSON
        entity.fileName = 'test.json'
        self.check_api(DatasService.post_my_datas, self.baseuri + "/web/mycontent/datas.json", HttpMethod.POST,
                       httpretty.Response(
                           body='{"childID":"2","isAsynchronizedReturn":false,"childContent":null,"childUrl":null,"customResult":null}',
                           status=201), entity=entity)

    @mock.patch('builtins.open', mock.mock_open(read_data='1'))
    def test_data(self):
        data_id = '18220636'
        get_body = '{"dataMetaInfo":null,"lastModfiedTime":1523946252375,"fileName":"test.json","thumbnail":"http://localhost:8090/iportal/services/../web/static/portal/img/map/cloud.png","dataItemServices":[],"dataCheckResult":{"serviceCheckInfos":null,"dataCheckInfo":null},"publishInfo":null,"authorizeSetting":[],"description":null,"userName":"admin","type":"JSON","tags":[],"coordType":null,"size":1006096,"createTime":1523946252375,"serviceStatus":"DOES_NOT_INVOLVE","nickname":"admin","id":18220636,"serviceId":null,"downloadCount":0,"storageId":"wdosrwih_pdb9lxhq_d7485aae_cd3d_413b_99f8_5e72930d2f53","status":"OK","MD5":"67492951f6d694e45d26278dc1a7d40d"}'
        self.check_api(DatasService.get_my_data, self.baseuri + "/web/datas/18220636.json", HttpMethod.GET,
                       httpretty.Response(body=get_body, status=201), data_id=data_id)
        entity = PutMyDataItem()
        entity.fileName = 'test2'
        entity.description = '123'
        self.check_api(DatasService.put_my_data, self.baseuri + "/web/mycontent/datas/18220636.json", HttpMethod.PUT,
                       httpretty.Response(body='{"succeed":true,"newResourceID":"1"}', status=201), data_id=data_id,
                       entity=entity)
        self.check_api(DatasService.delete_my_data, self.baseuri + "/web/mycontent/datas/18220636.json",
                       HttpMethod.DELETE,
                       httpretty.Response(body='{"succeed":true}', status=201), data_id=data_id)
        with open('./World.zip', 'rb') as fileb:
            self.check_api(DatasService.upload_my_data, self.baseuri + "/web/mycontent/datas/18220636/upload.json",
                           HttpMethod.POST,
                           httpretty.Response(
                               body='{"childContent":null,"childID":"1","childUrl":null,"customResult":null,"isAsynchronizedReturn":false}',
                               status=201), data_id=data_id, file=fileb)
        self.check_api(DatasService.get_upload_process, self.baseuri + "/web/mycontent/datas/18220636/progress.json",
                       HttpMethod.GET,
                       httpretty.Response(body='{"id":"null","read":94,"total":100}', status=201), data_id=data_id)

    def test_data_sharesetting(self):
        data_id = '629565098'
        self.check_api(DatasService.get_my_data_sharesetting,
                       self.baseuri + "/web/mycontent/datas/629565098/sharesetting.json",
                       HttpMethod.GET,
                       httpretty.Response(
                           body='[{"aliasName":"admin","dataPermissionType":"DELETE","entityId":null,"entityName":"admin","entityType":"USER"},{"aliasName":"GUEST","dataPermissionType":"DOWNLOAD","entityId":null,"entityName":"GUEST","entityType":"USER"}]',
                           status=201), data_id=data_id)
        entity = IportalDataAuthorizeEntity()
        entity.dataPermissionType = DataPermissionType.DOWNLOAD
        entity.entityType = EntityType.USER
        entity.entityName = 'GUEST'
        entity.aliasName = 'GUEST'
        self.check_api(DatasService.put_my_data_sharesetting,
                       self.baseuri + "/web/mycontent/datas/629565098/sharesetting.json", HttpMethod.PUT,
                       httpretty.Response(body='{"succeed": true}', status=201), data_id=data_id, entity=[entity])
