from typing import List,Callable,Iterable,Tuple,Dict
from ..rest.api.model import PostAgggregatePointsEntity, DatasetInputSetting, SummaryMeshAnalystSetting,SummaryAnalystType,MappingParameters,DistanceUnit
from ..comon import NamedObjects,Option
from ..dtojson import to_json_str
from functools import partial


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
            result[unit.name] = Option(partial(self._mesh_size_unit_selected, unit))
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
            self._region_dataset_options[name] = Option(partial(self._dataset_selected, name))

    @property
    def available_region_datasets(self):
        return self._region_dataset_options

    def __repr__(self):
        return self._job_builder.__repr__()



class AggregatePointsJobBuilder:
    _setting: PostAgggregatePointsEntity
    _field_options: NamedObjects
    _fields: List[str]
    _modes: List[str]
    _analyst: SummaryMeshAnalystSetting
    _region_dataset_names: List[str]

    def __init__(self, dataset_name: str, field_names: List[str], region_dataset_names: List[str] ):
        self._setting = PostAgggregatePointsEntity()
        self._setting.input = DatasetInputSetting()
        self._setting.input.datasetName = dataset_name
        self._analyst = SummaryMeshAnalystSetting()
        self._analyst.mappingParameters = MappingParameters()
        self._analyst.mappingParameters.numericPrecision = 1
        self._setting.analyst = self._analyst
        self._init_field_options(field_names)
        self._fields = []
        self._modes = []
        self._region_dataset_names = list(region_dataset_names)

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
        analyst = self._setting.analyst #type:SummaryMeshAnalystSetting
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
        self._setting.type = SummaryAnalystType.SUMMARYMESH
        return SummaryMeshBuilder(self._analyst, self)

    @property
    def prepare_summaryregion(self) -> SummaryRegionBuilder:
        """
        设置聚合类型为多边形聚合，返回一个多边形聚合设置对象以进一步设置格网聚合所需参数。

        Args:

        Returns:
            多边形聚合设置对象
        """
        self._setting.type = SummaryAnalystType.SUMMARYREGION
        return SummaryRegionBuilder(self._analyst, self, self._region_dataset_names)

    def set_numeric_precision(self, value):
        self._analyst.mappingParameters.numericPrecision = value
        return self

    def __repr__(self):
        return to_json_str(self._setting)

    @property
    def job_setting(self) -> PostAgggregatePointsEntity:
        return self._setting
