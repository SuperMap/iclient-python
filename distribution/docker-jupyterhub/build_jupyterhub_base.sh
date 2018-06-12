#!/bin/bash -e
docker rmi -f $(docker images | grep iclientpy/jupyterhubbase | awk '{print $3}' | uniq) || true
docker build -t iclientpy/jupyterhubbase -f Dockerfile_base .
docker tag iclientpy/jupyterhubbase:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhubbase:latest