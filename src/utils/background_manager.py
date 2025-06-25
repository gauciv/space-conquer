"""
Background manager for themed map visuals.
Handles nebulae, dying stars, and cosmic debris for the Starlight's End theme.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class BackgroundManager:
    def __init__(self):
        self.nebulae = []
        self.dying_stars = []
        self.cosmic_debris = []
        self.stellar_remnants = []
        
        # Create nebulae patches
        for _ in range(3):
            self.nebulae.append(self._create_nebula())
        
        # Create dying stars
        for _ in range(2):
            self.dying_stars.append(self._create_dying_star())
        
        # Create cosmic debris
        for _ in range(8):
            self.cosmic_debris.append(self._create_debris())
        
        # Create stellar remnants
        for _ in range(2):
            self.stellar_remnants.append(self._create_stellar_remnant())
    
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
    
    def _create_dying_star(self):
        return {
            'x': random.randint(100, SCREEN_WIDTH - 100),
            'y': random.randint(100, SCREEN_HEIGHT - 100),
            'size': random.randint(15, 25),
            'color': random.choice([
                (200, 100, 50),   # Orange
                (180, 80, 40),    # Red-orange
                (220, 120, 60)    # Bright orange
            ]),
            'flicker_speed': random.uniform(0.02, 0.05),
            'flicker_offset': random.uniform(0, 6.28),
            'glow_radius': random.randint(40, 80)
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
        # Update cosmic debris
        for debris in self.cosmic_debris:
            debris['x'] -= debris['speed']
            debris['rotation'] += debris['rotation_speed']
            
            if debris['x'] < -10:
                debris['x'] = SCREEN_WIDTH + 10
                debris['y'] = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, surface):
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
        
        # Draw dying stars
        for star in self.dying_stars:
            flicker = 0.6 + 0.4 * math.sin(pygame.time.get_ticks() * star['flicker_speed'] + star['flicker_offset'])
            
            # Draw glow
            glow_surface = pygame.Surface((star['glow_radius']*2, star['glow_radius']*2), pygame.SRCALPHA)
            for r in range(star['glow_radius'], 0, -2):
                alpha = int(80 * flicker * (r / star['glow_radius']))
                glow_color = (*star['color'], alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (star['glow_radius'], star['glow_radius']), r)
            
            surface.blit(glow_surface, (star['x'] - star['glow_radius'], star['y'] - star['glow_radius']))
            
            # Draw star core
            core_color = tuple(int(c * flicker) for c in star['color'])
            pygame.draw.circle(surface, core_color, (star['x'], star['y']), int(star['size'] * flicker))
        
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