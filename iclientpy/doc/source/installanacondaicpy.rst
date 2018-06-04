iClientPy从零开始
===============================

1. 从 `链接 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_ 下载Anaconda3安装包，建议使用最新的
2. 双击安装包进入安装想到进行安装

    .. image:: _static/anaconda_init.png

3. 点击下一步
4. 阅读许可，点击下一步

    .. image:: _static/anaconda_license.png

5. 如果仅为当前用户安装，勾选Just me，然后单击下一步；需要为所有用户安装(需要管理员权限)，勾选All users，点击下一步

    .. image:: _static/anaconda_user.png

6. 选择安装位置，点击下一步

    .. image:: _static/anaconda_path.png

7. 选择是否将Anaconda加入PATH环境变量中，可参考如下方式进行选择：

        * 打开cmd窗口，执行命令 python -V
        * 如能正常输出python版本信息，则不建议加入环境变量，否则建议加入环境变量

8. 选择是否将Anaconda注册为默认的python环境
9. 点击Install

    .. image:: _static/anaconda_advance.png

10. 安装完成后，点击下一步
11. 是否安装VS Code，不需要的点击skip即可

    .. image:: _static/anaconda_vscode.png

12. 将所有复选框勾选去掉，点击finish

    .. image:: _static/anaconda_finish.png

13. 根据第7步的选择，打开cmd或者Anaconda Prompt，执行命令conda -V 和 python -V，检查是否安装成功
14. 配置清华源以及第三库依赖源：在上一步打开窗口中执行：

    ::

        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
        conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
        conda config --set show_channel_urls yes

15. 执行命令：conda install -c http://iclientpy.supermap.io/conda/channel iclientpy （第一次安装耗时会比较久）
16. 执行命令在jupyter notebook中启用iclientpy

    ::

        jupyter nbextension install --py --symlink --sys-prefix iclientpy
        jupyter nbextension enable --py --sys-prefix iclientpy
