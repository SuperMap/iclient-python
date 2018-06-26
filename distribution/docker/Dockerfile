FROM jupyter/scipy-notebook:latest
MAINTAINER iclientpy@supermap.com

RUN mkdir -p /home/jovyan/.jupyter/custom
ADD ./custom /home/jovyan/.jupyter/custom
ADD pip.conf /home/jovyan/.pip/pip.conf
ADD ./sample /home/jovyan/work

ADD ./iclientpy-conda-package.tar /tmp/
RUN conda config --set show_channel_urls yes \
&& conda install -c http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/cloud/conda-forge/  -c http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/main/  -c http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/free/ -c /tmp/channel --override-channels iclientpy -y \
&& conda clean -yt \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension 

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/