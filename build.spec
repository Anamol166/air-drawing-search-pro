import sys
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Get absolute path to script directory
spec_dir = os.path.dirname(os.path.abspath(__file__))

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
    (os.path.join(spec_dir, 'bModel.h5'), '.'),
    (os.path.join(spec_dir, 'bestmodel.h5'), '.'),
    (os.path.join(spec_dir, 'drawing.h5'), '.'),
    (os.path.join(spec_dir, 'class.txt'), '.'),
]

# Add icon only if it exists - use absolute path
icon_path = os.path.join(spec_dir, 'logo.ico')
icon_param = icon_path if os.path.exists(icon_path) else None

a = Analysis(
    [os.path.join(spec_dir, 'main.py')],
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
