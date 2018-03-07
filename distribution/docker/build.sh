#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
docker rmi -f $(docker images | grep supermap/iclientpy-jupyter-notebook | awk '{print $3}')
rm -rf ./sample
cp ../../jupyter/sample ./sample -r
rm ./iclientpy-*.whl
cp ../../jupyter/dist/iclientpy-*.whl ./
docker build -t supermap/iclientpy-jupyter-notebook .
docker tag supermap/iclientpy-jupyter-notebook:latest registry.cn-beijing.aliyuncs.com/supermap/iclientpy-jupyter-notebook:latest
docker push registry.cn-beijing.aliyuncs.com/supermap/iclientpy-jupyter-notebook:latest