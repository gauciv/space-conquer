"""
Star background elements for the Space Impact game.
"""
import pygame
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 3)
        self.color = WHITE
    
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)
