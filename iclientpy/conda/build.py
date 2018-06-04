# coding: utf-8
import os
import sys
import shutil
import pathlib

conda_build_dir = os.path.abspath(os.path.join(sys.argv[0], os.pardir))


def main(cmd):
    output_dir = os.path.join(conda_build_dir, 'output')
    if cmd == 'build':
        if pathlib.Path(output_dir).exists():
           shutil.rmtree(output_dir)
        get_ipython().system('conda build -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ --output-folder {output_dir} iclientpy')
        return
    cur_platform_name = [name for name in os.listdir(output_dir) if name != 'noarch'][0]
    channel_dir = os.path.join(conda_build_dir, 'channel')
    if cmd == 'convert':
        if pathlib.Path(channel_dir).exists():
            shutil.rmtree(channel_dir)
        cur_platform_dir = os.path.join(channel_dir, cur_platform_name)
        pathlib.Path(channel_dir).mkdir(parents=True, exist_ok=True)
        shutil.copytree(os.path.join(output_dir, cur_platform_name), cur_platform_dir)
        filename = [name for name in os.listdir(cur_platform_dir) if name.endswith('bz2') and 'iclientpy' in name][0]
        convert_from = os.path.join(cur_platform_dir, filename)
        # 经测试conda-build版本3.0.19,3.10.5执行convert时都会报错，3.0.27正常。其它版本未测试。
        get_ipython().system('conda convert -o {channel_dir} -p all {convert_from}')
        return
    if cmd == 'index':
        paths = [os.path.join(channel_dir, dir) for dir in os.listdir(channel_dir)]
        paths.append(channel_dir)
        all_path = ' '.join(paths)
        get_ipython().system('conda index {all_path}')
        return
    if cmd == 'tar':
        tar_file_path = os.path.join(conda_build_dir, 'iclientpy-conda-package.tar')
        if pathlib.Path(tar_file_path).exists():
            os.remove(tar_file_path)
        import tarfile
        with tarfile.open(tar_file_path, 'w') as zipf:
            for root,dirs,files in os.walk(channel_dir):
                for file in files:
                    zipf.add(os.path.join(root, file), os.path.relpath(os.path.join(root, file), conda_build_dir))
        return


main(sys.argv[1])
