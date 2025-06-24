"""
Bullet sprite for the Space Impact game.
"""
import pygame
from ..config import SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        self.image = image if image else pygame.Surface((10, 5))
        if image is None:
            self.image.fill((255, 255, 255))  # Default white bullet if no image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10
    
    def update(self):
        self.rect.x += self.speed
        # Remove if it goes off-screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
