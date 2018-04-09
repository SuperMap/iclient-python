from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.model import *
from iclientpy.rest.api.datacatalog import Datacatalog
from iclientpy import env
import iclientpy as icp
from typing import List,Callable
from iclientpy.jupyter.widgets.sparkjobstate import SparkJobStateWidgets
import time


class Dataset:
    name: str

def get_datasets(profile_name:str = None, datacatalog_service_name:str = 'datacatalog/rest', distributedanalyst_service_name:str = 'distributedanalyst/rest') -> List[Dataset]:


    profile = env.get_profile(profile_name) #type: env.Profile
    api_factory = env.create_apifactory_from_profile(profile)
    datacatalog = api_factory.datacatalog_service(datacatalog_service_name)
    distributedanalyst = api_factory.distributedanalyst_service(distributedanalyst_service_name)

    class Job:
        _id: str
        _detail_method: Callable
        def __init__(self, id:str, detail_method:Callable):
            self._id = id
            self._detail_method = detail_method
            self._widget = SparkJobStateWidgets()


        def _ipython_display_(self, **kwargs):
            self._widget._ipython_display_(**kwargs)
            job = self._detail_method(self._id)#type:GetDensityResultItem
            self._widget.update(job.state)
            while not job.state.endState:
                time.sleep(3)
                job = self._detail_method(self._id)#type:GetDensityResultItem
                self._widget.update(job.state)
            for service_info in job.setting.serviceInfo.targetServiceInfos:
                if service_info.serviceType == TargetSericeType.RESTMAP:
                    service_name = service_info.serviceAddress[
                                   service_info.serviceAddress.rfind('/services/') + len('/services/'):]
                    map_service = api_factory.map_service(service_name)
                    map_name = 'kernelDensity_RecordCount_Density_Map'
                    bounds = map_service.get_map(map_name).viewBounds
                    default_tiles = icp.TileMapLayer(
                        url=service_info.serviceAddress + '/maps/' + map_name)
                    map = icp.MapView(default_tiles=default_tiles, crs='EPSG4326',
                                      fit_bounds=[[40, -74.5], [41, -73.5]])
                    map._ipython_display_(**kwargs)


    class CSVDataset(Dataset):
        def density(self, resolution:int, radius:int, mesh_size_unit:DistanceUnit, radius_unit:DistanceUnit, area_unit:AreaUnit, mesh_type:int, method:int):
            postentity = PostDensityEntity()
            postentity.input = DatasetInputSetting()
            postentity.input.datasetName = self.name
            postentity.analyst = KernelDensityAnalystSetting()
            postentity.analyst.resolution = resolution
            postentity.analyst.radius = radius
            postentity.analyst.meshSizeUnit = mesh_size_unit
            postentity.analyst.radiusUnit = radius_unit
            postentity.analyst.areaUnit = area_unit
            postentity.analyst.meshType = mesh_type
            postentity.analyst.method = method
            post_result = distributedanalyst.post_density(postentity)
            if not post_result.succeed:
                raise Exception(post_result.error.errorMsg)
            return Job(post_result.newResourceID, distributedanalyst.get_density_job)

    def _convert_sharefile(remote_dataset:BigDataFileShareDataSetInfo):
        result = CSVDataset()
        result.name = remote_dataset.name
        return result


    def _list_remote_dataset(result:List[Dataset], list_method:Callable[[], DatasetsContent], detail_method:Callable, convert_fun: Callable):
        contents = list_method() #type:DatasetsContent
        for name in contents.datasetNames:
            result.append(convert_fun(detail_method(name)))
    result = [] #type: List[Dataset]
    _list_remote_dataset(result, datacatalog.get_sharefile, datacatalog.get_sharefile_dataset,_convert_sharefile)
    return result