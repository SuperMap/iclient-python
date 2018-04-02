获取iClientPy
==============

iClientPy正在开发中，如果你有意试用，可以通过两个途径获取：

    * 检出源代码本地安装： **需要确保本地的python环境为3.6.x**

        1. 从https://gitee.com/isupermap/iClientPython下载代码或者复制git地址，通过git客户端复制代码到本地
        2. 打开命令行，进入到代码文件夹内
        3. 执行命令pip install -r requirements.txt安装依赖
        4. 执行命令python setup.py install进行安装
        5. 执行命令pip list，检查iclientpy是否已经安装
        6. 执行命令jupyter nbextension install --py --symlink --sys-prefix iclientpy为jupyter安装扩展
        7. 执行命令jupyter nbextension enable --py --sys-prefix iclientpy启动扩展

    * 从docker镜像启动

        1. 执行命令docker pull docker pull registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook拉取最新的iClientPy的jupyterhub镜像
        2. 执行命令docker run --name {containername} -p {port}:8888 docker pull registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook，{containername}为创建后docker容器名称，{port}为docker宿主机上未被占用端口
        3. 访问http://{ip}:{port}

            **注意：** 该服务默认需要token登录，可以通过命令 docker logs {containername}查看notebook日志获取token

使用过程中出现问题，可以：

    * 到https://gitee.com/isupermap/iClientPython/issues提试用issue，留下你的联系方式，开发人员会联系你。