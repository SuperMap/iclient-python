iClientPy概览
======================

iClinetPy主要有以下几个模块：

* viz模块是Jupyter Notebook中地图可视化部分，可直接在Jupyter Notebook将数据在地图进行展示

* rest模块是对iServer的REST API的封装，产生的python接口可直接调用，其中：

    1. APIFactory所有的服务产生的工厂类，用于生成各个api。
    2. cmd包下面主要是定制过的小工具，可以便捷的调用iServer，完成指定任务

* jupyter模块也是Jupyter Notebook可视化部分，但这一层级调用比较麻烦，建议使用viz模块下的函数



