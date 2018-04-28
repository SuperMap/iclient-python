from unittest import TestCase, mock
from iclientpy.data.portal import from_geodataframe_to_map
from iclientpy.rest.api.model import ViewerMap, Layer


class test_portal(TestCase):
    def test_from_geodataframe_publish(self):
        portal = mock.MagicMock()
        portal.upload_dataframe_as_json = mock.MagicMock(return_value='data_id')
        layer = Layer()
        vmap = ViewerMap()
        portal.prepare_geojson_layer = mock.MagicMock(return_value=layer)
        portal.create_map = mock.MagicMock(return_value='map_id')
        portal.get_map = mock.MagicMock(return_value=vmap)
        gdf = mock.MagicMock()
        result = from_geodataframe_to_map(portal, gdf, 'data', 'map', 'layer')
        self.assertEqual(result, 'map_id')
