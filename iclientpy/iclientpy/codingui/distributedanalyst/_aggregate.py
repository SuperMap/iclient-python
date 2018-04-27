import json
from typing import List, Iterable,Tuple
from iclientpy.rest.api.model import PostAgggregatePointsEntity, DatasetInputSetting, SummaryMeshAnalystSetting,SummaryAnalystType,MappingParameters,DistanceUnit, FieldType,MethodResult,TargetSericeType
from iclientpy.codingui.comon import NamedObjects,Option
from iclientpy.dtojson import to_json_str
from functools import partial
from iclientpy.rest.api.distributedanalyst import DistributedAnalyst


class SummaryMeshBuilder:
    _setting:SummaryMeshAnalystSetting

    def __init__(self, setting:SummaryMeshAnalystSetting, job_builder):
        self._setting = setting
        self._job_builder = job_builder

    def set_mesh_hexagon(self):
        self._setting.meshType = 1
        return self

    def set_mesh_square(self):
        self._setting.meshType = 0
        return self

    def set_bounds(self, bounds: Tuple[float, float, float, float]):
        self._setting.query = ','.join([str(f) for f in bounds])
        return self

    def set_resolution(self, value:float):
        self._setting.resolution = value
        return self

    def _mesh_size_unit_selected(self, value:DistanceUnit):
        self._setting.meshSizeUnit = value
        return self

    @property
    def mesh_sieze_units(self):
        result = NamedObjects()
        for unit in [DistanceUnit.Meter, DistanceUnit.Kilometer, DistanceUnit.Yard, DistanceUnit.Foot, DistanceUnit.Mile]:
            result[unit.name] = Option(partial(self._mesh_size_unit_selected, unit), 'select')
        return result

    @property
    def then(self):
        return self._job_builder

    def __repr__(self):
        return self._job_builder.__repr__()


class SummaryRegionBuilder:
    _setting:SummaryMeshAnalystSetting
    _region_dataset_options: NamedObjects
    def __init__(self, setting:SummaryMeshAnalystSetting, job_builder, region_dataset_names: List[str]):
        self._setting = setting
        self._job_builder = job_builder
        self._init_region_dataset_options(region_dataset_names)

    def _dataset_selected(self, dataset_name):
        self._setting.regionDataset = dataset_name
        return self._job_builder

    def _init_region_dataset_options(self, region_dataset_names: List[str]):
        self._region_dataset_options = NamedObjects()
        for name in region_dataset_names:
            self._region_dataset_options[name] = Option(partial(self._dataset_selected, name), 'select')

    @property
    def available_region_datasets(self):
        return self._region_dataset_options

    def __repr__(self):
        return self._job_builder.__repr__()



class PreparingAggregate:
    _postentity: PostAgggregatePointsEntity
    _field_options: NamedObjects
    _fields: List[str]
    _modes: List[str]
    _analyst: SummaryMeshAnalystSetting
    _region_dataset_names: List[str]
    _distributedanalyst: DistributedAnalyst

    def __init__(self, dataset_name: str, field_names: List[str], region_dataset_names: List[str], distributedanalyst: DistributedAnalyst ):
        self._postentity = PostAgggregatePointsEntity()
        self._postentity.input = DatasetInputSetting()
        self._postentity.input.datasetName = dataset_name
        self._analyst = SummaryMeshAnalystSetting()
        self._analyst.mappingParameters = MappingParameters()
        self._analyst.mappingParameters.numericPrecision = 1
        self._postentity.analyst = self._analyst
        self._init_field_options(field_names)
        self._fields = []
        self._modes = []
        self._region_dataset_names = list(region_dataset_names)
        self._distributedanalyst = distributedanalyst

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

    @property
    def prepare_summarymesh(self) -> SummaryMeshBuilder:
        """
        设置聚合类型为格网聚合，返回一个格网聚合设置对象以进一步设置格网聚合所需参数。

        Args:

        Returns:
            格网聚合设置对象
        """
        self._postentity.type = SummaryAnalystType.SUMMARYMESH
        return SummaryMeshBuilder(self._analyst, self)

    @property
    def prepare_summaryregion(self) -> SummaryRegionBuilder:
        """
        设置聚合类型为多边形聚合，返回一个多边形聚合设置对象以进一步设置格网聚合所需参数。

        Args:

        Returns:
            多边形聚合设置对象
        """
        self._postentity.type = SummaryAnalystType.SUMMARYREGION
        return SummaryRegionBuilder(self._analyst, self, self._region_dataset_names)

    def set_numeric_precision(self, value):
        self._analyst.mappingParameters.numericPrecision = value
        return self

    def __repr__(self):
        return json.dumps(json.loads(to_json_str(self._postentity)), indent = 2, sort_keys = True)

    @property
    def job_setting(self) -> PostAgggregatePointsEntity:
        return self._postentity

    def execute(self):
        post_result = self._distributedanalyst.post_aggregatepoints(self._postentity) #type:MethodResult
        if not post_result.succeed:
            raise Exception(post_result.error.errorMsg)


from ._common import *


def attach(distributedanalyst: DistributedAnalyst, dataset_and_fields: Iterable[DatasetAndFields], to_attach: NamedObjects):
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
        def aggregate():
            return PreparingAggregate(name, field_names, region_dataset_names, distributedanalyst)
        options.prepare_aggregate = aggregate