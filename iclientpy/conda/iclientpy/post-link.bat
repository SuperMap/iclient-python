@echo off
jupyter nbextension install --py --symlink --sys-prefix iclientpy
if errorlevel 1 exit 1
jupyter nbextension enable --py --sys-prefix iclientpy
if errorlevel 1 exit 1
