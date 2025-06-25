"""
Star background elements for the Space Impact game.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 3.0)  # Slower, more melancholic drift
        
        # Starlight's End theme colors - sparse, fading stars
        color_choice = random.randint(0, 10)
        if color_choice < 5:  # 50% dim white/gray stars (dying)
            brightness = random.randint(120, 180)
            self.color = (brightness, brightness, brightness)
        elif color_choice < 7:  # 20% cool blue (distant)
            self.color = (random.randint(80, 120), random.randint(120, 160), random.randint(180, 220))
        elif color_choice < 9:  # 20% warm orange/red (dying)
            self.color = (random.randint(180, 220), random.randint(100, 140), random.randint(60, 100))
        else:  # 10% very dim purple (ethereal)
            self.color = (random.randint(100, 140), random.randint(80, 120), random.randint(140, 180))
        
        # Add slow, melancholic twinkling effect
        self.twinkle_speed = random.uniform(0.005, 0.02)  # Slower twinkling
        self.twinkle_offset = random.uniform(0, 6.28)
        self.base_size = self.size
        self.fade_factor = random.uniform(0.6, 1.0)  # Some stars are naturally dimmer
        
        # Rare dying star flickers instead of shooting stars
        self.is_dying = random.random() < 0.01  # 1% chance
        if self.is_dying:
            self.death_timer = random.randint(300, 600)  # Frames until death
            self.flicker_intensity = random.uniform(0.3, 0.7)
            self.death_speed = random.uniform(0.01, 0.03)
    
    def update(self):
        self.x -= self.speed
        
        # Update twinkling/dying effect
        if self.is_dying:
            self.death_timer -= 1
            # Flickering death effect
            death_flicker = self.flicker_intensity * math.sin(pygame.time.get_ticks() * self.death_speed)
            fade_progress = 1.0 - (self.death_timer / 600)
            self.size = self.base_size * (0.5 + 0.5 * death_flicker) * (1.0 - fade_progress)
            
            if self.death_timer <= 0:
                # Star dies, respawn as new star
                self._respawn()
        else:
            # Normal gentle twinkling
            twinkle_factor = 0.4 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset) + 0.6
            self.size = self.base_size * twinkle_factor * self.fade_factor
        
        # Reset when off-screen
        if self.x < -10:
            self._respawn()
    
    def _respawn(self):
        """Respawn star with new properties."""
        self.x = SCREEN_WIDTH + random.randint(0, 50)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 3.0)
        self.fade_factor = random.uniform(0.6, 1.0)
        
        # Small chance to become a dying star
        self.is_dying = random.random() < 0.01
        if self.is_dying:
            self.death_timer = random.randint(300, 600)
            self.flicker_intensity = random.uniform(0.3, 0.7)
            self.death_speed = random.uniform(0.01, 0.03)
    
    def draw(self, surface):
        if self.size <= 0.5:  # Don't draw nearly dead stars
            return
            
        # Calculate current color with fading
        current_color = self.color
        if self.is_dying:
            death_progress = 1.0 - (self.death_timer / 600)
            # Fade to red as star dies
            fade_red = min(255, int(self.color[0] + (255 - self.color[0]) * death_progress))
            fade_green = int(self.color[1] * (1.0 - death_progress * 0.7))
            fade_blue = int(self.color[2] * (1.0 - death_progress * 0.8))
            current_color = (fade_red, fade_green, fade_blue)
        
        # Draw subtle glow for larger or dying stars
        if self.base_size >= 2 or self.is_dying:
            glow_size = max(self.size * 1.5, 3)
            glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
            
            # Softer, more ethereal glow
            for r in range(int(glow_size), 0, -1):
                alpha = int(30 * (r / glow_size) * self.fade_factor)
                if self.is_dying:
                    alpha = int(alpha * (1.5 - (self.death_timer / 600)))  # Brighter as it dies
                glow_color = (*current_color, alpha)
                pygame.draw.circle(glow_surface, glow_color, (int(glow_size), int(glow_size)), r)
            
            surface.blit(glow_surface, (int(self.x - glow_size), int(self.y - glow_size)))
        
        # Draw the star core
        final_color = tuple(int(c * self.fade_factor) for c in current_color)
        pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), max(1, int(self.size)))
