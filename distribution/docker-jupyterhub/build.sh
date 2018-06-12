#!/bin/bash -e
rm -rf ./sample
cp ../../iclientpy/iclientpy/sample ./sample -r
docker rmi -f $(docker images | grep iclientpy/jupyterhub | grep -v iclientpy/jupyterhubbase | awk '{print $3}' | uniq) || true
docker build -t iclientpy/jupyterhub .
docker tag iclientpy/jupyterhub:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest