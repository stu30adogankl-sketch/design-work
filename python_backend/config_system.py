#!/usr/bin/env python3
"""
Into the Dark - Configuration System
Manages game settings, user preferences, and configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class GameConfig:
    """Game configuration data structure"""
    # Display settings
    resolution: tuple = (1920, 1080)
    fullscreen: bool = False
    vsync: bool = True
    fps_limit: int = 60
    
    # Audio settings
    master_volume: float = 0.7
    music_volume: float = 0.6
    sfx_volume: float = 0.8
    voice_volume: float = 0.9
    muted: bool = False
    
    # Gameplay settings
    text_speed: float = 0.05
    auto_advance: bool = True
    auto_advance_delay: float = 3.0
    skip_confirmation: bool = False
    
    # Language and localization
    language: str = "en"
    subtitles: bool = True
    subtitle_size: str = "medium"  # small, medium, large
    
    # Accessibility
    colorblind_mode: bool = False
    high_contrast: bool = False
    reduced_motion: bool = False
    
    # Advanced settings
    debug_mode: bool = False
    log_level: str = "INFO"
    auto_save: bool = True
    auto_save_interval: int = 300  # seconds
    
    # Graphics settings
    texture_quality: str = "high"  # low, medium, high, ultra
    shadow_quality: str = "medium"
    particle_effects: bool = True
    bloom_effect: bool = True
    
    # Input settings
    mouse_sensitivity: float = 1.0
    controller_enabled: bool = True
    keybindings: Dict[str, str] = None
    
    def __post_init__(self):
        if self.keybindings is None:
            self.keybindings = {
                "skip_dialogue": "SPACE",
                "open_menu": "ESC",
                "quick_save": "F5",
                "quick_load": "F9",
                "screenshot": "F12"
            }

class ConfigManager:
    """Manages game configuration and settings"""
    
    def __init__(self, config_path: str = "config/game_config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(exist_ok=True)
        self.config = GameConfig()
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                # Update config with loaded data
                for key, value in data.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
                
                logger.info(f"Configuration loaded from {self.config_path}")
                return True
            else:
                logger.info("No configuration file found, using defaults")
                self.save_config()
                return True
                
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            config_dict = asdict(self.config)
            
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def get_config(self) -> GameConfig:
        """Get current configuration"""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        try:
            for key, value in updates.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                else:
                    logger.warning(f"Unknown configuration key: {key}")
            
            return self.save_config()
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        try:
            self.config = GameConfig()
            return self.save_config()
            
        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")
            return False
    
    def get_display_settings(self) -> Dict[str, Any]:
        """Get display-related settings"""
        return {
            "resolution": self.config.resolution,
            "fullscreen": self.config.fullscreen,
            "vsync": self.config.vsync,
            "fps_limit": self.config.fps_limit,
            "texture_quality": self.config.texture_quality,
            "shadow_quality": self.config.shadow_quality,
            "particle_effects": self.config.particle_effects,
            "bloom_effect": self.config.bloom_effect
        }
    
    def get_audio_settings(self) -> Dict[str, Any]:
        """Get audio-related settings"""
        return {
            "master_volume": self.config.master_volume,
            "music_volume": self.config.music_volume,
            "sfx_volume": self.config.sfx_volume,
            "voice_volume": self.config.voice_volume,
            "muted": self.config.muted
        }
    
    def get_gameplay_settings(self) -> Dict[str, Any]:
        """Get gameplay-related settings"""
        return {
            "text_speed": self.config.text_speed,
            "auto_advance": self.config.auto_advance,
            "auto_advance_delay": self.config.auto_advance_delay,
            "skip_confirmation": self.config.skip_confirmation,
            "auto_save": self.config.auto_save,
            "auto_save_interval": self.config.auto_save_interval
        }
    
    def get_accessibility_settings(self) -> Dict[str, Any]:
        """Get accessibility-related settings"""
        return {
            "colorblind_mode": self.config.colorblind_mode,
            "high_contrast": self.config.high_contrast,
            "reduced_motion": self.config.reduced_motion,
            "subtitles": self.config.subtitles,
            "subtitle_size": self.config.subtitle_size
        }
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Validate resolution
        if not isinstance(self.config.resolution, (tuple, list)) or len(self.config.resolution) != 2:
            issues.append("Invalid resolution format")
        
        # Validate volume levels
        for volume_name in ["master_volume", "music_volume", "sfx_volume", "voice_volume"]:
            volume = getattr(self.config, volume_name)
            if not isinstance(volume, (int, float)) or volume < 0 or volume > 1:
                issues.append(f"Invalid {volume_name}: must be between 0 and 1")
        
        # Validate text speed
        if not isinstance(self.config.text_speed, (int, float)) or self.config.text_speed <= 0:
            issues.append("Invalid text_speed: must be positive number")
        
        # Validate language
        valid_languages = ["en", "es", "fr", "de", "ja", "zh"]
        if self.config.language not in valid_languages:
            issues.append(f"Unsupported language: {self.config.language}")
        
        return issues

class SettingsUI:
    """Settings UI helper for generating settings menus"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def get_settings_menu_data(self) -> Dict[str, Any]:
        """Get structured data for settings menu"""
        return {
            "display": {
                "title": "Display Settings",
                "settings": [
                    {
                        "key": "resolution",
                        "label": "Resolution",
                        "type": "select",
                        "options": [(1920, 1080), (1600, 900), (1366, 768), (1280, 720)],
                        "current": self.config_manager.config.resolution
                    },
                    {
                        "key": "fullscreen",
                        "label": "Fullscreen",
                        "type": "checkbox",
                        "current": self.config_manager.config.fullscreen
                    },
                    {
                        "key": "vsync",
                        "label": "VSync",
                        "type": "checkbox",
                        "current": self.config_manager.config.vsync
                    },
                    {
                        "key": "texture_quality",
                        "label": "Texture Quality",
                        "type": "select",
                        "options": ["low", "medium", "high", "ultra"],
                        "current": self.config_manager.config.texture_quality
                    }
                ]
            },
            "audio": {
                "title": "Audio Settings",
                "settings": [
                    {
                        "key": "master_volume",
                        "label": "Master Volume",
                        "type": "slider",
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                        "current": self.config_manager.config.master_volume
                    },
                    {
                        "key": "music_volume",
                        "label": "Music Volume",
                        "type": "slider",
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                        "current": self.config_manager.config.music_volume
                    },
                    {
                        "key": "sfx_volume",
                        "label": "Sound Effects Volume",
                        "type": "slider",
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                        "current": self.config_manager.config.sfx_volume
                    },
                    {
                        "key": "muted",
                        "label": "Mute All Audio",
                        "type": "checkbox",
                        "current": self.config_manager.config.muted
                    }
                ]
            },
            "gameplay": {
                "title": "Gameplay Settings",
                "settings": [
                    {
                        "key": "text_speed",
                        "label": "Text Speed",
                        "type": "slider",
                        "min": 0.01,
                        "max": 0.2,
                        "step": 0.01,
                        "current": self.config_manager.config.text_speed
                    },
                    {
                        "key": "auto_advance",
                        "label": "Auto Advance Dialogue",
                        "type": "checkbox",
                        "current": self.config_manager.config.auto_advance
                    },
                    {
                        "key": "auto_advance_delay",
                        "label": "Auto Advance Delay (seconds)",
                        "type": "slider",
                        "min": 1.0,
                        "max": 10.0,
                        "step": 0.5,
                        "current": self.config_manager.config.auto_advance_delay
                    },
                    {
                        "key": "language",
                        "label": "Language",
                        "type": "select",
                        "options": ["en", "es", "fr", "de", "ja", "zh"],
                        "current": self.config_manager.config.language
                    }
                ]
            },
            "accessibility": {
                "title": "Accessibility Settings",
                "settings": [
                    {
                        "key": "subtitles",
                        "label": "Show Subtitles",
                        "type": "checkbox",
                        "current": self.config_manager.config.subtitles
                    },
                    {
                        "key": "subtitle_size",
                        "label": "Subtitle Size",
                        "type": "select",
                        "options": ["small", "medium", "large"],
                        "current": self.config_manager.config.subtitle_size
                    },
                    {
                        "key": "colorblind_mode",
                        "label": "Colorblind Mode",
                        "type": "checkbox",
                        "current": self.config_manager.config.colorblind_mode
                    },
                    {
                        "key": "high_contrast",
                        "label": "High Contrast",
                        "type": "checkbox",
                        "current": self.config_manager.config.high_contrast
                    },
                    {
                        "key": "reduced_motion",
                        "label": "Reduce Motion",
                        "type": "checkbox",
                        "current": self.config_manager.config.reduced_motion
                    }
                ]
            }
        }

def main():
    """Test the configuration system"""
    config_manager = ConfigManager()
    
    print("Into the Dark - Configuration System Test")
    print("=" * 50)
    
    # Display current config
    config = config_manager.get_config()
    print(f"Resolution: {config.resolution}")
    print(f"Master Volume: {config.master_volume}")
    print(f"Text Speed: {config.text_speed}")
    print(f"Language: {config.language}")
    
    # Test validation
    issues = config_manager.validate_config()
    if issues:
        print(f"\nConfiguration Issues: {issues}")
    else:
        print("\nConfiguration is valid")
    
    # Test settings UI
    settings_ui = SettingsUI(config_manager)
    menu_data = settings_ui.get_settings_menu_data()
    print(f"\nSettings Menu Categories: {list(menu_data.keys())}")
    
    print("\nConfiguration system test completed!")

if __name__ == "__main__":
    main()
