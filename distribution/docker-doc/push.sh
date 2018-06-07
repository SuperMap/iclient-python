#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
docker push \
registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supermap-io:latest
