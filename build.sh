#!/bin/bash
# Into the Dark - Build and Run Script

set -e  # Exit on any error

echo "Into the Dark - Build Script"
echo "============================"

# Check if we're in the right directory
if [ ! -f "CMakeLists.txt" ]; then
    echo "Error: CMakeLists.txt not found. Please run this script from the project root."
    exit 1
fi

# Create build directory
echo "Creating build directory..."
mkdir -p build
cd build

# Configure with CMake
echo "Configuring with CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build the project
echo "Building the project..."
make -j$(nproc)

# Make Python scripts executable
echo "Setting up Python scripts..."
chmod +x ../python_backend/story_engine.py
chmod +x ../python_backend/cli_interface.py

# Create save directory if it doesn't exist
mkdir -p ../save

echo ""
echo "Build completed successfully!"
echo ""
echo "To run the game:"
echo "  ./IntoTheDark"
echo ""
echo "Or from the project root:"
echo "  ./build/IntoTheDark"
echo ""
echo "To test the Python backend:"
echo "  cd ../python_backend && python3 story_engine.py"
echo ""

# Ask if user wants to run the game
read -p "Do you want to run the game now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting Into the Dark..."
    ./IntoTheDark
fi
