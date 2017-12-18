FROM jetbrains/teamcity-agent:latest
MAINTAINER iclientpy@supermap.com

ADD sources.list.16.04 /etc/apt/sources.list
RUN apt-get update \
&& apt-get install -y python3-pip nodejs npm \
&& apt-get autoclean \
&& apt-get autoremove
RUN rm -rf /usr/bin/python \
&& ln -s /usr/bin/python3.5 /usr/bin/python \
&& ln -s /usr/bin/nodejs /usr/bin/node \
&& npm config set registry https://registry.npm.taobao.org \
&& mkdir /root/.pip
ADD pip.conf /root/.pip/pip.conf
RUN npm install -g n \
&& n stable \
&& npm update npm -g \
&& pip3 install --upgrade pip \
&& pip install teamcity-messages
