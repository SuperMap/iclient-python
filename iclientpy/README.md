# iclientpy
===============================

## SuperMap iClient Python

超图云 GIS 客户端 Python SDK。可以与Jupyter Notebook深度结合，进行数据可视化，也可以使用Python进行数据处理然后调用超图云产品进行数据分析，服务发布等。

### 简介

官网：http://iclientpy.supermap.io/

### Samples

![sample](./iclientpy/doc/source/_static/sample.png)

### 许可

[ Apache License 2.0 ](./LICENSE)


## iclient for jupyter

Installation
------------

To install use pip:

    $ pip install iclientpy
    $ jupyter nbextension enable --py --sys-prefix iclientpy


For a development installation (requires npm),

    $ git clone https://github.com/SuperMap/iclient-python.git
    $ cd iclientpy
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix iclientpy
    $ jupyter nbextension enable --py --sys-prefix iclientpy
