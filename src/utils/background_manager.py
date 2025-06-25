"""
Background manager for themed map visuals.
Highly optimized version with reduced visual effects for better performance.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class BackgroundManager:
    def __init__(self, asset_loader=None):
        self.asset_loader = asset_loader
        self.background_image = None
        self.background_position = 0
        self.background_speed = 0.5  # Slow scrolling speed
        self.blue_stars_image = None
        self.blue_stars_alpha = 255
        self.blue_stars_fade_direction = -1  # -1 for fading out, 1 for fading in
        self.blue_stars_fade_speed = 0.5  # Speed of the fade effect
        
        # Pre-render surfaces for better performance
        self.blue_stars_surface = None
        self.overlay_surface = None
        self.last_stars_alpha = -1  # Track last alpha value to avoid unnecessary rendering
        
        # Load background image if asset_loader is provided
        if self.asset_loader:
            self.background_image = self.asset_loader.get_image('map_background')
            self.blue_stars_image = self.asset_loader.get_image('blue_stars')
            
            # Create the overlay surface once
            self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            self.overlay_surface.fill((20, 0, 40, 30))  # Dark purple with transparency
        
        # Minimal visual elements for better performance
        self.cosmic_debris = []
        
        # Create just a few cosmic debris (reduced from 5 to 3)
        for _ in range(3):
            self.cosmic_debris.append(self._create_debris())
        
        # Frame counter for staggered updates
        self.frame_counter = 0
        
        # Pre-render the blue stars at different alpha levels
        self.blue_stars_surfaces = {}
        if self.blue_stars_image:
            for alpha in range(100, 256, 10):  # Create surfaces for alpha values 100, 110, 120, ..., 250
                surface = self.blue_stars_image.copy()
                surface.set_alpha(alpha)
                self.blue_stars_surfaces[alpha] = surface
    
    def set_asset_loader(self, asset_loader):
        """Set the asset loader after initialization."""
        self.asset_loader = asset_loader
        self.background_image = self.asset_loader.get_image('map_background')
        self.blue_stars_image = self.asset_loader.get_image('blue_stars')
        
        # Create the overlay surface once
        self.overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((20, 0, 40, 30))  # Dark purple with transparency
        
        # Pre-render the blue stars at different alpha levels
        self.blue_stars_surfaces = {}
        if self.blue_stars_image:
            for alpha in range(100, 256, 10):  # Create surfaces for alpha values 100, 110, 120, ..., 250
                surface = self.blue_stars_image.copy()
                surface.set_alpha(alpha)
                self.blue_stars_surfaces[alpha] = surface
    
    def _create_debris(self):
        return {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'size': random.randint(2, 4),  # Reduced size
            'speed': random.uniform(0.5, 1.5),  # Reduced speed
            'color': (100, 100, 120),
            'rotation': random.uniform(0, 6.28),
            'rotation_speed': random.uniform(-0.01, 0.01)  # Reduced rotation speed
        }
    
    def update(self):
        # Increment frame counter
        self.frame_counter += 1
        
        # Update background position for parallax scrolling
        if self.background_image:
            self.background_position -= self.background_speed
            if self.background_position <= -SCREEN_WIDTH:
                self.background_position = 0
        
        # Update blue stars blinking effect (only every 2 frames)
        if self.blue_stars_image and self.frame_counter % 2 == 0:
            # Update alpha based on fade direction
            self.blue_stars_alpha += self.blue_stars_fade_direction * self.blue_stars_fade_speed
            
            # Change direction when reaching limits
            if self.blue_stars_alpha <= 100:  # Minimum visibility
                self.blue_stars_fade_direction = 1
            elif self.blue_stars_alpha >= 255:  # Maximum visibility
                self.blue_stars_fade_direction = -1
            
            # Ensure alpha stays within valid range
            self.blue_stars_alpha = max(100, min(255, self.blue_stars_alpha))
        
        # Update cosmic debris (only every 3 frames)
        if self.frame_counter % 3 == 0:
            for debris in self.cosmic_debris:
                debris['x'] -= debris['speed']
                
                if debris['x'] < -10:
                    debris['x'] = SCREEN_WIDTH + 10
                    debris['y'] = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, surface):
        # Draw background image with parallax scrolling
        if self.background_image:
            # Draw the background image twice for seamless scrolling
            surface.blit(self.background_image, (self.background_position, 0))
            surface.blit(self.background_image, (self.background_position + SCREEN_WIDTH, 0))
            
            # Add a subtle overlay to enhance the mood (using pre-rendered surface)
            if self.overlay_surface:
                surface.blit(self.overlay_surface, (0, 0))
        
        # Draw blue stars with blinking effect (using pre-rendered surfaces)
        if self.blue_stars_surfaces:
            # Find the closest pre-rendered alpha level
            alpha_key = round(self.blue_stars_alpha / 10) * 10
            alpha_key = max(100, min(250, alpha_key))  # Ensure it's within our pre-rendered range
            
            # Use the pre-rendered surface
            surface.blit(self.blue_stars_surfaces[alpha_key], (0, 0))
        
        # Draw cosmic debris (simplified)
        for debris in self.cosmic_debris:
            # Simple rectangle for debris (no rotation for better performance)
            pygame.draw.rect(surface, debris['color'], 
                           (debris['x'], debris['y'], debris['size'], debris['size']))
