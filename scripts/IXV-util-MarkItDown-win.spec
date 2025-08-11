# -*- mode: python ; coding: utf-8 -*-

import os
import site
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(os.path.abspath(SPECPATH)).parent

# Add the project root to Python path for imports
sys.path.insert(0, str(project_root))

# Get site_packages path
def get_site_packages():
    for path in sys.path:
        if 'site-packages' in path and Path(path).exists():
            return path
    packages = site.getsitepackages()
    if packages:
        return packages[0]
    return None

site_packages = Path(get_site_packages())

a = Analysis(
    [str(project_root / 'wrapper.py')],
    pathex=[str(project_root), str(project_root / 'src')],
    binaries=[],
    datas=[
        (str(site_packages / 'magika/models'), 'magika/models'),
        (str(site_packages / 'magika/config'), 'magika/config'),
        (str(project_root / 'src/image_extractor.py'), '.'),
    ],
    hiddenimports=['image_extractor'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='IXV-util-MarkItDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
)

# No COLLECT/BUNDLE for single executable
