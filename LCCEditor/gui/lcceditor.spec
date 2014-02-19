# -*- mode: python -*-
a = Analysis(['gui.py'],
             pathex=['C:\\Projects\\ATtILA2\\src\\LCCEditor\\LCCEditor\\gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='lcceditor.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
