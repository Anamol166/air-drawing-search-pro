import sys
import os

block_cipher = None

hiddenimports = [
    'tensorflow',
    'tensorflow.keras',
    'tensorflow.keras.models',
    'tensorflow.python.keras.engine',
    'mediapipe',
    'mediapipe.python',
    'mediapipe.python.solutions',
    'mediapipe.python.solutions.hands',
    'mediapipe.python.solutions.drawing_utils',
    'mediapipe.python.solutions.drawing_styles',
    'cv2',
    'numpy',
    'spellchecker',
    'matplotlib',
    'matplotlib.backends'
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
    excludes=['pandas', 'scipy', 'jupyter'],
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_param
)