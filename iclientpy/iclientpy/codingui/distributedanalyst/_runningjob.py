import iclientpy as icp
from typing import List,Callable
from iclientpy.jupyter.widgets.sparkjobstate import SparkJobStateWidgets
import time
from iclientpy.rest.api.model import DistributedAnalystJob,TargetSericeType, SparkJobSetting
from iclientpy.rest.api.restmap import MapService
from IPython.display import display

class RunningJob:
    _detail_method: Callable
    _map_service_fun: Callable[[str], MapService]
    def __init__(self, detail_method:Callable[[],DistributedAnalystJob], map_service_fun: Callable[[str], MapService]):
        self._detail_method = detail_method
        self._widget = SparkJobStateWidgets()
        self._map_service_fun = map_service_fun

    def display(self):
        display(self)

    def _ipython_display_(self, **kwargs):
        self._widget._ipython_display_(**kwargs)
        job = self._detail_method()#type:DistributedAnalystJob
        self._widget.update(job.state)
        while not job.state.endState:
            time.sleep(3)
            job = self._detail_method()  # type:DistributedAnalystJob
            self._widget.update(job.state)
        setting = job.setting  # type:SparkJobSetting
        for service_info in setting.serviceInfo.targetServiceInfos:
            if service_info.serviceType == TargetSericeType.RESTMAP:
                service_name = service_info.serviceAddress[
                               service_info.serviceAddress.rfind('/services/') + len('/services/'):]
                map_service = self._map_service_fun(service_name) #type:MapService
                map_name = map_service.get_map_resources()[0].name
                map_info = map_service.get_map(map_name)
                bounds = map_info.bounds
                default_tiles = icp.TileMapLayer(
                    url=service_info.serviceAddress + '/maps/' + map_name)
                map = icp.MapView(default_tiles=default_tiles, crs='EPSG' + str(map_info.prjCoordSys.epsgCode),
                                  fit_bounds=[[bounds.leftBottom.y, bounds.leftBottom.x],[bounds.rightTop.y, bounds.rightTop.x]])
                map._ipython_display_(**kwargs)
        return job