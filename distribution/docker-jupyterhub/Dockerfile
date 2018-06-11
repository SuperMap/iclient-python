FROM jupyterhub/jupyterhub:latest
MAINTAINER iclientpy@supermap.com

ADD jupyterhub_config.py /srv/jupyterhub/
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyter.png
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyterhub-80.png
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \
&& conda config --set show_channel_urls yes
RUN conda install -y python=3.6 && conda clean -yt 
RUN mkdir /iclientpy
ADD ./sample /iclientpy/sample
ADD ./iclientpy-conda-package.tar /tmp/
RUN conda install json-c=0.12.1 \
&& conda install -c /tmp/channel iclientpy -y \
&& conda clean -yt \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension

ADD pip.conf /root/.pip/pip.conf
ADD *.whl /tmp/
RUN pip install /tmp/*.whl


