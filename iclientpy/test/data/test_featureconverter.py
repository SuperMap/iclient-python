from unittest import TestCase
import geopandas
import geojson
from iclientpy.data.featuresconverter import from_geojson_feature, to_geojson_feature, \
    to_geojson_features, from_geojson_features
from iclientpy.rest.api.model import Feature, Geometry, Point2D


class FeatureConverterTestCase(TestCase):
    def test_fromgeojsonfeature(self):
        g_f = geojson.Feature()
        point = geojson.Point(coordinates=[12, 14])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = point
        feature = from_geojson_feature(g_f)
        self.assertEqual(feature.geometry.points[0].x, 12)
        self.assertEqual(feature.geometry.points[0].y, 14)
        self.assertEqual(feature.fieldNames, ['name', 'value'])
        self.assertEqual(feature.fieldValues, ['name', 'value'])

    def test_togeojsonfeature(self):
        s_f = Feature()
        s_f.fieldNames = ["name"]
        s_f.fieldValues = ["value"]
        s_f.geometry = Geometry()
        s_p = Point2D()
        s_p.x = 12
        s_p.y = 14
        s_f.geometry.points = []
        s_f.geometry.points.append(s_p)
        geo = to_geojson_feature(s_f)
        self.assertEqual(geo['geometry']['coordinates'][0], 12)
        self.assertEqual(geo['geometry']['coordinates'][1], 14)
        self.assertEqual(geo['properties'], {"name": "value"})

    def test_fromgeojsonfeatures(self):
        g_f = geojson.Feature()
        point = geojson.Point(coordinates=[12, 14])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = point
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].geometry.points[0].x, 12)
        self.assertEqual(result[0].geometry.points[0].y, 14)
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_fromgeojsonfeatures_line(self):
        g_f = geojson.Feature()
        line = geojson.LineString(coordinates=[[100.0, 0.0], [101.0, 1.0]])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = line
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(result[0].geometry.parts, [2])
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_fromgeojsonfeatures_multiline(self):
        g_f = geojson.Feature()
        line = geojson.MultiLineString(coordinates=[[[100.0, 0.0], [101.0, 1.0]], [[102.0, 2.0], [103.0, 3.0]]])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = line
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(result[0].geometry.parts, [2, 2])
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_fromgeojsonfeatures_polygon(self):
        g_f = geojson.Feature()
        polygon = geojson.Polygon(coordinates=[[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = polygon
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(result[0].geometry.parts, [5])
        self.assertEqual(result[0].geometry.partTopo, [1])
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_fromgeojsonfeatures_polygon_with_holes(self):
        g_f = geojson.Feature()
        polygon = geojson.Polygon(coordinates=[[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                                               [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                                               [[100.4, 0.4], [100.6, 0.4], [100.6, 0.6], [100.4, 0.6], [100.4, 0.4]]])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = polygon
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(result[0].geometry.parts, [5, 5, 5])
        self.assertEqual(result[0].geometry.partTopo, [1, -1, 1])
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_fromgeojsonfeatures_multipolygon(self):
        g_f = geojson.Feature()
        line = geojson.MultiPolygon(
            coordinates=[
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]],
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                 [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
            ])
        g_f['properties'] = {"name": "name", "value": "value"}
        g_f['geometry'] = line
        g_fc = geojson.FeatureCollection([g_f])
        s_fs = from_geojson_features(g_fc)
        result = list(s_fs)
        self.assertEqual(result[0].geometry.parts, [5, 5, 5])
        self.assertEqual(result[0].geometry.partTopo, [1, 1, -1])
        self.assertEqual(result[0].fieldNames, ['name', 'value'])
        self.assertEqual(result[0].fieldValues, ['name', 'value'])

    def test_togeojsonfeatures(self):
        s_f = Feature()
        s_f.fieldNames = ["name"]
        s_f.fieldValues = ["value"]
        s_f.geometry = Geometry()
        s_p = Point2D()
        s_p.x = 12
        s_p.y = 14
        s_f.geometry.points = []
        s_f.geometry.points.append(s_p)
        feature = to_geojson_features([s_f])
        self.assertEqual(feature['features'][0]['geometry']['coordinates'][0], 12)
        self.assertEqual(feature['features'][0]['geometry']['coordinates'][1], 14)
        self.assertEqual(feature['features'][0]['properties'], {"name": "value"})
