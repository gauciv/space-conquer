"""
Enemy sprites for the Space Impact game.
"""
import pygame
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type='normal', images=None):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Set default attributes
        self.health = 1
        self.speed = 5
        self.points = 10
        
        # Configure based on enemy type
        if enemy_type == 'normal':
            self.image = images.get('normal_enemy') if images else pygame.Surface((40, 40))
            if not images:
                self.image.fill((255, 0, 0))
            self.health = 1
            self.speed = random.randint(3, 7)
            self.points = 10
        elif enemy_type == 'fast':
            self.image = images.get('fast_enemy') if images else pygame.Surface((30, 20))
            if not images:
                self.image.fill((255, 0, 0))
            self.health = 1
            self.speed = random.randint(8, 12)
            self.points = 15
        elif enemy_type == 'tank':
            self.image = images.get('tank_enemy') if images else pygame.Surface((50, 50))
            if not images:
                self.image.fill((255, 0, 0))
            self.health = 3
            self.speed = random.randint(2, 4)
            self.points = 25
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def update(self):
        self.rect.x -= self.speed
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
