导入GeoDataFrame
======================
导入GeoDataFrame功能介绍

1. 引入Server，并创建一个实例，以服务地址为http://localhost:8090/iserver，用户名为admin，密码为supermap的服务为例

    ::

        import pandas as pd
        from geopandas import GeoDataFrame
        from iclientpy.server import Server
        server = Server('http://localhost:8090/iserver','admin','supermap')

2. 获取服务列表，选择数据服务，以data-World/rest为例：

    ::

        services = server.services
        services
        ds = services['data-World/rest']

3. 获取数据集，并选择数据集，选择数据集以World_Poly_REGION为例：

    ::

        datasets = ds.datasets
        datasets
        dataset = datasets['World_Poly_REGION']

4. 从外部读取数据，构建GeoDataFrame，以 `示范 <http://jupyter.supermap.io>`_ 中的province.csv和data.json数据为例

    ::

        df = pd.read_csv("province.csv")
        df["2015年"] = pd.to_numeric(df["2015年"],errors='coerce')
        gdf = GeoDataFrame.from_file('./data.json')
        result = gdf.merge(df,left_on='name',right_on='地区')
        result.drop(['name'],axis=1,inplace=True)

5. 导入数据集

    ::

        dataset.import_features_from_geodataframe(result)