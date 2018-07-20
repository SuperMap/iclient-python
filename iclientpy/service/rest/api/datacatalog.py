from ..decorator import get, post, head
from .model import *


class Datacatalog:
    @head('/datacatalog/relationship/datasets')
    def head_relationship_datasets(self) -> int:
        pass

    @get('/datacatalog/relationship/datasets')
    def get_relationship_datasets(self) -> DatasetsContent:
        pass

    @head('/datacatalog/relationship/datasets/{dataset_name}')
    def head_relationship_dataset(self, dataset_name: str) -> int:
        pass

    @get('/datacatalog/relationship/datasets/{dataset_name}')
    def get_relationship_dataset(self, dataset_name: str) -> RelationShipDatasetContent:
        pass

    @head('/datacatalog/relationship/datasets/{dataset_name}/fields')
    def head_relationship_dataset_fields(self, dataset_name: str) -> int:
        pass

    @get('/datacatalog/relationship/datasets/{dataset_name}/fields')
    def get_relationship_dataset_fields(self, dataset_name: str) -> FieldsContent:
        pass

    @head('/datacatalog/relationship/datasets/{dataset_name}/fields/{field_name}')
    def head_relationship_dataset_field(self, dataset_name: str, field_name: str) -> int:
        pass

    @get('/datacatalog/relationship/datasets/{dataset_name}/fields/{field_name}')
    def get_relationship_dataset_field(self, dataset_name: str, field_name: str) -> FieldContent:
        pass

    @head('/datacatalog/sharefile')
    def head_sharefile(self) -> int:
        pass

    @get('/datacatalog/sharefile')
    def get_sharefile(self) -> DatasetsContent:
        pass

    @head('/datacatalog/sharefile/{dataset_name}')
    def head_sharefile_dataset(self, dataset_name: str) -> int:
        pass

    @get('/datacatalog/sharefile/{dataset_name}')
    def get_sharefile_dataset(self, dataset_name: str) -> BigDataFileShareDatasetContent:
        pass

    @head('/datacatalog/sharefile/{dataset_name}/fields')
    def head_sharefile_dataset_fields(self, dataset_name: str) -> int:
        pass

    @get('/datacatalog/sharefile/{dataset_name}/fields')
    def get_sharefile_dataset_fields(self, dataset_name: str) -> FieldsContent:
        pass

    @head('/datacatalog/sharefile/{dataset_name}/fields/{field_name}')
    def head_sharefile_dataset_field(self, dataset_name: str, field_name: str) -> int:
        pass

    @get('/datacatalog/sharefile/{dataset_name}/fields/{field_name}')
    def get_sharefile_dataset_field(self, dataset_name: str, field_name: str) -> FieldContent:
        pass
