FROM jupyterhub/jupyterhub:latest
MAINTAINER iclientpy@supermap.com

RUN mkdir /iclientpy
ADD ./sample /iclientpy/sample
ADD jupyterhub_config.py /srv/jupyterhub/
ADD supermap_logo.png /srv/jupyterhub/

ADD ./iclientpy-conda-package.tar /tmp/
RUN conda config --set show_channel_urls yes \
&& conda install -c http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/cloud/conda-forge/ -c http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/main/ -c  http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/free/ -c /tmp/channel --override-channels python=3.6 json-c=0.12.1 iclientpy -y \
&& conda clean -yt \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension

ADD pip.conf /root/.pip/pip.conf
ADD *.whl /tmp/
RUN pip install /tmp/*.whl

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/


