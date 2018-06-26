#!/bin/bash -e
rm -rf ./sample
cp ../../iclientpy/iclientpy/sample ./sample -r
docker build --network agent_build_containers -t iclientpy/iclientpy-jupyter-notebook .
docker tag iclientpy/iclientpy-jupyter-notebook:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-jupyter-notebook:latest