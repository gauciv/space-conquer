"""
Bullet sprite for the Space Impact game.
"""
import pygame
from src.config import SCREEN_WIDTH

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
        """Draw the bullet with enhanced visual effects."""
        # Draw the bullet
        surface.blit(self.image, self.rect)
        
        # Debug: Draw hitbox (uncomment for debugging)
        # pygame.draw.rect(surface, (0, 255, 255), self.hitbox, 1)
        
        # Add a glowing trail effect
        trail_length = 20
        trail_segments = 5
        segment_length = trail_length / trail_segments
        
        for i in range(trail_segments):
            # Calculate position
            trail_x = self.rect.x - (i + 1) * segment_length
            trail_y = self.rect.centery
            
            # Calculate size (diminishing)
            trail_width = max(1, self.rect.width - i * 2)
            trail_height = max(1, self.rect.height - i)
            
            # Calculate alpha (fading)
            alpha = 200 - (i * 40)
            
            # Create trail segment
            trail_surface = pygame.Surface((trail_width, trail_height), pygame.SRCALPHA)
            trail_surface.fill((100, 150, 255, alpha))
            
            # Draw trail segment
            trail_rect = trail_surface.get_rect(center=(trail_x, trail_y))
            surface.blit(trail_surface, trail_rect)
