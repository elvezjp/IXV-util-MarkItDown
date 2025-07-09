# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(os.path.abspath(SPECPATH))

# Add the project root to Python path for imports
sys.path.insert(0, str(project_root))

a = Analysis(
    ['markitdown/cli.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include the upstream markitdown package
        ('upstream/packages/markitdown/src/markitdown', 'markitdown'),
        # Include magika model files
        ('.venv/lib/python3.11/site-packages/magika/models', 'magika/models'),
        # Include magika config files
        ('.venv/lib/python3.11/site-packages/magika/config', 'magika/config'),
    ],
    hiddenimports=[
        'markitdown',
        'markitdown.__main__',
        'markitdown._markitdown',
        'markitdown._base_converter',
        'markitdown._exceptions',
        'markitdown._stream_info',
        'markitdown._uri_utils',
        'markitdown.converters',
        'markitdown.converter_utils',
        'beautifulsoup4',
        'bs4',
        'markdownify',
        'mammoth',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'defusedxml',
        'defusedxml.ElementTree',
        'charset_normalizer',
        'requests',
        'urllib3',
        'certifi',
        'idna',
        'magika',
        'onnxruntime',
        'numpy',
        'protobuf',
        'sympy',
        'mpmath',
        'cobble',
    ],
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
    [],
    exclude_binaries=True,
    name='IXV-util-MarkItDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IXV-util-MarkItDown',
)

app = BUNDLE(
    coll,
    name='IXV-util-MarkItDown.app',
    icon=None,
    bundle_identifier='jp.elvez.ixv-util-markitdown',
    info_plist={
        'CFBundleDisplayName': 'IXV-util-MarkItDown',
        'CFBundleExecutable': 'IXV-util-MarkItDown',
        'CFBundleIdentifier': 'jp.elvez.ixv-util-markitdown',
        'CFBundleName': 'IXV-util-MarkItDown',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
        'LSMinimumSystemVersion': '10.15',
        'NSHighResolutionCapable': True,
    },
)
