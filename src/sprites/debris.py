"""
Debris sprite for the Space Impact game.
Debris moves in a straight line and damages the player on collision.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Debris(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = images.get('debris')
        
        # Check if image is None and provide a fallback
        if self.image is None:
            # Create a default colored surface
            self.image = pygame.Surface((40, 30))
            self.image.fill((100, 100, 100))  # Dark gray for debris
        
        self.rect = self.image.get_rect()
        
        # Position the debris at a random position on the right side of the screen
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create a hitbox (85% of sprite size)
        hitbox_width = int(self.rect.width * 0.85)
        hitbox_height = int(self.rect.height * 0.85)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # Debris properties
        self.speed = random.randint(4, 7)  # Faster than normal enemies
        self.damage = 1  # Damage dealt to player on collision
        self.points = 5  # Points awarded for destroying
        self.health = 1  # Takes 1 hit to destroy
        
        # Add slight rotation for visual effect
        self.angle = 0
        self.rotation_speed = random.uniform(-2.0, 2.0)  # Degrees per frame
        self.original_image = self.image.copy()
    
    def update(self):
        # Move from right to left
        self.rect.x -= self.speed
        
        # Rotate the debris
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Keep the center position the same after rotation
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
    
    def take_damage(self, damage=1):
        """Handle debris taking damage."""
        self.health -= damage
        return self.health <= 0  # Return True if destroyed
    
    def draw(self, surface):
        """Draw the debris with simplified visual effects for better performance."""
        # Draw the debris
        surface.blit(self.image, self.rect)
        
        # Draw a simple trail (just a rectangle)
        trail_x = self.rect.x + self.rect.width
        trail_y = self.rect.centery - 2
        trail_width = 8
        trail_height = 4
        
        # Draw trail
        pygame.draw.rect(surface, (200, 100, 50, 100), 
                       (trail_x, trail_y, trail_width, trail_height))
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 100, 0), self.hitbox, 1)
