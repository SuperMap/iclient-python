FROM jupyterhub/jupyterhub:latest
MAINTAINER iclientpy@supermap.com

ADD pip.conf /root/.pip/pip.conf
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
&& conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
&& conda config --set show_channel_urls yes \
&& conda install python=3.6 lxml beautifulsoup4 geopandas fiona -y \
&& mkdir /iclientpy
ADD ./sample /iclientpy/sample
ADD *.whl /tmp/
RUN pip install /tmp/*.whl \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension \
&& rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6* \
&& ln -s /opt/conda/lib/libstdc++.so.6.0.21 /usr/lib/x86_64-linux-gnu/libstdc++.so.6 \
&& ln -s /opt/conda/lib/libcurl.so.4.5.0 /usr/lib/x86_64-linux-gnu/libcurl.so.4 \
&& conda update --all
ADD jupyterhub_config.py /srv/jupyterhub/
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyter.png
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyterhub-80.png
