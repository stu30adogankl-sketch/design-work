#!/usr/bin/env python3
"""
Into the Dark - Complete Engine Test Suite
Tests all components of the Python game engine
"""

import sys
import os
import json
import time
from pathlib import Path

# Add python_backend to path
sys.path.insert(0, str(Path(__file__).parent / "python_backend"))

def test_game_engine():
    """Test the main game engine"""
    print("Testing Game Engine...")
    try:
        from game_engine import GameEngine
        
        engine = GameEngine()
        
        # Test scene data
        scene_data = engine.get_scene_data()
        assert scene_data["scene_id"] == 1
        assert scene_data["title"] == "The Awakening"
        print("✓ Scene data retrieval works")
        
        # Test memory data
        memory_data = engine.get_memory_data()
        assert "kindness" in memory_data
        assert "alignment" in memory_data
        print("✓ Memory data retrieval works")
        
        # Test choice making
        success, message = engine.make_choice(0)
        assert success == True
        print("✓ Choice making works")
        
        # Test memory update
        memory_data_after = engine.get_memory_data()
        assert memory_data_after["kindness"] > memory_data["kindness"]
        print("✓ Memory updates work")
        
        print("✓ Game Engine: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Game Engine: FAILED - {e}\n")
        return False

def test_cli_interface():
    """Test the CLI interface"""
    print("Testing CLI Interface...")
    try:
        import subprocess
        
        # Test get_scene command
        result = subprocess.run([
            "python3", "python_backend/cli_interface.py", "get_scene"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        assert result.returncode == 0
        scene_data = json.loads(result.stdout)
        assert "scene_id" in scene_data
        print("✓ get_scene command works")
        
        # Test get_memory command
        result = subprocess.run([
            "python3", "python_backend/cli_interface.py", "get_memory"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        assert result.returncode == 0
        memory_data = json.loads(result.stdout)
        assert "kindness" in memory_data
        print("✓ get_memory command works")
        
        # Test make_choice command
        result = subprocess.run([
            "python3", "python_backend/cli_interface.py", "make_choice", "0"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        assert result.returncode == 0
        choice_result = json.loads(result.stdout)
        assert choice_result["success"] == True
        print("✓ make_choice command works")
        
        print("✓ CLI Interface: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ CLI Interface: FAILED - {e}\n")
        return False

def test_config_system():
    """Test the configuration system"""
    print("Testing Configuration System...")
    try:
        from config_system import ConfigManager, SettingsUI
        
        # Test config manager
        config_manager = ConfigManager("test_config.json")
        config = config_manager.get_config()
        
        assert hasattr(config, "resolution")
        assert hasattr(config, "master_volume")
        print("✓ Configuration loading works")
        
        # Test settings update
        success = config_manager.update_config({"master_volume": 0.8})
        assert success == True
        assert config_manager.get_config().master_volume == 0.8
        print("✓ Configuration updates work")
        
        # Test settings UI
        settings_ui = SettingsUI(config_manager)
        menu_data = settings_ui.get_settings_menu_data()
        
        assert "display" in menu_data
        assert "audio" in menu_data
        print("✓ Settings UI data generation works")
        
        # Cleanup
        os.remove("test_config.json")
        
        print("✓ Configuration System: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Configuration System: FAILED - {e}\n")
        return False

def test_audio_system():
    """Test the audio system"""
    print("Testing Audio System...")
    try:
        from audio_system import AudioManager, AudioEventManager
        
        # Test audio manager
        audio_manager = AudioManager()
        
        # Test volume controls
        audio_manager.set_master_volume(0.5)
        assert audio_manager.master_volume == 0.5
        print("✓ Volume controls work")
        
        # Test mute toggle
        muted = audio_manager.toggle_mute()
        assert muted == True
        muted = audio_manager.toggle_mute()
        assert muted == False
        print("✓ Mute toggle works")
        
        # Test audio status
        status = audio_manager.get_audio_status()
        assert "master_volume" in status
        assert "muted" in status
        print("✓ Audio status retrieval works")
        
        # Test event manager
        event_manager = AudioEventManager(audio_manager)
        event_manager.trigger_event("choice_made")
        print("✓ Audio event triggers work")
        
        print("✓ Audio System: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Audio System: FAILED - {e}\n")
        return False

def test_transition_manager():
    """Test the transition manager"""
    print("Testing Transition Manager...")
    try:
        from transition_manager import TransitionManager, TransitionType
        
        # Test transition manager
        transition_manager = TransitionManager()
        
        # Test transition creation
        transition = transition_manager.create_transition(
            TransitionType.FADE_IN,
            duration=1.0
        )
        assert transition.transition_type == TransitionType.FADE_IN
        assert transition.duration == 1.0
        print("✓ Transition creation works")
        
        # Test transition status
        status = transition_manager.get_transition_status()
        assert "state" in status
        assert "is_transitioning" in status
        print("✓ Transition status works")
        
        # Test transition execution (quick test)
        transition_manager.execute_transition(transition)
        time.sleep(0.1)  # Brief wait
        print("✓ Transition execution works")
        
        print("✓ Transition Manager: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Transition Manager: FAILED - {e}\n")
        return False

def test_save_system():
    """Test the save system"""
    print("Testing Save System...")
    try:
        from game_engine import GameEngine
        
        engine = GameEngine()
        
        # Test save game
        success = engine.save_manager.save_game(engine.progress, 0)
        assert success == True
        print("✓ Save game works")
        
        # Test load game
        loaded_progress = engine.save_manager.load_game(0)
        assert loaded_progress is not None
        assert loaded_progress.current_scene == engine.progress.current_scene
        print("✓ Load game works")
        
        # Test save slots
        save_slots = engine.save_manager.get_save_slots()
        assert len(save_slots) > 0
        print("✓ Save slots listing works")
        
        print("✓ Save System: ALL TESTS PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Save System: FAILED - {e}\n")
        return False

def main():
    """Run all tests"""
    print("Into the Dark - Complete Engine Test Suite")
    print("=" * 50)
    
    tests = [
        test_game_engine,
        test_cli_interface,
        test_config_system,
        test_audio_system,
        test_transition_manager,
        test_save_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Engine is ready for production.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
