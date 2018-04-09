#!/bin/bash
Current_Dir=$(cd "$(dirname "$0")";pwd)
Project_RootDir=$(cd $Current_Dir/..;pwd)
Project_jsDir=$(cd $Current_Dir/../js;pwd)
cd $Project_jsDir
npm install
npm run ddl