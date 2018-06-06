FROM jetbrains/teamcity-agent:latest
MAINTAINER iclientpy@supermap.com

ADD sources.list.16.04.tsinghua /etc/apt/sources.list

ADD pip.conf /root/.pip/pip.conf

RUN apt-get update --fix-missing && apt-get install -y bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN curl http://172.17.0.1:8080/Anaconda3-5.1.0-Linux-x86_64.sh -o ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
	
RUN . /opt/conda/etc/profile.d/conda.sh && conda activate base \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \
    && conda config --set show_channel_urls yes \
    && conda install -y pyinstaller ipython conda-build=3.0.27 sphinx==1.7.2 coverage \
	&& pip install teamcity-messages
	
RUN apt-get update \
&& apt-get install -y nodejs npm \
&& apt-get autoclean \
&& apt-get autoremove

RUN ln -s /usr/bin/nodejs /usr/bin/node \
&& npm config set registry https://registry.npm.taobao.org 
RUN npm install -g n \
&& n stable \
&& npm update npm -g
