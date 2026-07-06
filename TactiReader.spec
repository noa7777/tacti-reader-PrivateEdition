# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tactireader.py'],
    pathex=[],
    binaries=[],
    datas=[('tactireader.png', '.'), ('docs/help.md', 'docs'), ('docs/about.md', 'docs'), ('docs/help_zh.md', 'docs'), ('docs/about_zh.md', 'docs'), ('tacti_reader', 'tacti_reader')],
    hiddenimports=[],
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
    name='TactiReader',
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
    icon=['tactireader.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TactiReader',
)
