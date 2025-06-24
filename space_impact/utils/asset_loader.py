"""
Asset loader for the Space Impact game.
Handles loading images and other assets.
"""
import pygame
import os
from ..config import get_asset_path

class AssetLoader:
    def __init__(self):
        self.images = {}
        self._load_images()
    
    def _load_images(self):
        """Load all game images."""
        image_files = {
            'player': 'player_ship.png',
            'normal_enemy': 'normal_enemy.png',
            'fast_enemy': 'fast_enemy.png',
            'tank_enemy': 'tank_enemy.png',
            'bullet': 'bullet.png',
            'health_powerup': 'health_powerup.png',
            'speed_powerup': 'speed_powerup.png',
            'rapid_fire_powerup': 'rapid_fire_powerup.png',
            'settings_cog': 'settings_cog.png',
            'slider_bar': 'slider_bar.png',
            'slider_handle': 'slider_handle.png',
            'full_heart': 'full_heart.png',
            'empty_heart': 'empty_heart.png'
        }
        
        for name, filename in image_files.items():
            self.load_image(name, filename)
    
    def load_image(self, name, filename):
        """Load an image and store it by name."""
        path = get_asset_path('assets', filename)
        if not os.path.exists(path):
            # Try the images directory as fallback
            path = get_asset_path('images', filename)
            
        try:
            self.images[name] = pygame.image.load(path)
            return self.images[name]
        except pygame.error as e:
            print(f"Cannot load image: {path}")
            print(e)
            self.images[name] = pygame.Surface((30, 30))
            return self.images[name]
    
    def get_image(self, name):
        """Get an image by name."""
        if name in self.images:
            return self.images[name]
        else:
            print(f"Warning: Image '{name}' not found")
            return pygame.Surface((30, 30))
    
    def scale_image(self, name, width, height):
        """Scale an image to the specified dimensions."""
        if name in self.images:
            self.images[name] = pygame.transform.scale(self.images[name], (width, height))
            return self.images[name]
        else:
            print(f"Warning: Cannot scale image '{name}' - not found")
            return pygame.Surface((width, height))
