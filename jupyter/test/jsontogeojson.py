import json
from geojson import Feature, FeatureCollection, MultiPolygon, Polygon
import geojson
import geojson_utils

# with open('./provinceialdata.json', 'r', encoding='utf-8') as jsonfile:
#     privs = json.load(jsonfile)
#     fc = []
#     for i in range(0, len(privs)):
#         name = privs[i]['name']
#         points = [tuple(x.values()) for x in privs[i]['data']]
#         priv = MultiPolygon(coordinates=[[points]])
#         privFeature = Feature(geometry=priv, properties={'name': name})
#         fc.append(privFeature)
#     print(len(fc))
#     with open('./output.json', 'w', encoding='utf-8')as out:
#         geojson.dump(obj=FeatureCollection(fc), fp=out, ensure_ascii=False)

# def centorids(poly):
#     """
#     get the centroid of polygon
#     adapted from http://paulbourke.net/geometry/polyarea/javascript.txt
#     Keyword arguments:
#     poly -- polygon geojson object
#     return polygon centroid
#     """
#     # f_total = 0
#     x_total = 0
#     y_total = 0
#     # TODO: polygon holes at coordinates[1]
#     points = poly['coordinates'][0]
#     x0 = poly['coordinates'][0][0][1]
#     y0 = poly['coordinates'][0][0][0]
#     count = len(points)
#
#     for i in range(0, count - 1):
#         p1_x = points[i][1]
#         p1_y = points[i][0]
#         p2_x = points[i + 1][1]
#         p2_y = points[i + 1][0]
#
#         # f_total = p1_x * p2_y - p2_x * p1_y
#         x_total += (p1_x + p2_x - 2 * x0) * ((p1_x - x0) * (p2_y - y0) - (p2_x - x0) * (p1_y - y0))
#         y_total += (p1_y + p2_y - 2 * y0) * ((p1_x - x0) * (p2_y - y0) - (p2_x - x0) * (p1_y - y0))
#
#     six_area = geojson_utils.area(poly) * 6
#     return {'type': 'Point', 'coordinates': [y0 + x_total / six_area, x0 + y_total / six_area]}
#
#
# with open('./chinageojson.json', 'r', encoding='utf-8') as file:
#     fc = geojson.load(file)
#     for feature in fc["features"]:
#         poly = Polygon(coordinates=feature["geometry"]["coordinates"][0])
#         centorid = centorids(poly)
#         feature["properties"]["cp"] = centorid["coordinates"]
#     with open('./outputchina2.json', 'w', encoding='utf-8') as out:
#         geojson.dump(obj=FeatureCollection(fc), fp=out, ensure_ascii=False)

shengfen = '''
[
    ["北京市", 116.407283, 39.904557, 22023, 24982, 27760, 30350, 33337],
    ["天津市", 117.215268, 39.120963, 15200, 17852, 20624, 22984, 26261],
    ["上海市", 121.47398, 31.230075, 26582, 32271, 35439, 36893, 39223],
    ["重庆市", 106.551417, 29.563228, 8494, 9723, 11832, 13655, 15270],
    ["黑龙江省", 126.661901, 45.742659, 7922, 9121, 10634, 11601, 12978],
    ["吉林省", 125.326104, 43.89604, 8538, 9241, 10811, 12276, 13676],
    ["辽宁省", 123.43707, 41.835528, 10906, 13016, 15635, 17999, 20156],
    ["山西省", 112.562359, 37.874938, 6854, 8447, 9746, 10829, 12078],
    ["河北省", 114.469767, 38.036032, 7193, 8057, 9551, 10749, 11557],
    ["陕西省", 108.953051, 34.267153, 7154, 8474, 10053, 11852, 13206],
    ["甘肃省", 103.826321, 36.059405, 5509, 6234, 7493, 8542, 9616],
    ["四川省", 104.075463, 30.651149, 6863, 8182, 9903, 11280, 12485],
    ["贵州省", 106.707603, 26.597997, 5456, 6218, 7389, 8372, 9541],
    ["云南省", 102.709129, 25.046619, 5976, 6811, 8278, 9782, 11224],
    ["海南省", 109.691225, 19.047108,  6695, 7553, 9238, 10634, 11712],
    ["浙江省", 120.154526, 30.267173, 15867, 18274, 21346, 22845, 24771],
    ["山东省", 117.020411, 36.669569, 10494, 11606, 13524, 15095, 16728],
    ["江苏省", 118.763288, 32.061173, 11993, 14035, 17167, 19452, 23585],
    ["安徽省", 117.285057, 31.861554, 6829, 8237, 10055, 10978, 11618],
    ["福建省", 119.296405, 26.100023, 11336, 13187, 14958, 16144, 17115],
    ["江西省", 115.908871, 28.674211, 6212, 7989, 9523, 10573, 11910],
    ["河南省", 113.687284, 34.767907, 6607, 7837, 9171, 10380, 11782],
    ["湖北省", 114.341949, 30.545553, 7791, 8977, 10873, 12283, 13912],
    ["湖南省", 112.983553, 28.116295, 7929, 8922, 10547, 11740, 12920],
    ["广东省", 113.265246, 23.130964, 15243, 17211, 19578, 21823, 23739],
    ["青海省", 101.780064, 36.620995, 6501, 7326, 8744, 10289, 12070],
    ["西藏自治区", 91.117774, 29.647017, 3985, 4469, 4730, 5340, 6275],
    ["广西壮族自治区", 108.327509, 22.816721, 6968, 7920, 9181, 10519, 11710],
    ["内蒙古自治区", 111.765996, 40.817419, 9460, 10925, 13264, 15196, 17168],
    ["宁夏回族自治区", 106.258639, 38.471179, 7918, 8992, 10937, 12120, 13537],
    ["新疆维吾尔自治区", 87.626951, 43.793217, 5945, 7400, 8895, 10675, 11401]
]'''
privjson = json.loads(shengfen)
with open('./outputchina2.json', 'r', encoding='utf-8') as file:
    fc = geojson.load(file)
    for feature in fc["features"]:
        for sheng in privjson:
            if sheng[0] in feature["properties"]["name"]:
                feature["properties"]["cp"] = [sheng[1], sheng[2]]
    with open('./outputchina3.json', 'w', encoding='utf-8') as out:
        geojson.dump(obj=FeatureCollection(fc), fp=out, ensure_ascii=False)
