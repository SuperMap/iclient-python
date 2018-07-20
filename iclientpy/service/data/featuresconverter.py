import geojson
from fiona import BytesCollection
from geopandas import GeoDataFrame
import iclientpy.rest.api.model as icp_model


def __to_geojson_point(s_geo: icp_model.Geometry):
    coordinates = []
    for point in s_geo.points:
        coordinates.append([point.x, point.y])
    if len(coordinates) == 1:
        geo = geojson.Point(coordinates=coordinates[0])
    else:
        geo = geojson.MultiPoint(coordinates=coordinates)
    return geo


def __from_geojson_point(geo):
    geometry = icp_model.Geometry()
    geometry.points = []
    geometry.parts = []
    geometry.partTopo = None
    geometry.type = icp_model.GeometryType.POINT
    if isinstance(geo, geojson.Point):
        geometry.parts.append(1)
        p = icp_model.Point2D()
        p.x = geo['coordinates'][0]
        p.y = geo['coordinates'][1]
        geometry.points.append(p)
    elif isinstance(geo, geojson.MultiPoint):
        for x, y in geo['coordinates']:
            geometry.parts.append(1)
            p = icp_model.Point2D()
            p.x = x
            p.y = y
            geometry.points.append(p)
    return geometry


def __from_geojson_line(geo):
    geometry = icp_model.Geometry()
    geometry.points = []
    geometry.parts = []
    geometry.partTopo = None
    geometry.type = icp_model.GeometryType.LINE
    if isinstance(geo, geojson.LineString):
        geometry.parts.append(len(geo['coordinates']))
        for x, y in geo['coordinates']:
            p = icp_model.Point2D()
            p.x = x
            p.y = y
            geometry.points.append(p)
    elif isinstance(geo, geojson.MultiLineString):
        for line in geo['coordinates']:
            geometry.parts.append(len(line))
            for x, y in line:
                p = icp_model.Point2D()
                p.x = x
                p.y = y
                geometry.points.append(p)
    return geometry


def __from_geojson_polygon(geo):
    geometry = icp_model.Geometry()
    geometry.points = []
    geometry.parts = []
    geometry.partTopo = []
    geometry.type = icp_model.GeometryType.REGION
    if isinstance(geo, geojson.Polygon):
        with_holes = len(geo['coordinates']) > 1
        index = 0
        for polygon in geo['coordinates']:
            geometry.parts.append(len(polygon))
            geometry.partTopo.append(-1 if with_holes and index % 2 == 1 else 1)
            index += 1
            for x, y in polygon:
                p = icp_model.Point2D()
                p.x = x
                p.y = y
                geometry.points.append(p)
    elif isinstance(geo, geojson.MultiPolygon):
        for s_polygon in geo['coordinates']:
            with_holes = len(s_polygon) > 1
            index = 0
            for polygon in s_polygon:
                geometry.parts.append(len(polygon))
                geometry.partTopo.append(-1 if with_holes and index % 2 == 1 else 1)
                index += 1
                for x, y in polygon:
                    p = icp_model.Point2D()
                    p.x = x
                    p.y = y
                    geometry.points.append(p)
    return geometry


def from_geojson_feature(geo):
    s_feature = icp_model.Feature()
    s_feature.fieldNames = list(geo['properties'].keys())
    s_feature.fieldValues = list(geo['properties'].values())
    if type(geo['geometry']) in (geojson.Point, geojson.MultiPoint):
        s_feature.geometry = __from_geojson_point(geo['geometry'])
    elif type(geo['geometry']) in (geojson.LineString, geojson.MultiLineString):
        s_feature.geometry = __from_geojson_line(geo['geometry'])
    elif type(geo['geometry']) in (geojson.Polygon, geojson.MultiPolygon):
        s_feature.geometry = __from_geojson_polygon(geo['geometry'])
    return s_feature


def to_geojson_feature(feature: icp_model.GetFeatureResult):
    attr = dict(zip(feature.fieldNames, feature.fieldValues))
    geo = __to_geojson_point(feature.geometry)
    return geojson.Feature(geometry=geo, properties=attr)


def from_geojson_features(features: geojson.FeatureCollection):
    return (from_geojson_feature(feature) for feature in features['features'])


def to_geojson_features(features):
    g_features = []
    for s_feature in features:
        g_features.append(to_geojson_feature(s_feature))
    return geojson.FeatureCollection(g_features)


def geojson_2_geodataframe_features(geo):
    with BytesCollection(bytes(geojson.dumps(geo), encoding='utf8')) as features:
        crs = features.crs
        columns = list(features.meta["schema"]["properties"]) + ["geometry"]
        gdf = GeoDataFrame.from_features(features, crs=crs)
        gdf = gdf[columns]
    return gdf


def from_geodataframe_features(gdf: GeoDataFrame):
    geojson_features = geojson.loads(gdf.to_json())
    return from_geojson_features(geojson_features)


def to_geodataframe_features(features):
    g_features = to_geojson_features(features)
    return geojson_2_geodataframe_features(g_features)
