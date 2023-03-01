# -*- mode: python ; coding: utf-8 -*-
import os
from kivy_deps import sdl2, glew
block_cipher = None
from kivymd import hooks_path as kivymd_hooks_path

current_path = os.path.abspath('.')
icon_path = os.path.join(current_path, 'imagens', 'icone.ico')
logo_path = os.path.join('imagens', 'icone.ico')
print('logo',logo_path)

a = Analysis(['main.py'],
             pathex=[current_path],
             binaries=[],
             datas=[(logo_path,'imagens\\')],
             hiddenimports=[],
             hookspath=[kivymd_hooks_path],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='PMK_Provisorio',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon=icon_path,
          console=False )
