import sys
from sphinx import main
from sphinx.ext.apidoc import main as apimain


def exit_if_not_zero(rt: int):
    if not rt == 0:
        sys.exit(rt)


argv = ['-f', '-o', './source/api', '../iclientpy']
exit_if_not_zero(apimain(argv))
argv = [sys.argv[0], '-M', 'html', 'source', 'build']
sys.argv = argv  # sphinx的main函数里竟然直接访问了sys.argv，所以，修改一下sys.argv
exit_if_not_zero(main(argv))

import os
import zipfile
import tarfile


def writedir2file(path, targetfile):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            targetfile.write(os.path.join(root, file), os.path.join(root, file)[len(path):])


zipf = zipfile.ZipFile('./doc.zip', 'w', zipfile.ZIP_DEFLATED)
writedir2file('./build/html/', zipf)
zipf.close()
tarf = tarfile.open('./doc.tar', 'w')
tarf.write = tarf.add
writedir2file('./build/html/', tarf)
tarf.close()
