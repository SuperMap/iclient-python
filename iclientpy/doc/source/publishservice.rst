服务发布
======================
服务发布API使用介绍

1. 引入Server，并创建一个实例，以服务地址为http://localhost:8090/iserver，用户名为admin，密码为supermap的服务为例

    ::

        from iclientpy.server import Server
        server = Server('http://localhost:8090/iserver','admin','supermap')

2. 构建服务发布准备实例

    ::

        prepare = server.prepare_workspace_for_publish()

3. 确定使用工作空间类型，支持文件型工作空间，带密码的文件型工作空间、ORACLE工作空间、SQL工作空间、PGSQL工作空间，以文件型工作空间为例

    ::

        prepare.use_file_workspace()

4. 远程浏览文件夹，找到工作空间，以位置 /home/supermap/iserver/webapps/iserver/World/World.sxwu 为例

    ::

        fe=prepare.workspace.get_file_explorer()
        # 查看当前路径下文件
        fe.files
        # 进入序列号为4文件夹
        fe[4].enter()
        # 查看文件夹下所有文件
        fe.files
        # 查看序列号为1的目标文件的路径
        fe.files[1].path
5. 设置工作空间路径：

    ::

        prepare.workspace.set_path(fe.files[1].path)
6. 设置地图发布类型，以RESTMAP为例

    ::

        prepare.avaliable_service_types.RESTMAP.select()
7. 执行发布

    ::

        prepare.execute()


