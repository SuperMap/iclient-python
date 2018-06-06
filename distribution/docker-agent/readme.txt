1:关于下列命令中的172.17.0.1
RUN curl http://172.17.0.1:8080/Anaconda3-5.1.0-Linux-x86_64.sh -o ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
是通过python3 -m http.server 8080启动了一个本地服务器，Anaconda安装文件是从清华大学开源软件镜像站（https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/）下载的
下载安装删除，而不是ADD 安装 ，这么做的目的是减小镜像大小（也许能吧）

2:关于sonar
需要去https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner下载sonar-scanner解压并添加到环境变量

3：使用的时候需要conda activate base，查看activate后的path，然后设置agent环境变量env.ICLIENTPY_CONDA_ENV_ACTIVATED_PATH为activate后的path。
因为teamcity-agent镜像中自己包含了python，为了避免冲突，故让conda环境独立，只在跑iclientpy时进行设置。
在iClientPy的teamcity构建中有设置env.PATH=%env.ICLIENTPY_CONDA_ENV_ACTIVATED_PATH%
