#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
rm ./iclientpy-*.whl
cp ../../iclientpy/dist/iclientpy-*.whl ./
rm -rf ./sample
cp ../../iclientpy/sample ./sample -r
docker build --cache-from registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub -t iclientpy/jupyterhub .
docker tag iclientpy/jupyterhub:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest
docker push registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest
docker image ls | grep iclientpy/jupyterhub | grep none | awk '{ print $3}' | xargs docker image rm