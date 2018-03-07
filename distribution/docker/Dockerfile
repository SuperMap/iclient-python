FROM jupyter/scipy-notebook:latest
MAINTAINER iclientpy@supermap.com
RUN mkdir -p /home/jovyan/.jupyter/custom
ADD ./custom /home/jovyan/.jupyter/custom
ADD pip.conf /home/jovyan/.pip/pip.conf
ADD ./sample /home/jovyan/work
ADD *.whl /tmp/
RUN pip install /tmp/*.whl \
&& jupyter nbextension install --py --symlink --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix iclientpy \
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension