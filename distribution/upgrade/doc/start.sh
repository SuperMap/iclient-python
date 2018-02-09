#!/bin/bash -e
Current_Dir=$(cd "$(dirname "$0")";pwd)
cd $Current_Dir
while read LINE
do
export $LINE
done < ./rancher.conf
rancher-compose up -p --force-upgrade -c -d
