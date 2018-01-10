import sys
from sphinx import main
from sphinx.apidoc import main as  apimain

def exit_if_not_zero(rt: int):
    if not rt == 0:
        sys.exit(rt)


argv = [sys.argv[0], '-f', '-o', './source/api', '../iclientpy']
exit_if_not_zero(apimain(argv))
argv = [sys.argv[0], '-M', 'html', 'source', 'build']
sys.argv = argv #sphinx的main函数里竟然直接访问了sys.argv，所以，修改一下sys.argv
exit_if_not_zero(main(argv))

import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(root, file)[len(path):])

zipf = zipfile.ZipFile('doc.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('./build/html/', zipf)
zipf.close()