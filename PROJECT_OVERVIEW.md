# Into the Dark - Complete Game Engine

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Qt6](https://img.shields.io/badge/Qt6-GUI-green.svg)](https://qt.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-6%2F6%20Passing-brightgreen.svg)](test_engine.py)

A comprehensive, production-ready Python game engine for cinematic narrative games, designed with a hybrid C++/Qt6 GUI architecture.

## 🎮 Project Overview

**Into the Dark** is a story-driven, pixel-art game featuring Rika, a female lone warrior navigating a ruined world. The game explores themes of Obsession, Kindness, Trust, and Truth through a sophisticated memory tracking system.

### **Hybrid Architecture**
- **Python Backend**: Complete game logic, story management, memory tracking, and analytics
- **C++/Qt6 Frontend**: High-performance rendering, GUI, and user interaction
- **JSON Communication**: Clean API between Python and C++ via subprocess calls

## 🚀 Quick Start

### **Prerequisites**
```bash
# Install dependencies
sudo apt install qt6-base-dev qt6-tools-dev cmake build-essential
pip3 install Pillow numpy scipy pygame
```

### **Build and Run**
```bash
# Clone the repository
git clone git@github.com:stu30adogankl-sketch/design-work.git
cd design-work

# Build the game
./build.sh

# Run the game
./build/IntoTheDark
```

### **Test the Engine**
```bash
# Run comprehensive test suite
python3 test_engine.py

# Test individual components
cd python_backend
python3 game_engine.py
python3 cli_interface.py get_scene
```

## 📁 Project Structure

```
IntoTheDark/
├── src/
│   └── main.cpp                    # C++/Qt6 GUI application
├── python_backend/
│   ├── game_engine.py              # Main game engine
│   ├── cli_interface.py             # CLI API for C++ communication
│   ├── audio_system.py             # Audio management system
│   ├── transition_manager.py       # Scene transition system
│   ├── config_system.py            # Configuration management
│   └── story_engine.py             # Legacy story engine
├── assets/
│   ├── cutscenes/                  # 10 placeholder cutscene images
│   └── audio/                      # 4 audio placeholder files
├── CMakeLists.txt                  # Build configuration
├── build.sh                        # Build script
├── test_engine.py                  # Comprehensive test suite
├── README.md                       # Main documentation
└── PYTHON_ENGINE_README.md         # Detailed engine documentation
```

## ✨ Key Features

### **🎬 Advanced Scene System**
- **10+ Cinematic Scenes**: Rich metadata including lighting, weather effects, camera effects
- **Multi-Speaker Dialogue**: Narrator, Rika, Penci with emotions and timing
- **Cinematic Choices**: Consequence text, memory impact, conditional choices
- **Audio Integration**: Background music and ambient sounds per scene

### **🧠 Sophisticated Memory System**
- **Four Memory Types**: Kindness, Obsession, Truth, Trust
- **Advanced Analytics**: Choice patterns, alignment changes, play style analysis
- **Dynamic Alignment**: Real-time alignment calculation
- **Progress Tracking**: Detailed statistics and insights

### **🎵 Complete Audio System**
- **Multi-track Audio**: Music, SFX, voice, and ambient sounds
- **Volume Controls**: Individual volume settings for each audio type
- **Event Triggers**: Automatic audio events based on game actions
- **Pygame Integration**: Ready for real audio playback

### **🎨 Scene Transition System**
- **12 Transition Types**: Fade, slide, zoom, dissolve, wipe effects
- **Easing Functions**: Linear, ease-in, ease-out, ease-in-out
- **Transition Queue**: Sequential transition management
- **Threaded Execution**: Non-blocking transition processing

### **⚙️ Configuration System**
- **Comprehensive Settings**: Display, audio, gameplay, accessibility
- **Settings UI Data**: Structured data for GUI settings menus
- **Configuration Validation**: Automatic validation of settings
- **Persistent Storage**: JSON-based configuration persistence

### **💾 Enhanced Save System**
- **Multiple Save Slots**: Up to 10 save slots
- **Comprehensive Data**: Scene progress, memory values, play time, achievements
- **Auto-save**: Automatic saving after each choice
- **Save Management**: List, save, load, and delete save slots

## 🔧 API Reference

### **CLI Commands**
```bash
# Core game commands
python3 cli_interface.py get_scene          # Get current scene data
python3 cli_interface.py get_memory         # Get memory analytics
python3 cli_interface.py make_choice <index> # Make a choice
python3 cli_interface.py reset_game         # Reset to beginning

# Save/Load commands
python3 cli_interface.py get_save_slots     # List all save slots
python3 cli_interface.py save_game <slot>   # Save to specific slot
python3 cli_interface.py load_game <slot>   # Load from specific slot

# Settings commands
python3 cli_interface.py get_settings       # Get current settings
python3 cli_interface.py update_settings <json> # Update settings

# Analytics commands
python3 cli_interface.py get_scene_list     # List all scenes
python3 cli_interface.py get_analytics      # Get game analytics
```

## 🧪 Testing

The project includes a comprehensive test suite that validates all components:

```bash
python3 test_engine.py
```

**Test Results**: 6/6 tests passing ✅
- Game Engine: Scene data, memory tracking, choice making
- CLI Interface: All commands and JSON communication
- Configuration System: Settings loading, updates, UI data
- Audio System: Volume controls, mute toggle, event triggers
- Transition Manager: Transition creation, execution, status
- Save System: Save/load functionality, slot management

## 📚 Documentation

- **[Main README](README.md)**: Complete setup and usage guide
- **[Python Engine README](PYTHON_ENGINE_README.md)**: Detailed engine documentation
- **[API Reference](PYTHON_ENGINE_README.md#api-reference)**: Complete CLI command reference
- **[Architecture Guide](PYTHON_ENGINE_README.md#architecture-benefits)**: Hybrid design benefits

## 🎯 Production Ready

This game engine is designed for production use with:

- **✅ Comprehensive Error Handling**: Robust error handling throughout
- **✅ Extensive Logging**: Detailed logging for debugging and monitoring
- **✅ Modular Architecture**: Easy to extend and maintain
- **✅ Performance Optimized**: Efficient algorithms and data structures
- **✅ Well Documented**: Comprehensive documentation and examples
- **✅ Tested Components**: Individual systems tested and verified

## 🔄 Integration with C++ GUI

The Python engine maintains full backward compatibility with the existing C++ GUI:

- **Same CLI Commands**: All existing commands work unchanged
- **Same JSON Format**: Scene and memory data formats preserved
- **Enhanced Data**: Additional fields provided when available
- **Error Handling**: Robust error handling for GUI integration

## 🚀 Future Enhancements

### **Planned Features**
- **Voice Acting Integration**: Full voice acting support
- **Advanced Analytics**: Player behavior analysis
- **Mod Support**: Plugin system for custom content
- **Multiplayer**: Cooperative story mode
- **VR Support**: Virtual reality integration

### **Technical Improvements**
- **Performance Optimization**: Faster scene loading
- **Memory Optimization**: Reduced memory footprint
- **Audio Enhancement**: 3D audio support
- **Graphics Integration**: Direct graphics API integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Qt6 Framework**: For the powerful GUI framework
- **Python Community**: For the excellent libraries and tools
- **Game Development Community**: For inspiration and best practices

---

**Ready to build cinematic narrative games?** 🎮✨

The complete Python game engine provides a solid foundation for building story-driven games while maintaining high-performance rendering capabilities through the hybrid C++/Qt6 architecture.
