FROM jupyter/scipy-notebook:latest
MAINTAINER iclientpy@supermap.com
RUN mkdir -p /home/jovyan/.jupyter/custom
ADD ./custom /home/jovyan/.jupyter/custom
ADD pip.conf /home/jovyan/.pip/pip.conf
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \
&& conda config --set show_channel_urls yes
ADD ./iclientpy-conda-package.tar /tmp/
RUN conda install -c /tmp/channel iclientpy -y \
&& conda clean -yt
ADD ./sample /home/jovyan/work
RUN jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension