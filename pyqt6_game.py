#!/usr/bin/env python3
"""
Into the Dark - Complete PyQt6 Game
Professional cinematic narrative game with proper story and mechanics
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# Handle PyInstaller bundled assets
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QFrame, QStackedWidget,
    QMessageBox, QToolTip, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize,
    pyqtSignal, QThread, QObject, QParallelAnimationGroup
)
from PyQt6.QtGui import (
    QPixmap, QPainter, QFont, QColor, QPalette, QBrush, QPen,
    QLinearGradient, QRadialGradient, QMovie, QIcon
)

class GameEngine(QObject):
    """Complete game engine with proper story"""
    
    sceneChanged = pyqtSignal(dict)
    memoryUpdated = pyqtSignal(dict)
    gameCompleted = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_scene = 1
        self.memory_values = {
            "kindness": 0,
            "obsession": 0,
            "truth": 0,
            "trust": 0
        }
        self.scenes = self._load_scenes()
        
    def _load_scenes(self):
        """Load complete story scenes"""
        return {
            1: {
                "title": "The Ashborn",
                "background": "cutscene1.jpg",
                "dialogue": "The world ended not with a bang, but with a whisper. Rika opens her eyes to find herself among the skeletal remains of what once was civilization. Red ash drifts through the air like snow, carrying with it the echoes of a thousand lost voices. The ruins stretch endlessly in every direction, monuments to humanity's final failure. But Rika is alive, and where there is life, there is hope.",
                "choices": [
                    {
                        "text": "Call out",
                        "memory_type": "kindness",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Rika's voice trembles, gentle and warm: 'Is anyone… still out there?'",
                            "obsession": "She shouts, demanding answers from the silent ruins.",
                            "truth": "She calls softly, listening for the echoes to reveal hidden truths.",
                            "trust": "She whispers Penci's name, hoping he's nearby.",
                            "mixed": "Rika calls out, her voice hopeful yet demanding, scanning every shadow for a sign."
                        }
                    },
                    {
                        "text": "Stay silent",
                        "memory_type": "obsession",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She watches the ruins, waiting patiently for signs of life.",
                            "obsession": "Her eyes scan every crack, analyzing the ruins for hidden secrets.",
                            "truth": "Rika listens intently, hoping the silence itself speaks.",
                            "trust": "She pauses, trusting that Penci or someone else will find her first.",
                            "mixed": "She studies the ruins silently, recording every anomaly in her mind."
                        }
                    },
                    {
                        "text": "Touch the mirror shard",
                        "memory_type": "truth",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She gently touches the shard, feeling a strange warmth.",
                            "obsession": "Her fingers trace the cracks, searching for hidden information.",
                            "truth": "The shard reflects more than her image; she studies its secrets.",
                            "trust": "She hesitates, hoping touching it won't trigger danger.",
                            "mixed": "Rika examines the shard obsessively, noting patterns and distortions."
                        }
                    },
                    {
                        "text": "Scan surroundings",
                        "memory_type": "trust",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She looks around, careful not to disturb anything fragile.",
                            "obsession": "Her eyes dart to every detail, cataloging every ruin meticulously.",
                            "truth": "She studies the environment for clues, reading every anomaly.",
                            "trust": "She cautiously scans, trusting her instincts to guide her safely.",
                            "mixed": "She moves slowly, scanning every shadow while relying on intuition."
                        }
                    }
                ]
            },
            2: {
                "title": "Echoes of the Machine",
                "background": "cutscene2.jpg",
                "dialogue": "Deep within the ruins, ancient machines still pulse with dying energy. Their screens flicker with fragments of data, whispers of a world that once was. Rika approaches cautiously, drawn by the ghostly glow. The terminals seem to recognize her, displaying fragments of her name, her past, her very essence. But are these machines friend or foe? Do they offer salvation or damnation?",
                "choices": [
                    {
                        "text": "Speak to terminals",
                        "memory_type": "kindness",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Rika greets the machines softly, hoping for guidance.",
                            "obsession": "She interrogates the terminals, demanding answers.",
                            "truth": "She deciphers every flicker, searching for hidden patterns.",
                            "trust": "She calls for Penci to assist in understanding them.",
                            "mixed": "She meticulously decodes each message, ignoring fear."
                        }
                    },
                    {
                        "text": "Ignore terminals",
                        "memory_type": "obsession",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She walks past without disturbing them, respecting their silence.",
                            "obsession": "She ignores them, but her mind keeps returning to their patterns.",
                            "truth": "She focuses on the path ahead, leaving the messages for later analysis.",
                            "trust": "She trusts Penci will investigate while she moves forward.",
                            "mixed": "She avoids the terminals, confident someone else will handle them."
                        }
                    },
                    {
                        "text": "Decode messages",
                        "memory_type": "truth",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She gently taps the keys, hoping to understand without breaking them.",
                            "obsession": "Her fingers fly over buttons, eager to extract every secret.",
                            "truth": "She focuses entirely on decoding, ignoring the world around her.",
                            "trust": "She consults Penci, sharing the effort.",
                            "mixed": "She deciphers cautiously, careful not to destroy what she discovers."
                        }
                    },
                    {
                        "text": "Call for Penci",
                        "memory_type": "trust",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Her voice carries warmth and relief as she seeks her friend.",
                            "obsession": "She calls, demanding Penci's presence to validate her discoveries.",
                            "truth": "She calls, needing confirmation of the patterns she observes.",
                            "trust": "She trusts he will answer and come quickly.",
                            "mixed": "She calls, half commanding, half hoping he listens."
                        }
                    }
                ]
            },
            3: {
                "title": "The Companion Appears",
                "background": "cutscene3.jpg",
                "dialogue": "From the shadows emerges a figure Rika thought she'd never see again. Penci Zorno, her oldest friend, steps into the light carrying a broken lantern that still flickers with stubborn hope. His eyes hold the weight of the world's end, but also the promise of new beginnings. In this desolate landscape, their reunion is a beacon of light against the darkness. Together, they might just have a chance to survive whatever comes next.",
                "choices": [
                    {
                        "text": "Move cautiously together",
                        "memory_type": "kindness",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Rika nods gently; together they move with care.",
                            "obsession": "She leads, scrutinizing every path while Penci follows.",
                            "truth": "They analyze each step, measuring risk and clues.",
                            "trust": "She trusts him to cover her back.",
                            "mixed": "They move together, careful yet hopeful."
                        }
                    },
                    {
                        "text": "Lead the way alone",
                        "memory_type": "obsession",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Rika glances back, worried for Penci, but presses forward.",
                            "obsession": "She advances relentlessly, eyes fixed on secrets ahead.",
                            "truth": "Every detail guides her path; she cannot wait.",
                            "trust": "She hopes Penci can follow safely.",
                            "mixed": "She charges ahead, analyzing every shadow and corner."
                        }
                    },
                    {
                        "text": "Talk about ruins",
                        "memory_type": "truth",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She asks softly, caring for Penci's thoughts.",
                            "obsession": "She presses him for every detail of the ruins.",
                            "truth": "She questions carefully, trying to piece together reality.",
                            "trust": "She shares thoughts openly, trusting him to be honest.",
                            "mixed": "They exchange insights, cautious but sincere."
                        }
                    },
                    {
                        "text": "Examine ruins first",
                        "memory_type": "trust",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "Rika examines carefully, mindful of Penci's safety.",
                            "obsession": "Her focus narrows to every fragment, ignoring all else.",
                            "truth": "She studies anomalies, seeking hidden patterns.",
                            "trust": "She hopes Penci follows her lead wisely.",
                            "mixed": "She examines relentlessly, confident he'll support her."
                        }
                    }
                ]
            },
            4: {
                "title": "The Mirror of Memory",
                "background": "cutscene4.jpg",
                "dialogue": "In the heart of the ruins, Rika discovers a massive mirror, its surface cracked and distorted by time. But this is no ordinary mirror - it shows not her reflection, but glimpses of the past, fragments of memories that may not even be her own. The images shift and change, showing moments of joy, sorrow, triumph, and loss. The mirror seems to hold the key to understanding what happened to the world, but at what cost?",
                "choices": [
                    {
                        "text": "Touch the mirror",
                        "memory_type": "truth",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She touches the mirror gently, hoping to understand without causing harm.",
                            "obsession": "She presses her hand against the glass, desperate to unlock its secrets.",
                            "truth": "She studies the mirror's surface, analyzing every crack and distortion for meaning.",
                            "trust": "She hesitates, hoping Penci's presence will protect her from whatever lies within.",
                            "mixed": "She approaches cautiously, torn between curiosity and caution."
                        }
                    },
                    {
                        "text": "Step back and observe",
                        "memory_type": "obsession",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She watches from a distance, respecting the mirror's mysterious power.",
                            "obsession": "She studies every detail, cataloging the shifting images for later analysis.",
                            "truth": "She observes the patterns, trying to understand the mirror's true nature.",
                            "trust": "She waits for Penci's guidance before making any decisions.",
                            "mixed": "She watches intently, balancing observation with caution."
                        }
                    },
                    {
                        "text": "Speak to the reflection",
                        "memory_type": "kindness",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She addresses the mirror with warmth, hoping for a gentle response.",
                            "obsession": "She demands answers from the reflection, refusing to be ignored.",
                            "truth": "She questions the mirror directly, seeking honest answers.",
                            "trust": "She speaks softly, trusting that the mirror will respond in kind.",
                            "mixed": "She speaks with both hope and determination, seeking understanding."
                        }
                    },
                    {
                        "text": "Ignore and move forward",
                        "memory_type": "trust",
                        "memory_value": 5,
                        "responses": {
                            "kindness": "She turns away gently, not wanting to disturb whatever sleeps within.",
                            "obsession": "She forces herself to move on, though the mirror's secrets haunt her.",
                            "truth": "She decides the mirror's mysteries are not worth the risk.",
                            "trust": "She trusts her instincts to guide her away from potential danger.",
                            "mixed": "She moves on reluctantly, torn between curiosity and wisdom."
                        }
                    }
                ]
            },
            5: {
                "title": "The Creator's Chamber",
                "background": "cutscene5.jpg",
                "dialogue": "At last, Rika and Penci reach the heart of the mystery - a vast chamber that seems to exist outside of time itself. Here, they find the Creator, a being of immense power who watches them with ancient eyes. The Creator speaks of cycles and patterns, of worlds that rise and fall, of the eternal dance between creation and destruction. Rika realizes that her journey has been a test, and now she must make the ultimate choice that will determine not just her fate, but the fate of all existence.",
                "choices": [
                    {
                        "text": "Accept the Creator's offer",
                        "memory_type": "trust",
                        "memory_value": 10,
                        "responses": {
                            "kindness": "She accepts with grace, hoping to bring compassion to the cycle of creation.",
                            "obsession": "She accepts eagerly, driven by the desire to understand all mysteries.",
                            "truth": "She accepts with understanding, ready to bear the weight of ultimate knowledge.",
                            "trust": "She accepts with faith, trusting in the Creator's wisdom.",
                            "mixed": "She accepts with both hope and trepidation, ready for whatever comes next."
                        }
                    },
                    {
                        "text": "Reject the Creator's offer",
                        "memory_type": "kindness",
                        "memory_value": 10,
                        "responses": {
                            "kindness": "She rejects with gentle firmness, choosing to preserve the world as it is.",
                            "obsession": "She rejects with defiance, refusing to be part of any predetermined cycle.",
                            "truth": "She rejects with understanding, choosing her own path over destiny.",
                            "trust": "She rejects with faith in her own choices and Penci's support.",
                            "mixed": "She rejects with both sadness and determination, forging her own way."
                        }
                    },
                    {
                        "text": "Challenge the Creator",
                        "memory_type": "obsession",
                        "memory_value": 10,
                        "responses": {
                            "kindness": "She challenges with compassion, hoping to change the Creator's heart.",
                            "obsession": "She challenges with fierce determination, refusing to accept the status quo.",
                            "truth": "She challenges with logic, seeking to understand the Creator's true nature.",
                            "trust": "She challenges with confidence, trusting in her own strength and Penci's support.",
                            "mixed": "She challenges with both passion and wisdom, ready to fight for what she believes."
                        }
                    },
                    {
                        "text": "Seek a third option",
                        "memory_type": "truth",
                        "memory_value": 10,
                        "responses": {
                            "kindness": "She seeks a path of compromise, hoping to find a way that serves all.",
                            "obsession": "She seeks a solution that breaks the cycle entirely, driven by her need for change.",
                            "truth": "She seeks understanding, wanting to know all options before deciding.",
                            "trust": "She seeks guidance, hoping the Creator will reveal a hidden path.",
                            "mixed": "She seeks with both determination and openness, ready to find a new way forward."
                        }
                    }
                ]
            }
        }
    
    def get_scene_data(self) -> Dict[str, Any]:
        """Get current scene data"""
        scene = self.scenes.get(self.current_scene, {})
        return {
            "scene_id": self.current_scene,
            "title": scene.get("title", ""),
            "background": scene.get("background", ""),
            "dialogue": scene.get("dialogue", ""),
            "choices": scene.get("choices", []),
            "memory_data": self.get_memory_data()
        }
    
    def get_memory_data(self) -> Dict[str, Any]:
        """Get memory data"""
        total = sum(self.memory_values.values())
        if total == 0:
            alignment = "Neutral"
        else:
            dominant = max(self.memory_values.items(), key=lambda x: x[1])
            alignment_map = {
                "kindness": "Kind",
                "obsession": "Obsessed",
                "truth": "Truth-Seeker",
                "trust": "Trusting"
            }
            alignment = alignment_map.get(dominant[0], "Balanced")
        
        return {
            "kindness": self.memory_values["kindness"],
            "obsession": self.memory_values["obsession"],
            "truth": self.memory_values["truth"],
            "trust": self.memory_values["trust"],
            "alignment": alignment
        }
    
    def make_choice(self, choice_index: int) -> bool:
        """Make a choice"""
        scene = self.scenes.get(self.current_scene)
        if not scene or choice_index >= len(scene["choices"]):
            return False
        
        choice = scene["choices"][choice_index]
        
        # Check if this is a "Play Again" choice
        if choice.get("is_play_again", False):
            self.reset_game()
            return True
        
        # Update memory
        memory_type = choice["memory_type"]
        self.memory_values[memory_type] += choice["memory_value"]
        
        # Get response based on current alignment
        memory_data = self.get_memory_data()
        alignment = memory_data["alignment"].lower()
        
        responses = choice.get("responses", {})
        response = responses.get(alignment, responses.get("mixed", "Choice made."))
        
        # Move to next scene or end game
        self.current_scene += 1
        if self.current_scene > len(self.scenes):
            # Game completed - show ending
            self.show_ending()
            return True
        
        # Emit signals
        self.sceneChanged.emit(self.get_scene_data())
        self.memoryUpdated.emit(self.get_memory_data())
        
        return True
    
    def show_ending(self):
        """Show game ending based on alignment"""
        memory_data = self.get_memory_data()
        alignment = memory_data["alignment"]
        
        endings = {
            "Kind": {
                "title": "The Path of Compassion",
                "dialogue": "Rika's kindness has illuminated the darkness. She and Penci escape the ruins, carrying hope for a better world. Though mysteries remain, their bond proves that compassion can overcome even the greatest darkness. The Creator watches from the shadows, moved by their humanity.",
                "background": "ending_kind.jpg"
            },
            "Obsessed": {
                "title": "The Truth Unveiled", 
                "dialogue": "Rika's obsession has led her to the ultimate truth. She discovers the Creator's secret: the world was never real, but a test of human nature. Knowledge comes at a price - she must choose between revealing the truth or preserving the illusion that gives others hope. The weight of this knowledge will define her forever.",
                "background": "ending_obsessed.jpg"
            },
            "Truth-Seeker": {
                "title": "The Final Revelation",
                "dialogue": "Rika's quest for truth has reached its conclusion. She stands before the Creator, who reveals that she herself is the key to rebuilding the world. The choice is hers: accept her destiny as the new Creator or forge a path that rejects the cycle of destruction and creation entirely.",
                "background": "ending_truth.jpg"
            },
            "Trusting": {
                "title": "The Bond Unbroken",
                "dialogue": "Rika's trust in Penci has been her greatest strength. Together, they face the Creator and refuse to be divided. Their unity becomes the foundation for a new world, built on trust and friendship. The Creator, impressed by their bond, offers them a chance to rebuild reality together.",
                "background": "ending_trust.jpg"
            },
            "Neutral": {
                "title": "The Balanced Path",
                "dialogue": "Rika's balanced approach has led her to a unique conclusion. She neither embraces nor rejects the Creator's world, but instead creates her own reality. In the end, she learns that the greatest truth is that there is no single truth - only the choices we make and the consequences we accept.",
                "background": "ending_neutral.jpg"
            }
        }
        
        ending = endings.get(alignment, endings["Neutral"])
        
        # Create ending scene
        ending_scene = {
            "scene_id": 999,
            "title": ending["title"],
            "background": ending["background"],
            "dialogue": ending["dialogue"],
            "choices": [
                {
                    "text": "Play Again",
                    "memory_type": "kindness",
                    "memory_value": 0,
                    "responses": {"kindness": "Starting a new journey..."},
                    "is_play_again": True
                }
            ],
            "is_ending": True
        }
        
        self.scenes[999] = ending_scene
        self.current_scene = 999
        self.sceneChanged.emit(self.get_scene_data())
    
    def reset_game(self):
        """Reset the game to the beginning"""
        self.current_scene = 1
        self.memory_values = {
            "kindness": 0,
            "obsession": 0,
            "truth": 0,
            "trust": 0
        }
        # Remove ending scene if it exists
        if 999 in self.scenes:
            del self.scenes[999]
        # Emit signals to update UI
        self.sceneChanged.emit(self.get_scene_data())
        self.memoryUpdated.emit(self.get_memory_data())

class TypewriterEffect(QObject):
    """Typewriter effect for dialogue"""
    
    textUpdated = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.current_text = ""
        self.target_text = ""
        self.current_index = 0
        self.speed = 30  # milliseconds per character
        
    def start_typing(self, text: str, speed: int = 30):
        """Start typewriter effect"""
        self.target_text = text
        self.current_text = ""
        self.current_index = 0
        self.speed = speed
        self.timer.start(self.speed)
    
    def update_text(self):
        """Update text character by character"""
        if self.current_index < len(self.target_text):
            self.current_text += self.target_text[self.current_index]
            self.textUpdated.emit(self.current_text)
            self.current_index += 1
        else:
            self.timer.stop()
            self.finished.emit()
    
    def skip_typing(self):
        """Skip to full text immediately"""
        self.timer.stop()
        self.current_text = self.target_text
        self.textUpdated.emit(self.current_text)
        self.finished.emit()

class CutsceneWidget(QGraphicsView):
    """High-quality cutscene display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Setup graphics view
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background: black; border: none;")
        
        # Fade effect
        self.fade_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(1500)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    def set_cutscene(self, image_path: str):
        """Set cutscene image"""
        # Use resource_path for bundled assets
        full_path = resource_path(image_path)
        pixmap = QPixmap(full_path)
        
        if pixmap.isNull():
            # Create high-quality placeholder
            pixmap = QPixmap(1920, 1080)
            pixmap.fill(QColor(20, 20, 20))
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Gradient background
            gradient = QLinearGradient(0, 0, 1920, 1080)
            gradient.setColorAt(0, QColor(40, 20, 20))
            gradient.setColorAt(1, QColor(20, 40, 20))
            painter.fillRect(pixmap.rect(), gradient)
            
            # Title text
            painter.setPen(QPen(QColor(200, 200, 200), 2))
            painter.setFont(QFont("Arial", 48, QFont.Weight.Bold))
            title = Path(image_path).stem.replace("cutscene", "Scene ").title()
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, title)
            
            painter.end()
        
        # Scale to fit widget while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Clear previous scene
        self.scene.clear()
        
        # Add new pixmap
        self.pixmap_item = self.scene.addPixmap(scaled_pixmap)
        self.scene.setSceneRect(scaled_pixmap.rect().toRectF())
        
        # Center the pixmap
        self.centerOn(scaled_pixmap.width() / 2, scaled_pixmap.height() / 2)
    
    def fade_in(self):
        """Fade in animation"""
        self.fade_effect.setOpacity(0.0)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

class DialogueBox(QFrame):
    """Professional dialogue display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.typewriter = TypewriterEffect()
        self.typewriter.textUpdated.connect(self.update_text)
        
    def setup_ui(self):
        """Setup dialogue box UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Title label
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            color: #FFD700;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        layout.addWidget(self.title_label)
        
        # Dialogue text
        self.text_label = QLabel()
        self.text_label.setStyleSheet("""
            color: #F0F0F0;
            font-size: 18px;
            line-height: 1.6;
        """)
        self.text_label.setWordWrap(True)
        self.text_label.setMinimumHeight(80)
        layout.addWidget(self.text_label)
        
        # Style the frame
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.85);
                border: 3px solid rgba(255, 215, 0, 0.3);
                border-radius: 15px;
                margin: 20px;
            }
        """)
        
        # Add shadow effect
        self.setGraphicsEffect(QGraphicsOpacityEffect())
    
    def set_dialogue(self, title: str, text: str):
        """Set dialogue with typewriter effect"""
        self.title_label.setText(title)
        self.typewriter.start_typing(text, 25)
    
    def update_text(self, text: str):
        """Update text during typewriter effect"""
        self.text_label.setText(text)
    
    def skip_typing(self):
        """Skip typewriter effect"""
        self.typewriter.skip_typing()

class ChoiceButton(QPushButton):
    """Professional choice button"""
    
    def __init__(self, text: str, alignment_type: str, parent=None):
        super().__init__(text, parent)
        self.alignment_type = alignment_type
        self.setup_style()
        
    def setup_style(self):
        """Setup button style"""
        colors = {
            "kindness": "#4A9EFF",    # Blue
            "obsession": "#FF6B6B",   # Red  
            "truth": "#FFD93D",       # Yellow
            "trust": "#6BCF7F"        # Green
        }
        
        color = colors.get(self.alignment_type, "#888888")
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: 3px solid {color};
                border-radius: 12px;
                padding: 20px 25px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
                border-color: {self.lighten_color(color)};
                font-size: 17px;
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
                border-color: {self.darken_color(color)};
            }}
        """)
    
    def lighten_color(self, color: str) -> str:
        """Lighten color for hover effect"""
        color_map = {
            "#4A9EFF": "#6BB6FF",
            "#FF6B6B": "#FF8A8A", 
            "#FFD93D": "#FFE066",
            "#6BCF7F": "#8DD99F"
        }
        return color_map.get(color, "#AAAAAA")
    
    def darken_color(self, color: str) -> str:
        """Darken color for pressed effect"""
        color_map = {
            "#4A9EFF": "#2A7ECC",
            "#FF6B6B": "#CC4A4A",
            "#FFD93D": "#CCB01A", 
            "#6BCF7F": "#4A9F5F"
        }
        return color_map.get(color, "#666666")

class MainWindow(QMainWindow):
    """Main game window - 1920x1080"""
    
    def __init__(self):
        super().__init__()
        self.game_engine = GameEngine()
        self.setup_ui()
        self.connect_signals()
        self.load_initial_scene()
        
    def setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("Into the Dark")
        self.setFixedSize(1920, 1080)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Cutscene (larger)
        self.cutscene_widget = CutsceneWidget()
        self.cutscene_widget.setFixedSize(1400, 1080)
        main_layout.addWidget(self.cutscene_widget)
        
        # Right side - UI panel
        ui_panel = QWidget()
        ui_panel.setFixedSize(520, 1080)
        ui_panel.setStyleSheet("background-color: rgba(0, 0, 0, 0.9);")
        
        ui_layout = QVBoxLayout(ui_panel)
        ui_layout.setContentsMargins(20, 20, 20, 20)
        ui_layout.setSpacing(20)
        
        # Dialogue box
        self.dialogue_box = DialogueBox()
        ui_layout.addWidget(self.dialogue_box)
        
        # Choice buttons
        self.choice_buttons = []
        for i in range(4):
            button = ChoiceButton(f"Choice {i+1}", "kindness")
            button.clicked.connect(lambda checked, idx=i: self.make_choice(idx))
            self.choice_buttons.append(button)
            ui_layout.addWidget(button)
        
        # Spacer
        ui_layout.addStretch()
        
        # Controls
        controls_layout = QHBoxLayout()
        
        reset_button = QPushButton("Reset Game")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: 2px solid #888;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        reset_button.clicked.connect(self.reset_game)
        controls_layout.addWidget(reset_button)
        
        ui_layout.addLayout(controls_layout)
        main_layout.addWidget(ui_panel)
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply professional dark theme"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(10, 10, 10))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
    
    def connect_signals(self):
        """Connect game engine signals"""
        self.game_engine.sceneChanged.connect(self.update_scene)
        self.game_engine.memoryUpdated.connect(self.update_memory)
    
    def load_initial_scene(self):
        """Load initial scene"""
        scene_data = self.game_engine.get_scene_data()
        self.update_scene(scene_data)
    
    def update_scene(self, scene_data: Dict[str, Any]):
        """Update scene display"""
        # Update cutscene
        background = scene_data.get("background", "")
        if background:
            image_path = f"assets/cutscenes/{background}"
            self.cutscene_widget.set_cutscene(image_path)
            self.cutscene_widget.fade_in()
        
        # Update dialogue
        title = scene_data.get("title", "")
        dialogue = scene_data.get("dialogue", "")
        if title and dialogue:
            self.dialogue_box.set_dialogue(title, dialogue)
        
        # Update choices
        choices = scene_data.get("choices", [])
        for i, button in enumerate(self.choice_buttons):
            if i < len(choices):
                choice = choices[i]
                button.setText(choice.get("text", f"Choice {i+1}"))
                button.alignment_type = choice.get("memory_type", "kindness")
                button.setup_style()
                button.setVisible(True)
            else:
                button.setVisible(False)
    
    def update_memory(self, memory_data: Dict[str, Any]):
        """Update memory (kept in backend)"""
        pass  # Memory tracking is internal
    
    def make_choice(self, choice_index: int):
        """Make a choice"""
        success = self.game_engine.make_choice(choice_index)
        if not success:
            QMessageBox.warning(self, "Error", "Failed to make choice")
    
    def reset_game(self):
        """Reset the game"""
        reply = QMessageBox.question(
            self, 
            "Reset Game", 
            "Are you sure you want to reset the game?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.game_engine = GameEngine()
            self.load_initial_scene()
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key.Key_Space:
            # Skip typewriter effect
            self.dialogue_box.skip_typing()
        else:
            super().keyPressEvent(event)

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Into the Dark")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Game Studio")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()