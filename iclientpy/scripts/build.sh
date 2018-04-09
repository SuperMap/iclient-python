#!/bin/bash
Current_Dir=$(cd "$(dirname "$0")";pwd)
Project_RootDir=$(cd $Current_Dir/..;pwd)
cd $Project_RootDir
python setup.py jsdeps
python setup.py bdist_wheel