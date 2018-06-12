#!/bin/bash -e
docker rmi -f $(docker images | grep iclientpy-supermap-io | awk '{print $3}' | uniq) || true
docker build -t iclientpy/iclientpy-supermap-io:latest .
docker tag iclientpy/iclientpy-supermap-io:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supermap-io:latest
