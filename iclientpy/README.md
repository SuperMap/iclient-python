iclientpy
===============================

iclient for jupyter

Installation
------------

To install use pip:

    $ pip install iclientpy
    $ jupyter nbextension enable --py --sys-prefix iclientpy


For a development installation (requires npm),

    $ git clone https://github.com/SuperMap/iclient-python.git
    $ cd iclientpy
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix iclientpy
    $ jupyter nbextension enable --py --sys-prefix iclientpy
