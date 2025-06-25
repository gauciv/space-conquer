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
        
        # Trail effect properties
        self.trail_positions = []
        self.max_trail_length = 5
    
    def update(self):
        # Store current position for trail effect
        if len(self.trail_positions) >= self.max_trail_length:
            self.trail_positions.pop(0)
        self.trail_positions.append(self.rect.center)
        
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
        """Draw the debris with visual effects."""
        # Draw motion trail
        for i, pos in enumerate(self.trail_positions):
            # Calculate alpha based on position in trail
            alpha = int(100 * (i / len(self.trail_positions)))
            
            # Create a smaller, faded copy of the image for the trail
            trail_size = int(self.rect.width * 0.7)
            trail_surface = pygame.Surface((trail_size, trail_size), pygame.SRCALPHA)
            
            # Draw a fading circle for the trail
            pygame.draw.circle(trail_surface, (200, 100, 50, alpha), 
                             (trail_size // 2, trail_size // 2), 
                             trail_size // 2)
            
            # Position the trail
            trail_rect = trail_surface.get_rect(center=pos)
            surface.blit(trail_surface, trail_rect)
        
        # Draw the debris
        surface.blit(self.image, self.rect)
        
        # Add a subtle glow effect
        glow_size = self.rect.width + 6
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        
        # Draw the glow
        pygame.draw.circle(glow_surface, (200, 100, 50, 30), 
                         (glow_size // 2, glow_size // 2), 
                         glow_size // 2)
        
        # Draw the glow centered on the debris
        glow_rect = glow_surface.get_rect(center=self.rect.center)
        surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 100, 0), self.hitbox, 1)
