

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = [
    'tensorflow',
    'mediapipe',
    'cv2',
    'numpy',
    'spellchecker'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bModel.h5', '.'),
        ('bestmodel.h5', '.'),
        ('drawing.h5', '.'),
        ('class.txt', '.'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AirDrawingApp',
    icon='logo.ico',
    console=False,
    upx=False,
    runtime_tmpdir=None,
    bootloader_ignore_signals=False,
    strip=False,
    upx_exclude=[],
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
