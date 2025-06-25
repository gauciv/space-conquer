"""
Power-up sprites for the Space Impact game.
"""
import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, images, powerup_type=None):
        super().__init__()
        
        # Randomly select power-up type if not specified
        if powerup_type is None:
            self.type = random.choice(['health', 'speed', 'rapid_fire', 'score_multiplier'])
        else:
            self.type = powerup_type
        
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
        
        # Create a hitbox that's slightly smaller than the sprite (90% of sprite size)
        # Power-ups should be easier to collect, so we use a larger hitbox ratio
        hitbox_width = int(self.rect.width * 0.9)
        hitbox_height = int(self.rect.height * 0.9)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
    
    def update(self):
        self.rect.x -= self.speed
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, surface):
        """Draw the powerup with visual effects."""
        # Draw the powerup
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
