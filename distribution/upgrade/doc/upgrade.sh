#!/bin/bash -e
Current_Dir=$(cd "$(dirname "$0")";pwd)
cd $Current_Dir
while read LINE
do
export $LINE
done < ./rancher.conf
oldid=$(docker image ls -q $IMAGE_ADDRESS:latest)
docker pull $IMAGE_ADDRESS
newid=$(docker image ls -q $IMAGE_ADDRESS:latest)
if [[ "$oldid" != "$newid" ]];then
echo $IMAGE_ADDRESS:latest is newer. Upgrading container...
rancher-compose up -p --force-upgrade -c -d
else
echo $IMAGE_ADDRESS:latest is up to date. There is no need to upgrade container.
fi
docker image ls $IMAGE_ADDRESS | grep none | awk '{ print $3}' | xargs docker image rm
