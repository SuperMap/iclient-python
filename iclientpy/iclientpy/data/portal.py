from io import StringIO, FileIO
from geopandas import GeoDataFrame
from IPython.display import display
from ipywidgets import IntProgress
from iclientpy.rest.apifactory import iPortalAPIFactory
from iclientpy.rest.api.mydatas import MyDatas
from iclientpy.rest.api.mapsservice import MapsService
from iclientpy.jupyter import PortalThumbnail
from iclientpy.rest.api.model import PostMyDatasItem, DataItemType, PostMapsItem, Point2D, Layer, LayerType, SourceType, \
    PrjCoordSys, LayerStyle, Status, PointStyle
import threading


# __default_layer_style = LayerStyle()
# __default_layer_style.pointStyle = PointStyle()
# __default_layer_style.pointStyle.fill = True
# __default_layer_style.pointStyle.fillColor = '#f5222d'
# __default_layer_style.pointStyle.fillOpacity = 0.5
# __default_layer_style.pointStyle.fontOpacity = 0
# __default_layer_style.pointStyle.graphicHeight = 0
# __default_layer_style.pointStyle.graphicOpacity = 0
# __default_layer_style.pointStyle.graphicWidth = 0
# __default_layer_style.pointStyle.graphicXOffset = 0
# __default_layer_style.pointStyle.graphicYOffset = 0
# __default_layer_style.pointStyle.isUnicode = False
# __default_layer_style.pointStyle.labelSelect = False
# __default_layer_style.pointStyle.labelXOffset = 0
# __default_layer_style.pointStyle.labelYOffset = 0
# __default_layer_style.pointStyle.pointRadius = 6
# __default_layer_style.pointStyle.stroke = True
# __default_layer_style.pointStyle.strokeColor = '#3498db'
# __default_layer_style.pointStyle.strokeDashstyle = 'solid'
# __default_layer_style.pointStyle.strokeLinecap = 'round'
# __default_layer_style.pointStyle.strokeOpacity = 1
# __default_layer_style.pointStyle.strokeWidth = 1


def __upload_data_to_portal(ds: MyDatas, data: FileIO, data_id: str):
    ds.upload_my_data(data_id, data)


def __create_data_to_portal(ds: MyDatas, name: str):
    entity = PostMyDatasItem()
    entity.type = DataItemType.JSON
    entity.fileName = name
    return ds.post_my_datas(entity)


def __wait_data_upload_progress(ds: MyDatas, data_id: str):
    progress = IntProgress()
    progress.max = 100
    progress.value = 0
    progress.description = '上传文件：'
    display(progress)
    item = ds.get_my_data(data_id)
    while (item.status != Status.OK):
        result = ds.get_upload_process(data_id)
        item = ds.get_my_data(data_id)
        if (item.status == Status.OK and result.total == -1 and result.read == -1):
            result.total = 100
            result.read = 100
        progress.value = result.read


def __prepare_base_layer():
    base_layer = Layer()
    base_layer.url = 'http://t1.tianditu.cn'
    base_layer.title = '天地图'
    base_layer.zindex = 0
    base_layer.layerType = LayerType.BASE_LAYER
    base_layer.name = '天地图'
    base_layer.isVisible = True
    base_layer.type = SourceType.TIANDITU_VEC
    base_layer_label = Layer()
    base_layer_label.url = 'http://t1.tianditu.cn'
    base_layer_label.title = '天地图-标签'
    base_layer_label.zindex = 1
    base_layer_label.layerType = LayerType.OVERLAY_LAYER
    base_layer_label.name = '天地图-标签'
    base_layer_label.isVisible = True
    base_layer_label.type = SourceType.TIANDITU_VEC
    return [base_layer, base_layer_label]


def __prepare_layer(layer_name: str, data_url: str, layer_style: LayerStyle):
    layer = Layer()
    layer.prjCoordSys = PrjCoordSys()
    layer.prjCoordSys.epsgCode = 4326
    layer.name = layer_name
    layer.layerType = LayerType.FEATURE_LAYER
    layer.zindex = 2
    layer.isVisible = True
    layer.title = layer_name
    layer.style = layer_style
    # layer.identifier = 'THEME'
    layer.cartoCSS = '{"isAddFile":true,"needTransform":"needTransform"}'
    layer.url = data_url + '/content.json'
    # layer.themeSettings = '{"type":"VECTOR","filter":"","settings":null,"vectorType":"REGION","colors":null,"heatUnit":"","labelField":null,"labelFont":"仿宋","labelColor":"#000000","titleArray":["地区","2015年","2014年","2013年","2012年","2011年","2010年","2009年","2008年","2007年","2006年"],"themeLength":6,"rangeMethod":""}'
    return [layer]


def __create_map_on_portal(maps: MapsService, map_title: str, layer_name: str, data_url: str,
                           layer_style: LayerStyle = None):
    entity = PostMapsItem()
    entity.center = Point2D()
    entity.center.x = 12626762.220726
    entity.center.y = 2619886.8435466
    entity.epsgCode = 3857
    entity.title = map_title
    entity.layers = __prepare_base_layer() + __prepare_layer(layer_name, data_url, layer_style)
    return maps.post_maps(entity)


def from_geodataframe_pubilsh(api: iPortalAPIFactory, geodataframe: GeoDataFrame, data_name: str, map_title: str,
                              layer_name: str, layer_style: LayerStyle = None):
    mds = api.mydatas_service()
    maps = api.maps_service()
    cdr = __create_data_to_portal(mds, data_name)
    data_id = cdr.childID

    with StringIO(geodataframe.to_json()) as dataf:
        threading.Thread(target=__wait_data_upload_progress, args=(mds, data_id)).start()
        __upload_data_to_portal(mds, dataf, data_id)
    data_url = api._base_url + '/datas/' + data_id
    cmr = __create_map_on_portal(maps, map_title, layer_name, data_url, layer_style)
    mr = maps.get_map(cmr.newResourceID)
    pm = PortalThumbnail(mr)
    display(pm)
    return mr
