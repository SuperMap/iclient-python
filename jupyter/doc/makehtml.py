import sys
from sphinx import main
argv = [sys.argv[0], '-M', 'html', 'source', 'build'] #sphinx的main函数里竟然直接访问了sys.argv，所以，修改一下sys.argv
sys.argv = argv
sys.exit(main(argv))