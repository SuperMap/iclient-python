@echo off
jupyter nbextension disable --py --sys-prefix iclientpy
if errorlevel 1 exit 1
jupyter nbextension uninstall --py  --sys-prefix iclientpy
if errorlevel 1 exit 1
