服务API简介
==============

这部分内容主要是将iServer和iPortal的REST API封装为可直接调用的python api，方便直接脚本化iServer或者iPortal任务。

API列表如下：

* APIFactory_
* DataService_
* Management_
* MapService_
* SecurityService_
* DistributedAnalyst_
* Datacatalog_
* 其他_

APIFactory
************

api的工厂类，所有的api从这个类中生产
**注：** {tokenstr}为占位字符串，生成token字符串请参考：:ref:`token工具`.

* data_service

    生成iServer的数据服务类的api的方法。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        ds = api.data_service('data-World/rest')

* management

    生成iServer管理类api的方法。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()


* map_service

    返回指定地图服务的相关数据的api
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.map_service('map-World')


* security_service

    返回安全类服务的api
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.security_service()

* distributedanalyst_service

    返回分布式分析服务的api
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.distributedanalyst_service()

* datacatalog_service

    返回数据目录服务api
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.datacatalog_service()


DataService
************

数据服务类api

* get_features

    获取要素（feature）信息集合。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        ds = api.data_service('data-World/rest')
        result = ds.get_features(datasourceName='World',datasetName='Countries',fromIndex=0,toIndex=3)

* post_features

    添加、删除、修改要素集中的要素。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        ds = api.data_service('data-World/rest')
        entity=[...]
        result = ds.post_features(datasourceName='World',datasetName='Countries',entity=entity)

Management
*************

管理类api

* get_workspaces

    获取当前所有工作空间列表。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_workspaces()

* post_workspaces

    将工作空间快速发布成服务。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        param = PostWorkspaceParameter()
        param....
        result = mng.post_workspaces(param)

* head_tilejobs

    检查 tileJobs 资源是否存在，或权限是否可以访问 tileJobs 资源。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.head_tilejobs()

* get_tilejobs

    获取 tileJobs 资源的表述，即创建分布式缓存任务的入口，返回切图任务列表。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_tilejobs()

* post_tilejobs

    创建新的切图任务。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        entity = PostTileJobsItem()
        result = mng.post_tilejobs(entity)

* head_tilejob

    检查 tileJob 资源是否存在，或权限是否可以访问 tileJob 资源。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.head_tilejob()

* get_tilejob

    获取指定切图任务的状态和信息。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        idstr = 'id'
        result = mng.get_tilejob(idstr)

* put_tilejob

    更新指定切图任务的运行状态。即启动/暂停切图任务。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        idstr = 'id'
        result = mng.put_tilejob(idstr,entity=BuildState.STOPPED)

* delete_tilejob

    删除当前指定的切图任务。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        idstr = 'id'
        result = mng.delete_tilejob(idstr)

* get_tilesetupdatejobs

    获取切片更新的任务列表。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_tilesetupdatejobs()

* post_tilesetupdatejobs

    创建新的切片更新任务。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        entity = PostTilesetUpdateJobs()
        entity....
        result = mng.post_tilesetupdatejobs(entity)

* get_tilesetupdatejob

    获取指定切片更新任务的状态和信息。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        idstr = 'id'
        result = mng.get_tilesetupdatejob(idstr)

* get_service

    获取服务信息。
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_service('map-World')


* get_fileuploadtasks

    获取文件上传任务列表
    ::

        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_fileuploadtasks()

* post_fileuploadtask

    创建文件上传任务
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        param = PostFileUploadTasksParam()
        result = mng.get_fileuploadtasks(param)

* post_fileuploadtask

    上传文件
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        id = 'id'
        f = open('./World.zip')
        result=mng.post_fileuploadtask(id, f, 'world')

* get_fileuploadtask

    获取指定的文件上传任务信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        id = 'id'
        result=mng.get_fileuploadtask(id)

* get_datastores

    获取所有的数据注册列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        result = mng.get_datastores()

* get_datastore

    获取指定的存储位置信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        mng = api.management()
        id = 'id'
        result = mng.get_datastore(id)


MapService
**************

* get_map

    获取地图当前状态的基本信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        map_s = api.map_service('map-World')
        map_name = 'World'
        result = map_s.get_map(map_name)

SecurityService
*********************

* post_tokens

    输入用户信息申请 Token。
    ::
        api = APIFactory('http://localhost:8090/iserver', {name}, {password})
        sec = api.security_service()
        param = PostTokenParameter()
        result = sec.post_tokens(param)

DistributedAnalyst
*************************

* get_aggregatepoints

    获取点聚合分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_aggregatepoints()

* post_aggregatepoints

    创建点聚合分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostAgggregatePointsEntity()
        result = dis.post_aggregatepoints(param)

* get_aggregatepoints_job

    获取指定id的点聚合分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_aggregatepoints_job(job_id)

* get_featurejoin

    获取要素连接作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_featurejoin()

* post_featurejoin

    创建要素连接作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostFeatureJoinEntity()
        result = dis.post_featurejoin(param)

* get_featurejoin_job

    获取指定的要素连接作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_featurejoin_job(job_id)

* get_buffers

    获取缓冲区分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_buffers()

* post_buffers

    创建缓冲区分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostBuffersEntity()
        rsult = dis.post_buffers(param)

* get_buffers_job

    获取指定的缓冲区分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_buffers_job(job_id)

* get_density

    获取密度分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_density()

* post_density

    创建密度分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostDensityentity()
        result = dis.post_density(param)

* get_density_job

    获取指定的密度分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_density_job(job_id)

* get_overlay

    获取叠加分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_overlay()

* post_overlay

    创建叠加分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostOverlayEntity()
        result = dis.post_overlay(param)

* get_overlay_job

    获取指定的叠加分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_overlay_job(job_id)

* get_query

    获取单对象空间查询分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_query()

* post_query

    创建单对象空间查询分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostQueryEntity()
        result = dis.post_query(param)

* get_query_job

    获取指定的单对象空间查询分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_query_job(job_id)

* get_summary_attributes

    获取属性汇总统计分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_summary_attributes()

* post_summary_attributes

    创建属性汇总统计分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostSummaryAttributesEntity()
        result = dis.post_summary_attributes(param)

* get_summary_attributes_job

    获取指定的属性汇总统计分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_summary_attributes_job(job_id)

* get_summary_region

    获取区域汇总分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_summary_region()

* post_summary_region

    创建区域汇总分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostSummaryRegionEntity()
        result = dis.post_summary_region(param)

* get_summary_region_job

    获取指定的区域汇总分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_summary_region_job(job_id)

* get_topologyvalidator

    获取拓扑检查作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_topologyvalidator()

* post_topologyvalidator

    创建拓扑检查作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostTopologyValidatorEntity()
        result = dis.post_topologyvalidator(param)

* get_topologyvalidator_job

    获取指定的拓扑检查作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_topologyvalidator_job(job_id)

* get_vector_clip

    获取矢量裁剪分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        result = dis.get_vector_clip()

* post_vector_clip

    创建矢量裁剪分析作业列表
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        param = PostVectorClipEntity()
        result = dis.post_vector_clip(param)

* get_vector_clip_job

    获取指定的矢量裁剪分析作业
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dis = api.distributedanalyst_service()
        job_id = 'job_id'
        result = dis.get_vector_clip_job(job_id)

Datacatalog
**********************

* get_relationship_datasets

    获取关系数据源中所有数据集的信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        result = dat.get_relationship_datasets()

* get_relationship_dataset

    获取关系数据集的详细信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        result = dat.get_relationship_dataset(dataset_name)

* get_relationship_dataset_fields

    获取关系数据集的字段列表信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        result = dat.get_relationship_dataset_fields(dataset_name)

* get_relationship_dataset_field

    获取关系数据集中某一字段详细信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        field_name = 'field'
        result = dat.get_relationship_dataset_field(dataset_name, field_name)

* get_sharefile

    获取共享文件数据源中所有数据集的信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        result = dat.get_sharefile()

* get_sharefile_dataset

    获取共享文件数据集的详细信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        result = dat.get_sharefile_dataset(dataset_name)

* get_sharefile_dataset_fields

    获取共享文件数据集的字段列表信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        result = dat.get_sharefile_dataset_fields(dataset_name)

* get_sharefile_dataset_field

    获取共享文件数据集中某一字段详细信息
    ::
        api = APIFactory('http://localhost:8090/iserver',token={tokenstr})
        dat =  api.datacatalog_service()
        dataset_name = 'dataset'
        field_name = 'field'
        result = dat.get_sharefile_dataset_field(dataset_name, field_name)

其他
******

* update_smtilestileset

    便捷的对smtiles切片缓存进行更新。
    ::

        update_smtilestileset("http://localhost:8090/iserver", None, None, '/etc/data/World/World.sxwu', 'World', (-180, 90),(-180, -90, 180, 90), '/etc/data/update/update.smtiles',[4000000.000014754, 8000000.000197801],token={tokenstr})

* recache_tileset

    对某一地图组件进行重新切图
    ::
        recache_tileset('http://192.168.20.182:8090/iserver', 'admin', 'Supermap123', component_name='map-World',  map_name='World', storageid={storageid})