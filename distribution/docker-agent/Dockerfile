FROM jetbrains/teamcity-agent:latest
MAINTAINER iclientpy@supermap.com

ADD sources.list.16.04 /etc/apt/sources.list
RUN apt-get update \
&& apt-get install -y nodejs npm \
&& apt-get autoclean \
&& apt-get autoremove
ADD *.deb /root/
RUN dpkg -i /root/*.deb
RUN rm -rf /usr/bin/python3 \
&& ln -s /usr/bin/python3.6 /usr/bin/python3 \
&& rm -rf /usr/bin/python \
&& ln -s /usr/bin/python3.6 /usr/bin/python \
&& apt-get install -y python3-pip
RUN ln -s /usr/bin/nodejs /usr/bin/node \
&& npm config set registry https://registry.npm.taobao.org \
&& mkdir /root/.pip
ADD pip.conf /root/.pip/pip.conf
RUN npm install -g n \
&& n stable \
&& npm update npm -g \
&& pip3 install --upgrade pip \
&& pip install teamcity-messages
