# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec : `make package` construit dist/pac-man/ puis le zip.
# On embarque les images (sans les fichiers GIMP .xcf). La config est
# copiée à côté de l'exécutable par le Makefile, pour rester modifiable.
import os

datas = []
for root, _dirs, files in os.walk('sprites'):
    for name in files:
        if not name.endswith('.xcf') and name != '.DS_Store':
            datas.append((os.path.join(root, name), root))

a = Analysis(
    ['pac-man.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['mypy', 'flake8', 'pytest', 'tkinter'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pac-man',
    debug=False,
    strip=False,
    upx=False,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='pac-man',
)
