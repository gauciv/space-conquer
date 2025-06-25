"""
Asset loader for the Space Impact game.
Handles loading images and other assets.
This is a legacy class that now uses the new AssetManager internally.
"""
import pygame
import os
from src.config import get_asset_path
from src.utils.asset_manager import AssetManager

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.asset_manager = AssetManager()
        self.asset_manager.load_all_assets()
        self._load_images()
    
    def _load_images(self):
        """Load all game images using the asset manager."""
        image_ids = {
            'player': 'player-default',
            'normal_enemy': 'SE-monster-lower',
            'fast_enemy': 'SE-monster-elite',
            'tank_enemy': 'SE-monster-super',
            'bullet': 'player-bullet-default',
            'health_powerup': 'powerup-health',
            'speed_powerup': 'powerup-speed',
            'rapid_fire_powerup': 'powerup-rapid-fire',
            'score_multiplier': 'powerup-score-multiplier',
            'settings_cog': 'ui-settings-cog',
            'slider_bar': 'ui-slider-bar',
            'slider_handle': 'ui-slider-handle',
            'full_heart': 'ui-heart-full',
            'empty_heart': 'ui-heart-empty',
            'mini_boss': 'SE-monster-mini-boss',
            'main_boss': 'SE-monster-boss',
            'health_bar_bg': 'ui-health-bar-bg',
            'health_bar_fill': 'ui-health-bar-fill',
            'asteroid': 'asteroid',
            'debris': 'debris'
        }
        
        for old_name, new_id in image_ids.items():
            self.images[old_name] = self.asset_manager.get_image(new_id)
    
    def load_image(self, name, filename):
        """
        Legacy method to load an image and store it by name.
        Now uses the asset manager.
        """
        # Try to determine the asset ID from the filename
        asset_id = filename.split('.')[0]
        
        # Special cases for the new naming convention
        if filename == 'player_ship.png':
            asset_id = 'player-default'
        elif filename == 'bullet.png':
            asset_id = 'player-bullet-default'
        elif filename.startswith('normal_'):
            asset_id = 'SE-monster-lower'
        elif filename.startswith('fast_'):
            asset_id = 'SE-monster-elite'
        elif filename.startswith('tank_'):
            asset_id = 'SE-monster-super'
        elif filename.startswith('mini_boss'):
            asset_id = 'SE-monster-mini-boss'
        elif filename.startswith('main_boss'):
            asset_id = 'SE-monster-boss'
        elif filename.startswith('health_powerup'):
            asset_id = 'powerup-health'
        elif filename.startswith('speed_powerup'):
            asset_id = 'powerup-speed'
        elif filename.startswith('rapid_fire_powerup'):
            asset_id = 'powerup-rapid-fire'
        elif filename.startswith('score_multiplier'):
            asset_id = 'powerup-score-multiplier'
        elif filename.startswith('settings_cog'):
            asset_id = 'ui-settings-cog'
        elif filename.startswith('slider_bar'):
            asset_id = 'ui-slider-bar'
        elif filename.startswith('slider_handle'):
            asset_id = 'ui-slider-handle'
        elif filename.startswith('full_heart'):
            asset_id = 'ui-heart-full'
        elif filename.startswith('empty_heart'):
            asset_id = 'ui-heart-empty'
        elif filename.startswith('health_bar_bg'):
            asset_id = 'ui-health-bar-bg'
        elif filename.startswith('health_bar_fill'):
            asset_id = 'ui-health-bar-fill'
        
        # Get the image from the asset manager
        self.images[name] = self.asset_manager.get_image(asset_id)
        return self.images[name]
    
    def get_image(self, name):
        """Get an image by name."""
        if name in self.images:
            return self.images[name]
        else:
            print(f"Warning: Image '{name}' not found")
            # Try to load it from the asset manager using the name as the asset ID
            image = self.asset_manager.get_image(name)
            if image:
                self.images[name] = image
                return image
            return pygame.Surface((30, 30))
    
    def scale_image(self, name, width, height):
        """Scale an image to the specified dimensions."""
        if name in self.images:
            self.images[name] = pygame.transform.scale(self.images[name], (width, height))
            return self.images[name]
        else:
            print(f"Warning: Cannot scale image '{name}' - not found")
            return pygame.Surface((width, height))
