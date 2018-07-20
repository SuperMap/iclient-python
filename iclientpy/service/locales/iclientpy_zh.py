iclientpy_locale = {
    "iclientpy.online.Online.search_map": """
        查找地图
        
        Args:
            owners: 地图所有者
            tags: 地图标签
            keywords: 关键字

        Returns:
            简略的地图信息列表
        """,
    "iclientpy.online.Online.get_map": """
        获取指定id的地图的详细信息
        
        Args:
            map_id: 地图的id

        Returns:
            地图信息
        """,
    "iclientpy.online.Online.upload_data": """
        上传数据
        
        Args:
            data_name: 数据名称
            data_content: 数据流
            type: 数据类型
            callback: 上传进度回调方法

        Returns:
            数据的id
        """,
    "iclientpy.online.Online.upload_dataframe_as_json": """
        上传DataFrame为JSON类型数据
        
        Args:
            data_name: 上传后数据名称
            df: DataFrame数据
            
        """,
    "iclientpy.online.Online.search_data": """
        查找数据
        
        Args:
            owners: 数据所有者
            tags: 数据标签
            keywords: 数据关键字

        Returns:
            数据信息的列表
        """,
    "iclientpy.online.Online.get_data": """
        获取数据详细信息
        
        Args:
            data_id: 数据的id

        Returns:
            数据的信息
        """,
    "iclientpy.online.Online.get_data_upload_progress": """
        获取数据上传进度
        
        Args:
            data_id: 数据的id

        Returns:

        """,
    "iclientpy.online.Online.create_map": """
        创建地图
        
        Args:
            layers: 地图图层
            epsgCode: 投影编码
            map_title: 地图名称
            center: 地图中心点
            extend: 地图缩放范围
            base_layer_type: 默认底图类型
            tags: 地图标签

        Returns:
            地图的id
        """,
    "iclientpy.online.Online.delete_map": """
        删除一个地图
        
        Args:
            map_id:地图id
        """,
    "iclientpy.online.Online.delete_maps": """
        删除多个地图
        
        Args:
            map_ids: 地图的id列表
        """,
    "iclientpy.online.Online.delete_data": """
        删除一个数据
        
        Args:
            data_id: 数据的id
        """,
    "iclientpy.online.Online.delete_datas": """
        批量删除多个数据
        
        Args:
            data_ids: 数据的id列表
        """,
    "iclientpy.online.Online.prepare_geojson_layer": """
        根据上传到Online的geojson数据，生成Layer
        
        Args:
            data_id: 数据在Online中的id
            layer_name: 图层名称

        Returns:
            Layer信息
        """,
    "iclientpy.online.Online.share_data": """
        共享数据
        
        Args:
            data_id: 数据id
            is_public: 是否公开
        """,
    "iclientpy.online.Online.share_map": """
        共享地图
        
        Args:
            map_id: 地图id
            is_public: 是否公开
        """,
    "iclientpy.dtojson.to_json_str": """
   将json对象转为json字符串

   Args:
       obj: Python对象，用于转为json字符串

   Returns:
       字符串，Python对象转成的json字符串
   """

}
