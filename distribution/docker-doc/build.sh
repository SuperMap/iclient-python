#!/bin/bash
docker login registry.cn-beijing.aliyuncs.com -u guyongquan@outlook.com -p $(cat /data/teamcity_agent/conf/alidockerregistrypwd)
rm -rf doc.tar
rm -rf conda_pkg.tar
curl --output ./conda_pkg.tar http://ci.ispeco.com:90/guestAuth/repository/download/IClientPy_iClientPyCondaPkg/.lastSuccessful/iclientpy/conda/iclientpy-conda-package.tar
curl --output ./doc.tar http://ci.ispeco.com:90/guestAuth/repository/download/IClientPy_IClientPyDoc/.lastSuccessful/doc.tar
docker rmi -f $(docker images | grep iclientpy-supermap-io | awk '{print $3}')
docker build -t iclientpy/iclientpy-supermap-io:latest .
docker tag iclientpy/iclientpy-supermap-io:latest registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supermap-io:latest
docker push registry.cn-beijing.aliyuncs.com/iclientpy/iclientpy-supermap-io:latest
