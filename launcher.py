#!/usr/bin/env python3
"""
Into the Dark - Game Launcher
Simple launcher script for the Python game engine
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pygame
        print("✓ Pygame available")
    except ImportError:
        print("✗ Pygame not found. Install with: pip3 install pygame")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow available")
    except ImportError:
        print("✗ Pillow not found. Install with: pip3 install Pillow")
        return False
    
    return True

def launch_game():
    """Launch the game"""
    print("Into the Dark - Game Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return False
    
    # Check if C++ GUI is available
    cpp_gui_path = Path("build/IntoTheDark")
    if cpp_gui_path.exists():
        print("\n🚀 Launching C++/Qt6 GUI version...")
        try:
            subprocess.run([str(cpp_gui_path)], check=True)
            return True
        except subprocess.CalledProcessError:
            print("✗ C++ GUI failed to launch")
        except FileNotFoundError:
            print("✗ C++ GUI not found")
    
    # Fallback to Python-only version
    print("\n🐍 Launching Python-only version...")
    try:
        python_script = Path("python_backend/game_engine.py")
        if python_script.exists():
            subprocess.run([sys.executable, str(python_script)], check=True)
            return True
        else:
            print("✗ Python game engine not found")
            return False
    except subprocess.CalledProcessError:
        print("✗ Python game engine failed to launch")
        return False

def build_game():
    """Build the C++ GUI version"""
    print("🔨 Building C++ GUI version...")
    try:
        subprocess.run(["./build.sh"], check=True)
        print("✓ Build completed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Build failed")
        return False
    except FileNotFoundError:
        print("✗ Build script not found")
        return False

def main():
    """Main launcher function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "build":
            build_game()
        elif command == "test":
            print("🧪 Running tests...")
            try:
                subprocess.run([sys.executable, "test_engine.py"], check=True)
            except subprocess.CalledProcessError:
                print("✗ Tests failed")
        elif command == "help":
            print("Into the Dark - Game Launcher")
            print("Usage:")
            print("  python3 launcher.py          # Launch the game")
            print("  python3 launcher.py build     # Build C++ GUI")
            print("  python3 launcher.py test      # Run tests")
            print("  python3 launcher.py help      # Show this help")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python3 launcher.py help' for usage information")
    else:
        # Default: launch the game
        launch_game()

if __name__ == "__main__":
    main()
