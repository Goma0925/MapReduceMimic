# -*- mode: python ; coding: utf-8 -*-
import sys
import pkgutil

block_cipher = None

modules_to_exclude = ["django", "test"]
def get_all_default_modules():
    modules = []

    default_module_list = list(pkgutil.walk_packages())
    for i in range(len(default_module_list)):
        print("LOOP:", i)
        try:
            should_include = True
            if "test" in str(default_module_list[i].name):
                should_include = False
            if "django" in str(default_module_list[i].name):
                should_include = False
            if "dj" in str(default_module_list[i].name):
                should_include = False

            if should_include:
                modules.append(str(default_module_list[i].name))
                print("INCLUDE", str(default_module_list[i].name))
            else:
                print("EXCLUDE", str(default_module_list[i].name))
        except:
            print("ERROR OCCURED WHILE INSTALLING DEFAULT MODULES")

    for module in modules:
        print("INSTALLED:", module)

get_all_default_modules()

a = Analysis(['Adoop.py'],
             pathex=['/Users/Amon/Desktop/@Python_project/MapReduceMimic'],
             binaries=[],
             datas=[],
             hiddenimports=get_all_default_modules(),
             hookspath=[],
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
          name='Adoop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
