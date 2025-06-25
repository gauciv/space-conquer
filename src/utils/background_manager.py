"""
Background manager for themed map visuals.
Handles nebulae, blue stars, and cosmic debris for the Starlight's End theme.
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
        
        # Load background image if asset_loader is provided
        if self.asset_loader:
            self.background_image = self.asset_loader.get_image('map_background')
            self.blue_stars_image = self.asset_loader.get_image('blue_stars')
        
        self.nebulae = []
        self.cosmic_debris = []
        self.stellar_remnants = []
        
        # Create nebulae patches
        for _ in range(3):
            self.nebulae.append(self._create_nebula())
        
        # Create cosmic debris
        for _ in range(8):
            self.cosmic_debris.append(self._create_debris())
        
        # Create stellar remnants
        for _ in range(2):
            self.stellar_remnants.append(self._create_stellar_remnant())
    
    def set_asset_loader(self, asset_loader):
        """Set the asset loader after initialization."""
        self.asset_loader = asset_loader
        self.background_image = self.asset_loader.get_image('map_background')
        self.blue_stars_image = self.asset_loader.get_image('blue_stars')
    
    def _create_nebula(self):
        return {
            'x': random.randint(-100, SCREEN_WIDTH + 100),
            'y': random.randint(-50, SCREEN_HEIGHT + 50),
            'width': random.randint(200, 400),
            'height': random.randint(150, 300),
            'color': random.choice([
                (30, 50, 120, 40),   # Deep blue
                (60, 30, 100, 35),   # Purple
                (20, 40, 80, 30)     # Dark blue
            ]),
            'drift_speed': random.uniform(0.1, 0.3),
            'pulse_speed': random.uniform(0.005, 0.015),
            'pulse_offset': random.uniform(0, 6.28)
        }
    
    def _create_debris(self):
        return {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT),
            'size': random.randint(2, 6),
            'speed': random.uniform(0.5, 2.0),
            'color': (100, 100, 120),
            'rotation': random.uniform(0, 6.28),
            'rotation_speed': random.uniform(-0.02, 0.02)
        }
    
    def _create_stellar_remnant(self):
        return {
            'x': random.randint(50, SCREEN_WIDTH - 50),
            'y': random.randint(50, SCREEN_HEIGHT - 50),
            'radius': random.randint(30, 60),
            'color': (80, 40, 20, 60),
            'pulse_speed': random.uniform(0.01, 0.03),
            'pulse_offset': random.uniform(0, 6.28)
        }
    
    def update(self):
        # Update background position for parallax scrolling
        if self.background_image:
            self.background_position -= self.background_speed
            if self.background_position <= -SCREEN_WIDTH:
                self.background_position = 0
        
        # Update blue stars blinking effect
        if self.blue_stars_image:
            # Update alpha based on fade direction
            self.blue_stars_alpha += self.blue_stars_fade_direction * self.blue_stars_fade_speed
            
            # Change direction when reaching limits
            if self.blue_stars_alpha <= 100:  # Minimum visibility
                self.blue_stars_fade_direction = 1
            elif self.blue_stars_alpha >= 255:  # Maximum visibility
                self.blue_stars_fade_direction = -1
            
            # Ensure alpha stays within valid range
            self.blue_stars_alpha = max(100, min(255, self.blue_stars_alpha))
        
        # Update cosmic debris
        for debris in self.cosmic_debris:
            debris['x'] -= debris['speed']
            debris['rotation'] += debris['rotation_speed']
            
            if debris['x'] < -10:
                debris['x'] = SCREEN_WIDTH + 10
                debris['y'] = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, surface):
        # Draw background image with parallax scrolling
        if self.background_image:
            # Draw the background image twice for seamless scrolling
            surface.blit(self.background_image, (self.background_position, 0))
            surface.blit(self.background_image, (self.background_position + SCREEN_WIDTH, 0))
            
            # Add a subtle overlay to enhance the mood
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 0, 40, 30))  # Dark purple with transparency
            surface.blit(overlay, (0, 0))
        
        # Draw blue stars with blinking effect
        if self.blue_stars_image:
            # Create a copy of the image with adjusted alpha
            stars_surface = self.blue_stars_image.copy()
            stars_surface.set_alpha(int(self.blue_stars_alpha))
            surface.blit(stars_surface, (0, 0))
        
        # Draw nebulae
        for nebula in self.nebulae:
            pulse = 0.7 + 0.3 * math.sin(pygame.time.get_ticks() * nebula['pulse_speed'] + nebula['pulse_offset'])
            alpha = int(nebula['color'][3] * pulse)
            
            nebula_surface = pygame.Surface((nebula['width'], nebula['height']), pygame.SRCALPHA)
            color_with_alpha = (*nebula['color'][:3], alpha)
            
            # Create gradient nebula effect
            center_x, center_y = nebula['width'] // 2, nebula['height'] // 2
            for radius in range(min(nebula['width'], nebula['height']) // 2, 0, -5):
                fade_alpha = int(alpha * (radius / (min(nebula['width'], nebula['height']) // 2)))
                fade_color = (*nebula['color'][:3], fade_alpha)
                pygame.draw.ellipse(nebula_surface, fade_color, 
                                  (center_x - radius, center_y - radius//2, radius*2, radius))
            
            surface.blit(nebula_surface, (nebula['x'], nebula['y']))
        
        # Draw stellar remnants
        for remnant in self.stellar_remnants:
            pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * remnant['pulse_speed'] + remnant['pulse_offset'])
            alpha = int(remnant['color'][3] * pulse)
            
            remnant_surface = pygame.Surface((remnant['radius']*2, remnant['radius']*2), pygame.SRCALPHA)
            
            # Create fading circle effect
            for r in range(remnant['radius'], 0, -3):
                fade_alpha = int(alpha * (r / remnant['radius']))
                fade_color = (*remnant['color'][:3], fade_alpha)
                pygame.draw.circle(remnant_surface, fade_color, 
                                 (remnant['radius'], remnant['radius']), r)
            
            surface.blit(remnant_surface, (remnant['x'] - remnant['radius'], remnant['y'] - remnant['radius']))
        
        # Draw cosmic debris
        for debris in self.cosmic_debris:
            # Simple rotating rectangle for debris
            debris_surface = pygame.Surface((debris['size']*2, debris['size']*2), pygame.SRCALPHA)
            rotated_rect = pygame.Rect(0, 0, debris['size'], debris['size']//2)
            rotated_rect.center = (debris['size'], debris['size'])
            
            pygame.draw.rect(debris_surface, debris['color'], rotated_rect)
            
            # Rotate the debris
            rotated_surface = pygame.transform.rotate(debris_surface, math.degrees(debris['rotation']))
            rect = rotated_surface.get_rect(center=(debris['x'], debris['y']))
            surface.blit(rotated_surface, rect)
            
        # Add light rays effect
        self._draw_light_rays(surface)
    
    def _draw_light_rays(self, surface):
        """Draw subtle light rays for atmospheric effect."""
        ray_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Create several light rays
        for i in range(3):
            # Calculate ray properties based on time
            time = pygame.time.get_ticks() * 0.001
            ray_width = 100 + 50 * math.sin(time * 0.2 + i * 2)
            ray_alpha = 10 + 5 * math.sin(time * 0.3 + i * 1.5)
            ray_x = (SCREEN_WIDTH * 0.3 + i * SCREEN_WIDTH * 0.2) + 50 * math.sin(time * 0.1 + i)
            
            # Create ray polygon
            ray_points = [
                (ray_x, 0),
                (ray_x + ray_width, 0),
                (ray_x + ray_width * 2, SCREEN_HEIGHT),
                (ray_x - ray_width, SCREEN_HEIGHT)
            ]
            
            # Draw ray
            pygame.draw.polygon(ray_surface, (150, 100, 200, int(ray_alpha)), ray_points)
        
        # Apply the rays to the surface
        surface.blit(ray_surface, (0, 0))
