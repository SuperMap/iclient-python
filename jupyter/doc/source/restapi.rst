restapi
=======

这部分内容主要是将iServer和iPortal的REST API封装为可直接调用的python api，方便直接脚本化iServer或者iPortal任务。

API列表如下：

* APIFactory_
* RestData_
* Management_
* 其他_

APIFactory
************

api的工厂类，所有的api从这个类中生产

* management

    生成iServer管理类api的方法

* data_service

    生成iServer的数据服务类的api的方法

RestData
**********

数据服务类api

* get_features

    获取要素（feature）信息集合。

* post_features

    添加、删除、修改要素集中的要素

Management
*************

管理类api

* get_workspaces

    获取当前所有工作空间列表

* post_workspaces

    将工作空间快速发布成服务

* head_tilejobs

    检查 tileJobs 资源是否存在，或权限是否可以访问 tileJobs 资源。

* get_tilejobs

    获取 tileJobs 资源的表述，即创建分布式缓存任务的入口，返回切图任务列表。

* post_tilejobs

    创建新的切图任务。

* head_tilejob

    检查 tileJob 资源是否存在，或权限是否可以访问 tileJob 资源。

* get_tilejob

    获取指定切图任务的状态和信息。

* put_tilejob

    更新指定切图任务的运行状态。即启动/暂停切图任务。

* delete_tilejob

    删除当前指定的切图任务。

* get_tilesetupdatejobs

    获取切片更新的任务列表

* post_tilesetupdatejobs

    创建新的切片更新任务

* get_tilesetupdatejob

    获取指定切片更新任务的状态和信息

其他
******

* update_smtilestileset

    便捷的对smtiles切片缓存进行更新