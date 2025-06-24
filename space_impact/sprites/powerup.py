"""
Power-up sprites for the Space Impact game.
"""
import pygame
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, images=None):
        super().__init__()
        self.type = random.choice(['health', 'speed', 'rapid_fire'])
        
        if images:
            if self.type == 'health':
                self.image = images.get('health_powerup')
            elif self.type == 'speed':
                self.image = images.get('speed_powerup')
            elif self.type == 'rapid_fire':
                self.image = images.get('rapid_fire_powerup')
        else:
            self.image = pygame.Surface((20, 20))
            if self.type == 'health':
                self.image.fill((0, 255, 0))  # Green
            elif self.type == 'speed':
                self.image.fill((0, 0, 255))  # Blue
            elif self.type == 'rapid_fire':
                self.image.fill((255, 255, 255))  # White
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = 3
    
    def update(self):
        self.rect.x -= self.speed
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
