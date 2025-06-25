"""
Map Manager for Space Conquer.
Handles loading, managing, and transitioning between game maps.
"""
import pygame
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MapManager')

class MapManager:
    def __init__(self, asset_manager, sound_manager):
        """
        Initialize the map manager.
        
        Args:
            asset_manager: The AssetManager instance to use for loading assets
            sound_manager: The SoundManager instance to use for playing music
        """
        self.asset_manager = asset_manager
        self.sound_manager = sound_manager
        
        # Map state
        self.maps = []
        self.current_map_index = 0
        self.current_map = None
        
        # Transition state
        self.transitioning = False
        self.transition_timer = 0
        self.transition_duration = 180  # 3 seconds at 60 FPS
        self.showing_map_name = False
        
        # Load maps
        self._load_maps()
    
    def _load_maps(self):
        """Load all maps from the asset manager."""
        self.maps = self.asset_manager.get_all_maps()
        
        if not self.maps:
            logger.warning("No maps found in asset manager")
            return
        
        logger.info(f"Loaded {len(self.maps)} maps")
        
        # Set the first map as current
        self.current_map = self.maps[0]
        self.current_map_index = 0
    
    def start_first_map(self):
        """Start the first map."""
        if not self.maps:
            logger.warning("No maps available to start")
            return
        
        self.current_map_index = 0
        self.current_map = self.maps[0]
        self.showing_map_name = True
        self.transition_timer = self.transition_duration
        
        # Play the map's music
        music_id = self.current_map.get("music")
        if music_id:
            self.sound_manager.play_music(music_id, fade_ms=2000)
        
        logger.info(f"Starting first map: {self.current_map['name']}")
    
    def next_map(self):
        """
        Transition to the next map.
        
        Returns:
            True if there is a next map, False if this was the last map
        """
        if self.current_map_index >= len(self.maps) - 1:
            logger.info("No more maps available")
            return False
        
        self.current_map_index += 1
        self.current_map = self.maps[self.current_map_index]
        self.showing_map_name = True
        self.transition_timer = self.transition_duration
        
        # Play the map's music
        music_id = self.current_map.get("music")
        if music_id:
            self.sound_manager.play_music(music_id, fade_ms=2000)
        
        logger.info(f"Transitioning to next map: {self.current_map['name']}")
        return True
    
    def update(self):
        """
        Update the map state.
        
        Returns:
            A dictionary with map update information
        """
        update_info = {
            "showing_map_name": self.showing_map_name,
            "map_changed": False
        }
        
        # Handle map name display timer
        if self.showing_map_name:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.showing_map_name = False
                update_info["showing_map_name"] = False
        
        return update_info
    
    def draw_map_name(self, surface):
        """
        Draw the current map name on the screen.
        
        Args:
            surface: The pygame surface to draw on
        """
        if not self.showing_map_name or not self.current_map:
            return
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), 100), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 180))
        surface.blit(overlay, (0, surface.get_height() // 2 - 50))
        
        # Draw map name
        font = self.asset_manager.get_font("title", 36)
        text = font.render(self.current_map["name"], True, (220, 220, 255))
        
        # Add glow effect
        glow_text = font.render(self.current_map["name"], True, (60, 60, 120))
        surface.blit(glow_text, (surface.get_width() // 2 - glow_text.get_width() // 2 + 2, 
                                surface.get_height() // 2 - glow_text.get_height() // 2 + 2))
        
        # Draw main text
        surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, 
                           surface.get_height() // 2 - text.get_height() // 2))
    
    def get_current_map_id(self):
        """
        Get the ID of the current map.
        
        Returns:
            The map ID as a string
        """
        if not self.current_map:
            return None
        return self.current_map.get("id")
    
    def get_current_map_name(self):
        """
        Get the name of the current map.
        
        Returns:
            The map name as a string
        """
        if not self.current_map:
            return "Unknown Map"
        return self.current_map.get("name", "Unknown Map")
    
    def get_enemy_spawn_rate(self):
        """
        Get the enemy spawn rate for the current map.
        
        Returns:
            The spawn rate in milliseconds
        """
        if not self.current_map:
            return 1500  # Default
        return self.current_map.get("enemy_spawn_rate", 1500)
    
    def get_enemy_types(self):
        """
        Get the enemy types available in the current map.
        
        Returns:
            A list of enemy type strings
        """
        if not self.current_map:
            return ["normal"]
        return self.current_map.get("enemy_types", ["normal"])
    
    def get_boss_type(self):
        """
        Get the boss type for the current map.
        
        Returns:
            The boss type as a string, or None if no boss
        """
        if not self.current_map:
            return None
        return self.current_map.get("boss")
    
    def get_background_image(self):
        """
        Get the background image for the current map.
        
        Returns:
            The background image filename, or None if not specified
        """
        if not self.current_map:
            return None
        return self.current_map.get("background")
    
    def reset(self):
        """Reset the map manager to the first map."""
        self.current_map_index = 0
        if self.maps:
            self.current_map = self.maps[0]
        self.showing_map_name = False
        self.transition_timer = 0
