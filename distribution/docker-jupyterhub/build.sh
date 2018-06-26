#!/bin/bash -e
rm -rf ./sample
cp ../../iclientpy/iclientpy/sample ./sample -r
docker build --network agent_build_containers -t iclientpy/jupyterhub .
docker tag iclientpy/jupyterhub:latest registry.cn-beijing.aliyuncs.com/iclientpy/jupyterhub:latest