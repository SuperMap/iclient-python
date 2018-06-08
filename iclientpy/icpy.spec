# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None


cachetool_a = Analysis(['iclientpy/rest/cmd/updatecache.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
tokentool_a = Analysis(['iclientpy/rest/cmd/obaintoken.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
initserver_a = Analysis(['iclientpy/rest/cmd/initserver.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
		
		
MERGE( (cachetool_a, 'cachetool', 'cachetool'), (tokentool_a, 'tokentool', 'tokentool'), (initserver_a,'initserver','initserver') )


cachetool_pyz = PYZ(cachetool_a.pure, cachetool_a.zipped_data, cipher=block_cipher)
cachetool_exe = EXE(cachetool_pyz,
          cachetool_a.scripts,
          exclude_binaries=True,
          name='icpy-cachetool',
          debug=False,
          strip=False,
          upx=True,
          console=True )
cachetool_coll = COLLECT(cachetool_exe,
               cachetool_a.binaries,
               cachetool_a.zipfiles,
               cachetool_a.datas,
               strip=False,
               upx=True,
               name='cachetool')

			   
tokentool_pyz = PYZ(tokentool_a.pure, tokentool_a.zipped_data, cipher=block_cipher)
tokentool_exe = EXE(tokentool_pyz,
          tokentool_a.scripts,
          exclude_binaries=True,
          name='icpy-tokentool',
          debug=False,
          strip=False,
          upx=True,
          console=True )
tokentool_coll = COLLECT(tokentool_exe,
               tokentool_a.binaries,
               tokentool_a.zipfiles,
               tokentool_a.datas,
               strip=False,
               upx=True,
               name='tokentool')

initserver_pyz = PYZ(initserver_a.pure, initserver_a.zipped_data, cipher=block_cipher)
initserver_exe = EXE(initserver_pyz,
          initserver_a.scripts,
          exclude_binaries=True,
          name='icpy-initserver',
          debug=False,
          strip=False,
          upx=True,
          console=True )
initserver_coll = COLLECT(initserver_exe,
               initserver_a.binaries,
               initserver_a.zipfiles,
               initserver_a.datas,
               strip=False,
               upx=True,
               name='initserver')
		  


