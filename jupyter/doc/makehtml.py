import sys
from sphinx import main
from sphinx.apidoc import main as  apimain
argv = [sys.argv[0], '-f', '-o', './source/api', '../iclientpy']
api_main_result = apimain(argv)
if not api_main_result is 0:
    sys.exit(api_main_result)
argv = [sys.argv[0], '-M', 'html', 'source', 'build']
sys.argv = argv #sphinx的main函数里竟然直接访问了sys.argv，所以，修改一下sys.argv
sys.exit(main(argv))