set Current_Dir=%~dp0
set Project_RootDir=%~dp0..\
cd /d %Project_RootDir%

python setup.py build
pip install -e .

jupyter nbextension install --py --symlink --sys-prefix iclientpy
jupyter nbextension enable --py --sys-prefix iclientpy