#!/usr/bin/env python3
"""
Into the Dark - Story Engine
Handles dialogue, choices, memory tracking, and save/load functionality.
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class MemoryType(Enum):
    KINDNESS = "kindness"
    OBSESSION = "obsession"
    TRUTH = "truth"
    TRUST = "trust"

@dataclass
class Choice:
    """Represents a single choice option"""
    text: str
    memory_type: MemoryType
    memory_value: int
    next_scene: Optional[int] = None

@dataclass
class Scene:
    """Represents a game scene with dialogue and choices"""
    scene_id: int
    background: str
    dialogue: str
    choices: List[Choice]
    audio_track: Optional[str] = None

@dataclass
class GameState:
    """Current game state including memory values and progress"""
    current_scene: int
    watched_cutscenes: List[int]
    memory_values: Dict[str, int]
    act_progression: int
    
    def __post_init__(self):
        if not self.memory_values:
            self.memory_values = {
                MemoryType.KINDNESS.value: 0,
                MemoryType.OBSESSION.value: 0,
                MemoryType.TRUTH.value: 0,
                MemoryType.TRUST.value: 0
            }

class StoryEngine:
    """Main story engine that manages game state and progression"""
    
    def __init__(self, save_path: str = "save/save.json"):
        self.save_path = save_path
        self.scenes = self._load_scenes()
        self.game_state = self._load_game_state()
    
    def _load_scenes(self) -> Dict[int, Scene]:
        """Load all game scenes with dialogue and choices"""
        scenes = {}
        
        # Scene 1 - The Awakening
        scenes[1] = Scene(
            scene_id=1,
            background="cutscene1.jpg",
            dialogue="Rika wakes in the red-ash wasteland, surrounded by shattered ruins.\n\nRika: \"This place again... the world that forgot how to die.\"",
            choices=[
                Choice("Call out for anyone.", MemoryType.KINDNESS, 5),
                Choice("Stay silent and listen.", MemoryType.OBSESSION, 5),
                Choice("Touch the mirror shard beside you.", MemoryType.TRUTH, 5),
                Choice("Scan the surroundings carefully.", MemoryType.TRUST, 5)
            ],
            audio_track="audio1.mp3"
        )
        
        # Scene 2 - Echoes of the Machine
        scenes[2] = Scene(
            scene_id=2,
            background="cutscene2.jpg",
            dialogue="Rika approaches flickering terminals whispering fragments of her name.",
            choices=[
                Choice("Speak to the terminals.", MemoryType.KINDNESS, 5),
                Choice("Ignore them and focus on her path.", MemoryType.OBSESSION, 5),
                Choice("Try to decode the messages.", MemoryType.TRUTH, 5),
                Choice("Call for Penci to help.", MemoryType.TRUST, 5)
            ],
            audio_track="audio2.mp3"
        )
        
        # Scene 3 - The Companion Appears
        scenes[3] = Scene(
            scene_id=3,
            background="cutscene3.jpg",
            dialogue="Penci Zorno emerges from the ruins carrying a broken lantern.\n\nPenci: \"Rika… I thought I lost you again.\"\n\nRika: \"Then let's move together.\"",
            choices=[
                Choice("Move cautiously together.", MemoryType.TRUST, 5),
                Choice("Lead the way alone.", MemoryType.OBSESSION, 5),
                Choice("Talk to Penci about the ruins.", MemoryType.KINDNESS, 5),
                Choice("Examine the ruins first.", MemoryType.TRUTH, 5)
            ],
            audio_track="audio3.mp3"
        )
        
        # Scene 4 - The Mirror of Memory
        scenes[4] = Scene(
            scene_id=4,
            background="cutscene4.jpg",
            dialogue="Rika sees her reflection in a cracked mirror, distorted by light.",
            choices=[
                Choice("Touch the reflection.", MemoryType.TRUTH, 5),
                Choice("Step back and observe.", MemoryType.OBSESSION, 5),
                Choice("Speak to it gently.", MemoryType.KINDNESS, 5),
                Choice("Ignore and move forward.", MemoryType.TRUST, 5)
            ],
            audio_track="audio4.mp3"
        )
        
        # Placeholder scenes 5-10
        for i in range(5, 11):
            scenes[i] = Scene(
                scene_id=i,
                background=f"cutscene{i}.jpg",
                dialogue=f"Scene {i} - Placeholder dialogue for future development.",
                choices=[
                    Choice(f"Choice 1 for scene {i}", MemoryType.KINDNESS, 5),
                    Choice(f"Choice 2 for scene {i}", MemoryType.OBSESSION, 5),
                    Choice(f"Choice 3 for scene {i}", MemoryType.TRUTH, 5),
                    Choice(f"Choice 4 for scene {i}", MemoryType.TRUST, 5)
                ],
                audio_track="audio1.mp3"  # Reuse audio tracks
            )
        
        return scenes
    
    def _load_game_state(self) -> GameState:
        """Load game state from save file or create new one"""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                return GameState(**data)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error loading save file: {e}")
        
        # Create new game state
        return GameState(
            current_scene=1,
            watched_cutscenes=[],
            memory_values={},
            act_progression=1
        )
    
    def get_current_scene(self) -> Scene:
        """Get the current scene"""
        return self.scenes[self.game_state.current_scene]
    
    def make_choice(self, choice_index: int) -> Tuple[bool, str]:
        """
        Make a choice and update game state
        Returns: (success, message)
        """
        if choice_index < 0 or choice_index >= 4:
            return False, "Invalid choice index"
        
        scene = self.get_current_scene()
        choice = scene.choices[choice_index]
        
        # Update memory values
        memory_key = choice.memory_type.value
        self.game_state.memory_values[memory_key] += choice.memory_value
        
        # Mark scene as watched
        if self.game_state.current_scene not in self.game_state.watched_cutscenes:
            self.game_state.watched_cutscenes.append(self.game_state.current_scene)
        
        # Move to next scene
        if choice.next_scene:
            self.game_state.current_scene = choice.next_scene
        else:
            # Default progression
            if self.game_state.current_scene < len(self.scenes):
                self.game_state.current_scene += 1
        
        # Save game state
        self.save_game()
        
        return True, f"Choice made: {choice.text}"
    
    def get_memory_percentages(self) -> Dict[str, float]:
        """Get memory values as percentages (0-100)"""
        max_value = 100  # Maximum possible value for each memory type
        percentages = {}
        
        for memory_type in MemoryType:
            value = self.game_state.memory_values.get(memory_type.value, 0)
            percentages[memory_type.value] = min((value / max_value) * 100, 100.0)
        
        return percentages
    
    def get_memory_alignment(self) -> str:
        """Determine overall memory alignment based on dominant traits"""
        percentages = self.get_memory_percentages()
        
        # Find the dominant memory type
        dominant = max(percentages.items(), key=lambda x: x[1])
        
        if dominant[1] < 20:
            return "Neutral"
        elif dominant[0] == MemoryType.KINDNESS.value:
            return "Kind"
        elif dominant[0] == MemoryType.OBSESSION.value:
            return "Obsessed"
        elif dominant[0] == MemoryType.TRUTH.value:
            return "Truth-Seeker"
        elif dominant[0] == MemoryType.TRUST.value:
            return "Trusting"
        else:
            return "Balanced"
    
    def save_game(self) -> bool:
        """Save current game state to file"""
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            with open(self.save_path, 'w') as f:
                json.dump(asdict(self.game_state), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def reset_game(self) -> bool:
        """Reset game to initial state"""
        self.game_state = GameState(
            current_scene=1,
            watched_cutscenes=[],
            memory_values={},
            act_progression=1
        )
        return self.save_game()

def main():
    """Command-line interface for testing the story engine"""
    engine = StoryEngine()
    
    print("Into the Dark - Story Engine")
    print("=" * 40)
    
    while True:
        scene = engine.get_current_scene()
        print(f"\nScene {scene.scene_id}: {scene.background}")
        print(f"Dialogue: {scene.dialogue}")
        print("\nChoices:")
        
        for i, choice in enumerate(scene.choices):
            print(f"{i + 1}. {choice.text} (+{choice.memory_value} {choice.memory_type.value})")
        
        print(f"\nMemory Values: {engine.get_memory_percentages()}")
        print(f"Alignment: {engine.get_memory_alignment()}")
        
        try:
            choice = input("\nEnter choice (1-4) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                break
            
            choice_index = int(choice) - 1
            success, message = engine.make_choice(choice_index)
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
                
        except (ValueError, KeyboardInterrupt):
            print("Invalid input or interrupted")
            break
    
    print("\nGame saved. Goodbye!")

if __name__ == "__main__":
    main()
