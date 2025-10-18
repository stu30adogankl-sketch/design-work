#!/usr/bin/env python3
"""
Into the Dark - PyQt6 GUI Application
Complete cinematic, retro-pixel-art game interface
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QFrame, QStackedWidget,
    QMessageBox, QToolTip, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize,
    pyqtSignal, QThread, QObject, QParallelAnimationGroup
)
from PyQt6.QtGui import (
    QPixmap, QPainter, QFont, QColor, QPalette, QBrush, QPen,
    QLinearGradient, QRadialGradient, QGraphicsOpacityEffect,
    QMovie, QIcon
)

class GameEngine(QObject):
    """Game engine interface for PyQt6"""
    
    sceneChanged = pyqtSignal(dict)
    memoryUpdated = pyqtSignal(dict)
    gameCompleted = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_scene = None
        self.memory_data = None
        
    def get_scene_data(self) -> Dict[str, Any]:
        """Get current scene data"""
        try:
            result = subprocess.run([
                "python3", "python_backend/cli_interface.py", "get_scene"
            ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {}
        except Exception as e:
            print(f"Error getting scene data: {e}")
            return {}
    
    def get_memory_data(self) -> Dict[str, Any]:
        """Get memory data"""
        try:
            result = subprocess.run([
                "python3", "python_backend/cli_interface.py", "get_memory"
            ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {}
        except Exception as e:
            print(f"Error getting memory data: {e}")
            return {}
    
    def make_choice(self, choice_index: int) -> bool:
        """Make a choice"""
        try:
            result = subprocess.run([
                "python3", "python_backend/cli_interface.py", "make_choice", str(choice_index)
            ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if result.returncode == 0:
                choice_result = json.loads(result.stdout)
                if choice_result.get("success", False):
                    # Emit signals for updates
                    self.sceneChanged.emit(self.get_scene_data())
                    self.memoryUpdated.emit(self.get_memory_data())
                    return True
            return False
        except Exception as e:
            print(f"Error making choice: {e}")
            return False
    
    def reset_game(self) -> bool:
        """Reset the game"""
        try:
            result = subprocess.run([
                "python3", "python_backend/cli_interface.py", "reset_game"
            ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if result.returncode == 0:
                reset_result = json.loads(result.stdout)
                if reset_result.get("success", False):
                    self.sceneChanged.emit(self.get_scene_data())
                    self.memoryUpdated.emit(self.get_memory_data())
                    return True
            return False
        except Exception as e:
            print(f"Error resetting game: {e}")
            return False

class TypewriterEffect(QObject):
    """Typewriter effect for dialogue text"""
    
    textUpdated = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.current_text = ""
        self.target_text = ""
        self.current_index = 0
        self.speed = 50  # milliseconds per character
        
    def start_typing(self, text: str, speed: int = 50):
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

class CRTOverlay(QWidget):
    """Retro CRT overlay effect"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
    def paintEvent(self, event):
        """Paint CRT scanlines and effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        # Scanlines effect
        painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
        for y in range(0, self.height(), 2):
            painter.drawLine(0, y, self.width(), y)
        
        # Subtle flicker effect
        import random
        if random.random() < 0.1:  # 10% chance of flicker
            painter.fillRect(self.rect(), QColor(255, 255, 255, 5))

class CutsceneWidget(QGraphicsView):
    """Cutscene display widget with effects"""
    
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
        self.fade_animation.setDuration(1000)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Current pixmap item
        self.pixmap_item = None
        
    def set_cutscene(self, image_path: str):
        """Set cutscene image"""
        pixmap = QPixmap(image_path)
        
        if pixmap.isNull():
            # Create placeholder if image doesn't exist
            pixmap = QPixmap(960, 540)
            pixmap.fill(QColor(40, 40, 40))
            
            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor(100, 100, 100), 2))
            painter.setFont(QFont("Arial", 24))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                           f"Cutscene: {Path(image_path).stem}\n(Placeholder)")
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
        self.scene.setSceneRect(scaled_pixmap.rect())
        
        # Center the pixmap
        self.centerOn(scaled_pixmap.width() / 2, scaled_pixmap.height() / 2)
    
    def fade_in(self):
        """Fade in animation"""
        self.fade_effect.setOpacity(0.0)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
    
    def fade_out(self):
        """Fade out animation"""
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()

class DialogueBox(QFrame):
    """Semi-transparent dialogue text box"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.typewriter = TypewriterEffect()
        self.typewriter.textUpdated.connect(self.update_text)
        
    def setup_ui(self):
        """Setup dialogue box UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Speaker label
        self.speaker_label = QLabel()
        self.speaker_label.setStyleSheet("""
            color: #E0E0E0;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        layout.addWidget(self.speaker_label)
        
        # Text label
        self.text_label = QLabel()
        self.text_label.setStyleSheet("""
            color: #F0F0F0;
            font-size: 14px;
            line-height: 1.4;
            word-wrap: true;
        """)
        self.text_label.setWordWrap(True)
        layout.addWidget(self.text_label)
        
        # Style the frame
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);
                border: 2px solid rgba(100, 100, 100, 0.5);
                border-radius: 10px;
                margin: 10px;
            }
        """)
        
        # Add shadow effect
        self.setGraphicsEffect(QGraphicsOpacityEffect())
    
    def set_dialogue(self, speaker: str, text: str):
        """Set dialogue with typewriter effect"""
        self.speaker_label.setText(speaker)
        self.typewriter.start_typing(text, 50)
    
    def update_text(self, text: str):
        """Update text during typewriter effect"""
        self.text_label.setText(text)
    
    def skip_typing(self):
        """Skip typewriter effect"""
        self.typewriter.skip_typing()

class ChoiceButton(QPushButton):
    """Styled choice button with hover effects"""
    
    def __init__(self, text: str, alignment_type: str, parent=None):
        super().__init__(text, parent)
        self.alignment_type = alignment_type
        self.setup_style()
        
    def setup_style(self):
        """Setup button style based on alignment type"""
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
                border: 2px solid {color};
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
                border-color: {self.lighten_color(color)};
                transform: scale(1.02);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
                border-color: {self.darken_color(color)};
            }}
        """)
    
    def lighten_color(self, color: str) -> str:
        """Lighten color for hover effect"""
        # Simple color lightening - in production, use proper color manipulation
        return color.replace("#", "#80")
    
    def darken_color(self, color: str) -> str:
        """Darken color for pressed effect"""
        # Simple color darkening - in production, use proper color manipulation
        return color.replace("#", "#40")

class MemoryBar(QWidget):
    """Dynamic memory alignment bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup memory bar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("Memory Alignment")
        title.setStyleSheet("""
            color: #E0E0E0;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Memory bars
        self.memory_bars = {}
        memory_types = [
            ("kindness", "Kindness", "#4A9EFF"),
            ("obsession", "Obsession", "#FF6B6B"),
            ("truth", "Truth", "#FFD93D"),
            ("trust", "Trust", "#6BCF7F")
        ]
        
        for memory_type, label, color in memory_types:
            # Label
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {color}; font-size: 12px; margin-bottom: 2px;")
            layout.addWidget(label_widget)
            
            # Progress bar
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #666;
                    border-radius: 3px;
                    text-align: center;
                    background-color: #333;
                    color: white;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 2px;
                }}
            """)
            layout.addWidget(bar)
            
            self.memory_bars[memory_type] = bar
        
        # Alignment label
        self.alignment_label = QLabel("Alignment: Neutral")
        self.alignment_label.setStyleSheet("""
            color: #E0E0E0;
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
        """)
        layout.addWidget(self.alignment_label)
        
        # Style the widget
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(42, 42, 42, 0.9);
                border: 1px solid #666;
                border-radius: 8px;
            }
        """)
        
        self.setFixedWidth(200)
    
    def update_memory(self, memory_data: Dict[str, Any]):
        """Update memory bars with animation"""
        # Update bars
        for memory_type, bar in self.memory_bars.items():
            value = int(memory_data.get(memory_type, 0))
            bar.setValue(value)
        
        # Update alignment
        alignment = memory_data.get("alignment", "Neutral")
        self.alignment_label.setText(f"Alignment: {alignment}")

class AudioManager(QObject):
    """Audio manager for PyQt6"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_track = None
        
    def play_track(self, track_name: str):
        """Play audio track"""
        # In a real implementation, this would use pygame or similar
        print(f"Playing audio track: {track_name}")
        self.current_track = track_name
    
    def stop_track(self):
        """Stop current track"""
        if self.current_track:
            print(f"Stopping audio track: {self.current_track}")
            self.current_track = None

class MainWindow(QMainWindow):
    """Main game window"""
    
    def __init__(self):
        super().__init__()
        self.game_engine = GameEngine()
        self.audio_manager = AudioManager()
        self.setup_ui()
        self.connect_signals()
        self.load_initial_scene()
        
    def setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("Into the Dark")
        self.setFixedSize(960, 540)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Game area
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Cutscene widget
        self.cutscene_widget = CutsceneWidget()
        self.cutscene_widget.setFixedSize(760, 540)
        left_layout.addWidget(self.cutscene_widget)
        
        # Bottom area for dialogue and choices
        bottom_widget = QWidget()
        bottom_widget.setFixedHeight(200)
        bottom_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.8);")
        
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(20, 20, 20, 20)
        
        # Dialogue box
        self.dialogue_box = DialogueBox()
        bottom_layout.addWidget(self.dialogue_box)
        
        # Choice buttons
        self.choice_buttons = []
        choices_layout = QHBoxLayout()
        for i in range(4):
            button = ChoiceButton(f"Choice {i+1}", "kindness")
            button.clicked.connect(lambda checked, idx=i: self.make_choice(idx))
            self.choice_buttons.append(button)
            choices_layout.addWidget(button)
        bottom_layout.addLayout(choices_layout)
        
        left_layout.addWidget(bottom_widget)
        main_layout.addLayout(left_layout)
        
        # Right side - Memory bar
        self.memory_bar = MemoryBar()
        main_layout.addWidget(self.memory_bar)
        
        # Add CRT overlay
        self.crt_overlay = CRTOverlay()
        self.crt_overlay.setParent(central_widget)
        self.crt_overlay.resize(960, 540)
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
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
        self.game_engine.gameCompleted.connect(self.handle_game_completion)
    
    def load_initial_scene(self):
        """Load initial scene"""
        scene_data = self.game_engine.get_scene_data()
        if scene_data:
            self.update_scene(scene_data)
        
        memory_data = self.game_engine.get_memory_data()
        if memory_data:
            self.update_memory(memory_data)
    
    def update_scene(self, scene_data: Dict[str, Any]):
        """Update scene display"""
        # Update cutscene
        background = scene_data.get("background", "")
        if background:
            image_path = f"assets/cutscenes/{background}"
            self.cutscene_widget.set_cutscene(image_path)
            self.cutscene_widget.fade_in()
        
        # Update dialogue
        dialogue = scene_data.get("dialogue", "")
        if dialogue:
            # Parse dialogue (simple implementation)
            lines = dialogue.split("\n\n")
            if lines:
                first_line = lines[0]
                if ": " in first_line:
                    speaker, text = first_line.split(": ", 1)
                    self.dialogue_box.set_dialogue(speaker, text)
                else:
                    self.dialogue_box.set_dialogue("Narrator", first_line)
        
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
        
        # Play audio
        audio_track = scene_data.get("audio_track", "")
        if audio_track:
            self.audio_manager.play_track(audio_track)
    
    def update_memory(self, memory_data: Dict[str, Any]):
        """Update memory bar"""
        self.memory_bar.update_memory(memory_data)
    
    def make_choice(self, choice_index: int):
        """Make a choice"""
        success = self.game_engine.make_choice(choice_index)
        if not success:
            QMessageBox.warning(self, "Error", "Failed to make choice")
    
    def handle_game_completion(self, completion_data: Dict[str, Any]):
        """Handle game completion"""
        alignment = completion_data.get("alignment", "Unknown")
        QMessageBox.information(
            self, 
            "Game Completed", 
            f"Congratulations! You completed the journey as: {alignment}"
        )
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key.Key_Space:
            # Skip typewriter effect
            self.dialogue_box.skip_typing()
        elif event.key() == Qt.Key.Key_R:
            # Reset game
            reply = QMessageBox.question(
                self, 
                "Reset Game", 
                "Are you sure you want to reset the game?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.game_engine.reset_game()
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
    
    # Start CRT overlay animation
    crt_timer = QTimer()
    crt_timer.timeout.connect(window.crt_overlay.update)
    crt_timer.start(100)  # Update every 100ms for flicker effect
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
