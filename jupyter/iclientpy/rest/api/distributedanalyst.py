from ..decorator import get, post, put, head
from .model import *
from .abstracttypefields import aggregate_points_job_settting_list_deserializer, \
    aggregate_point_job_settting_deserializer, feature_join_deserializer, feature_join_list_deserializer, \
    buffers_deserializer, buffers_list_deserializer, density_deserializer, density_list_deserializer, \
    overlay_deserializer, overlay_list_deserializer, query_list_deserializer, query_deserializer, \
    summary_attributes_list_deserializer, summary_attributes_deserializer, summary_region_list_deserializer, \
    summary_region_deserializer, topologyvalidator_list_deserializer, topologyvalidator_deserializer, \
    vector_clip_deserializer, vector_clip_list_deserializer


class DistributedAnalyst:
    @head('/spatialanalyst/aggregatepoints')
    def head_aggregatepoints(self) -> int:
        pass

    @get('/spatialanalyst/aggregatepoints', json_deserializer=aggregate_points_job_settting_list_deserializer)
    def get_aggregatepoints(self) -> List[GetAggregatePointsResultItem]:
        pass

    @post('/spatialanalyst/aggregatepoints', entityKW='entity')
    def post_aggregatepoints(self, entity: PostAgggregatePointsEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/aggregatepoints/{job_id}')
    def head_aggregatepoints_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/aggregatepoints/{job_id}', json_deserializer=aggregate_point_job_settting_deserializer)
    def get_aggregatepoints_job(self, job_id: str) -> GetAggregatePointsResultItem:
        pass

    @head('/spatialanalyst/featurejoin')
    def head_featurejoin(self) -> int:
        pass

    @get('/spatialanalyst/featurejoin', json_deserializer=feature_join_list_deserializer)
    def get_featurejoin(self) -> List[GetFeatureJoinResultItem]:
        pass

    @post('/spatialanalyst/featurejoin', entityKW='entity')
    def post_featurejoin(self, entity: PostFeatureJoinEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/featurejoin/{job_id}')
    def head_featurejoin_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/featurejoin/{job_id}', json_deserializer=feature_join_deserializer)
    def get_featurejoin_job(self, job_id: str) -> GetFeatureJoinResultItem:
        pass

    @head('/spatialanalyst/buffers')
    def head_buffers(self) -> int:
        pass

    @get('/spatialanalyst/buffers', json_deserializer=buffers_list_deserializer)
    def get_buffers(self) -> List[GetBuffersResultItem]:
        pass

    @post('/spatialanalyst/buffers', entityKW='entity')
    def post_buffers(self, entity: PostBuffersEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/buffers/{job_id}')
    def head_buffers_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/buffers/{job_id}', json_deserializer=buffers_deserializer)
    def get_buffers_job(self, job_id: str) -> GetBuffersResultItem:
        pass

        # TODO: buffers  map资源没有封装

    @head('/spatialanalyst/density')
    def head_density(self) -> int:
        pass

    @get('/spatialanalyst/density', json_deserializer=density_list_deserializer)
    def get_density(self) -> List[GetDensityResultItem]:
        pass

    @post('/spatialanalyst/density', entityKW='entity')
    def post_density(self, entity: PostDensityEntiy) -> MethodResult:
        pass

    @head('/spatialanalyst/density/{job_id}')
    def head_density_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/density/{job_id}', json_deserializer=density_deserializer)
    def get_density_job(self, job_id: str) -> GetDensityResultItem:
        pass

    @head('/spatialanalyst/overlay')
    def head_overlay(self) -> int:
        pass

    @get('/spatialanalyst/overlay', json_deserializer=overlay_list_deserializer)
    def get_overlay(self) -> List[GetOverlayResultItem]:
        pass

    @post('/spatialanalyst/overlay', entityKW='entity')
    def post_overlay(self, entity: PostOverlayEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/overlay/{job_id}')
    def head_overlay_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/overlay/{job_id}', json_deserializer=overlay_deserializer)
    def get_overlay_job(self, job_id: str) -> GetOverlayResultItem:
        pass

        # TODO: overlay  map资源没有封装

    @head('/spatialanalyst/query')
    def head_query(self) -> int:
        pass

    @get('/spatialanalyst/query', json_deserializer=query_list_deserializer)
    def get_query(self) -> List[GetQueryResultItem]:
        pass

    @post('/spatialanalyst/query', entityKW='entity')
    def post_query(self, entity: PostQueryEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/query/{job_id}')
    def head_query_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/query/{job_id}', json_deserializer=query_deserializer)
    def get_query_job(self, job_id: str) -> GetQueryResultItem:
        pass

        # TODO: query  map资源没有封装

    @head('/spatialanalyst/summaryattributes')
    def head_summary_attributes(self) -> int:
        pass

    @get('/spatialanalyst/summaryattributes', json_deserializer=summary_attributes_list_deserializer)
    def get_summary_attributes(self) -> List[GetSummaryAttributesResultItem]:
        pass

    @post('/spatialanalyst/summaryattributes', entityKW='entity')
    def post_summary_attributes(self, entity: PostSummaryAttributesEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/summaryattributes/{job_id}')
    def head_summary_attributes_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/summaryattributes/{job_id}', json_deserializer=summary_attributes_deserializer)
    def get_summary_attributes_job(self, job_id: str) -> GetSummaryAttributesResultItem:
        pass

    @head('/spatialanalyst/summaryregion')
    def head_summary_region(self) -> int:
        pass

    @get('/spatialanalyst/summaryregion', json_deserializer=summary_region_list_deserializer)
    def get_summary_region(self) -> List[GetSummaryRegionResultItem]:
        pass

    @post('/spatialanalyst/summaryregion', entityKW='entity')
    def post_summary_region(self, entity: PostSummaryRegionEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/summaryregion/{job_id}')
    def head_summary_region_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/summaryregion/{job_id}', json_deserializer=summary_region_deserializer)
    def get_summary_region_job(self, job_id: str) -> GetSummaryRegionResultItem:
        pass

    @head('/spatialanalyst/topologyvalidator')
    def head_topologyvalidator(self) -> int:
        pass

    @get('/spatialanalyst/topologyvalidator', json_deserializer=topologyvalidator_list_deserializer)
    def get_topologyvalidator(self) -> List[GetTopologyValidatorResultItem]:
        pass

    @post('/spatialanalyst/topologyvalidator', entityKW='entity')
    def post_topologyvalidator(self, entity: PostTopologyValidatorEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/topologyvalidator/{job_id}')
    def head_topologyvalidator_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/topologyvalidator/{job_id}', json_deserializer=topologyvalidator_deserializer)
    def get_topologyvalidator_job(self, job_id: str) -> GetTopologyValidatorResultItem:
        pass

    @head('/spatialanalyst/vectorclip')
    def head_vector_clip(self) -> int:
        pass

    @get('/spatialanalyst/vectorclip', json_deserializer=vector_clip_list_deserializer)
    def get_vector_clip(self) -> List[GetVectorClipResultItem]:
        pass

    @post('/spatialanalyst/vectorclip', entityKW='entity')
    def post_vector_clip(self, entity: PostVectorClipEntity) -> MethodResult:
        pass

    @head('/spatialanalyst/vectorclip/{job_id}')
    def head_vector_clip_job(self, job_id: str) -> int:
        pass

    @get('/spatialanalyst/vectorclip/{job_id}', json_deserializer=vector_clip_deserializer)
    def get_vector_clip_job(self, job_id: str) -> GetVectorClipResultItem:
        pass
