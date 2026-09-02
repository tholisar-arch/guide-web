# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build spec for the Supply Chain & Sales Decision Assistant.

Build a standalone Windows executable with:

    pyinstaller build.spec

The result is placed under dist/SupplyChainAssistant/ (one-folder build,
recommended for faster startup) including SupplyChainAssistant.exe.
"""
import sys
from pathlib import Path

block_cipher = None
project_root = Path(SPECPATH)

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / "resources"), "resources"),
    ],
    hiddenimports=[
        "pandas",
        "numpy",
        "openpyxl",
        "reportlab",
        "matplotlib.backends.backend_qtagg",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SupplyChainAssistant",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(project_root / "resources" / "app_icon.ico") if (project_root / "resources" / "app_icon.ico").exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SupplyChainAssistant",
)
