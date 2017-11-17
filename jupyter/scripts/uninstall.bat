set Current_Dir=%~dp0
set Project_RootDir=%~dp0..\
cd /d %Project_RootDir%

jupyter nbextension disable --py --sys-prefix iclientpy
jupyter nbextension uninstall --py  --sys-prefix iclientpy
rd /S /Q %Project_RootDir%iclientpy\static
rd /S /Q %Project_RootDir%build