#! /bin/bash -e
jupyter nbextension install --py --symlink --sys-prefix iclientpy
jupyter nbextension enable --py --sys-prefix iclientpy
