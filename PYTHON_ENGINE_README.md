# Into the Dark - Complete Python Game Engine

A comprehensive, production-ready Python game engine for cinematic narrative games, designed to work seamlessly with the existing C++/Qt6 GUI rendering system.

## 🎮 Engine Architecture

### **Hybrid Design Philosophy**
- **Python Backend**: Complete game logic, story management, memory tracking, and analytics
- **C++/Qt6 Frontend**: High-performance rendering, GUI, and user interaction
- **JSON Communication**: Clean API between Python and C++ via subprocess calls

### **Core Components**

```
python_backend/
├── game_engine.py          # Main game engine with complete story system
├── cli_interface.py         # Enhanced CLI API for C++ communication
├── config_system.py        # Configuration and settings management
├── audio_system.py         # Audio management with music, SFX, and voice
├── transition_manager.py   # Scene transition system with effects
└── story_engine.py         # Legacy story engine (backward compatibility)
```

## 🚀 Key Features

### **1. Advanced Game Engine (`game_engine.py`)**
- **Complete Scene Management**: 10+ scenes with rich metadata
- **Enhanced Dialogue System**: Multi-speaker dialogue with emotions and timing
- **Memory Analytics**: Advanced tracking of player choices and patterns
- **Save System**: Multiple save slots with comprehensive progress tracking
- **Settings Management**: Runtime configuration updates

### **2. Audio System (`audio_system.py`)**
- **Multi-track Audio**: Music, SFX, voice, and ambient sounds
- **Volume Controls**: Individual volume settings for each audio type
- **Event Triggers**: Automatic audio events based on game actions
- **Fade Effects**: Smooth audio transitions and crossfades
- **Audio Library Support**: Ready for pygame or other audio libraries

### **3. Transition Manager (`transition_manager.py`)**
- **12 Transition Types**: Fade, slide, zoom, dissolve, wipe effects
- **Easing Functions**: Linear, ease-in, ease-out, ease-in-out
- **Transition Queue**: Sequential transition management
- **Custom Transitions**: Extensible system for new effects
- **Threaded Execution**: Non-blocking transition processing

### **4. Configuration System (`config_system.py`)**
- **Comprehensive Settings**: Display, audio, gameplay, accessibility
- **Settings UI Data**: Structured data for GUI settings menus
- **Configuration Validation**: Automatic validation of settings
- **Persistent Storage**: JSON-based configuration persistence
- **Runtime Updates**: Hot-reload of settings during gameplay

### **5. Enhanced CLI Interface (`cli_interface.py`)**
- **Backward Compatible**: Works with existing C++ GUI
- **Extended Commands**: 12+ commands for complete game control
- **Error Handling**: Robust error handling and reporting
- **JSON API**: Clean JSON communication protocol

## 📊 Memory System

### **Four Memory Types**
- **Kindness**: Compassionate, helpful choices
- **Obsession**: Focused, single-minded decisions  
- **Truth**: Seeking knowledge and understanding
- **Trust**: Relying on others and cooperation

### **Advanced Analytics**
- **Choice Patterns**: Track player decision patterns
- **Alignment Changes**: Monitor alignment shifts over time
- **Play Style Analysis**: Determine player's dominant approach
- **Progress Tracking**: Detailed statistics and insights

### **Memory Alignment**
- **Neutral**: Balanced or low memory values
- **Kind**: Dominant kindness choices
- **Obsessed**: Dominant obsession choices
- **Truth-Seeker**: Dominant truth choices
- **Trusting**: Dominant trust choices

## 🎬 Scene System

### **Rich Scene Metadata**
```python
@dataclass
class Scene:
    scene_id: int
    title: str
    background: str
    dialogues: List[Dialogue]
    choices: List[Choice]
    audio_track: Optional[str]
    ambient_sound: Optional[str]
    lighting: str  # normal, dim, bright, eerie
    weather_effect: Optional[str]  # rain, snow, ash
    camera_effect: Optional[str]  # shake, zoom, pan
```

### **Enhanced Dialogue System**
- **Multi-speaker Support**: Narrator, Rika, Penci, etc.
- **Emotion Tracking**: Emotional context for each line
- **Timing Control**: Auto-advance with customizable delays
- **Typewriter Effect**: Smooth text animation (ready for GUI integration)

### **Cinematic Choices**
- **Consequence Text**: Immediate feedback for choices
- **Memory Impact**: Clear indication of memory changes
- **Conditional Choices**: Support for conditional choice availability
- **Sound Effects**: Audio feedback for choice selection

## 🔧 API Reference

### **CLI Commands**

#### **Core Game Commands**
```bash
python3 cli_interface.py get_scene          # Get current scene data
python3 cli_interface.py get_memory         # Get memory analytics
python3 cli_interface.py make_choice <index> # Make a choice
python3 cli_interface.py reset_game         # Reset to beginning
```

#### **Save/Load Commands**
```bash
python3 cli_interface.py get_save_slots     # List all save slots
python3 cli_interface.py save_game <slot>   # Save to specific slot
python3 cli_interface.py load_game <slot>   # Load from specific slot
```

#### **Settings Commands**
```bash
python3 cli_interface.py get_settings       # Get current settings
python3 cli_interface.py update_settings <json> # Update settings
```

#### **Analytics Commands**
```bash
python3 cli_interface.py get_scene_list     # List all scenes
python3 cli_interface.py get_analytics      # Get game analytics
```

### **JSON Response Format**

#### **Scene Data**
```json
{
  "scene_id": 1,
  "title": "The Awakening",
  "background": "cutscene1.jpg",
  "dialogue": "Narrator: Rika wakes...",
  "audio_track": "audio1.mp3",
  "ambient_sound": "wind_ruins.mp3",
  "lighting": "dim",
  "weather_effect": "ash",
  "camera_effect": null,
  "choices": [
    {
      "text": "Call out for anyone.",
      "memory_type": "kindness",
      "memory_value": 5,
      "consequence_text": "Your voice echoes through the ruins."
    }
  ]
}
```

#### **Memory Data**
```json
{
  "kindness": 15.0,
  "obsession": 5.0,
  "truth": 10.0,
  "trust": 0.0,
  "alignment": "Kind",
  "total_choices": 3,
  "play_time": 125.5,
  "insights": {
    "total_choices": 3,
    "alignment_changes": 1,
    "most_common_choice_type": "scene_1_choice_kindness",
    "play_style": "Kind"
  }
}
```

## 🎵 Audio System

### **Audio Types**
- **Music**: Background tracks with looping support
- **SFX**: Sound effects for interactions
- **Voice**: Character voice acting
- **Ambient**: Environmental audio

### **Audio Events**
- **Automatic Triggers**: Scene changes, choices, memory updates
- **Manual Control**: Direct audio playback control
- **Volume Management**: Individual volume controls
- **Fade Effects**: Smooth audio transitions

### **Available Tracks**
- **Main Theme**: Primary background music
- **Machine Hum**: Industrial ambient track
- **Companion Theme**: Emotional character music
- **Memory Echo**: Mysterious atmospheric track
- **Sound Effects**: Choice select, page turn, footsteps
- **Ambient**: Wind, machine hum, environmental sounds

## 🎨 Transition System

### **Transition Types**
- **Fade**: Fade in/out, crossfade
- **Slide**: Left, right, up, down
- **Zoom**: Zoom in/out effects
- **Dissolve**: Pixelated dissolve effect
- **Wipe**: Left/right wipe transitions

### **Easing Functions**
- **Linear**: Constant speed
- **Ease In**: Slow start, fast finish
- **Ease Out**: Fast start, slow finish
- **Ease In Out**: Slow start and finish

### **Usage Example**
```python
transition = transition_manager.create_transition(
    TransitionType.CROSSFADE,
    duration=2.0,
    easing="ease_in_out"
)
transition_manager.execute_transition(transition)
```

## ⚙️ Configuration System

### **Settings Categories**

#### **Display Settings**
- Resolution, fullscreen, VSync
- Texture quality, shadow quality
- Particle effects, bloom effects

#### **Audio Settings**
- Master, music, SFX, voice volumes
- Mute controls
- Audio device selection

#### **Gameplay Settings**
- Text speed, auto-advance
- Language selection
- Skip confirmations

#### **Accessibility Settings**
- Colorblind mode, high contrast
- Reduced motion
- Subtitle settings

### **Settings UI Integration**
The configuration system provides structured data for GUI settings menus, making it easy to create comprehensive settings interfaces.

## 🔄 Integration with C++ GUI

### **Backward Compatibility**
The enhanced Python engine maintains full backward compatibility with the existing C++ GUI:

- **Same CLI Commands**: All existing commands work unchanged
- **Same JSON Format**: Scene and memory data formats preserved
- **Enhanced Data**: Additional fields provided when available
- **Error Handling**: Robust error handling for GUI integration

### **New Features Available**
- **Rich Scene Metadata**: Lighting, weather, camera effects
- **Advanced Memory Analytics**: Detailed player insights
- **Multiple Save Slots**: Enhanced save/load system
- **Settings Management**: Runtime configuration updates
- **Audio Integration**: Ready for audio system integration

## 🚀 Getting Started

### **1. Test the Engine**
```bash
cd python_backend
python3 game_engine.py
```

### **2. Test CLI Interface**
```bash
python3 cli_interface.py get_scene
python3 cli_interface.py get_memory
```

### **3. Test Individual Systems**
```bash
python3 config_system.py      # Test configuration
python3 audio_system.py       # Test audio system
python3 transition_manager.py # Test transitions
```

### **4. Build and Run Full Game**
```bash
cd ..
./build.sh
```

## 🔧 Development

### **Extending the Engine**

#### **Adding New Scenes**
1. Add scene data to `_load_scenes()` in `game_engine.py`
2. Create corresponding cutscene image
3. Add audio tracks if needed
4. Test with CLI interface

#### **Adding New Audio Tracks**
1. Add track to `_load_audio_tracks()` in `audio_system.py`
2. Place audio file in `assets/audio/`
3. Register with audio manager
4. Test playback

#### **Adding New Transitions**
1. Implement transition function in `transition_manager.py`
2. Register with transition registry
3. Test with transition manager

#### **Adding New Settings**
1. Add setting to `GameConfig` in `config_system.py`
2. Add to settings UI data structure
3. Implement validation if needed
4. Test configuration system

### **Performance Considerations**
- **Threading**: Audio and transitions run in separate threads
- **Memory Management**: Efficient data structures and cleanup
- **Caching**: Scene data cached for performance
- **Lazy Loading**: Audio tracks loaded on demand

### **Error Handling**
- **Graceful Degradation**: System continues if components fail
- **Comprehensive Logging**: Detailed logging for debugging
- **User Feedback**: Clear error messages for users
- **Recovery**: Automatic recovery from common errors

## 📈 Future Enhancements

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

## 🎯 Production Readiness

This Python game engine is designed for production use with:

- **Comprehensive Error Handling**: Robust error handling throughout
- **Extensive Logging**: Detailed logging for debugging and monitoring
- **Modular Architecture**: Easy to extend and maintain
- **Performance Optimized**: Efficient algorithms and data structures
- **Well Documented**: Comprehensive documentation and examples
- **Tested Components**: Individual systems tested and verified

The engine provides a solid foundation for building cinematic narrative games while maintaining the high-performance rendering capabilities of the C++/Qt6 GUI system.
