FROM jupyterhub/jupyterhub:latest
MAINTAINER iclientpy@supermap.com

RUN mkdir /iclientpy
ADD ./sample /iclientpy/sample
ADD jupyterhub_config.py /srv/jupyterhub/
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyter.png
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyterhub-80.png

ADD ./iclientpy-conda-package.tar /tmp/
RUN conda config --add channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/free/ \
&& conda config --add channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/main/ \
&& conda config --add channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/cloud/conda-forge/ \
&& conda config --set show_channel_urls yes \
&& conda install -y python=3.6 \
&& conda install -y json-c=0.12.1 \
&& conda install -c /tmp/channel iclientpy -y \
&& conda clean -yt \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension \
&& conda config --remove channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/free/ \
&& conda config --remove channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/pkgs/main/ \
&& conda config --remove channels http://mirrortsinghua:8081/repository/tuna_conda-forge/anaconda/cloud/conda-forge/

ADD pip.conf /root/.pip/pip.conf
ADD *.whl /tmp/
RUN pip install /tmp/*.whl

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/


