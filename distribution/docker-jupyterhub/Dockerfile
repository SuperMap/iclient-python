FROM jupyterhub/jupyterhub:latest
MAINTAINER iclientpy@supermap.com

ADD pip.conf /root/.pip/pip.conf
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --set show_channel_urls yes \
&& conda install python=3.6 -y
ADD *.whl /tmp/
RUN pip install /tmp/*.whl \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy
ADD jupyterhub_config.py /srv/jupyterhub/
