# Into the Dark - Game Skeleton

A story-driven, pixel-art game with hybrid C++/Qt6 GUI and Python backend architecture.

## Project Structure

```
IntoTheDark/
├── src/
│   └── main.cpp              # C++/Qt6 GUI application
├── python_backend/
│   ├── story_engine.py       # Core story logic and memory system
│   └── cli_interface.py      # Command-line interface for C++ communication
├── assets/
│   ├── cutscenes/            # Cutscene images (cutscene1.jpg - cutscene10.jpg)
│   └── audio/                # Audio tracks (audio1.mp3 - audio4.mp3)
├── save/
│   └── save.json             # Game save file
├── CMakeLists.txt            # Build configuration
└── README.md                 # This file
```

## Features

- **Hybrid Architecture**: C++/Qt6 for GUI, Python for story logic
- **Memory System**: Tracks Kindness, Obsession, Truth, and Trust values
- **Choice-Driven Narrative**: 4 choices per scene affecting memory alignment
- **Save System**: JSON-based progress tracking
- **Dark Theme**: Cinematic, melancholic visual design
- **Fade Transitions**: Smooth cutscene transitions
- **Memory Bar**: Real-time display of character alignment

## Story Overview

**Main Character**: Rika, a female lone warrior navigating a ruined world.

**Theme**: Obsession, Kindness, Trust, and Truth.

**Setting**: A world in chaos — ruined cities, remnants of advanced technology, ash, and fading light.

**Goal**: Uncover the truth behind the Creator and the origins of the world.

## Act I Scenes

1. **The Awakening** - Rika wakes in the red-ash wasteland
2. **Echoes of the Machine** - Flickering terminals whisper her name
3. **The Companion Appears** - Penci Zorno emerges from ruins
4. **The Mirror of Memory** - Reflection distorted by light
5-10. **Placeholder Scenes** - Ready for future development

## Dependencies

### C++/Qt6
- Qt6 (Core, Widgets)
- CMake 3.16+
- C++17 compatible compiler

### Python
- Python 3.7+
- PIL (Pillow) for image generation
- NumPy and SciPy for audio generation (optional)

## Building

### Prerequisites
```bash
# Install Qt6 development packages
sudo apt install qt6-base-dev qt6-tools-dev cmake build-essential

# Install Python dependencies
pip3 install Pillow numpy scipy
```

### Build Process
```bash
# Create build directory
mkdir build
cd build

# Configure with CMake
cmake ..

# Build the project
make -j$(nproc)

# Run the game
./IntoTheDark
```

## Running

### From Build Directory
```bash
cd build
./IntoTheDark
```

### From Source Directory
```bash
# Make sure Python backend is executable
chmod +x python_backend/story_engine.py
chmod +x python_backend/cli_interface.py

# Run the game
./build/IntoTheDark
```

## Testing Python Backend

You can test the story engine independently:

```bash
cd python_backend
python3 story_engine.py
```

This provides a command-line interface to test the story progression and memory system.

## Game Controls

- **Choice Buttons**: Click to make story choices
- **Reset Game**: Reset all progress and return to Scene 1
- **Memory Bar**: Shows current alignment and memory percentages

## Memory System

The game tracks four memory types:

- **Kindness**: Compassionate, helpful choices
- **Obsession**: Focused, single-minded decisions
- **Truth**: Seeking knowledge and understanding
- **Trust**: Relying on others and cooperation

Each choice adds +5 to the corresponding memory type. The dominant memory determines Rika's alignment.

## Save System

Game progress is automatically saved to `save/save.json` after each choice. The file contains:

- Current scene
- Watched cutscenes
- Memory values
- Act progression

## Asset Placeholders

The project includes placeholder assets:

- **Cutscenes**: Generated dark-themed placeholder images
- **Audio**: Silent audio files with metadata

Replace these with actual game assets for production.

## Development Notes

### Extending the Story
1. Add new scenes to `story_engine.py` in the `_load_scenes()` method
2. Create corresponding cutscene images
3. Update the scene progression logic as needed

### Memory System Customization
- Modify memory values in scene choices
- Adjust alignment thresholds in `get_memory_alignment()`
- Add new memory types by extending the `MemoryType` enum

### GUI Customization
- Modify styles in `setupDarkTheme()` and widget stylesheets
- Adjust layout in `setupUI()`
- Add new UI elements as needed

## Architecture Benefits

- **Separation of Concerns**: Story logic separate from GUI
- **Easy Testing**: Python backend can be tested independently
- **Modular Design**: Easy to extend with new scenes and features
- **Cross-Platform**: Qt6 provides native look and feel
- **Maintainable**: Clean, well-commented code structure

## Future Enhancements

- Audio playback integration
- More sophisticated memory system
- Multiple save slots
- Settings menu
- Full-screen mode
- Controller support
- Localization support

## License

This project is a game development skeleton for educational and development purposes.
# design-work
