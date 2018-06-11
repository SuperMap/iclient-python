#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
rm -rf ./sample
cp ../../iclientpy/iclientpy/sample ./sample -r
docker build -t iclientpy/iclientpy-jupyter-notebook .
docker tag iclientpy/iclientpy-jupyter-notebook:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook:latest
docker push registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook:latest
docker image ls | grep iclientpy/iclientpy-jupyter-notebook | grep none | awk '{ print $3}' | xargs docker image rm || true