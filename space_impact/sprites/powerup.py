"""
Power-up sprites for the Space Impact game.
"""
import pygame
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        
        # Randomly select power-up type
        self.type = random.choice(['health', 'speed', 'rapid_fire', 'score_multiplier'])
        
        # Set image based on power-up type
        if self.type == 'health':
            self.image = images.get('health_powerup')
        elif self.type == 'speed':
            self.image = images.get('speed_powerup')
        elif self.type == 'rapid_fire':
            self.image = images.get('rapid_fire_powerup')
        elif self.type == 'score_multiplier':
            self.image = images.get('score_multiplier')
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.randint(2, 4)
    
    def update(self):
        self.rect.x -= self.speed
        
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
