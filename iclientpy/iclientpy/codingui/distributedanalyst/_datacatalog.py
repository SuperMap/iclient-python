from typing import Callable
from iclientpy.rest.api.datacatalog import *
from iclientpy.rest.api.distributedanalyst import DistributedAnalyst
from iclientpy.codingui.comon import NamedObjects
from ._common import *


def get_datas(distributedanalyst: DistributedAnalyst, datacatalog: Datacatalog, attach_list: List[Callable[[DistributedAnalyst, Iterable[DatasetAndFields], NamedObjects], None]]) -> NamedObjects:
    result = NamedObjects()
    sharefile_contents = datacatalog.get_sharefile() #type:DatasetsContent
    relationship_contents = datacatalog.get_relationship_datasets() #type:DatasetsContent
    dataset_and_fields_list = [] #type:List[DatasetAndFields]
    for name in sharefile_contents.datasetNames:
        dataset_and_fields_list.append(_get_dataset(datacatalog.get_sharefile_dataset, datacatalog.get_sharefile_dataset_fields, datacatalog.get_sharefile_dataset_field, name))
    for name in relationship_contents.datasetNames:
        dataset_and_fields_list.append(_get_dataset(datacatalog.get_relationship_dataset, datacatalog.get_relationship_dataset_fields, datacatalog.get_relationship_dataset_field, name))
    for attach in attach_list:
        attach(distributedanalyst, dataset_and_fields_list, result)
    return result


def _get_dataset(dataset_method: Callable, fields_method: Callable, field_method: Callable, dataset_name: str) -> DatasetAndFields:
    dataset = dataset_method(dataset_name)
    fields_content = fields_method(dataset_name) #type: FieldsContent
    field_list = [] #type: List[FieldContent]
    for field_name in fields_content.fieldNames:
        field_list.append(field_method(dataset_name, field_name))
    return DatasetAndFields(dataset, field_list)
