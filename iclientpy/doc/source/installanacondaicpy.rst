iClientPy从零开始
===============================

iClientPy的一些第三方依赖需要c++库，pip安装的时候不会安装所需的c++库，会导致这些第三方依赖安装不完整，导致iClientPy无法正常使用。

所以我们建议在Anaconda（`https://www.anaconda.com/ <https://www.anaconda.com/>`_）环境中通过Conda安装iClientPy。

建议版本Anaconda3 5.1.0及以上。

1. 因为Anaconda网站在国外，直接从Anaconda官网下载速度较慢，可以从清华大学开源软件镜像站下载安装包。根据系统版本从下面链接地址下载Anaconda3安装包

    `win64链接 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.1.0-Windows-x86_64.exe>`_

    `win32链接 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.1.0-Windows-x86.exe>`_

    `其他系统链接 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_

2. 双击安装包进入安装向导进行安装

    .. image:: _static/anaconda_init.png

3. 安装类型选择，建议仅为当前用户安装，点击下一步

    .. image:: _static/anaconda_user.png

4. 选择安装位置，点击下一步

    .. image:: _static/anaconda_path.png

5. 选择是否将Anaconda加入PATH环境变量中，可参考如下方式进行选择：

        * 打开cmd窗口，执行命令 python -V
        * 如能正常输出python版本信息，则不建议加入环境变量，否则建议加入环境变量

6. 选择是否将Anaconda注册为默认的python环境
7. 点击Install

    .. image:: _static/anaconda_advance.png

8. 安装完成后，点击下一步
9. 是否安装VS Code，不需要的点击skip即可

    .. image:: _static/anaconda_vscode.png

10. 将所有复选框勾选去掉，点击finish

    .. image:: _static/anaconda_finish.png

11. 根据第7步的选择，从菜单栏打开Anaconda Prompt，执行命令conda -V 和 python -V，检查是否安装成功
12. 配置清华源以及第三库依赖源：在上一步打开窗口中执行：

    ::

        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
        conda config --set show_channel_urls yes

13. 执行命令：

    ::

        conda install -y -c http://iclientpy.supermap.io/conda/channel iclientpy && jupyter nbextension install --py --symlink --sys-prefix iclientpy && jupyter nbextension enable --py --sys-prefix iclientpy

    **提醒：** 第一次安装耗时会比较久

14. 在已经打开的Anaconda Prompt中，执行命令，进入iclientpy引导使用的notebook

    ::

        icpy-iclientpystart

15. 在上一步执行过后，会在浏览器中打开一个网页(如果没有打开，手动访问http://localhost:8888)，点击iclientpy_start.ipynb，开始了解，使用iclientpy

