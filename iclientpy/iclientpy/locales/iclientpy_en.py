iclientpy_locale = {
    "iclientpy.online.Online.search_map": """
        search map
        Args:
            owners: map owner
            tags: map tags
            keywords: map keywords

        Returns:
            map info
        """,
    "iclientpy.online.Online.get_map": """
        get map by map's id
        Args:
            map_id: map's id

        Returns:
            地图信息
        """,
    "iclientpy.online.Online.upload_data": """
        upload data
        Args:
            data_name: data name
            data_content: data stream
            type: data type
            callback: upload progress callback function

        Returns:
            data id
        """,
    "iclientpy.online.Online.upload_dataframe_as_json": """
        upload DataFrame as json type data
        Args:
            data_name: data name
            df: DataFrame content

        Returns:

        """,
    "iclientpy.online.Online.search_data": """
        search data
        Args:
            owners: data owner
            tags: data tags
            keywords: data keywords

        Returns:
            data info
        """,
    "iclientpy.online.Online.get_data": """
        get data info by data id
        Args:
            data_id: data id

        Returns:
            data info
        """,
    "iclientpy.online.Online.get_data_upload_progress": """
        get data upload progress
        Args:
            data_id: data id

        Returns:

        """,
    "iclientpy.online.Online.create_map": """
        create map
        Args:
            layers: map layers
            epsgCode: epsg code
            map_title: map title
            center: map center point
            extend: map extend
            base_layer_type: base layer type
            tags: map tags

        Returns:
            map id
        """,
    "iclientpy.online.Online.delete_map": """
        delete map
        Args:
            map_id:map id
        """,
    "iclientpy.online.Online.delete_maps": """
        delete multi map
        Args:
            map_ids: map id list
        """,
    "iclientpy.online.Online.delete_data": """
        delete data
        Args:
            data_id: data id
        """,
    "iclientpy.online.Online.delete_datas": """
        delete multi data
        Args:
            data_ids: data id list
        """,
    "iclientpy.online.Online.prepare_geojson_layer": """
        prepare layer by geojson
        Args:
            data_id: geojson data id
            layer_name: layer name

        Returns:
            Layer信息
        """,
    "iclientpy.online.Online.share_data": """
        share data
        Args:
            data_id: data id 
            is_public: public or not
        """,
    "iclientpy.online.Online.share_map": """
        share map 
        Args:
            map_id: map id 
            is_public: public or not
        """,
    "iclientpy.dtojson.to_json_str": """
   convert json object to json string

   Args:
       obj: python object

   Returns:
       string 
   """

}
