#!/bin/bash -e
rm -rf ./sample
cp ../../iclientpy/iclientpy/sample ./sample -r
docker rmi -f $(docker images | grep iclientpy/iclientpy-jupyter-notebook | awk '{print $3}' | uniq) || true
docker build -t iclientpy/iclientpy-jupyter-notebook .
docker tag iclientpy/iclientpy-jupyter-notebook:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook:latest