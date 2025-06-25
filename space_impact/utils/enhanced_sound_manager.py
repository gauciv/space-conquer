"""
Enhanced Sound Manager for Space Conquer.
Handles loading, playing, and controlling volume of sound effects and music.
Works with the new AssetManager system.
"""
import pygame
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SoundManager')

class EnhancedSoundManager:
    def __init__(self, asset_manager, default_sfx_volume=0.7, default_music_volume=0.5):
        """
        Initialize the sound manager.
        
        Args:
            asset_manager: The AssetManager instance to use for loading assets
            default_sfx_volume: Default volume for sound effects (0.0 to 1.0)
            default_music_volume: Default volume for music (0.0 to 1.0)
        """
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.asset_manager = asset_manager
        self.sound_enabled = True
        self.music_enabled = True
        self.sfx_volume = default_sfx_volume
        self.music_volume = default_music_volume
        
        # Track the currently playing music
        self.current_track = None
        
        # Load sounds
        try:
            self._load_sounds()
            logger.info("Sound effects loaded successfully!")
        except Exception as e:
            self.sound_enabled = False
            logger.error(f"Error loading sound effects: {e}")
            logger.info("Game will run without sound effects.")
    
    def _load_sounds(self):
        """Load all sound effects from the asset manager."""
        # The sounds are loaded on-demand by the asset manager
        pass
    
    def play_sound(self, sound_id):
        """
        Play a sound effect by ID.
        
        Args:
            sound_id: The ID of the sound to play
        """
        if not self.sound_enabled:
            return
        
        # Get the sound from the asset manager
        sound = self.asset_manager.get_sound(sound_id)
        if sound:
            sound.play()
    
    def play_music(self, track_id='menu', loop=-1, fade_ms=1000):
        """
        Start playing a specific music track with optional fade-in.
        
        Args:
            track_id: ID of the track to play ('menu', 'starlight_end', etc.)
            loop: Number of times to loop (-1 for infinite)
            fade_ms: Fade-in time in milliseconds
        """
        if not self.music_enabled:
            return
            
        # If the requested track is already playing, do nothing
        if track_id == self.current_track and pygame.mixer.music.get_busy():
            return
        
        # Get the music path from the asset manager
        music_path = self.asset_manager.get_music_path(track_id)
        if not music_path:
            logger.warning(f"Music track '{track_id}' not found")
            return
        
        # Get the volume from the asset manager
        volume = self.asset_manager.music.get(track_id, {}).get("volume", self.music_volume)
        
        # Stop current music with fade out if playing
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
        
        # Load and play the new track
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume * self.music_volume)  # Apply both volume settings
            pygame.mixer.music.play(loop)
            
            # Update the current track
            self.current_track = track_id
            logger.info(f"Now playing music: {track_id}")
        except Exception as e:
            logger.error(f"Error playing music track '{track_id}': {e}")
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
        self.current_track = None
    
    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause background music."""
        pygame.mixer.music.unpause()
    
    def set_sfx_volume(self, volume):
        """
        Set volume for all sound effects.
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        self.sfx_volume = max(0, min(1, volume))
        
        if self.sound_enabled:
            # Update volume for all loaded sounds
            for sound_id, sound in self.asset_manager.sounds.items():
                if sound:
                    # Get the base volume from the manifest
                    base_volume = self.asset_manager.sound_manifest.get(sound_id, {}).get("volume", 1.0)
                    sound.set_volume(base_volume * self.sfx_volume)
    
    def set_music_volume(self, volume):
        """
        Set volume for background music.
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        self.music_volume = max(0, min(1, volume))
        
        if self.music_volume <= 0.01:  # Effectively zero
            if self.music_enabled:
                pygame.mixer.music.pause()
                self.music_enabled = False
        else:
            if not self.music_enabled:
                pygame.mixer.music.unpause()
                self.music_enabled = True
            
            # Apply both the global music volume and the track-specific volume
            if self.current_track:
                track_volume = self.asset_manager.music.get(self.current_track, {}).get("volume", 1.0)
                pygame.mixer.music.set_volume(track_volume * self.music_volume)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
    
    def temporarily_lower_music(self, duration=1000, factor=0.3):
        """
        Temporarily lower music volume and restore it after duration.
        
        Args:
            duration: Duration in milliseconds
            factor: Volume factor (0.0 to 1.0)
            
        Returns:
            The original volume
        """
        if self.music_enabled:
            current_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(current_volume * factor)
            return current_volume
        return 0
    
    def restore_music_volume(self, original_volume=None):
        """
        Restore music volume to original level or default.
        
        Args:
            original_volume: The original volume to restore to
        """
        if self.music_enabled:
            if original_volume is not None:
                pygame.mixer.music.set_volume(original_volume)
            elif self.current_track:
                track_volume = self.asset_manager.music.get(self.current_track, {}).get("volume", 1.0)
                pygame.mixer.music.set_volume(track_volume * self.music_volume)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
    
    def enable_sound(self, enabled=True):
        """
        Enable or disable sound effects.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.sound_enabled = enabled
    
    def enable_music(self, enabled=True):
        """
        Enable or disable music.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.music_enabled = enabled
        if self.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
