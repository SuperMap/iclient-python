import re
import time
import uuid
import os
from typing import List
import progressbar
from iclientpy.rest.api.model import Rectangle2D, Point2D, ServiceType, TileSize, OutputFormat, PostWorkspaceParameter, \
    PostTileJobsItem, BuildState, PostTilesetUpdateJobs, SMTilesTileSourceInfo, TilesetExportJobRunState, TileType, \
    TileSourceInfo
from iclientpy.rest.api.management import Management
from iclientpy.rest.api.model import PostFileUploadTasksParam, FileUploadState
from iclientpy.rest.apifactory import APIFactory
from .cacheutils import provider_setting_to_tile_source_info
from iclientpy.dtojson import to_json_str
import zipfile
from io import BufferedIOBase


def output(tip: str):
    print(tip)


field_and_desc = {
    'address': '地址',
    'username': '用户名',
    'password': '密码',
    'token': 'token',
    'component_name': '待更新缓存服务名称',
    'w_loc': '工作空间路径',
    'map_name': '切图地图名称',
    'original_point': '切图原点',
    'cache_bounds': '缓存范围',
    'scale': '缓存比例尺分母',
    'w_servicetype': '工作空间服务类型',
    'tile_size': '切片大小',
    'tile_type': '切片类型',
    'format': '切片输出格式',
    'epsg_code': '投影',
    'remote_workspace': '远程工作空间',
    'source_component_name': '缓存更新数据来源服务',
    'update': '更新服务缓存'
}


def confirm(**d):
    output('执行参数如下：')
    for field in field_and_desc.keys():
        if field in d:
            val = ''
            if d[field] is None:
                val = ''
            elif isinstance(d[field], tuple):
                val = ','.join(map(str, d[field]))
            elif isinstance(d[field], bool):
                val = str(d[field])
            elif not isinstance(d[field], str):
                val = to_json_str(d[field])
            else:
                val = d[field]
            output(field_and_desc[field] + ": " + val)
    print('是否继续?(Y/N)', end=' ')
    return input('')


def recache_tileset(address: str, username: str, password: str, component_name: str, map_name: str,
                    storageid: str = None, tileset_name: str = None, token: str = None):
    api = APIFactory(address, username, password, token)
    mng = api.management()
    storage_info = mng.get_datastore(storageid)
    tilesetinfos = [info for info in storage_info.tilesetInfos if info.metaData.mapName == map_name]
    if len(tilesetinfos) != 1 and tileset_name is None:
        raise Exception("存在多个地图名称相同的缓存")
    tilesetinfo = None
    if len(tilesetinfos) == 1:
        tilesetinfo = tilesetinfos[0]
    else:
        for info in tilesetinfos:
            if info.name == tileset_name:
                tilesetinfo = info

    storage_config = storage_info.tileSourceInfo
    post_tile_jobs_param = PostTileJobsItem()
    post_tile_jobs_param.dataConnectionString = component_name
    post_tile_jobs_param.mapName = map_name
    post_tile_jobs_param.scaleDenominators = tilesetinfo.metaData.scaleDenominators
    if tilesetinfo.metaData.tileHeight == 512:
        post_tile_jobs_param.tileSize = TileSize.SIZE_512
    elif tilesetinfo.metaData.tileHeight == 1024:
        post_tile_jobs_param.tileSize = TileSize.SIZE_1024
    else:
        post_tile_jobs_param.tileSize = TileSize.SIZE_256
    post_tile_jobs_param.tileType = tilesetinfo.metaData.tileType
    post_tile_jobs_param.format = tilesetinfo.metaData.tileFormat
    post_tile_jobs_param.epsgCode = tilesetinfo.metaData.prjCoordSys.epsgCode
    post_tile_jobs_param.storeConfig = storage_config
    post_tile_jobs_param.originalPoint = tilesetinfo.metaData.originalPoint
    post_tile_jobs_param.cacheBounds = tilesetinfo.metaData.bounds
    post_tile_jobs_param.tileVersionDescription = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_tile_jobs_param.createNewTileVersion = True
    ptjr = mng.post_tilejobs(post_tile_jobs_param)
    jobstate = mng.get_tilejob(ptjr.newResourceID).state

    bar = _process_bar('切图', _PercentageCounter(), jobstate.total)
    while (jobstate.runState is BuildState.BUILDING):
        time.sleep(5)
        jobstate = mng.get_tilejob(ptjr.newResourceID).state
        bar.update(jobstate.completed)

    gjr = mng.get_tilejob(ptjr.newResourceID)
    if (gjr.state.runState is not BuildState.COMPLETED):
        raise Exception('切图失败')


def update_smtilestileset(address: str, username: str, password: str, component_name: str, w_loc: str, map_name: str,
                          original_point: tuple, cache_bounds: tuple, scale: List[float] = None,
                          w_servicetypes: List[ServiceType] = [ServiceType.RESTMAP],
                          tile_size: TileSize = TileSize.SIZE_256, tile_type: TileType = TileType.Image,
                          format: OutputFormat = OutputFormat.PNG, epsgcode: int = -1, storageid: str = None,
                          storageconfig: TileSourceInfo = None, remote_workspace: bool = False,
                          quite: bool = False, source_component_name: str = '', update: bool = False,
                          tile_version: str = None, token: str = None):
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
    api = APIFactory(address, username, password, token)
    mng = api.management()
    if scale is None:
        map_service = api.map_service(component_name + '/rest')
        mr = map_service.get_map(map_name)
        scale = [1 / x for x in mr.visibleScales]
    if scale is None or len(scale) is 0:
        raise Exception('无法获取目标地图比例尺且未指定比例尺')
    if storageid is not None:
        storage_info = mng.get_datastore(storageid)
        for info in storage_info.tilesetInfos:
            if info.metaData.mapName == map_name:
                storageconfig = storage_info.tileSourceInfo

    if storageconfig is None:
        storageconfig = SMTilesTileSourceInfo()
        storageconfig.type = 'SMTiles'
        storageconfig.outputPath = '../webapps/iserver/output/sqlite_' + uuid.uuid1().__str__()

    if not quite:
        confirmResult = confirm(address=address, username=username, password=password, component_name=component_name,
                                w_loc=w_loc, map_name=map_name, original_point=original_point,
                                cache_bounds=cache_bounds, scale=scale, w_servicetype=w_servicetypes,
                                tile_size=tile_size, tile_type=tile_type, format=format, epsg_code=epsgcode,
                                storageid=storageid, remote_workspace=remote_workspace,
                                source_component_name=source_component_name, update=update, token=token)
        if confirmResult.lower() == 'n':
            return

    wkn = source_component_name
    if not update:
        param = PostFileUploadTasksParam()
        if remote_workspace:
            remote_workspace_file_full_path = w_loc
        else:
            pfutsr = mng.post_fileuploadtasks(param)
            remote_workspace_file_full_path = _upload_workspace_file(mng, w_loc, pfutsr.newResourceID)
            gfutr = mng.get_fileuploadtask(pfutsr.newResourceID)
            if gfutr.state is not FileUploadState.COMPLETED:
                raise Exception('文件上传失败')
        post_param = PostWorkspaceParameter()
        post_param.workspaceConnectionInfo = remote_workspace_file_full_path
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
    post_tile_jobs_param.storeConfig = storageconfig
    post_tile_jobs_param.originalPoint = tem_original_point
    post_tile_jobs_param.cacheBounds = tem_cache_Bounds
    post_tile_jobs_param.tileVersionDescription = tile_version
    ptjr = mng.post_tilejobs(post_tile_jobs_param)
    jobstate = mng.get_tilejob(ptjr.newResourceID).state

    bar = _process_bar('切图', _PercentageCounter(), jobstate.total)
    while (jobstate.runState is BuildState.BUILDING):
        time.sleep(5)
        jobstate = mng.get_tilejob(ptjr.newResourceID).state
        bar.update(jobstate.completed)

    gjr = mng.get_tilejob(ptjr.newResourceID)
    if (gjr.state.runState is not BuildState.COMPLETED):
        raise Exception('切图失败')

    if isinstance(storageconfig, SMTilesTileSourceInfo):
        post_tile_update_param = PostTilesetUpdateJobs()
        post_tile_update_param.scaleDenominators = scale
        post_tile_update_param.bounds = tem_cache_Bounds
        post_tile_update_param.targetTilesetIdentifier = None
        post_tile_update_param.targetTileSourceInfo = _get_tile_source_info_from_service(mng, component_name)
        post_tile_update_param.sourceTilesetIdentifier = gjr.targetTilesetInfo.filePath
        post_tile_update_param.sourceTileSourceInfo = SMTilesTileSourceInfo()
        post_tile_update_param.sourceTileSourceInfo.type = 'SMTiles'
        post_tile_update_param.sourceTileSourceInfo.outputPath = post_tile_jobs_param.storeConfig.outputPath
        ptur = mng.post_tilesetupdatejobs(post_tile_update_param)
        gtur = mng.get_tilesetupdatejob(ptur.newResourceID)
        bar = _process_bar('更新', _PercentageCounter(), gtur.state.total)
        while (not hasattr(gtur.state, 'runState') or gtur.state.runState is TilesetExportJobRunState.RUNNING):
            time.sleep(5)
            gtur = mng.get_tilesetupdatejob(ptur.newResourceID)
            bar.update(gtur.state.actualCompleted)
        if (gtur.state.runState is not TilesetExportJobRunState.COMPLETED):
            raise Exception('更新切片失败')
    if not update:
        mng.delete_mapcomponent(name=wkn)


def _get_tile_source_info_from_service(mng: Management, name: str) -> TileSourceInfo:
    service_info = mng.get_service(name)
    return provider_setting_to_tile_source_info(service_info.providers[0].spSetting.config)


def _custom_len(value):
    total = 0
    for c in value:
        if c >= u'\u4e00' and c <= u'\u9fa5':
            # 中文字符宽度为2
            total += 2
        else:
            total += 1
    return total


def _process_bar(name: str, counter: progressbar.Counter, max_value: int) -> progressbar.ProgressBar:
    return progressbar.ProgressBar(
        widgets=[
            name + '进度: ',
            progressbar.Bar(),
            ' ',
            counter,
        ],
        len_func=_custom_len,
        max_value=max_value
    )


class _PercentageCounter(progressbar.Counter):
    def __call__(self, progress, data, format=None):
        # processbar似乎计算宽度有问题导致换行，给多加几个空格让希望显示的内容不换行。
        return '{0:5}%    '.format(round(data['value'] / data['max_value'] * 100, 2))


class _DisableSeekAndTellIOWrapper(BufferedIOBase):
    """
    zipfile压缩文件的时候会通过seek和tell来定位写入zip文件头信息。
    但是管道流不能正常的seek和tell，故通过这个wrapper来禁用seek和tell，从而强迫zipfile使用流式压缩
    """

    def __init__(self, towrap):
        self._wrapped = towrap

    def seek(self, *args, **kwargs):
        raise AttributeError()

    def tell(self, *args, **kwargs):
        raise AttributeError()

    def seekable(self, *args, **kwargs):
        return False

    def __getattribute__(self, item):
        if item in ('_wrapped', 'seek', 'seekable', 'tell'):
            return object.__getattribute__(self, item)
        return self._wrapped.__getattribute__(item)

    def __enter__(self):
        self._wrapped.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self._wrapped.__exit__(*args, **kwargs)


def _zip_files_in_workspace_directory(w_loc: str) -> BufferedIOBase:
    rfd, wfd = os.pipe()

    def zip_in_thread(wfd):
        dirname = os.path.dirname(w_loc)
        with os.fdopen(wfd, 'wb') as outputfile:
            with zipfile.ZipFile(_DisableSeekAndTellIOWrapper(outputfile), 'w') as zfile:
                for root, dirs, files in os.walk(dirname):
                    for name in files:
                        fullpath = os.path.join(root, name)
                        arcname = os.path.relpath(fullpath, dirname)
                        zfile.write(fullpath, arcname=arcname)

    import threading
    threading.Thread(target=zip_in_thread, args=(wfd,), name='zip ' + w_loc).start()
    return os.fdopen(rfd, 'rb')


def _upload_workspace_file(mng: Management, w_loc: str, upload_task_id: str) -> str:
    r_post = None  # type PostFileUploadTaskResult
    if w_loc.lower().endswith('.zip'):
        with zipfile.ZipFile(w_loc) as zipf:
            zipfns = zipf.namelist()
            workspace_file_name = [item for item in zipfns if item.endswith('.sxwu')][0]
        with open(w_loc, 'rb') as wf:
            r_post = mng.post_fileuploadtask(upload_task_id, wf, './' + os.path.basename(w_loc), overwrite=True,
                                             unzip=True)
    else:
        workspace_file_name = os.path.basename(w_loc)
        with _zip_files_in_workspace_directory(w_loc) as wf:
            r_post = mng.post_fileuploadtask(upload_task_id, wf, './' + workspace_file_name.split('.')[0] + '.zip',
                                             overwrite=True, unzip=True)
    return r_post.filePath + './' + workspace_file_name
