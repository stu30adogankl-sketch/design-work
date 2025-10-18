#!/usr/bin/env python3
"""
Into the Dark - Audio System
Handles background music, sound effects, and voice acting
"""

import os
import threading
import time
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AudioType(Enum):
    """Audio type enumeration"""
    MUSIC = "music"
    SFX = "sfx"
    VOICE = "voice"
    AMBIENT = "ambient"

@dataclass
class AudioTrack:
    """Audio track data structure"""
    name: str
    file_path: str
    audio_type: AudioType
    duration: float
    loop: bool = False
    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0

class AudioManager:
    """Enhanced audio management system"""
    
    def __init__(self, audio_directory: str = "assets/audio"):
        self.audio_directory = Path(audio_directory)
        self.audio_directory.mkdir(exist_ok=True)
        
        # Audio settings
        self.master_volume = 0.7
        self.music_volume = 0.6
        self.sfx_volume = 0.8
        self.voice_volume = 0.9
        self.muted = False
        
        # Current audio state
        self.current_music: Optional[AudioTrack] = None
        self.current_ambient: Optional[AudioTrack] = None
        self.active_sfx: List[AudioTrack] = []
        self.active_voice: List[AudioTrack] = []
        
        # Audio library placeholder (would use pygame, pydub, or similar)
        self.audio_library_available = self._check_audio_library()
        
        # Audio tracks database
        self.audio_tracks: Dict[str, AudioTrack] = {}
        self._load_audio_tracks()
        
        # Callbacks for audio events
        self.on_music_start: Optional[Callable] = None
        self.on_music_end: Optional[Callable] = None
        self.on_sfx_play: Optional[Callable] = None
        
    def _check_audio_library(self) -> bool:
        """Check if audio library is available"""
        try:
            # Try to import pygame or other audio library
            import pygame
            pygame.mixer.init()
            logger.info("Audio library (pygame) initialized successfully")
            return True
        except ImportError:
            logger.warning("Audio library not available. Audio will be simulated.")
            return False
    
    def _load_audio_tracks(self):
        """Load available audio tracks"""
        # Background music tracks
        self.audio_tracks["main_theme"] = AudioTrack(
            "Main Theme", "audio1.mp3", AudioType.MUSIC, 30.0, True, 0.8
        )
        self.audio_tracks["machine_hum"] = AudioTrack(
            "Machine Hum", "audio2.mp3", AudioType.MUSIC, 30.0, True, 0.6
        )
        self.audio_tracks["companion_theme"] = AudioTrack(
            "Companion Theme", "audio3.mp3", AudioType.MUSIC, 30.0, True, 0.7
        )
        self.audio_tracks["memory_echo"] = AudioTrack(
            "Memory Echo", "audio4.mp3", AudioType.MUSIC, 30.0, True, 0.5
        )
        
        # Sound effects
        self.audio_tracks["choice_select"] = AudioTrack(
            "Choice Select", "sfx_choice.mp3", AudioType.SFX, 0.5, False, 0.7
        )
        self.audio_tracks["page_turn"] = AudioTrack(
            "Page Turn", "sfx_page.mp3", AudioType.SFX, 0.3, False, 0.6
        )
        self.audio_tracks["footstep"] = AudioTrack(
            "Footstep", "sfx_footstep.mp3", AudioType.SFX, 0.4, False, 0.5
        )
        self.audio_tracks["wind"] = AudioTrack(
            "Wind", "sfx_wind.mp3", AudioType.AMBIENT, 10.0, True, 0.4
        )
        self.audio_tracks["machine_hum_ambient"] = AudioTrack(
            "Machine Hum Ambient", "sfx_machine.mp3", AudioType.AMBIENT, 15.0, True, 0.3
        )
        
        # Voice acting (placeholder)
        self.audio_tracks["rika_voice"] = AudioTrack(
            "Rika Voice", "voice_rika.mp3", AudioType.VOICE, 2.0, False, 0.9
        )
        self.audio_tracks["penci_voice"] = AudioTrack(
            "Penci Voice", "voice_penci.mp3", AudioType.VOICE, 2.0, False, 0.9
        )
    
    def play_music(self, track_name: str, fade_in: float = 1.0) -> bool:
        """Play background music"""
        if self.muted or track_name not in self.audio_tracks:
            return False
        
        track = self.audio_tracks[track_name]
        if track.audio_type != AudioType.MUSIC:
            logger.warning(f"Track {track_name} is not music")
            return False
        
        # Stop current music if playing
        if self.current_music:
            self.stop_music()
        
        self.current_music = track
        logger.info(f"Playing music: {track.name}")
        
        if self.audio_library_available:
            # Real audio implementation would go here
            pass
        else:
            # Simulate audio playback
            self._simulate_audio_playback(track)
        
        if self.on_music_start:
            self.on_music_start(track)
        
        return True
    
    def stop_music(self, fade_out: float = 1.0) -> bool:
        """Stop background music"""
        if not self.current_music:
            return False
        
        logger.info(f"Stopping music: {self.current_music.name}")
        
        if self.audio_library_available:
            # Real audio implementation would go here
            pass
        
        if self.on_music_end:
            self.on_music_end(self.current_music)
        
        self.current_music = None
        return True
    
    def play_sfx(self, track_name: str, volume: float = None) -> bool:
        """Play sound effect"""
        if self.muted or track_name not in self.audio_tracks:
            return False
        
        track = self.audio_tracks[track_name]
        if track.audio_type != AudioType.SFX:
            logger.warning(f"Track {track_name} is not a sound effect")
            return False
        
        # Set volume if specified
        if volume is not None:
            track.volume = volume
        
        logger.info(f"Playing SFX: {track.name}")
        
        if self.audio_library_available:
            # Real audio implementation would go here
            pass
        else:
            # Simulate audio playback
            self._simulate_audio_playback(track)
        
        if self.on_sfx_play:
            self.on_sfx_play(track)
        
        return True
    
    def play_ambient(self, track_name: str, loop: bool = True) -> bool:
        """Play ambient sound"""
        if self.muted or track_name not in self.audio_tracks:
            return False
        
        track = self.audio_tracks[track_name]
        if track.audio_type != AudioType.AMBIENT:
            logger.warning(f"Track {track_name} is not ambient")
            return False
        
        # Stop current ambient if playing
        if self.current_ambient:
            self.stop_ambient()
        
        track.loop = loop
        self.current_ambient = track
        
        logger.info(f"Playing ambient: {track.name}")
        
        if self.audio_library_available:
            # Real audio implementation would go here
            pass
        else:
            # Simulate audio playback
            self._simulate_audio_playback(track)
        
        return True
    
    def stop_ambient(self) -> bool:
        """Stop ambient sound"""
        if not self.current_ambient:
            return False
        
        logger.info(f"Stopping ambient: {self.current_ambient.name}")
        self.current_ambient = None
        return True
    
    def play_voice(self, track_name: str, volume: float = None) -> bool:
        """Play voice acting"""
        if self.muted or track_name not in self.audio_tracks:
            return False
        
        track = self.audio_tracks[track_name]
        if track.audio_type != AudioType.VOICE:
            logger.warning(f"Track {track_name} is not voice")
            return False
        
        # Set volume if specified
        if volume is not None:
            track.volume = volume
        
        logger.info(f"Playing voice: {track.name}")
        
        if self.audio_library_available:
            # Real audio implementation would go here
            pass
        else:
            # Simulate audio playback
            self._simulate_audio_playback(track)
        
        return True
    
    def _simulate_audio_playback(self, track: AudioTrack):
        """Simulate audio playback when audio library is not available"""
        def playback():
            logger.info(f"[SIMULATED] Playing {track.name} for {track.duration}s")
            time.sleep(track.duration)
            logger.info(f"[SIMULATED] Finished playing {track.name}")
        
        thread = threading.Thread(target=playback)
        thread.daemon = True
        thread.start()
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        logger.info(f"Master volume set to {self.master_volume}")
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        logger.info(f"Music volume set to {self.music_volume}")
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        logger.info(f"SFX volume set to {self.sfx_volume}")
    
    def set_voice_volume(self, volume: float):
        """Set voice volume (0.0 to 1.0)"""
        self.voice_volume = max(0.0, min(1.0, volume))
        logger.info(f"Voice volume set to {self.voice_volume}")
    
    def toggle_mute(self) -> bool:
        """Toggle audio mute"""
        self.muted = not self.muted
        logger.info(f"Audio {'muted' if self.muted else 'unmuted'}")
        return self.muted
    
    def get_audio_status(self) -> Dict[str, Any]:
        """Get current audio status"""
        return {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "voice_volume": self.voice_volume,
            "muted": self.muted,
            "current_music": self.current_music.name if self.current_music else None,
            "current_ambient": self.current_ambient.name if self.current_ambient else None,
            "active_sfx_count": len(self.active_sfx),
            "active_voice_count": len(self.active_voice),
            "audio_library_available": self.audio_library_available
        }
    
    def get_available_tracks(self) -> Dict[str, List[str]]:
        """Get list of available audio tracks by type"""
        tracks_by_type = {
            AudioType.MUSIC.value: [],
            AudioType.SFX.value: [],
            AudioType.VOICE.value: [],
            AudioType.AMBIENT.value: []
        }
        
        for track_name, track in self.audio_tracks.items():
            tracks_by_type[track.audio_type.value].append(track_name)
        
        return tracks_by_type
    
    def fade_out_music(self, duration: float = 2.0):
        """Fade out current music"""
        if not self.current_music:
            return
        
        logger.info(f"Fading out music over {duration} seconds")
        # Implementation would handle gradual volume reduction
        time.sleep(duration)  # Simulate fade
        self.stop_music()
    
    def fade_in_music(self, track_name: str, duration: float = 2.0):
        """Fade in music"""
        logger.info(f"Fading in music over {duration} seconds")
        # Implementation would handle gradual volume increase
        time.sleep(duration)  # Simulate fade
        self.play_music(track_name)

class AudioEventManager:
    """Manages audio events and triggers"""
    
    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.event_triggers: Dict[str, List[str]] = {}
        self._setup_default_triggers()
    
    def _setup_default_triggers(self):
        """Setup default audio event triggers"""
        self.event_triggers = {
            "scene_start": ["main_theme"],
            "scene_end": [],
            "choice_made": ["choice_select"],
            "dialogue_advance": ["page_turn"],
            "memory_update": [],
            "game_start": ["main_theme"],
            "game_end": [],
            "menu_open": [],
            "menu_close": [],
            "save_game": [],
            "load_game": []
        }
    
    def trigger_event(self, event_name: str):
        """Trigger audio event"""
        if event_name not in self.event_triggers:
            logger.warning(f"Unknown audio event: {event_name}")
            return
        
        tracks = self.event_triggers[event_name]
        for track_name in tracks:
            if track_name in self.audio_manager.audio_tracks:
                track = self.audio_manager.audio_tracks[track_name]
                
                if track.audio_type == AudioType.MUSIC:
                    self.audio_manager.play_music(track_name)
                elif track.audio_type == AudioType.SFX:
                    self.audio_manager.play_sfx(track_name)
                elif track.audio_type == AudioType.AMBIENT:
                    self.audio_manager.play_ambient(track_name)
                elif track.audio_type == AudioType.VOICE:
                    self.audio_manager.play_voice(track_name)
    
    def add_event_trigger(self, event_name: str, track_names: List[str]):
        """Add or update event trigger"""
        self.event_triggers[event_name] = track_names
        logger.info(f"Added audio trigger for event '{event_name}': {track_names}")
    
    def remove_event_trigger(self, event_name: str):
        """Remove event trigger"""
        if event_name in self.event_triggers:
            del self.event_triggers[event_name]
            logger.info(f"Removed audio trigger for event '{event_name}'")

def main():
    """Test the audio system"""
    audio_manager = AudioManager()
    event_manager = AudioEventManager(audio_manager)
    
    print("Into the Dark - Audio System Test")
    print("=" * 40)
    
    # Test audio status
    status = audio_manager.get_audio_status()
    print(f"Master Volume: {status['master_volume']}")
    print(f"Muted: {status['muted']}")
    print(f"Audio Library Available: {status['audio_library_available']}")
    
    # Test available tracks
    tracks = audio_manager.get_available_tracks()
    print(f"\nAvailable Tracks:")
    for track_type, track_list in tracks.items():
        print(f"  {track_type}: {len(track_list)} tracks")
    
    # Test music playback
    print(f"\nTesting music playback...")
    audio_manager.play_music("main_theme")
    time.sleep(2)
    
    # Test SFX
    print(f"Testing SFX...")
    audio_manager.play_sfx("choice_select")
    time.sleep(1)
    
    # Test ambient
    print(f"Testing ambient...")
    audio_manager.play_ambient("wind")
    time.sleep(2)
    
    # Test event triggers
    print(f"\nTesting event triggers...")
    event_manager.trigger_event("choice_made")
    time.sleep(1)
    
    # Test volume controls
    print(f"\nTesting volume controls...")
    audio_manager.set_master_volume(0.5)
    audio_manager.toggle_mute()
    audio_manager.toggle_mute()
    
    print("\nAudio system test completed!")

if __name__ == "__main__":
    main()
