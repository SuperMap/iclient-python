set Current_Dir=%~dp0
set Project_RootDir=%~dp0..\
cd /d %Project_RootDir%
python setup.py bdist_wheel