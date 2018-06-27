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
    'component_name': '服务名称',
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


def cache_remoteworkspace(address: str, username: str, password: str, component_name: str, map_name: str,
                          original_point: tuple, cache_bounds: tuple, scale: List[float] = None,
                          tile_size: TileSize = TileSize.SIZE_256, tile_type: TileType = TileType.Image,
                          format: OutputFormat = OutputFormat.PNG, epsg_code: int = -1, storageid: str = None,
                          storageconfig: TileSourceInfo = None, token: str = None, quite: bool = False,
                          job_tile_source_type: str = 'SMTiles'):
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
    if scale is None or len(scale) is 0:
        raise Exception('未指定比例尺')
    if storageid is not None:
        storage_info = mng.get_datastore(storageid)
        for info in storage_info.tilesetInfos:
            if info.metaData.mapName == map_name:
                storageconfig = storage_info.tileSourceInfo

    if storageconfig is None:
        storageconfig = SMTilesTileSourceInfo()
        storageconfig.type = job_tile_source_type
        storageconfig.outputPath = '../webapps/iserver/output/sqlite_' + uuid.uuid1().__str__()

    if not quite:
        confirmResult = confirm(address=address, username=username, password=password, component_name=component_name,
                                map_name=map_name, original_point=original_point, cache_bounds=cache_bounds,
                                scale=scale, tile_size=tile_size, tile_type=tile_type, format=format,
                                epsg_code=epsg_code, storageid=storageid, token=token)
        if confirmResult.lower() == 'n':
            return

    post_tile_jobs_param = PostTileJobsItem()
    post_tile_jobs_param.dataConnectionString = component_name
    post_tile_jobs_param.mapName = map_name
    post_tile_jobs_param.scaleDenominators = scale
    post_tile_jobs_param.tileSize = tile_size
    post_tile_jobs_param.tileType = tile_type
    post_tile_jobs_param.format = format
    post_tile_jobs_param.epsgCode = epsg_code
    post_tile_jobs_param.storeConfig = storageconfig
    post_tile_jobs_param.originalPoint = tem_original_point
    post_tile_jobs_param.cacheBounds = tem_cache_Bounds
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


def cache_localworkspace(address: str, username: str, password: str, w_loc: str, map_name: str, original_point: tuple,
                         cache_bounds: tuple, scale: List[float] = None,
                         w_servicetypes: List[ServiceType] = [ServiceType.RESTMAP],
                         tile_size: TileSize = TileSize.SIZE_256, tile_type: TileType = TileType.Image,
                         format: OutputFormat = OutputFormat.PNG, epsg_code: int = -1, storageid: str = None,
                         storageconfig: TileSourceInfo = None, token: str = None, quite: bool = False,
                         job_tile_source_type: str = 'SMTiles'):
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
    if scale is None or len(scale) is 0:
        raise Exception('未指定比例尺')
    # if storageid is not None:
    #     storage_info = mng.get_datastore(storageid)
    #     for info in storage_info.tilesetInfos:
    #         if info.metaData.mapName == map_name:
    #             storageconfig = storage_info.tileSourceInfo
    #
    # if storageconfig is None:
    #     storageconfig = SMTilesTileSourceInfo()
    #     storageconfig.type = jobTileSourceType
    #     storageconfig.outputPath = '../webapps/iserver/output/sqlite_' + uuid.uuid1().__str__()

    if not quite:
        confirmResult = confirm(address=address, username=username, password=password,
                                w_loc=w_loc, map_name=map_name, original_point=original_point,
                                cache_bounds=cache_bounds, scale=scale, w_servicetype=w_servicetypes,
                                tile_size=tile_size, tile_type=tile_type, format=format, epsg_code=epsg_code,
                                storageid=storageid, token=token)
        if confirmResult.lower() == 'n':
            return

    param = PostFileUploadTasksParam()
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

    cache_remoteworkspace(address=address, username=username, password=password, component_name=wkn, map_name=map_name,
                          original_point=original_point, cache_bounds=cache_bounds, scale=scale, tile_size=tile_size,
                          tile_type=tile_type, format=format, epsg_code=epsg_code, storageid=storageid,
                          storageconfig=storageconfig, token=token, quite=True,
                          job_tile_source_type=job_tile_source_type)


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
