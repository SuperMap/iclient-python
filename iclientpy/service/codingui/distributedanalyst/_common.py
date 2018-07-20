from typing import NamedTuple, Any, List, Iterable
from iclientpy.rest.api.model import FieldContent, BigDataFileShareDataSetInfo, BigDataFileShareDatasetInfoType, RelationShipDatasetContent, DatasetType

class DatasetAndFields(NamedTuple):
    dataset: Any
    fields: Iterable[FieldContent]


def is_file_share(resource:DatasetAndFields):
    return isinstance(resource.dataset.datasetInfo, BigDataFileShareDataSetInfo)


def is_relationship(resource: DatasetAndFields):
    return isinstance(resource.dataset, RelationShipDatasetContent)


def is_expect_datasettype(resource: DatasetAndFields, expect_type: DatasetType) -> bool:
    if is_file_share(resource):
        info = resource.dataset #type:BigDataFileShareDataSetInfo
        return BigDataFileShareDatasetInfoType.UDB == info.datasetInfo.type and expect_type == info.datasetInfo.datasetType
    if is_relationship(resource):
        info = resource.dataset #type:RelationShipDatasetContent
        return  expect_type == info.datasetInfo.type
    return False


def is_point(resource: DatasetAndFields) -> bool:
    return is_expect_datasettype(resource, DatasetType.POINT)


def is_csv(resource: DatasetAndFields) -> bool:
    if not isinstance(resource.dataset, BigDataFileShareDataSetInfo):
        return False
    info = resource.dataset #type:BigDataFileShareDataSetInfo
    return BigDataFileShareDatasetInfoType.CSV == info.type


def is_region(resource: DatasetAndFields) -> bool:
    return is_expect_datasettype(resource, DatasetType.REGION)


def get_name(resource: DatasetAndFields) -> str:
    if is_file_share(resource):
        info = resource.dataset #type: BigDataFileShareDataSetInfo
        return info.datasetInfo.name
    if is_relationship(resource):
        info = resource.dataset #type: RelationShipDatasetContent
        return info.datasetInfo.name
    raise Exception('unexpected type.')