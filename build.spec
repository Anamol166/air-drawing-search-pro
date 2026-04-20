import sys
import os

block_cipher = None

hiddenimports = [
    'tensorflow',
    'tensorflow.keras',
    'tensorflow.keras.models',
    'mediapipe',
    'mediapipe.python',
    'mediapipe.python.solutions',
    'mediapipe.python.solutions.hands',
    'cv2',
    'numpy',
    'spellchecker'
]

datas = [
    ('bModel.h5', '.'),
    ('bestmodel.h5', '.'),
    ('drawing.h5', '.'),
    ('class.txt', '.'),
]

icon_param = 'logo.ico' if os.path.exists('logo.ico') else None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
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
    icon=icon_param,
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