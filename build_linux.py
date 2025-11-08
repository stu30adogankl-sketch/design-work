#!/usr/bin/env python3
"""
Build script for Linux .appimage (onefile)
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def build_appimage():
    """Build Linux AppImage using PyInstaller and appimagetool"""
    print("Building Linux AppImage (onefile)...")
    
    # Step 1: Build with PyInstaller
    print("\n[1/3] Building executable with PyInstaller...")
    spec_file = Path("IntoTheDark.spec")
    if spec_file.exists():
        print("Using IntoTheDark.spec file...")
        cmd = ["pyinstaller", "--clean", str(spec_file)]
    else:
        cmd = [
            "pyinstaller",
            "--name=IntoTheDark",
            "--onefile",
            "--add-data=assets:assets",  # Linux uses colon
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--collect-all=PyQt6",
            "pyqt6_game.py"
        ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ PyInstaller build successful")
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("✗ PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)
    
    # Step 2: Create AppDir structure
    print("\n[2/3] Creating AppDir structure...")
    appdir = Path("AppDir")
    if appdir.exists():
        shutil.rmtree(appdir)
    
    appdir.mkdir()
    (appdir / "usr" / "bin").mkdir(parents=True)
    (appdir / "usr" / "share" / "applications").mkdir(parents=True)
    (appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True)
    
    # Copy executable
    shutil.copy("dist/IntoTheDark", appdir / "usr" / "bin" / "intothedark")
    os.chmod(appdir / "usr" / "bin" / "intothedark", 0o755)
    
    # Create .desktop file (must be in AppDir root for appimagetool)
    desktop_content = """[Desktop Entry]
Type=Application
Name=Into the Dark
Comment=Story-driven narrative game
Exec=intothedark
Categories=Game;
Terminal=false
"""
    (appdir / "intothedark.desktop").write_text(desktop_content)
    # Also create in the standard location
    (appdir / "usr" / "share" / "applications" / "intothedark.desktop").write_text(desktop_content)
    
    # Create AppRun
    apprun_content = """#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/intothedark" "$@"
"""
    (appdir / "AppRun").write_text(apprun_content)
    os.chmod(appdir / "AppRun", 0o755)
    
    print("✓ AppDir structure created")
    
    # Step 3: Build AppImage
    print("\n[3/3] Building AppImage...")
    print("Note: This requires appimagetool.")
    print("Install it from: https://github.com/AppImage/AppImageKit/releases")
    print("Or use: wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage")
    print("      chmod +x appimagetool-x86_64.AppImage")
    
    appimagetool = Path("appimagetool-x86_64.AppImage")
    if not appimagetool.exists():
        # Try to find it in PATH
        appimagetool_path = shutil.which("appimagetool")
        if appimagetool_path:
            appimagetool = Path(appimagetool_path)
        else:
            print("\n⚠ appimagetool not found. Creating AppDir only.")
            print(f"✓ AppDir created at: {appdir.absolute()}")
            print("Run manually: appimagetool AppDir")
            return
    
    try:
        subprocess.run([str(appimagetool), "AppDir", "IntoTheDark-x86_64.AppImage"], check=True)
        print("\n✓ AppImage build successful!")
        print(f"✓ AppImage: IntoTheDark-x86_64.AppImage")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ AppImage build failed: {e}")
        print(f"✓ AppDir created at: {appdir.absolute()}")
        print("You can build the AppImage manually with: appimagetool AppDir")
        sys.exit(1)

if __name__ == "__main__":
    build_appimage()

