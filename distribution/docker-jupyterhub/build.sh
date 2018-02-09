#!/bin/bash -e
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
docker rmi -f $(docker images | grep iclientpy/jupyterhub | awk '{print $3}')
rm ./iclientpy-*.whl
cp ../../jupyter/dist/iclientpy-*.whl ./
docker build -t iclientpy/jupyterhub .
docker tag iclientpy/iclientpy-supermap-io:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest
docker push registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest