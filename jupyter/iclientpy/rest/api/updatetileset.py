import re
import time
import uuid
from typing import List
from iclientpy.rest.api.model import Rectangle2D, Point2D
from iclientpy.rest.api.management import ServiceType, TileSize, OutputFormat, PostWorkspaceParameter, PostTileJobsItem, \
    BuildState, PostTilesetUpdateJobs, SMTilesTileSourceInfo, TilesetExportJobRunState, TileType
from iclientpy.rest.apifactory import APIFactory


def update_smtilestileset(address: str, username: str, password: str, w_loc: str, map_name: str,
                          original_point: tuple, cache_bounds: tuple, u_loc: str,
                          scale: List[float], w_servicetypes: List[ServiceType] = [ServiceType.RESTMAP],
                          tile_size: TileSize = TileSize.SIZE_256, tile_type: TileType = TileType.Image,
                          format: OutputFormat = OutputFormat.PNG, epsgcode: int = -1, storageid: str = None,
                          storageconfig: SMTilesTileSourceInfo = None):
    if len(original_point) is not 2:
        raise Exception("切图原点坐标长度错误")
    tem_original_point = Point2D()
    tem_original_point.x = original_point[0]
    tem_original_point.y = original_point[1]
    if len(cache_bounds) is not 4:
        raise Exception("切图范围长度错误")
    tem_cache_Bounds = Rectangle2D()
    tem_cache_Bounds.leftBottom = Point2D()
    tem_cache_Bounds.leftBottom.x = cache_bounds[0]
    tem_cache_Bounds.leftBottom.y = cache_bounds[1]
    tem_cache_Bounds.rightTop = Point2D()
    tem_cache_Bounds.rightTop.x = cache_bounds[2]
    tem_cache_Bounds.rightTop.y = cache_bounds[3]
    api = APIFactory(address, username, password)
    mng = api.management()
    post_param = PostWorkspaceParameter()
    post_param.workspaceConnectionInfo = w_loc
    post_param.servicesTypes = w_servicetypes
    pwr = mng.post_workspaces(post_param)
    wkn = re.findall('services/[^/]*', pwr[0].serviceAddress)[0].lstrip('services/')
    post_tile_jobs_param = PostTileJobsItem()
    post_tile_jobs_param.dataConnectionString = wkn
    post_tile_jobs_param.mapName = map_name
    post_tile_jobs_param.scaleDenominators = scale
    post_tile_jobs_param.tileSize = tile_size
    post_tile_jobs_param.tileType = tile_type
    post_tile_jobs_param.format = format
    post_tile_jobs_param.epsgCode = epsgcode
    post_tile_jobs_param.storageID = storageid if storageid is not None else 'iclientpy_' + uuid.uuid1().__str__()
    if storageconfig is not None:
        post_tile_jobs_param.storeConfig = storageconfig
    else:
        post_tile_jobs_param.storeConfig = SMTilesTileSourceInfo()
        post_tile_jobs_param.storeConfig.type = 'SMTiles'
        post_tile_jobs_param.storeConfig.outputPath = '../webapps/iserver/output/sqlite_' + uuid.uuid1().__str__()
    post_tile_jobs_param.originalPoint = tem_original_point
    post_tile_jobs_param.cacheBounds = tem_cache_Bounds
    ptjr = mng.post_tilejobs(post_tile_jobs_param)
    while (mng.get_job(ptjr.newResourceID).state.runState is BuildState.BUILDING):
        time.sleep(5)
    gjr = mng.get_job(ptjr.newResourceID)
    if (gjr.state.runState is not BuildState.COMPLETED):
        raise Exception('切图失败')
    post_tile_update_param = PostTilesetUpdateJobs()
    post_tile_update_param.scaleDenominators = scale
    post_tile_update_param.bounds = tem_cache_Bounds
    post_tile_update_param.targetTilesetIdentifier = u_loc
    post_tile_update_param.targetTileSourceInfo = SMTilesTileSourceInfo()
    post_tile_update_param.targetTileSourceInfo.type = 'SMTiles'
    post_tile_update_param.targetTileSourceInfo.outputPath = "/".join(u_loc.split('/')[:-1])
    post_tile_update_param.sourceTilesetIdentifier = gjr.targetTilesetInfo.filePath
    post_tile_update_param.sourceTileSourceInfo = SMTilesTileSourceInfo()
    post_tile_update_param.sourceTileSourceInfo.type = 'SMTiles'
    post_tile_update_param.sourceTileSourceInfo.outputPath = post_tile_jobs_param.storeConfig.outputPath
    ptur = mng.post_tilesetupdatejobs(post_tile_update_param)
    gtur = mng.get_tilesetupdatejob(ptur.newResourceID)
    while (not hasattr(gtur.state, 'runState') or gtur.state.runState is TilesetExportJobRunState.RUNNING):
        time.sleep(5)
        gtur = mng.get_tilesetupdatejob(ptur.newResourceID)
    if (gtur.state.runState is not TilesetExportJobRunState.COMPLETED):
        raise Exception('更新切片失败')
