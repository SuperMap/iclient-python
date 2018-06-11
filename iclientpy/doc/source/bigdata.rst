大数据分析
======================
大数据分析服务的API使用介绍

* 点聚合分析_
* 其他分析_


点聚合分析
------------------
指的是针对点数据集制作聚合图的一种空间分析作业。指通过网格面或多边形对地图点要素进行划分，然后，计算每个面对象内点要素的数量，并作为面对象的统计值，也可以引入点的权重信息，考虑面对象内点的加权值作为面对象的统计值；最后基于面对象的统计值，按照统计值大小排序的结果，通过色带对面对象进行色彩填充。将分别通过网格面和多边形进行划分要素的点聚合分析分别称为网格面聚合和多边形聚合，下面分别对这两种点聚合分析的使用进行介绍：

网格面聚合
***************
以点数据data_cities_newyorkPoint_P为例：

1. 引入Server，并创建一个实例，以服务地址为http://localhost:8090/iserver，用户名为admin，密码为supermap的服务为例

    ::

        from iclientpy.server import Server
        server = Server('http://localhost:8090/iserver','admin','supermap')
2. 构建网格面聚合分析的准备实例

    ::

        prepare = server.bigdatas.datas_cites_newyorkPoint_P.prepare_summary_mesh_aggregate()
3. 设置聚合使用字段，以及统计方法（max,min,average,sum,variance,stdDeviation），以trip_distance字段进行max统计为例：

    ::

        prepare.available_fields.trip_distance.statistic_with_max()
4. 可重复第三步，设置多个统计字段，并为字段设置统计方法
5. 设置网格面为四边形或者六边形（可省略，默认为四边形网格）

    ::

        prepare.set_mesh_square()
        or
        prepare.set_mesh_hexagon()

6. 设置网格大小，网格单位，以大小为100，单位为Meter为例（单位可省略，默认为Meter）

    ::

        prepare.set_resolution(100)
        prepare.available_mesh_sieze_units.Meter.select()

7. 设置数字精度，分析范围等（可省略，数字精度默认为1，分析范围默认为全图）

    ::

        prepare.set_numeric_precision(1)
        prepare.set_bounds((-74.050,40.650,-73.850,40.850))
8. 执行分析

    ::

        prepare.execute()


多边形聚合
****************
以点数据data_cities_newyorkPoint_P和面数据datas_cites_newyorkZone_R为例：

1. 引入Server，并创建一个实例，以服务地址为http://localhost:8090/iserver，用户名为admin，密码为supermap的服务为例

    ::

        from iclientpy.server import Server
        server = Server('http://localhost:8090/iserver','admin','supermap')
2. 构建多边形聚合分析的准备实例

    ::

        prepare = server.bigdatas.datas_cites_newyorkPoint_P.prepare_summary_region_aggregate()
3. 设置聚合使用字段，以及统计方法（max,min,average,sum,variance,stdDeviation），以trip_distance字段进行max统计为例：

    ::

        prepare.available_fields.trip_distance.statistic_with_max()
4. 可重复第三步，设置多个统计字段，并为字段设置统计方法
5. 设置聚合面数据集

    ::

        prepare.available_region_datasets.datas_cites_newyorkZone_R.select()
6. 设置数字精度（可省略，数字精度默认为1）

    ::

        prepare.set_numeric_precision(100)
7. 执行分析

    ::

        prepare.execute()

其他分析
---------------
密度分析、单对象空间查询分析、区域汇总分析、矢量裁剪分析、叠加分析、缓冲区分析、属性汇总分析、拓扑检查分析、要素连接分析仍在开发中...