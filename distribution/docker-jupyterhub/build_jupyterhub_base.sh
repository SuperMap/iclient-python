#!/bin/bash -e
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
docker build -t iclientpy/jupyterhubbase .
docker tag iclientpy/jupyterhubbase:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhubbase:latest
docker push registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhubbase:latest
docker image ls | grep iclientpy/jupyterhubbase | grep none | awk '{ print $3}' | xargs docker image rm || true