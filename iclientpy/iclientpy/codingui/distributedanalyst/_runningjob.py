import iclientpy as icp
from typing import List,Callable
from iclientpy.jupyter.widgets.sparkjobstate import SparkJobStateWidgets
import time
from iclientpy.rest.api.model import DistributedAnalystJob,TargetSericeType
from iclientpy.rest.api.restmap import MapService


class RunningJob:
    _id: str
    _detail_method: Callable
    _map_service_fun: Callable[[str], MapService]
    def __init__(self, id:str, detail_method:Callable[[],DistributedAnalystJob], map_service_fun: Callable[[str], MapService]):
        self._id = id
        self._detail_method = detail_method
        self._widget = SparkJobStateWidgets()
        self._map_service_fun = map_service_fun


    def _ipython_display_(self, **kwargs):
        self._widget._ipython_display_(**kwargs)
        job = self._detail_method(self._id)#type:DistributedAnalystJob
        self._widget.update(job.state)
        while not job.state.endState:
            time.sleep(3)
            job = self._detail_method(self._id)#type:GetDensityResultItem
            self._widget.update(job.state)
        for service_info in job.setting.serviceInfo.targetServiceInfos:
            if service_info.serviceType == TargetSericeType.RESTMAP:
                service_name = service_info.serviceAddress[
                               service_info.serviceAddress.rfind('/services/') + len('/services/'):]
                map_service = self._map_service_fun(service_name) #type:MapService
                map_name = map_service.get_map_resources()[0].name
                bounds = map_service.get_map(map_name).viewBounds
                default_tiles = icp.TileMapLayer(
                    url=service_info.serviceAddress + '/maps/' + map_name)
                map = icp.MapView(default_tiles=default_tiles, crs='EPSG4326',
                                  fit_bounds=[[40, -74.5], [41, -73.5]])
                map._ipython_display_(**kwargs)