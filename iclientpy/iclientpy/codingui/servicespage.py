from functools import partial
from typing import Iterable,Dict,Union
from ..rest.api.model import ServiceMetaInfo
from ..rest.api.servicespage import ServiceComponentType
from .comon import NamedObjects



def get_services_by_component_type(services: Iterable[ServiceMetaInfo], *args):
    result = {} #type: Dict[ServiceComponentType, ServiceMetaInfo]
    for com_type in args:
        type_name = com_type.value # type: str
        for service in services:
            if type_name == service.componentType:
                result[com_type] = service
                break
        else:
            result[com_type] = None
    return result


from ._serviceuiregister import ServiceUIRegister
from iclientpy.rest.apifactory import APIFactory
ui_class_register = ServiceUIRegister()

from iclientpy.rest.api.servicespage import ServiceComponentType,ServiceInterfaceType

from iclientpy.rest.api.restdata import DataService, GetDataSourceResult, GetDatasetResult, GetDatasetsResult
from iclientpy.rest.api.model import DatasetType,DatasetInfo
from iclientpy.data.featuresconverter import from_geojson_features
import geojson


def _post_geojson_to_dataset(data_service: DataService, datasource: str, dataset: str, geojson: Union[str, geojson.FeatureCollection]):
    feature_list = from_geojson_features(geojson)
    data_service.post_features(datasource, dataset, feature_list)


_DATASET_KEY_TEMPLATE = '{datasource}_{dataset}_{type}'


@ui_class_register(ServiceComponentType.data, ServiceInterfaceType.rest, APIFactory.data_service)
class DataServiceUI:
    _data_service: DataService
    def __init__(self, data_service: DataService):
        self._data_service = data_service

    @staticmethod
    def _get_dataset_key(datasource: str, dataset: str, type:DatasetType):
        return _DATASET_KEY_TEMPLATE.format(datasource= datasource, dataset=dataset, type=type.name)

    @property
    def datasets(self):
        data_service = self._data_service
        datasource_names = data_service.get_datasources().datasourceNames  # type:List[str]
        result = NamedObjects()
        for datasource_name in datasource_names:
            get_datasource_result = data_service.get_datasource(datasource_name)  # type:GetDataSourceResult
            get_datasets_result = data_service.get_datasets(get_datasource_result.datasourceInfo.name)  # type:GetDatasetsResult
            get_datasets_result.datasetNames
            for dataset_name in get_datasets_result.datasetNames:
                dataset_result = data_service.get_dataset(datasource_name, dataset_name)  # type:GetDatasetResult
                dataset_info = dataset_result.datasetInfo  # type:DatasetInfo
                options = NamedObjects()
                self._init_dataset_options(options, dataset_info)
                result[DataServiceUI._get_dataset_key(datasource_name, dataset_info.name, dataset_info.type)] = options
        return result

    def _init_dataset_options(self, options, dataset_info: DatasetInfo):
        if dataset_info.type in (DatasetType.POINT, DatasetType.LINE, DatasetType.REGION):
            options['import_features_from_geojson'] = partial(_post_geojson_to_dataset, self._data_service, dataset_info.dataSourceName, dataset_info.name)
        else:
            options['no_action_available'] = None


from iclientpy.rest.api.restmap import MapService


@ui_class_register(ServiceComponentType.map, ServiceInterfaceType.rest, APIFactory.map_service)
class MapServiceUI:
    _map_service: MapService

    def __init__(self, map_service: MapService):
        self._map_service = map_service

    def _create_map_widget(self, map_name: str, path: str):
        map_info = self._map_service.get_map(map_name)
        bounds = map_info.bounds
        from iclientpy.jupyter.widgets.mapview import MapView
        from iclientpy.jupyter.widgets.tilemaplayer import TileMapLayer
        default_tiles = TileMapLayer(url=path)
        map = MapView(default_tiles=default_tiles, crs='EPSG' + str(map_info.prjCoordSys.epsgCode),
                          fit_bounds=[[bounds.leftBottom.y, bounds.leftBottom.x],
                                      [bounds.rightTop.y, bounds.rightTop.x]])
        return map
    @property
    def maps(self):
        result = NamedObjects()
        map_resources = self._map_service.get_map_resources()
        for map_resource in map_resources:
            map_name = map_resource.name
            result[map_name] = self._create_map_widget(map_name, map_resource.path)
        return result