#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
curl --output ./doc.tar http://ci.ispeco.com:90/guestAuth/repository/download/IClientPy_IClientPyDoc/.lastSuccessful/doc.tar
docker rmi -f $(docker images | grep iclientpy-supmap-io | awk '{print $3}')
docker build -t iclientpy/iclientpy-supmap-io:latest .
docker tag iclientpy/iclientpy-supmap-io:latest registry-internal.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supmap-io:latest
docker push registry-internal.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supmap-io:latest
