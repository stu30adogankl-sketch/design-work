#!/usr/bin/env python3
"""
Build script for Windows .exe (onefile)
"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build Windows .exe using PyInstaller"""
    print("Building Windows .exe (onefile)...")
    
    # Use spec file if it exists, otherwise use command line
    spec_file = Path("IntoTheDark.spec")
    if spec_file.exists():
        print("Using IntoTheDark.spec file...")
        cmd = ["pyinstaller", "--clean", str(spec_file)]
    else:
        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--name=IntoTheDark",
            "--onefile",
            "--windowed",  # No console window
            "--icon=NONE",  # Add icon path if you have one
            "--add-data=assets;assets",  # Windows uses semicolon
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--collect-all=PyQt6",
            "pyqt6_game.py"
        ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
        print(f"✓ Executable: dist/IntoTheDark.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n✗ PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()

