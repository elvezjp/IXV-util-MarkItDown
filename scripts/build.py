#!/usr/bin/env python3
"""
Build script for IXV-util-MarkItDown
Creates PyInstaller spec file and builds the executable
"""

import os
import sys
import subprocess
from pathlib import Path

def create_spec_file():
    """Create PyInstaller spec file with proper configuration"""
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['wrapper.py'],
    pathex=['{project_root}'],
    binaries=[],
    datas=[
        ('pyproject.toml', '.'),
        ('src', 'src'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
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
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    distpath='./dist',
)
'''
    
    spec_path = project_root / "IXV-util-MarkItDown.spec"
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"Created spec file: {{spec_path}}")
    return spec_path

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Create spec file
    spec_path = create_spec_file()
    
    # Run PyInstaller with the spec file
    try:
        print("Building executable...")
        subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            str(spec_path)
        ], check=True, cwd=spec_path.parent)
        
        print("Build completed successfully!")
        print(f"Executable created: ./dist/IXV-util-MarkItDown")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()