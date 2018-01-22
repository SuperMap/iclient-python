import re
import time
from typing import List
from iclientpy.rest.api.model import Rectangle2D, Point2D
from iclientpy.rest.api.management import ServiceType, TileSize, OutputFormat, PostWorkspaceParameter, PostTileJobsItem, \
    BuildState, PostTilesetUpdateJobs, SMTilesTileSourceInfo, TilesetExportJobRunState
from iclientpy.rest.apifactory import APIFactory


def update_smtilestileset(address: str, username: str, password: str, w_loc: str, w_servicetypes: List[ServiceType],
                          map_name: str, scale: List[float], tile_size: TileSize, tile_type: str, format: OutputFormat,
                          epsgcode: int, storageid: str, storageconfig: SMTilesTileSourceInfo, original_point: Point2D,
                          cacheBounds: Rectangle2D, u_loc: str, bounds: Rectangle2D):
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
    post_tile_jobs_param.storageID = storageid
    post_tile_jobs_param.storeConfig = storageconfig
    post_tile_jobs_param.originalPoint = original_point
    post_tile_jobs_param.cacheBounds = cacheBounds
    ptjr = mng.post_tilejobs(post_tile_jobs_param)
    while (mng.get_job(ptjr.newResourceID).state.runState is BuildState.BUILDING):
        time.sleep(5)
    gjr = mng.get_job(ptjr.newResourceID)
    if (gjr.state.runState is not BuildState.COMPLETED):
        raise Exception('切图失败')
    post_tile_update_param = PostTilesetUpdateJobs()
    post_tile_update_param.scaleDenominators = scale
    post_tile_update_param.bounds = bounds
    post_tile_update_param.targetTilesetIdentifier = u_loc
    post_tile_update_param.targetTileSourceInfo = SMTilesTileSourceInfo()
    post_tile_update_param.targetTileSourceInfo.type = 'SMTiles'
    post_tile_update_param.targetTileSourceInfo.outputPath = "/".join(u_loc.split('/')[:-1])
    post_tile_update_param.sourceTilesetIdentifier = gjr.targetTilesetInfo.filePath
    post_tile_update_param.sourceTileSourceInfo = SMTilesTileSourceInfo()
    post_tile_update_param.sourceTileSourceInfo.type = 'SMTiles'
    post_tile_update_param.sourceTileSourceInfo.outputPath = storageconfig.outputPath
    ptur = mng.post_tilesetupdatejobs(post_tile_update_param)
    while (mng.get_tilesetupdatejob(ptur.newResourceID).state.runState is TilesetExportJobRunState.RUNNING):
        time.sleep(5)
    gtur = mng.get_tilesetupdatejob(ptur.newResourceID)
    if (gtur.state.runState is not TilesetExportJobRunState.COMPLETED):
        raise Exception('更新切片失败')
