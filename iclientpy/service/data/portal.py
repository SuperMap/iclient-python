from geopandas import GeoDataFrame
from IPython.display import display
from ipywidgets import IntProgress
from iclientpy.jupyter import PortalThumbnail
from iclientpy.portal import Portal


def from_geodataframe_to_map(portal: Portal, gdf: GeoDataFrame, data_name: str, map_title: str, layer_name: str):
    progress = IntProgress()
    progress.max = 100
    progress.value = 0
    progress.description = '上传文件：'
    display(progress)

    def refresh_progress(read, total):
        progress.value = read

    data_id = portal.upload_dataframe_as_json(data_name, gdf, callback=refresh_progress)
    layer = portal.prepare_geojson_layer(data_id, layer_name)
    map_id = portal.create_map([layer], 3857, map_title)
    mr = portal.get_map(map_id)
    pm = PortalThumbnail(mr)
    display(pm)
    return map_id
