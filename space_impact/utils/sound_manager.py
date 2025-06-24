"""
Sound manager for the Space Impact game.
Handles loading, playing, and controlling volume of sound effects and music.
"""
import pygame
import os
from ..config import DEFAULT_SFX_VOLUME, DEFAULT_MUSIC_VOLUME, get_asset_path

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.sound_enabled = True
        self.music_enabled = True
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sounds = {}
        
        try:
            self._load_sounds()
            print("Sound effects loaded successfully!")
        except Exception as e:
            self.sound_enabled = False
            print(f"Error loading sound effects: {e}")
            print("Game will run without sound effects.")
        
        try:
            self._load_music()
            print("Background music loaded successfully!")
        except Exception as e:
            self.music_enabled = False
            print(f"Error loading background music: {e}")
            print("Game will run without background music.")
    
    def _load_sounds(self):
        """Load all sound effects."""
        sound_files = {
            'shoot': 'shoot.wav',
            'explosion': 'explosion.wav',
            'powerup': 'powerup.wav',
            'game_start': 'game_start.wav',
            'game_over': 'game_over.wav'
        }
        
        for name, filename in sound_files.items():
            path = get_asset_path('sounds', filename)
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(self.sfx_volume)
            else:
                print(f"Warning: Sound file not found: {path}")
    
    def _load_music(self):
        """Load background music."""
        music_path = get_asset_path('music', 'background_music.wav')
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
        else:
            print(f"Warning: Music file not found: {music_path}")
            self.music_enabled = False
    
    def play_sound(self, sound_name):
        """Play a sound effect by name."""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, loop=-1):
        """Start playing background music."""
        if self.music_enabled:
            pygame.mixer.music.play(loop)
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause background music."""
        pygame.mixer.music.unpause()
    
    def set_sfx_volume(self, volume):
        """Set volume for all sound effects."""
        self.sfx_volume = max(0, min(1, volume))
        
        if self.sound_enabled:
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Set volume for background music."""
        self.music_volume = max(0, min(1, volume))
        
        if self.music_volume <= 0.01:  # Effectively zero
            if self.music_enabled:
                pygame.mixer.music.pause()
                self.music_enabled = False
        else:
            if not self.music_enabled:
                pygame.mixer.music.unpause()
                self.music_enabled = True
            pygame.mixer.music.set_volume(self.music_volume)
    
    def temporarily_lower_music(self, duration=1000, factor=0.3):
        """Temporarily lower music volume and restore it after duration."""
        if self.music_enabled:
            current_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(current_volume * factor)
            return current_volume
        return 0
    
    def restore_music_volume(self, original_volume=None):
        """Restore music volume to original level or default."""
        if self.music_enabled:
            if original_volume is not None:
                pygame.mixer.music.set_volume(original_volume)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
