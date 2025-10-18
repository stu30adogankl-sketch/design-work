#!/usr/bin/env python3
"""
Into the Dark - Enhanced Command Line Interface
Provides JSON API for C++ GUI to communicate with the complete game engine
"""

import sys
import json
import os
from pathlib import Path
from game_engine import GameEngine

def main():
    """Enhanced command line interface for C++ GUI communication"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        return
    
    command = sys.argv[1]
    
    # Initialize game engine
    try:
        engine = GameEngine()
    except Exception as e:
        print(json.dumps({"error": f"Failed to initialize game engine: {str(e)}"}))
        return
    
    try:
        if command == "get_scene":
            scene_data = engine.get_scene_data()
            if not scene_data:
                print(json.dumps({"error": "No scene data available"}))
                return
            
            # Format for backward compatibility with C++ GUI
            result = {
                "scene_id": scene_data["scene_id"],
                "title": scene_data["title"],
                "background": scene_data["background"],
                "dialogue": "\n\n".join([f"{d['speaker']}: {d['text']}" for d in scene_data["dialogues"]]),
                "audio_track": scene_data["audio_track"],
                "ambient_sound": scene_data["ambient_sound"],
                "lighting": scene_data["lighting"],
                "weather_effect": scene_data["weather_effect"],
                "camera_effect": scene_data["camera_effect"],
                "choices": [
                    {
                        "text": choice["text"],
                        "memory_type": choice["memory_type"],
                        "memory_value": choice["memory_value"],
                        "consequence_text": choice["consequence_text"]
                    }
                    for choice in scene_data["choices"]
                ]
            }
            print(json.dumps(result))
            
        elif command == "get_memory":
            memory_data = engine.get_memory_data()
            result = {
                "kindness": memory_data["kindness"],
                "obsession": memory_data["obsession"],
                "truth": memory_data["truth"],
                "trust": memory_data["trust"],
                "alignment": memory_data["alignment"],
                "total_choices": memory_data["total_choices"],
                "play_time": memory_data["play_time"],
                "insights": memory_data["insights"]
            }
            print(json.dumps(result))
            
        elif command == "make_choice":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Choice index required"}))
                return
            
            choice_index = int(sys.argv[2])
            success, message = engine.make_choice(choice_index)
            result = {
                "success": success,
                "message": message
            }
            print(json.dumps(result))
            
        elif command == "reset_game":
            success = engine.reset_game()
            result = {
                "success": success,
                "message": "Game reset successfully" if success else "Failed to reset game"
            }
            print(json.dumps(result))
            
        elif command == "get_save_slots":
            save_slots = engine.save_manager.get_save_slots()
            result = {
                "save_slots": save_slots
            }
            print(json.dumps(result))
            
        elif command == "save_game":
            slot = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            success = engine.save_manager.save_game(engine.progress, slot)
            result = {
                "success": success,
                "message": f"Game saved to slot {slot}" if success else "Failed to save game"
            }
            print(json.dumps(result))
            
        elif command == "load_game":
            slot = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            loaded_progress = engine.save_manager.load_game(slot)
            if loaded_progress:
                engine.progress = loaded_progress
                result = {
                    "success": True,
                    "message": f"Game loaded from slot {slot}"
                }
            else:
                result = {
                    "success": False,
                    "message": f"Failed to load game from slot {slot}"
                }
            print(json.dumps(result))
            
        elif command == "get_settings":
            result = {
                "settings": engine.settings
            }
            print(json.dumps(result))
            
        elif command == "update_settings":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Settings JSON required"}))
                return
            
            try:
                settings = json.loads(sys.argv[2])
                engine.update_settings(settings)
                result = {
                    "success": True,
                    "message": "Settings updated successfully"
                }
            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "message": "Invalid JSON format"
                }
            print(json.dumps(result))
            
        elif command == "get_scene_list":
            scene_list = []
            for scene_id, scene in engine.scenes.items():
                scene_list.append({
                    "scene_id": scene_id,
                    "title": scene.title,
                    "background": scene.background,
                    "watched": scene_id in engine.progress.watched_cutscenes
                })
            result = {
                "scenes": scene_list
            }
            print(json.dumps(result))
            
        elif command == "get_analytics":
            analytics = engine.memory_analytics.get_memory_insights()
            result = {
                "analytics": analytics,
                "total_scenes": len(engine.scenes),
                "watched_scenes": len(engine.progress.watched_cutscenes),
                "completion_percentage": (len(engine.progress.watched_cutscenes) / len(engine.scenes)) * 100
            }
            print(json.dumps(result))
            
        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
