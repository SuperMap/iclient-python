ipyiclient
===============================

iclient for jupyter

Installation
------------

To install use pip:

    $ pip install ipyiclient
    $ jupyter nbextension enable --py --sys-prefix ipyiclient


For a development installation (requires npm),

    $ git clone https://gitee.com/isupermap/iClientPython.git
    $ cd iclientpy/jupyter
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipyiclient
    $ jupyter nbextension enable --py --sys-prefix ipyiclient
