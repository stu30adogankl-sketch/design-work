#!/usr/bin/env python3
"""
Into the Dark - Complete Python Game Engine
A comprehensive, production-ready game engine for cinematic narrative games.
"""

import json
import os
import sys
import time
import threading
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GameState(Enum):
    """Game state enumeration"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    CUTSCENE = "cutscene"
    DIALOGUE = "dialogue"
    CHOICE = "choice"
    SAVING = "saving"
    LOADING = "loading"

class MemoryType(Enum):
    """Memory type enumeration"""
    KINDNESS = "kindness"
    OBSESSION = "obsession"
    TRUTH = "truth"
    TRUST = "trust"

class TransitionType(Enum):
    """Transition type enumeration"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    CROSSFADE = "crossfade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    NONE = "none"

@dataclass
class Choice:
    """Represents a single choice option with enhanced metadata"""
    text: str
    memory_type: MemoryType
    memory_value: int
    next_scene: Optional[int] = None
    condition: Optional[str] = None  # Python expression for conditional choices
    consequence_text: Optional[str] = None  # Text shown after choice
    sound_effect: Optional[str] = None
    animation: Optional[str] = None

@dataclass
class Dialogue:
    """Represents dialogue with speaker and timing"""
    speaker: str
    text: str
    duration: float = 3.0  # Auto-advance duration
    emotion: str = "neutral"  # neutral, happy, sad, angry, etc.
    voice_actor: Optional[str] = None
    sound_effect: Optional[str] = None

@dataclass
class Scene:
    """Enhanced scene representation with full metadata"""
    scene_id: int
    title: str
    background: str
    dialogues: List[Dialogue]
    choices: List[Choice]
    audio_track: Optional[str] = None
    ambient_sound: Optional[str] = None
    transition_in: TransitionType = TransitionType.FADE_IN
    transition_out: TransitionType = TransitionType.FADE_OUT
    duration: Optional[float] = None  # Auto-advance duration
    weather_effect: Optional[str] = None  # rain, snow, ash, etc.
    lighting: str = "normal"  # normal, dim, bright, eerie
    camera_effect: Optional[str] = None  # shake, zoom, pan

@dataclass
class GameProgress:
    """Enhanced game progress tracking"""
    current_scene: int
    current_act: int
    watched_cutscenes: List[int]
    memory_values: Dict[str, int] = field(default_factory=dict)
    choices_made: List[Tuple[int, int]] = field(default_factory=list)  # (scene_id, choice_index)
    play_time: float = 0.0
    save_slots: Dict[int, Dict] = field(default_factory=dict)
    achievements: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)

class MemoryAnalytics:
    """Advanced memory tracking and analytics"""
    
    def __init__(self):
        self.memory_history: List[Tuple[float, Dict[str, int]]] = []
        self.choice_patterns: Dict[str, int] = {}
        self.alignment_changes: List[Tuple[float, str]] = []
    
    def track_choice(self, scene_id: int, choice: Choice, timestamp: float):
        """Track a choice and its impact on memory"""
        memory_key = f"scene_{scene_id}_choice_{choice.memory_type.value}"
        self.choice_patterns[memory_key] = self.choice_patterns.get(memory_key, 0) + 1
        
        # Track alignment changes (this would be called after memory update)
        # For now, we'll skip this complex tracking
        pass
    
    def get_current_alignment(self, memory_values: Dict[str, int] = None) -> str:
        """Calculate current alignment based on memory values"""
        if not memory_values:
            return "Neutral"
        
        max_value = max(memory_values.values())
        if max_value < 20:
            return "Neutral"
        
        dominant = max(memory_values.items(), key=lambda x: x[1])
        
        alignment_map = {
            MemoryType.KINDNESS.value: "Kind",
            MemoryType.OBSESSION.value: "Obsessed", 
            MemoryType.TRUTH.value: "Truth-Seeker",
            MemoryType.TRUST.value: "Trusting"
        }
        
        return alignment_map.get(dominant[0], "Balanced")
    
    def get_memory_insights(self) -> Dict[str, Any]:
        """Get insights about player's memory patterns"""
        return {
            "total_choices": len(self.choice_patterns),
            "alignment_changes": len(self.alignment_changes),
            "most_common_choice_type": max(self.choice_patterns.items(), key=lambda x: x[1])[0] if self.choice_patterns else None,
            "play_style": self._analyze_play_style()
        }
    
    def _analyze_play_style(self) -> str:
        """Analyze player's choice patterns"""
        if not self.choice_patterns:
            return "Unknown"
        
        kindness_count = sum(1 for k in self.choice_patterns.keys() if "kindness" in k)
        obsession_count = sum(1 for k in self.choice_patterns.keys() if "obsession" in k)
        truth_count = sum(1 for k in self.choice_patterns.keys() if "truth" in k)
        trust_count = sum(1 for k in self.choice_patterns.keys() if "trust" in k)
        
        counts = {
            "Kind": kindness_count,
            "Obsessed": obsession_count,
            "Truth-Seeker": truth_count,
            "Trusting": trust_count
        }
        
        dominant = max(counts.items(), key=lambda x: x[1])
        return dominant[0] if dominant[1] > 0 else "Balanced"

class AudioManager:
    """Audio management system"""
    
    def __init__(self):
        self.current_track: Optional[str] = None
        self.volume: float = 0.7
        self.muted: bool = False
        self.sound_effects: Dict[str, str] = {}
        
    def play_background_music(self, track_path: str, loop: bool = True):
        """Play background music"""
        if self.muted:
            return
        
        logger.info(f"Playing background music: {track_path}")
        self.current_track = track_path
        # Implementation would use pygame or similar audio library
        
    def play_sound_effect(self, effect_name: str):
        """Play a sound effect"""
        if self.muted or effect_name not in self.sound_effects:
            return
        
        logger.info(f"Playing sound effect: {effect_name}")
        # Implementation would use pygame or similar audio library
        
    def set_volume(self, volume: float):
        """Set audio volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
    def toggle_mute(self):
        """Toggle audio mute"""
        self.muted = not self.muted
        return self.muted

class TransitionManager:
    """Manages scene transitions and animations"""
    
    def __init__(self):
        self.current_transition: Optional[TransitionType] = None
        self.transition_duration: float = 1.0
        self.callbacks: Dict[TransitionType, Callable] = {}
        
    def register_transition(self, transition_type: TransitionType, callback: Callable):
        """Register a transition callback"""
        self.callbacks[transition_type] = callback
        
    def execute_transition(self, transition_type: TransitionType, duration: float = None):
        """Execute a transition"""
        if duration:
            self.transition_duration = duration
            
        self.current_transition = transition_type
        
        if transition_type in self.callbacks:
            self.callbacks[transition_type]()
        else:
            logger.warning(f"No callback registered for transition: {transition_type}")
            
    def is_transitioning(self) -> bool:
        """Check if currently transitioning"""
        return self.current_transition is not None

class DialogueManager:
    """Manages dialogue display with typewriter effect"""
    
    def __init__(self):
        self.current_dialogue: Optional[Dialogue] = None
        self.typewriter_speed: float = 0.05  # seconds per character
        self.auto_advance: bool = True
        self.typewriter_thread: Optional[threading.Thread] = None
        self.display_callback: Optional[Callable] = None
        
    def set_display_callback(self, callback: Callable[[str], None]):
        """Set callback for displaying dialogue text"""
        self.display_callback = callback
        
    def start_dialogue(self, dialogue: Dialogue):
        """Start displaying dialogue with typewriter effect"""
        self.current_dialogue = dialogue
        
        if self.typewriter_thread and self.typewriter_thread.is_alive():
            self.typewriter_thread.join()
            
        self.typewriter_thread = threading.Thread(
            target=self._typewriter_effect,
            args=(dialogue.text,)
        )
        self.typewriter_thread.start()
        
    def _typewriter_effect(self, text: str):
        """Typewriter effect implementation"""
        displayed_text = ""
        
        for i, char in enumerate(text):
            displayed_text += char
            
            if self.display_callback:
                self.display_callback(displayed_text)
                
            time.sleep(self.typewriter_speed)
            
        # Auto-advance after completion
        if self.auto_advance and self.current_dialogue:
            time.sleep(self.current_dialogue.duration)
            self._advance_dialogue()
            
    def _advance_dialogue(self):
        """Advance to next dialogue or choice"""
        # This would trigger the next dialogue or show choices
        pass
        
    def skip_typewriter(self):
        """Skip typewriter effect and show full text"""
        if self.current_dialogue and self.display_callback:
            self.display_callback(self.current_dialogue.text)

class SaveManager:
    """Enhanced save/load system with multiple slots"""
    
    def __init__(self, save_directory: str = "save"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
        self.max_save_slots = 10
        
    def save_game(self, game_progress: GameProgress, slot: int = 0) -> bool:
        """Save game to specified slot"""
        try:
            save_data = {
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "progress": asdict(game_progress),
                "metadata": {
                    "play_time": game_progress.play_time,
                    "current_scene": game_progress.current_scene,
                    "alignment": self._get_current_alignment(game_progress.memory_values)
                }
            }
            
            save_file = self.save_directory / f"save_slot_{slot}.json"
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
                
            logger.info(f"Game saved to slot {slot}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
            
    def load_game(self, slot: int = 0) -> Optional[GameProgress]:
        """Load game from specified slot"""
        try:
            save_file = self.save_directory / f"save_slot_{slot}.json"
            
            if not save_file.exists():
                logger.warning(f"Save file not found: {save_file}")
                return None
                
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                
            progress_data = save_data["progress"]
            game_progress = GameProgress(**progress_data)
            
            logger.info(f"Game loaded from slot {slot}")
            return game_progress
            
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return None
            
    def get_save_slots(self) -> List[Dict[str, Any]]:
        """Get information about all save slots"""
        slots = []
        
        for slot in range(self.max_save_slots):
            save_file = self.save_directory / f"save_slot_{slot}.json"
            
            if save_file.exists():
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    
                    slots.append({
                        "slot": slot,
                        "timestamp": save_data.get("timestamp", "Unknown"),
                        "current_scene": save_data.get("metadata", {}).get("current_scene", 0),
                        "play_time": save_data.get("metadata", {}).get("play_time", 0),
                        "alignment": save_data.get("metadata", {}).get("alignment", "Unknown")
                    })
                except Exception as e:
                    logger.error(f"Failed to read save slot {slot}: {e}")
            else:
                slots.append({
                    "slot": slot,
                    "timestamp": None,
                    "current_scene": 0,
                    "play_time": 0,
                    "alignment": "Empty"
                })
                
        return slots
        
    def _get_current_alignment(self, memory_values: Dict[str, int]) -> str:
        """Calculate current alignment"""
        if not memory_values:
            return "Neutral"
            
        max_value = max(memory_values.values())
        if max_value < 20:
            return "Neutral"
            
        dominant = max(memory_values.items(), key=lambda x: x[1])
        
        alignment_map = {
            MemoryType.KINDNESS.value: "Kind",
            MemoryType.OBSESSION.value: "Obsessed",
            MemoryType.TRUTH.value: "Truth-Seeker", 
            MemoryType.TRUST.value: "Trusting"
        }
        
        return alignment_map.get(dominant[0], "Balanced")

class GameEngine:
    """Main game engine class"""
    
    def __init__(self):
        self.state = GameState.MENU
        self.scenes: Dict[int, Scene] = {}
        self.progress = GameProgress(
            current_scene=1,
            current_act=1,
            watched_cutscenes=[],
            memory_values={
                MemoryType.KINDNESS.value: 0,
                MemoryType.OBSESSION.value: 0,
                MemoryType.TRUTH.value: 0,
                MemoryType.TRUST.value: 0
            }
        )
        
        # Initialize subsystems
        self.memory_analytics = MemoryAnalytics()
        self.audio_manager = AudioManager()
        self.transition_manager = TransitionManager()
        self.dialogue_manager = DialogueManager()
        self.save_manager = SaveManager()
        
        # Game settings
        self.settings = {
            "text_speed": 0.05,
            "auto_advance": True,
            "volume": 0.7,
            "fullscreen": False,
            "language": "en"
        }
        
        # Load scenes
        self._load_scenes()
        
        # Start game timer
        self.start_time = time.time()
        
    def _load_scenes(self):
        """Load all game scenes with enhanced metadata"""
        
        # Scene 1 - The Awakening
        self.scenes[1] = Scene(
            scene_id=1,
            title="The Awakening",
            background="cutscene1.jpg",
            dialogues=[
                Dialogue("Narrator", "Rika wakes in the red-ash wasteland, surrounded by shattered ruins.", 4.0),
                Dialogue("Rika", "This place again... the world that forgot how to die.", 3.0, emotion="melancholic")
            ],
            choices=[
                Choice("Call out for anyone.", MemoryType.KINDNESS, 5, consequence_text="Your voice echoes through the ruins."),
                Choice("Stay silent and listen.", MemoryType.OBSESSION, 5, consequence_text="You hear whispers in the wind."),
                Choice("Touch the mirror shard beside you.", MemoryType.TRUTH, 5, consequence_text="The shard pulses with ancient energy."),
                Choice("Scan the surroundings carefully.", MemoryType.TRUST, 5, consequence_text="You notice movement in the distance.")
            ],
            audio_track="audio1.mp3",
            ambient_sound="wind_ruins.mp3",
            lighting="dim",
            weather_effect="ash"
        )
        
        # Scene 2 - Echoes of the Machine
        self.scenes[2] = Scene(
            scene_id=2,
            title="Echoes of the Machine",
            background="cutscene2.jpg",
            dialogues=[
                Dialogue("Narrator", "Rika approaches flickering terminals whispering fragments of her name.", 4.0),
                Dialogue("Terminal", "Rika... Rika...", 2.0, emotion="mechanical")
            ],
            choices=[
                Choice("Speak to the terminals.", MemoryType.KINDNESS, 5, consequence_text="The terminals respond with warmth."),
                Choice("Ignore them and focus on her path.", MemoryType.OBSESSION, 5, consequence_text="You block out the distractions."),
                Choice("Try to decode the messages.", MemoryType.TRUTH, 5, consequence_text="Patterns emerge in the data."),
                Choice("Call for Penci to help.", MemoryType.TRUST, 5, consequence_text="Penci's voice echoes back.")
            ],
            audio_track="audio2.mp3",
            ambient_sound="machine_hum.mp3",
            lighting="eerie",
            camera_effect="shake"
        )
        
        # Scene 3 - The Companion Appears
        self.scenes[3] = Scene(
            scene_id=3,
            title="The Companion Appears",
            background="cutscene3.jpg",
            dialogues=[
                Dialogue("Narrator", "Penci Zorno emerges from the ruins carrying a broken lantern.", 4.0),
                Dialogue("Penci", "Rika… I thought I lost you again.", 3.0, emotion="relieved"),
                Dialogue("Rika", "Then let's move together.", 2.0, emotion="determined")
            ],
            choices=[
                Choice("Move cautiously together.", MemoryType.TRUST, 5, consequence_text="You walk side by side, watching each other's backs."),
                Choice("Lead the way alone.", MemoryType.OBSESSION, 5, consequence_text="You forge ahead, focused on your goal."),
                Choice("Talk to Penci about the ruins.", MemoryType.KINDNESS, 5, consequence_text="Penci shares stories of the old world."),
                Choice("Examine the ruins first.", MemoryType.TRUTH, 5, consequence_text="You discover ancient inscriptions.")
            ],
            audio_track="audio3.mp3",
            ambient_sound="footsteps.mp3",
            lighting="normal"
        )
        
        # Scene 4 - The Mirror of Memory
        self.scenes[4] = Scene(
            scene_id=4,
            title="The Mirror of Memory",
            background="cutscene4.jpg",
            dialogues=[
                Dialogue("Narrator", "Rika sees her reflection in a cracked mirror, distorted by light.", 4.0),
                Dialogue("Reflection", "Who are you really?", 2.0, emotion="mysterious")
            ],
            choices=[
                Choice("Touch the reflection.", MemoryType.TRUTH, 5, consequence_text="The mirror shatters, revealing hidden depths."),
                Choice("Step back and observe.", MemoryType.OBSESSION, 5, consequence_text="You study the reflection carefully."),
                Choice("Speak to it gently.", MemoryType.KINDNESS, 5, consequence_text="The reflection softens and smiles."),
                Choice("Ignore and move forward.", MemoryType.TRUST, 5, consequence_text="You trust your instincts and continue.")
            ],
            audio_track="audio4.mp3",
            ambient_sound="glass_chimes.mp3",
            lighting="eerie",
            camera_effect="zoom"
        )
        
        # Scene 5 - The Broken Path
        self.scenes[5] = Scene(
            scene_id=5,
            title="The Broken Path",
            background="cutscene5.jpg",
            dialogues=[
                Dialogue("Narrator", "A fork in the road leads to different futures, each more uncertain than the last.", 4.0),
                Dialogue("Rika", "Which path holds the truth?", 2.0, emotion="uncertain")
            ],
            choices=[
                Choice("Take the left path.", MemoryType.KINDNESS, 5, consequence_text="The path feels warm and inviting."),
                Choice("Take the right path.", MemoryType.OBSESSION, 5, consequence_text="The path calls to your determination."),
                Choice("Study both paths carefully.", MemoryType.TRUTH, 5, consequence_text="You notice subtle differences in the terrain."),
                Choice("Ask Penci for guidance.", MemoryType.TRUST, 5, consequence_text="Penci shares ancient wisdom about the paths.")
            ],
            audio_track="audio1.mp3",
            ambient_sound="wind_ruins.mp3",
            lighting="dim",
            weather_effect="ash"
        )
        
        # Scene 6 - Whispers in the Dark
        self.scenes[6] = Scene(
            scene_id=6,
            title="Whispers in the Dark",
            background="cutscene6.jpg",
            dialogues=[
                Dialogue("Narrator", "Voices from the past echo through the ruins, calling her name.", 4.0),
                Dialogue("Voice", "Rika... remember who you were...", 3.0, emotion="mysterious")
            ],
            choices=[
                Choice("Answer the voices.", MemoryType.KINDNESS, 5, consequence_text="The voices respond with warmth."),
                Choice("Ignore the voices and press on.", MemoryType.OBSESSION, 5, consequence_text="You focus on your mission."),
                Choice("Try to understand what they're saying.", MemoryType.TRUTH, 5, consequence_text="The voices reveal fragments of truth."),
                Choice("Stay close to Penci.", MemoryType.TRUST, 5, consequence_text="Penci helps you resist the voices.")
            ],
            audio_track="audio2.mp3",
            ambient_sound="machine_hum.mp3",
            lighting="eerie",
            camera_effect="shake"
        )
        
        # Scene 7 - The Tower of Truth
        self.scenes[7] = Scene(
            scene_id=7,
            title="The Tower of Truth",
            background="cutscene7.jpg",
            dialogues=[
                Dialogue("Narrator", "A towering structure pierces the sky, its purpose lost to time.", 4.0),
                Dialogue("Rika", "This must be where the answers lie.", 2.0, emotion="determined")
            ],
            choices=[
                Choice("Approach the tower cautiously.", MemoryType.KINDNESS, 5, consequence_text="You move with care and respect."),
                Choice("Charge toward the tower.", MemoryType.OBSESSION, 5, consequence_text="You rush forward with single-minded purpose."),
                Choice("Examine the tower's architecture.", MemoryType.TRUTH, 5, consequence_text="You discover ancient symbols and patterns."),
                Choice("Wait for Penci to catch up.", MemoryType.TRUST, 5, consequence_text="Together you approach the tower.")
            ],
            audio_track="audio3.mp3",
            ambient_sound="footsteps.mp3",
            lighting="normal"
        )
        
        # Scene 8 - The Final Choice
        self.scenes[8] = Scene(
            scene_id=8,
            title="The Final Choice",
            background="cutscene8.jpg",
            dialogues=[
                Dialogue("Narrator", "The path ahead splits into four directions, each representing a different truth.", 4.0),
                Dialogue("Rika", "This is it... the moment that will define everything.", 3.0, emotion="resolved")
            ],
            choices=[
                Choice("Choose the path of compassion.", MemoryType.KINDNESS, 10, consequence_text="You embrace kindness as your guiding light."),
                Choice("Choose the path of determination.", MemoryType.OBSESSION, 10, consequence_text="You commit to your unwavering purpose."),
                Choice("Choose the path of knowledge.", MemoryType.TRUTH, 10, consequence_text="You seek the ultimate truth above all else."),
                Choice("Choose the path of unity.", MemoryType.TRUST, 10, consequence_text="You trust in the power of togetherness.")
            ],
            audio_track="audio4.mp3",
            ambient_sound="glass_chimes.mp3",
            lighting="bright",
            camera_effect="zoom"
        )
        
        # Scene 9 - The Creator's Chamber
        self.scenes[9] = Scene(
            scene_id=9,
            title="The Creator's Chamber",
            background="cutscene9.jpg",
            dialogues=[
                Dialogue("Narrator", "Deep within the ruins lies a chamber that holds the answers she seeks.", 4.0),
                Dialogue("Creator", "Welcome, Rika. You have come far.", 3.0, emotion="wise")
            ],
            choices=[
                Choice("Ask about the world's destruction.", MemoryType.KINDNESS, 5, consequence_text="The Creator speaks of hope and renewal."),
                Choice("Demand answers about your past.", MemoryType.OBSESSION, 5, consequence_text="The Creator reveals your true purpose."),
                Choice("Seek the ultimate truth.", MemoryType.TRUTH, 5, consequence_text="The Creator shows you the cosmic truth."),
                Choice("Trust in the Creator's wisdom.", MemoryType.TRUST, 5, consequence_text="The Creator guides you to understanding.")
            ],
            audio_track="audio1.mp3",
            ambient_sound="wind_ruins.mp3",
            lighting="eerie",
            weather_effect="ash"
        )
        
        # Scene 10 - Into the Light
        self.scenes[10] = Scene(
            scene_id=10,
            title="Into the Light",
            background="cutscene10.jpg",
            dialogues=[
                Dialogue("Narrator", "The journey ends where it began, but everything has changed.", 4.0),
                Dialogue("Rika", "I understand now... the truth was always within me.", 3.0, emotion="peaceful")
            ],
            choices=[
                Choice("Embrace your new understanding.", MemoryType.KINDNESS, 5, consequence_text="You feel a deep sense of peace."),
                Choice("Commit to your chosen path.", MemoryType.OBSESSION, 5, consequence_text="You are resolved in your purpose."),
                Choice("Share the truth with others.", MemoryType.TRUTH, 5, consequence_text="You become a beacon of knowledge."),
                Choice("Build a new world together.", MemoryType.TRUST, 5, consequence_text="You and Penci create something beautiful.")
            ],
            audio_track="audio2.mp3",
            ambient_sound="machine_hum.mp3",
            lighting="bright",
            weather_effect="light"
        )
    
    def get_current_scene(self) -> Optional[Scene]:
        """Get the current scene"""
        return self.scenes.get(self.progress.current_scene)
    
    def make_choice(self, choice_index: int) -> Tuple[bool, str]:
        """Make a choice and update game state"""
        scene = self.get_current_scene()
        if not scene or choice_index < 0 or choice_index >= len(scene.choices):
            return False, "Invalid choice"
        
        choice = scene.choices[choice_index]
        timestamp = time.time()
        
        # Update memory values
        memory_key = choice.memory_type.value
        self.progress.memory_values[memory_key] += choice.memory_value
        
        # Track choice in analytics
        self.memory_analytics.track_choice(self.progress.current_scene, choice, timestamp)
        
        # Record choice
        self.progress.choices_made.append((self.progress.current_scene, choice_index))
        
        # Mark scene as watched
        if self.progress.current_scene not in self.progress.watched_cutscenes:
            self.progress.watched_cutscenes.append(self.progress.current_scene)
        
        # Move to next scene
        if choice.next_scene:
            self.progress.current_scene = choice.next_scene
        else:
            # Default progression
            if self.progress.current_scene < len(self.scenes):
                self.progress.current_scene += 1
            else:
                # Game completed
                self.progress.current_scene = 1  # Loop back to start
                self._handle_game_completion()
        
        # Update play time
        self.progress.play_time = time.time() - self.start_time
        
        # Auto-save
        self.save_manager.save_game(self.progress)
        
        return True, choice.consequence_text or f"Choice made: {choice.text}"
    
    def _handle_game_completion(self):
        """Handle game completion"""
        logger.info("Game completed! Calculating final results...")
        
        # Calculate final alignment
        final_alignment = self.memory_analytics.get_current_alignment(self.progress.memory_values)
        
        # Add completion achievement
        achievement = f"Completed the journey as {final_alignment}"
        if achievement not in self.progress.achievements:
            self.progress.achievements.append(achievement)
        
        # Log completion stats
        logger.info(f"Final alignment: {final_alignment}")
        logger.info(f"Total choices made: {len(self.progress.choices_made)}")
        logger.info(f"Play time: {self.progress.play_time:.1f} seconds")
        logger.info(f"Scenes watched: {len(self.progress.watched_cutscenes)}")
        
        # Save completion data
        self.save_manager.save_game(self.progress, 0)  # Save to slot 0 as completion save
    
    def get_memory_data(self) -> Dict[str, Any]:
        """Get comprehensive memory data"""
        percentages = self.get_memory_percentages()
        alignment = self.memory_analytics.get_current_alignment(self.progress.memory_values)
        insights = self.memory_analytics.get_memory_insights()
        
        return {
            "kindness": percentages["kindness"],
            "obsession": percentages["obsession"],
            "truth": percentages["truth"],
            "trust": percentages["trust"],
            "alignment": alignment,
            "insights": insights,
            "total_choices": len(self.progress.choices_made),
            "play_time": self.progress.play_time
        }
    
    def get_memory_percentages(self) -> Dict[str, float]:
        """Get memory values as percentages"""
        max_value = 100
        percentages = {}
        
        for memory_type in MemoryType:
            value = self.progress.memory_values.get(memory_type.value, 0)
            percentages[memory_type.value] = min((value / max_value) * 100, 100.0)
        
        return percentages
    
    def reset_game(self) -> bool:
        """Reset game to initial state"""
        self.progress = GameProgress(
            current_scene=1,
            current_act=1,
            watched_cutscenes=[],
            memory_values={
                MemoryType.KINDNESS.value: 0,
                MemoryType.OBSESSION.value: 0,
                MemoryType.TRUTH.value: 0,
                MemoryType.TRUST.value: 0
            }
        )
        
        self.memory_analytics = MemoryAnalytics()
        self.start_time = time.time()
        
        return self.save_manager.save_game(self.progress)
    
    def get_scene_data(self) -> Dict[str, Any]:
        """Get current scene data for GUI"""
        scene = self.get_current_scene()
        if not scene:
            return {}
        
        return {
            "scene_id": scene.scene_id,
            "title": scene.title,
            "background": scene.background,
            "dialogues": [
                {
                    "speaker": d.speaker,
                    "text": d.text,
                    "duration": d.duration,
                    "emotion": d.emotion
                }
                for d in scene.dialogues
            ],
            "choices": [
                {
                    "text": c.text,
                    "memory_type": c.memory_type.value,
                    "memory_value": c.memory_value,
                    "consequence_text": c.consequence_text
                }
                for c in scene.choices
            ],
            "audio_track": scene.audio_track,
            "ambient_sound": scene.ambient_sound,
            "lighting": scene.lighting,
            "weather_effect": scene.weather_effect,
            "camera_effect": scene.camera_effect
        }
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update game settings"""
        self.settings.update(new_settings)
        
        # Apply settings to subsystems
        if "volume" in new_settings:
            self.audio_manager.set_volume(new_settings["volume"])
        
        if "text_speed" in new_settings:
            self.dialogue_manager.typewriter_speed = new_settings["text_speed"]
        
        if "auto_advance" in new_settings:
            self.dialogue_manager.auto_advance = new_settings["auto_advance"]

def main():
    """Main function for testing the game engine"""
    engine = GameEngine()
    
    print("Into the Dark - Python Game Engine")
    print("=" * 50)
    
    while True:
        scene_data = engine.get_scene_data()
        if not scene_data:
            print("No scene data available")
            break
        
        print(f"\nScene {scene_data['scene_id']}: {scene_data['title']}")
        print(f"Background: {scene_data['background']}")
        
        # Display dialogues
        for dialogue in scene_data['dialogues']:
            print(f"\n{dialogue['speaker']}: {dialogue['text']}")
        
        # Display choices
        print("\nChoices:")
        for i, choice in enumerate(scene_data['choices']):
            print(f"{i + 1}. {choice['text']} (+{choice['memory_value']} {choice['memory_type']})")
        
        # Display memory data
        memory_data = engine.get_memory_data()
        print(f"\nMemory Values: {memory_data['alignment']}")
        print(f"Kindness: {memory_data['kindness']:.1f}%")
        print(f"Obsession: {memory_data['obsession']:.1f}%")
        print(f"Truth: {memory_data['truth']:.1f}%")
        print(f"Trust: {memory_data['trust']:.1f}%")
        
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
    
    print("\nGame session ended. Goodbye!")

if __name__ == "__main__":
    main()
