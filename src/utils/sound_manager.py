"""
Sound manager for the Space Impact game.
Handles loading, playing, and controlling volume of sound effects and music.
"""
import pygame
import os
from src.config import DEFAULT_SFX_VOLUME, DEFAULT_MUSIC_VOLUME, get_asset_path

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
        self.music_tracks = {}
        self.current_music = None
        
        try:
            self._load_sounds()
            print("Sound effects loaded successfully!")
        except Exception as e:
            self.sound_enabled = False
            print(f"Error loading sound effects: {e}")
            print("Game will run without sound effects.")
        
        try:
            self._load_music_tracks()
            print("Music tracks loaded successfully!")
        except Exception as e:
            self.music_enabled = False
            print(f"Error loading music tracks: {e}")
            print("Game will run without background music.")
    
    def _load_sounds(self):
        """Load all sound effects."""
        sound_files = {
            'shoot': 'shoot.wav',
            'explosion': 'explosion.wav',
            'enemy_death': 'enemy_death.wav',  # New sound for enemy death
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
                # For enemy_death, fall back to explosion sound if not found
                if name == 'enemy_death' and 'explosion' in self.sounds:
                    self.sounds[name] = self.sounds['explosion']
                    print(f"Using explosion sound as fallback for {name}")
    
    def _load_music_tracks(self):
        """Load all music tracks."""
        music_files = {
            'menu': 'background_music.wav',
            'gameplay': 'starlight_end.wav', 
            'starlight_end': 'starlight_end.wav',
            'boss': 'boss_battle.wav',
            'boss_battle': 'boss_battle.wav'
        }
        
        for track_name, filename in music_files.items():
            path = get_asset_path('music', filename)
            if os.path.exists(path):
                self.music_tracks[track_name] = path
                print(f"Loaded music track: {track_name}")
            else:
                print(f"Music file not found: {path}")
                # Fallback logic
                if track_name == 'gameplay' and 'menu' in self.music_tracks:
                    self.music_tracks[track_name] = self.music_tracks['menu']
                    print(f"Using menu music as fallback for {track_name}")
                elif track_name == 'boss' and 'gameplay' in self.music_tracks:
                    self.music_tracks[track_name] = self.music_tracks['gameplay']
                    print(f"Using gameplay music as fallback for {track_name}")
        
        if not self.music_tracks:
            self.music_enabled = False
    
    def play_sound(self, sound_name):
        """Play a sound effect by name."""
        if self.sound_enabled:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
            elif sound_name == 'enemy_death' and 'explosion' in self.sounds:
                # Fall back to explosion sound if enemy_death is requested but not available
                self.sounds['explosion'].play()
                print("Using explosion sound as fallback for enemy_death")
    
    def play_music(self, track='menu', loop=-1):
        """Start playing a specific music track."""
        if self.music_enabled and track in self.music_tracks:
            # Only load and play if it's a different track
            if self.current_music != track:
                pygame.mixer.music.load(self.music_tracks[track])
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = track
            pygame.mixer.music.play(loop)
            print(f"Playing music track: {track}")
        elif self.music_enabled:
            print(f"Music track '{track}' not found, available tracks: {list(self.music_tracks.keys())}")
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
        self.current_music = None
    
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
    
    def switch_music(self, track, loop=-1):
        """Switch to a different music track smoothly."""
        if self.music_enabled and track in self.music_tracks:
            if self.current_music != track:
                pygame.mixer.music.fadeout(500)  # Fade out over 500ms
                pygame.time.wait(500)  # Wait for fade out
                self.play_music(track, loop)
    
    def get_available_tracks(self):
        """Get list of available music tracks."""
        return list(self.music_tracks.keys())
    
    def get_current_track(self):
        """Get the currently playing track name."""
        return self.current_music
    
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
