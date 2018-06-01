# coding: utf-8
import os
import sys
conda_build_dir = os.path.abspath(os.path.join(sys.argv[0], os.pardir))
output_dir = os.path.join(conda_build_dir, 'output')
get_ipython().system('conda build -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ --output-folder {output_dir} iclientpy')
import pathlib
cur_platform_name = [name for name in os.listdir('./output') if name != 'noarch'][0]
channel_dir = os.path.join(conda_build_dir, 'channel')
cur_platform_dir = os.path.join(channel_dir, cur_platform_name)
pathlib.Path(channel_dir).mkdir(parents=True, exist_ok=True)
import shutil
shutil.copytree(os.path.join(output_dir, cur_platform_name), cur_platform_dir)
filename = [name for name in os.listdir(cur_platform_dir) if name.endswith('bz2')][0]
convert_from = os.path.join(cur_platform_dir, filename)
get_ipython().system('conda convert -o {channel_dir} -p all {convert_from}')
get_ipython().system('conda index {channel_dir}')
noarch_dir = os.path.join(channel_dir, 'noarch')
get_ipython().system('conda index {noarch_dir}')
import tarfile
with tarfile.open(os.path.join(conda_build_dir, 'iclientpy-conda-package.tar'), 'w') as zipf:
    for root,dirs,files in os.walk(channel_dir):
        for file in files:
            zipf.add(os.path.join(root, file), os.path.relpath(os.path.join(root, file), conda_build_dir))
