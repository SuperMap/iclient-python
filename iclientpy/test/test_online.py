from unittest import TestCase, mock
from iclientpy.online import Online
from iclientpy.rest.api.model import GetMapsResult, ViewerMap, MethodResult, MyDatasMethodResult, DataItem, Status, \
    DataItemType, MyDataUploadProcess, Layer, GetMyDatasResult
from io import FileIO
from pandas import DataFrame


class MockOnlineAPIFactory:
    def __init__(self, url, *args, **kwargs):
        self._base_url = url
        pass


@mock.patch("iclientpy.online.OnlineAPIFactory", MockOnlineAPIFactory)
class OnlineTestCase(TestCase):
    def test_search_map(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        result = GetMapsResult()
        result.content = []
        maps_service = mock.MagicMock()
        maps_service.get_maps = mock.MagicMock(return_value=result)
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        result = online.search_map()
        self.assertEqual(result, [])

    def test_get_map(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        m = ViewerMap()
        maps_service = mock.MagicMock()
        maps_service.get_map = mock.MagicMock(return_value=m)
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        result = online.get_map('map_id')
        self.assertEqual(result, m)

    def test_upload_data(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        mdmr = MyDatasMethodResult()
        mdmr.childID = 'data_id'
        data_services.post_datas = mock.MagicMock(return_value=mdmr)
        data_services.upload_data = mock.MagicMock(return_value=mdmr)
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        online.get_data = mock.MagicMock()
        data1 = DataItem()
        data1.status = Status.CREATED
        data2 = DataItem()
        data2.status = Status.CREATED
        data3 = DataItem()
        data3.status = Status.OK
        online.get_data.side_effect = [data1, data2, data3]
        online.get_data_upload_progress = mock.MagicMock()
        online.get_data_upload_progress.side_effect = [(0, 100), (50, 100), (100, 100)]
        callback = mock.MagicMock()
        data_content = mock.MagicMock()
        data_content.__class__ = FileIO
        result = online.upload_data('test.json', data_content, DataItemType.JSON, callback)
        self.assertEqual(result, 'data_id')

    def test_upload_dataframe_as_json(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        online.upload_data = mock.MagicMock(return_value='data_id')
        df = mock.MagicMock()
        df.__class__ = DataFrame
        df.to_json = mock.MagicMock(return_value='testtesttest')
        result = online.upload_dataframe_as_json('data', df)
        self.assertEqual(result, 'data_id')

    def test_get_datas(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        res = GetMyDatasResult()
        res.content = []
        data_services.get_datas = mock.MagicMock(return_value=res)
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        result = online.search_data()
        self.assertEqual(result, [])

    def test_get_data(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data = DataItem()
        data_services = mock.MagicMock()
        data_services.get_data = mock.MagicMock(return_value=data)
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        result = online.get_data('data_id')
        self.assertEqual(result, data)

    def test_get_data_upload_progress(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        process = MyDataUploadProcess()
        process.read = 10
        process.total = 100
        data_services.get_upload_process = mock.MagicMock(return_value=process)
        result = online.get_data_upload_progress('data_id')
        self.assertEqual(result, (10, 100))

    def test_create_map(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        maps_service = mock.MagicMock()
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.newResourceID = 'map_id';
        maps_service.post_maps = mock.MagicMock(return_value=res)
        result = online.create_map([Layer()], 3857, 'map', (0, 0), (-180, -90, 180, 90))
        self.assertEqual(result, 'map_id')

    def test_prepare_geojson_layer(self):
        online = Online('test', 'test')
        data_id = 'data_id'
        result = online.prepare_geojson_layer(data_id, 'layer')
        self.assertEqual(result.url, 'https://www.supermapol.com/datas/data_id/content.json')
        self.assertEqual(result.title, 'layer')

    def test_share_data_public(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.put_sharesetting = mock.MagicMock(return_value=res)
        online.share_data('data_id', True)
        data_services.put_sharesetting.assert_called_once()

    def test_share_data_private(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.put_sharesetting = mock.MagicMock(return_value=res)
        online.share_data('data_id', False)
        data_services.put_sharesetting.assert_called_once()

    def test_share_map_public(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        maps_service = mock.MagicMock()
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.put_map_sharesetting = mock.MagicMock(return_value=res)
        online.share_map('map_id', True)
        maps_service.put_map_sharesetting.assert_called_once()

    def test_share_map_private(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        maps_service = mock.MagicMock()
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.put_map_sharesetting = mock.MagicMock(return_value=res)
        online.share_map('map_id', False)
        maps_service.put_map_sharesetting.assert_called_once()

    def test_delete_map(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        maps_service = mock.MagicMock()
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.delete_maps = mock.MagicMock(return_value=res)
        online.delete_map('map_id')
        maps_service.delete_maps.assert_called_once_with(['map_id'])

    def test_delete_maps(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        maps_service = mock.MagicMock()
        online._online.maps_service = mock.MagicMock(return_value=maps_service)
        res = MethodResult()
        res.succeed = True
        maps_service.delete_maps = mock.MagicMock(return_value=res)
        online.delete_maps(['map_id'])
        maps_service.delete_maps.assert_called_once_with(['map_id'])

    def test_delete_data(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.delete_data = mock.MagicMock(return_value=res)
        online.delete_data('data_id')
        data_services.delete_data.assert_called_once_with('data_id')

    def test_delete_datas(self):
        online = Online('test', 'test')
        online._online = mock.MagicMock()
        data_services = mock.MagicMock()
        online._online.datas_service = mock.MagicMock(return_value=data_services)
        res = MethodResult()
        res.succeed = True
        data_services.delete_data = mock.MagicMock(return_value=res)
        online.delete_datas(['data_id', 'data_id2'])
        self.assertEqual(data_services.delete_data.call_count, 2)
        self.assertEqual(data_services.delete_data.call_args_list, [mock.call('data_id'), mock.call('data_id2')])
