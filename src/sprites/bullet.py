"""
Bullet sprite for the Space Impact game.
"""
import pygame
from src.config import SCREEN_WIDTH, DEBUG_HITBOXES

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
        
        # Create a smaller hitbox for more precise collision detection
        # Bullets should have a very precise hitbox (60% of sprite size)
        self.hitbox = self.rect.inflate(-4, -2)  # 4px smaller on width, 2px smaller on height
    
    def update(self):
        self.rect.x += self.speed
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        # Remove if it goes off-screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
    def draw(self, surface):
        """Draw the bullet with simplified visual effects for better performance."""
        # Draw the bullet
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (0, 255, 255), self.hitbox, 1)
        
        # Add a simple trail (just a rectangle)
        trail_x = self.rect.x - 10
        trail_y = self.rect.centery - self.rect.height // 2
        trail_width = 10
        trail_height = self.rect.height
        
        # Draw trail
        pygame.draw.rect(surface, (100, 150, 255, 100), 
                       (trail_x, trail_y, trail_width, trail_height))
