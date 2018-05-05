from unittest import TestCase, mock
from iclientpy.portal import Portal, MapShareSettingBuilder, DataShareSettingBuilder
from iclientpy.rest.api.model import GetMapsResult, ViewerMap, MethodResult, MyDatasMethodResult, DataItem, Status, \
    DataItemType, MyDataUploadProcess, Layer, GetGroupsResult, PermissionType, DataPermissionType, EntityType, \
    GetMyDatasResult
from io import FileIO
from pandas import DataFrame


class MockiPortalAPIFactory:
    def __init__(self, url, *args, **kwargs):
        self._base_url = url
        pass


@mock.patch("iclientpy.portal.iPortalAPIFactory", MockiPortalAPIFactory)
class PortalTestCase(TestCase):
    def test_search_map(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        result = GetMapsResult()
        result.content = []
        maps_service = mock.MagicMock()
        maps_service.get_maps = mock.MagicMock(return_value=result)
        portal._portal.maps_service = mock.MagicMock(return_value=maps_service)
        result = portal.search_map()
        self.assertEqual(result, [])

    def test_get_map(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        m = ViewerMap()
        maps_service = mock.MagicMock()
        maps_service.get_map = mock.MagicMock(return_value=m)
        portal._portal.maps_service = mock.MagicMock(return_value=maps_service)
        result = portal.get_map('map_id')
        self.assertEqual(result, m)

    def test_upload_data(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        mdmr = MyDatasMethodResult()
        mdmr.childID = 'data_id'
        data_services.post_datas = mock.MagicMock(return_value=mdmr)
        data_services.upload_data = mock.MagicMock(return_value=mdmr)
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        portal.get_data = mock.MagicMock()
        data1 = DataItem()
        data1.status = Status.CREATED
        data2 = DataItem()
        data2.status = Status.CREATED
        data3 = DataItem()
        data3.status = Status.OK
        portal.get_data.side_effect = [data1, data2, data3]
        portal.get_data_upload_progress = mock.MagicMock()
        portal.get_data_upload_progress.side_effect = [(0, 100), (50, 100), (100, 100)]
        callback = mock.MagicMock()
        data_content = mock.MagicMock()
        data_content.__class__ = FileIO
        result = portal.upload_data('test.json', data_content, DataItemType.JSON, callback)
        self.assertEqual(result, 'data_id')

    def test_upload_dataframe_as_json(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        portal.upload_data = mock.MagicMock(return_value='data_id')
        df = mock.MagicMock()
        df.__class__ = DataFrame
        df.to_json = mock.MagicMock(return_value='testtesttest')
        result = portal.upload_dataframe_as_json('data', df)
        self.assertEqual(result, 'data_id')

    def test_get_datas(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        res = GetMyDatasResult()
        res.content = []
        data_services.get_datas = mock.MagicMock(return_value=res)
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        result = portal.search_data()
        self.assertEqual(result, [])

    def test_get_data(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data = DataItem()
        data_services = mock.MagicMock()
        data_services.get_data = mock.MagicMock(return_value=data)
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        result = portal.get_data('data_id')
        self.assertEqual(result, data)

    def test_get_data_upload_progress(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        process = MyDataUploadProcess()
        process.read = 10
        process.total = 100
        data_services.get_upload_process = mock.MagicMock(return_value=process)
        result = portal.get_data_upload_progress('data_id')
        self.assertEqual(result, (10, 100))

    def test_create_map(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_service = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.newResourceID = 'map_id';
        maps_service.post_maps = mock.MagicMock(return_value=res)
        result = portal.create_map([Layer()], 3857, 'map', (0, 0), (-180, -90, 180, 90))
        self.assertEqual(result, 'map_id')

    def test_prepare_geojson_layer(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        data_id = 'data_id'
        result = portal.prepare_geojson_layer(data_id, 'layer')
        self.assertEqual(result.url, 'http://localhost:8090/iportal/datas/data_id/content.json')
        self.assertEqual(result.title, 'layer')

    def test_search_groups(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        groups_service = mock.MagicMock()
        portal._portal.groups_service = mock.MagicMock(return_value=groups_service)
        res = GetGroupsResult()
        res.content = []
        groups_service.get_groups = mock.MagicMock(return_value=res)
        result = portal.search_group()
        self.assertEqual(result, [])

    def test_get_data_sharesetting(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        data_services.get_data_sharesetting = mock.MagicMock(return_value=[])
        result = portal.get_data_sharesetting('data_id')
        self.assertEqual(result, [])

    def test_config_data_sharesetting(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.put_data_sharesetting = mock.MagicMock(return_value=res)
        portal.config_data_sharesetting('data_id', [])
        data_services.put_data_sharesetting.assert_called_once_with('data_id', [])

    def test_config_data_sharesetting_exception(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = False
        data_services.put_data_sharesetting = mock.MagicMock(return_value=res)
        with self.assertRaises(Exception):
            portal.config_data_sharesetting('data_id', [])
        data_services.put_data_sharesetting.assert_called_once_with('data_id', [])

    def test_get_map_sharesetting(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_services = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_services)
        maps_services.get_map_sharesetting = mock.MagicMock(return_value=[])
        result = portal.get_map_sharesetting('map_id')
        self.assertEqual(result, [])

    def test_config_map_sharesetting(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_services = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_services)
        res = MethodResult()
        res.succeed = True
        maps_services.put_map_sharesetting = mock.MagicMock(return_value=res)
        portal.config_map_sharesetting('map_id', [])
        maps_services.put_map_sharesetting.assert_called_once_with('map_id', [])

    def test_config_map_sharesetting_exception(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_services = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_services)
        res = MethodResult()
        res.succeed = False
        maps_services.put_map_sharesetting = mock.MagicMock(return_value=res)
        with self.assertRaises(Exception):
            portal.config_map_sharesetting('map_id', [])
        maps_services.put_map_sharesetting.assert_called_once_with('map_id', [])

    def test_delete_map(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_service = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.delete_maps = mock.MagicMock(return_value=res)
        portal.delete_map('map_id')
        maps_service.delete_maps.assert_called_once_with(['map_id'])

    def test_delete_maps(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        maps_service = mock.MagicMock()
        portal._portal.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.delete_maps = mock.MagicMock(return_value=res)
        portal.delete_maps(['map_id'])
        maps_service.delete_maps.assert_called_once_with(['map_id'])

    def test_delete_data(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.delete_data = mock.MagicMock(return_value=res)
        portal.delete_data('data_id')
        data_services.delete_data.assert_called_once_with('data_id')

    def test_delete_datas(self):
        portal = Portal('http://localhost:8090/iportal', 'admin', 'Supermap123')
        portal._portal = mock.MagicMock()
        data_services = mock.MagicMock()
        portal._portal.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.delete_data = mock.MagicMock(return_value=res)
        portal.delete_datas(['data_id', 'data_id2'])
        self.assertEqual(data_services.delete_data.call_count, 2)
        self.assertEqual(data_services.delete_data.call_args_list, [mock.call('data_id'), mock.call('data_id2')])


class MapShareSettingBuilderTestCase(TestCase):
    def test_builder(self):
        result = MapShareSettingBuilder().share_to_user("user", PermissionType.READ).share_to_department(
            'department_id', PermissionType.READ).share_to_group('group_id',
                                                                 PermissionType.READWRITE).share_to_everyone(
            PermissionType.READ).share_to_users(['user1', 'user2'], PermissionType.READWRITE).build()
        self.assertEqual(result[0].entityName, 'user')
        self.assertEqual(result[0].permissionType, PermissionType.READ.value)
        self.assertEqual(result[0].entityType, EntityType.USER)
        self.assertEqual(result[1].entityId, 'department_id')
        self.assertEqual(result[1].permissionType, PermissionType.READ.value)
        self.assertEqual(result[1].entityType, EntityType.DEPARTMENT)
        self.assertEqual(result[2].entityId, 'group_id')
        self.assertEqual(result[2].permissionType, PermissionType.READWRITE.value)
        self.assertEqual(result[2].entityType, EntityType.IPORTALGROUP)
        self.assertEqual(result[3].entityName, 'GUEST')
        self.assertEqual(result[3].permissionType, PermissionType.READ.value)
        self.assertEqual(result[3].entityType, EntityType.USER)
        self.assertEqual(result[4].entityName, 'user1')
        self.assertEqual(result[4].permissionType, PermissionType.READWRITE.value)
        self.assertEqual(result[4].entityType, EntityType.USER)
        self.assertEqual(result[5].entityName, 'user2')
        self.assertEqual(result[5].permissionType, PermissionType.READWRITE.value)
        self.assertEqual(result[5].entityType, EntityType.USER)


class DataShareSettingBuilderTestCase(TestCase):
    def test_builder(self):
        result = DataShareSettingBuilder().share_to_user('user', DataPermissionType.DOWNLOAD).share_to_everyone(
            DataPermissionType.DOWNLOAD).share_to_group('group_id', DataPermissionType.DOWNLOAD).share_to_users(
            ['user1', 'user2'], DataPermissionType.DELETE).build()
        self.assertEqual(result[0].entityName, 'user')
        self.assertEqual(result[0].dataPermissionType, DataPermissionType.DOWNLOAD.value)
        self.assertEqual(result[0].entityType, EntityType.USER)
        self.assertEqual(result[1].entityName, 'GUEST')
        self.assertEqual(result[1].dataPermissionType, DataPermissionType.DOWNLOAD.value)
        self.assertEqual(result[1].entityType, EntityType.USER)
        self.assertEqual(result[2].entityId, 'group_id')
        self.assertEqual(result[2].dataPermissionType, DataPermissionType.DOWNLOAD.value)
        self.assertEqual(result[2].entityType, EntityType.IPORTALGROUP)
        self.assertEqual(result[3].entityName, 'user1')
        self.assertEqual(result[3].dataPermissionType, DataPermissionType.DELETE.value)
        self.assertEqual(result[3].entityType, EntityType.USER)
        self.assertEqual(result[4].entityName, 'user2')
        self.assertEqual(result[4].dataPermissionType, DataPermissionType.DELETE.value)
        self.assertEqual(result[4].entityType, EntityType.USER)
