#!/bin/bash
docker rmi -f $(docker images | grep iclientpy-supermap-io | awk '{print $3}')
docker build -t iclientpy/iclientpy-supermap-io:latest .
docker tag iclientpy/iclientpy-supermap-io:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supermap-io:latest
