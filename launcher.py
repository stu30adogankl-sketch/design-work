#!/usr/bin/env python3
"""
Into the Dark - Simple Game Launcher
Launches the PyQt6 game directly
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the PyQt6 game"""
    print("Into the Dark - Launching Game...")
    
    # Check if PyQt6 is available
    try:
        import PyQt6
        print("✓ PyQt6 available")
    except ImportError:
        print("✗ PyQt6 not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
        print("✓ PyQt6 installed")
    
    # Launch the game
    try:
        subprocess.run(["python3", "pyqt6_game.py"], check=True)
    except subprocess.CalledProcessError:
        print("✗ Failed to launch game")
        sys.exit(1)

if __name__ == "__main__":
    main()