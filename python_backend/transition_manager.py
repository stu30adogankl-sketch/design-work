#!/usr/bin/env python3
"""
Into the Dark - Scene Transition Manager
Handles smooth transitions between scenes with various effects
"""

import time
import threading
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TransitionType(Enum):
    """Transition type enumeration"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    CROSSFADE = "crossfade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DISSOLVE = "dissolve"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    NONE = "none"

class TransitionState(Enum):
    """Transition state enumeration"""
    IDLE = "idle"
    PREPARING = "preparing"
    TRANSITIONING = "transitioning"
    COMPLETED = "completed"

@dataclass
class Transition:
    """Transition data structure"""
    transition_type: TransitionType
    duration: float
    easing: str = "linear"  # linear, ease_in, ease_out, ease_in_out
    delay: float = 0.0
    callback: Optional[Callable] = None
    parameters: Dict[str, Any] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class TransitionManager:
    """Manages scene transitions and animations"""
    
    def __init__(self):
        self.current_transition: Optional[Transition] = None
        self.transition_state = TransitionState.IDLE
        self.transition_queue: List[Transition] = []
        
        # Transition callbacks
        self.on_transition_start: Optional[Callable] = None
        self.on_transition_end: Optional[Callable] = None
        self.on_transition_progress: Optional[Callable] = None
        
        # Default transition settings
        self.default_duration = 1.0
        self.default_easing = "ease_in_out"
        
        # Transition registry
        self.transition_registry: Dict[TransitionType, Callable] = {}
        self._register_default_transitions()
        
        # Transition thread
        self.transition_thread: Optional[threading.Thread] = None
        self.stop_transition = False
    
    def _register_default_transitions(self):
        """Register default transition implementations"""
        self.transition_registry = {
            TransitionType.FADE_IN: self._fade_in_transition,
            TransitionType.FADE_OUT: self._fade_out_transition,
            TransitionType.CROSSFADE: self._crossfade_transition,
            TransitionType.SLIDE_LEFT: self._slide_left_transition,
            TransitionType.SLIDE_RIGHT: self._slide_right_transition,
            TransitionType.SLIDE_UP: self._slide_up_transition,
            TransitionType.SLIDE_DOWN: self._slide_down_transition,
            TransitionType.ZOOM_IN: self._zoom_in_transition,
            TransitionType.ZOOM_OUT: self._zoom_out_transition,
            TransitionType.DISSOLVE: self._dissolve_transition,
            TransitionType.WIPE_LEFT: self._wipe_left_transition,
            TransitionType.WIPE_RIGHT: self._wipe_right_transition,
            TransitionType.NONE: self._no_transition
        }
    
    def execute_transition(self, transition: Transition) -> bool:
        """Execute a transition"""
        if self.transition_state != TransitionState.IDLE:
            logger.warning("Transition already in progress, queuing...")
            self.transition_queue.append(transition)
            return False
        
        self.current_transition = transition
        self.transition_state = TransitionState.PREPARING
        self.stop_transition = False
        
        logger.info(f"Executing transition: {transition.transition_type.value}")
        
        # Start transition in separate thread
        self.transition_thread = threading.Thread(
            target=self._execute_transition_thread,
            args=(transition,)
        )
        self.transition_thread.daemon = True
        self.transition_thread.start()
        
        return True
    
    def _execute_transition_thread(self, transition: Transition):
        """Execute transition in separate thread"""
        try:
            # Apply delay if specified
            if transition.delay > 0:
                time.sleep(transition.delay)
            
            # Execute transition
            self.transition_state = TransitionState.TRANSITIONING
            
            if self.on_transition_start:
                self.on_transition_start(transition)
            
            # Get transition function
            transition_func = self.transition_registry.get(
                transition.transition_type, 
                self._no_transition
            )
            
            # Execute transition with progress callback
            transition_func(transition)
            
            # Transition completed
            self.transition_state = TransitionState.COMPLETED
            
            if self.on_transition_end:
                self.on_transition_end(transition)
            
            # Execute callback if provided
            if transition.callback:
                transition.callback()
            
            # Process next transition in queue
            self._process_next_transition()
            
        except Exception as e:
            logger.error(f"Transition execution failed: {e}")
            self.transition_state = TransitionState.IDLE
        
        finally:
            self.current_transition = None
            self.transition_state = TransitionState.IDLE
    
    def _process_next_transition(self):
        """Process next transition in queue"""
        if self.transition_queue:
            next_transition = self.transition_queue.pop(0)
            self.execute_transition(next_transition)
    
    def _fade_in_transition(self, transition: Transition):
        """Fade in transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            alpha = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"alpha": alpha})
            
            time.sleep(duration / steps)
    
    def _fade_out_transition(self, transition: Transition):
        """Fade out transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            alpha = 1.0 - self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"alpha": alpha})
            
            time.sleep(duration / steps)
    
    def _crossfade_transition(self, transition: Transition):
        """Crossfade transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            alpha_out = 1.0 - self._apply_easing(progress, transition.easing)
            alpha_in = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {
                    "alpha_out": alpha_out,
                    "alpha_in": alpha_in
                })
            
            time.sleep(duration / steps)
    
    def _slide_left_transition(self, transition: Transition):
        """Slide left transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            offset = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {
                    "offset_x": -offset,
                    "offset_y": 0
                })
            
            time.sleep(duration / steps)
    
    def _slide_right_transition(self, transition: Transition):
        """Slide right transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            offset = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {
                    "offset_x": offset,
                    "offset_y": 0
                })
            
            time.sleep(duration / steps)
    
    def _slide_up_transition(self, transition: Transition):
        """Slide up transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            offset = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {
                    "offset_x": 0,
                    "offset_y": -offset
                })
            
            time.sleep(duration / steps)
    
    def _slide_down_transition(self, transition: Transition):
        """Slide down transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            offset = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {
                    "offset_x": 0,
                    "offset_y": offset
                })
            
            time.sleep(duration / steps)
    
    def _zoom_in_transition(self, transition: Transition):
        """Zoom in transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            scale = 1.0 + self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"scale": scale})
            
            time.sleep(duration / steps)
    
    def _zoom_out_transition(self, transition: Transition):
        """Zoom out transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            scale = 1.0 - self._apply_easing(progress, transition.easing) * 0.5
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"scale": scale})
            
            time.sleep(duration / steps)
    
    def _dissolve_transition(self, transition: Transition):
        """Dissolve transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            noise = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"noise": noise})
            
            time.sleep(duration / steps)
    
    def _wipe_left_transition(self, transition: Transition):
        """Wipe left transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            wipe_position = self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"wipe_position": wipe_position})
            
            time.sleep(duration / steps)
    
    def _wipe_right_transition(self, transition: Transition):
        """Wipe right transition implementation"""
        duration = transition.duration
        steps = int(duration * 60)  # 60 FPS
        
        for i in range(steps + 1):
            if self.stop_transition:
                break
            
            progress = i / steps
            wipe_position = 1.0 - self._apply_easing(progress, transition.easing)
            
            if self.on_transition_progress:
                self.on_transition_progress(progress, {"wipe_position": wipe_position})
            
            time.sleep(duration / steps)
    
    def _no_transition(self, transition: Transition):
        """No transition implementation"""
        time.sleep(transition.duration)
    
    def _apply_easing(self, progress: float, easing: str) -> float:
        """Apply easing function to progress value"""
        if easing == "linear":
            return progress
        elif easing == "ease_in":
            return progress * progress
        elif easing == "ease_out":
            return 1.0 - (1.0 - progress) * (1.0 - progress)
        elif easing == "ease_in_out":
            if progress < 0.5:
                return 2.0 * progress * progress
            else:
                return 1.0 - 2.0 * (1.0 - progress) * (1.0 - progress)
        else:
            return progress
    
    def stop_current_transition(self):
        """Stop current transition"""
        if self.transition_state == TransitionState.TRANSITIONING:
            self.stop_transition = True
            logger.info("Stopping current transition")
    
    def clear_transition_queue(self):
        """Clear transition queue"""
        self.transition_queue.clear()
        logger.info("Transition queue cleared")
    
    def is_transitioning(self) -> bool:
        """Check if currently transitioning"""
        return self.transition_state != TransitionState.IDLE
    
    def get_transition_status(self) -> Dict[str, Any]:
        """Get current transition status"""
        return {
            "state": self.transition_state.value,
            "current_transition": self.current_transition.transition_type.value if self.current_transition else None,
            "queue_length": len(self.transition_queue),
            "is_transitioning": self.is_transitioning()
        }
    
    def create_transition(self, 
                        transition_type: TransitionType, 
                        duration: float = None,
                        easing: str = None,
                        delay: float = 0.0,
                        callback: Optional[Callable] = None,
                        **parameters) -> Transition:
        """Create a transition object"""
        return Transition(
            transition_type=transition_type,
            duration=duration or self.default_duration,
            easing=easing or self.default_easing,
            delay=delay,
            callback=callback,
            parameters=parameters
        )
    
    def register_custom_transition(self, 
                                 transition_type: TransitionType, 
                                 implementation: Callable):
        """Register custom transition implementation"""
        self.transition_registry[transition_type] = implementation
        logger.info(f"Registered custom transition: {transition_type.value}")

def main():
    """Test the transition manager"""
    transition_manager = TransitionManager()
    
    print("Into the Dark - Transition Manager Test")
    print("=" * 45)
    
    # Test transition status
    status = transition_manager.get_transition_status()
    print(f"Initial state: {status['state']}")
    print(f"Is transitioning: {status['is_transitioning']}")
    
    # Test fade in transition
    print("\nTesting fade in transition...")
    fade_in = transition_manager.create_transition(
        TransitionType.FADE_IN, 
        duration=2.0,
        easing="ease_in_out"
    )
    
    transition_manager.execute_transition(fade_in)
    
    # Wait for transition to complete
    while transition_manager.is_transitioning():
        time.sleep(0.1)
    
    print("Fade in transition completed")
    
    # Test crossfade transition
    print("\nTesting crossfade transition...")
    crossfade = transition_manager.create_transition(
        TransitionType.CROSSFADE,
        duration=1.5,
        easing="ease_out"
    )
    
    transition_manager.execute_transition(crossfade)
    
    # Wait for transition to complete
    while transition_manager.is_transitioning():
        time.sleep(0.1)
    
    print("Crossfade transition completed")
    
    # Test transition queue
    print("\nTesting transition queue...")
    slide_left = transition_manager.create_transition(TransitionType.SLIDE_LEFT, duration=1.0)
    slide_right = transition_manager.create_transition(TransitionType.SLIDE_RIGHT, duration=1.0)
    
    transition_manager.execute_transition(slide_left)
    transition_manager.execute_transition(slide_right)  # Should be queued
    
    # Wait for all transitions to complete
    while transition_manager.is_transitioning():
        time.sleep(0.1)
    
    print("Transition queue test completed")
    
    print("\nTransition manager test completed!")

if __name__ == "__main__":
    main()
