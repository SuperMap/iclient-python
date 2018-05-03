import json
from typing import List, Iterable,Tuple, Callable, Any
from iclientpy.rest.api.model import PostAgggregatePointsEntity, DatasetInputSetting, SummaryMeshAnalystSetting,SummaryAnalystType,MappingParameters,DistanceUnit, FieldType,MethodResult,TargetSericeType
from iclientpy.rest.api.restmap import MapService
from iclientpy.codingui.comon import NamedObjects,Option
from iclientpy.dtojson import to_json_str
from functools import partial
from iclientpy.rest.api.distributedanalyst import DistributedAnalyst


class PreparingAggregate:
    _postentity: PostAgggregatePointsEntity
    _field_options: NamedObjects
    _fields: List[str]
    _modes: List[str]
    _analyst_setting: SummaryMeshAnalystSetting
    _executor: DistributedAnalyst

    def __init__(self, dataset_name: str, field_names: List[str], executor: Callable[[PostAgggregatePointsEntity], Any] ):
        self._postentity = PostAgggregatePointsEntity()
        self._postentity.input = DatasetInputSetting()
        self._postentity.input.datasetName = dataset_name
        self._analyst_setting = SummaryMeshAnalystSetting()
        self._analyst_setting.meshSizeUnit = DistanceUnit.Meter
        self._analyst_setting.mappingParameters = MappingParameters()
        self._analyst_setting.mappingParameters.numericPrecision = 1
        self._postentity.analyst = self._analyst_setting
        self._init_field_options(field_names)
        self._fields = []
        self._modes = []
        self._executor = executor

    def _init_field_options(self, field_names:Iterable[str]):
        self._field_options = NamedObjects()
        modes = ['max', 'min', 'average', 'sum', 'variance']
        for name in field_names:
            statistic_mode_options = NamedObjects()
            for mode_name in modes:
                statistic_mode_options['statistic_with_' + mode_name] = Option(partial(self._add_statistic_field, name, mode_name))
            statistic_mode_options['statistic_with_std_deviation'] = Option(partial(self._add_statistic_field, name, 'stdDeviation'))
            self._field_options[name] = statistic_mode_options

    @property
    def available_fields(self) ->  NamedObjects:
        return self._field_options

    def _add_statistic_field(self, field_name: str, mode: str):
        self._fields.append(field_name)
        self._modes.append(mode)
        analyst = self._postentity.analyst #type:SummaryMeshAnalystSetting
        analyst.fields = ",".join(self._fields)
        analyst.statisticModes = ','.join(self._modes)
        return self

    def set_numeric_precision(self, value):
        self._analyst_setting.mappingParameters.numericPrecision = value
        return self

    def __repr__(self):
        return json.dumps(json.loads(to_json_str(self._postentity)), indent = 2, sort_keys = True)

    @property
    def job_setting(self) -> PostAgggregatePointsEntity:
        return self._postentity

    def execute(self):
        #TODO 验证设置是否完整，不完整的话给予提示
        return self._executor(self._postentity)


class SummaryRegion(PreparingAggregate):
    _region_dataset_options: NamedObjects
    def __init__(self, dataset_name: str, field_names: List[str], region_dataset_names: List[str], executor: Callable[[PostAgggregatePointsEntity], Any]):
        PreparingAggregate.__init__(self, dataset_name, field_names, executor)
        self._postentity.type = SummaryAnalystType.SUMMARYREGION
        self._init_region_dataset_options(region_dataset_names)

    def _dataset_selected(self, dataset_name):
        self._analyst_setting.regionDataset = dataset_name
        return self

    def _init_region_dataset_options(self, region_dataset_names: List[str]):
        self._region_dataset_options = NamedObjects()
        for name in region_dataset_names:
            self._region_dataset_options[name] = Option(partial(self._dataset_selected, name), 'select')

    @property
    def available_region_datasets(self):
        return self._region_dataset_options


class SummaryMesh(PreparingAggregate):

    def __init__(self, dataset_name: str, field_names: List[str], executor: Callable[[PostAgggregatePointsEntity], Any] ):
        PreparingAggregate.__init__(self, dataset_name, field_names, executor)
        self._postentity.type = SummaryAnalystType.SUMMARYMESH
        self._analyst_setting.meshType = 0

    def set_mesh_hexagon(self):
        self._analyst_setting.meshType = 1
        return self

    def set_mesh_square(self):
        self._analyst_setting.meshType = 0
        return self

    def set_bounds(self, bounds: Tuple[float, float, float, float]):
        self._analyst_setting.query = ','.join([str(f) for f in bounds])
        return self

    def set_resolution(self, value:float):
        self._analyst_setting.resolution = value
        return self

    def _mesh_size_unit_selected(self, value:DistanceUnit):
        self._analyst_setting.meshSizeUnit = value
        return self

    @property
    def available_mesh_sieze_units(self):
        result = NamedObjects()
        for unit in [DistanceUnit.Meter, DistanceUnit.Kilometer, DistanceUnit.Yard, DistanceUnit.Foot, DistanceUnit.Mile]:
            result[unit.name] = Option(partial(self._mesh_size_unit_selected, unit), 'select')
        return result


from ._common import *


def attach(executor: Callable[[PostAgggregatePointsEntity], Any], dataset_and_fields: Iterable[DatasetAndFields], to_attach: NamedObjects):
    point_datasets = [resource for resource in dataset_and_fields if is_point(resource)]
    region_dataset_names = [get_name(resource) for resource in dataset_and_fields if is_region(resource)]
    for dataset in point_datasets:
        name = get_name(dataset)
        options = None
        if hasattr(to_attach, name):
            options = to_attach[name]
        else:
            options = NamedObjects()
            to_attach[name] = options
        field_names = [field.fieldInfo.name for field in dataset.fields
                       if not field.fieldInfo.isSystemField
                       and field.fieldInfo.name.lower() != 'smuserid'
                       and field.fieldInfo.type in (FieldType.INT16, FieldType.INT32, FieldType.INT64, FieldType.SINGLE, FieldType.DOUBLE)
                       ]

        options.prepare_summary_region_aggregate = lambda :SummaryRegion(name, field_names, region_dataset_names, executor)
        options.prepare_summary_messh_aggregate = lambda :SummaryMesh(name, field_names, executor)


from ._runningjob import RunningJob
from functools import partial


class DisplayRunningStateExecutor:
    _distributedanalyst: DistributedAnalyst
    _map_service_factory: Callable[[str], MapService]

    def __init__(self, distributedanalyst: DistributedAnalyst, map_service_factory: Callable[[str], MapService]):
        self._distributedanalyst = distributedanalyst
        self._map_service_factory = map_service_factory

    def __call__(self, method_result: MethodResult):
        job = RunningJob(partial(self._distributedanalyst.get_aggregatepoints_job, method_result.newResourceID), self._map_service_factory)
        return job.display()


class _Executor:
    _invoke_post: Callable[[PostAgggregatePointsEntity], MethodResult]
    _display: Callable[[MethodResult], Any]

    def __init__(self, invoke_post: Callable[[PostAgggregatePointsEntity], MethodResult], display: Callable[[MethodResult], Any]):
        self._invoke_post = invoke_post
        self._display = display


    def __call__(self, entity: PostAgggregatePointsEntity):
        method_result = self._invoke_post(entity)
        return self._display(method_result)


def new_executor(distributedanalyst: DistributedAnalyst,map_service_fun: Callable[[str], MapService]):
    return _Executor(distributedanalyst.post_aggregatepoints, DisplayRunningStateExecutor(distributedanalyst, map_service_fun))