FROM iclientpy/jupyterhubbase:latest
MAINTAINER iclientpy@supermap.com

ADD jupyterhub_config.py /srv/jupyterhub/
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyter.png
ADD supermap_logo.png /opt/conda/share/jupyter/hub/static/images/jupyterhub-80.png
RUN mkdir /iclientpy
ADD ./sample /iclientpy/sample
ADD *.whl /tmp/
RUN pip install /tmp/*.whl \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension


