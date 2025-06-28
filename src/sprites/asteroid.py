"""
Asteroid sprite for the Space Impact game.
Asteroids are stationary objects that drop powerups when destroyed.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, images, sound_manager):
        super().__init__()
        self.image = images.get('asteroid')
        self.sound_manager = sound_manager
        
        # Check if image is None and provide a fallback
        if self.image is None:
            # Create a default colored surface
            self.image = pygame.Surface((50, 50))
            self.image.fill((150, 150, 150))  # Gray for asteroid
        
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        
        # Position the asteroid at a random position on the right side of the screen
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create a hitbox that matches the sprite size (same as enemies)
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.hitbox.center = self.rect.center
        
        # Asteroid properties
        self.health = 3  # Takes 3 hits to destroy
        self.speed = 1   # Very slow movement
        self.points = 45  # Points awarded for destroying (increased from 15 to 45, 3x)
        
        # Rotation properties
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(-1.0, 1.0)  # Degrees per frame
        
        # Animation properties for destruction
        self.is_exploding = False
        self.explosion_frame = 0
        self.explosion_max_frames = 8
        self.explosion_speed = 2  # Frames per update
        self.explosion_counter = 0
        
        # Powerup to drop when destroyed
        self.powerup_type = random.choice(['health', 'speed', 'rapid_fire', 'score_multiplier'])
        
        # Chance to drop a powerup (can be modified by game phases)
        self.powerup_drop_chance = 0.3  # 30% chance (3 out of 10 asteroids)
        
        # Damage to player on collision - increased to make asteroids more dangerous
        self.collision_damage = 3  # Increased from 1 to 3 (asteroids are massive and should be very dangerous)
        print(f"Asteroid created with collision_damage: {self.collision_damage}")
        
        # Visual effect properties
        self.glow_alpha = 0
        self.hit_flash = False
        self.hit_flash_duration = 0
    
    def update(self):
        if self.is_exploding:
            # Update explosion animation
            self.explosion_counter += 1
            if self.explosion_counter >= self.explosion_speed:
                self.explosion_counter = 0
                self.explosion_frame += 1
                
                # If explosion animation is complete, remove the asteroid
                if self.explosion_frame >= self.explosion_max_frames:
                    self.kill()
        else:
            # Move slowly from right to left
            self.rect.x -= self.speed
            
            # Rotate the asteroid
            self.angle += self.rotation_speed
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Keep the center position the same after rotation
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            # Update hitbox position to match the rotated image
            self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            self.hitbox.center = self.rect.center
            
            # Update hit flash effect
            if self.hit_flash:
                self.hit_flash_duration -= 1
                if self.hit_flash_duration <= 0:
                    self.hit_flash = False
            
            # Remove if it goes off-screen
            if self.rect.right < 0:
                self.kill()
    
    def take_damage(self, damage=1):
        """Handle asteroid taking damage."""
        if not self.is_exploding:
            self.health -= damage
            
            # Visual feedback for hit
            self.hit_flash = True
            self.hit_flash_duration = 5  # Flash for 5 frames
            
            # Play hit sound
            self.sound_manager.play_sound('explosion')
            
            # If health is depleted, start explosion animation
            if self.health <= 0:
                self.is_exploding = True
                return True  # Asteroid destroyed
        
        return False  # Asteroid not destroyed yet
    
    def draw(self, surface):
        """Draw the asteroid with simplified visual effects for better performance."""
        if self.is_exploding:
            # Draw simplified explosion animation
            explosion_size = int(self.rect.width * (1 + self.explosion_frame * 0.2))
            
            # Draw a simple circle for explosion
            explosion_color = (255, 100, 0)  # Orange
            explosion_rect = pygame.Rect(0, 0, explosion_size, explosion_size)
            explosion_rect.center = self.rect.center
            pygame.draw.circle(surface, explosion_color, self.rect.center, explosion_size // 2)
        else:
            # Draw the asteroid
            if self.hit_flash:
                # Create a white flash effect when hit (simplified)
                flash_surface = self.image.copy()
                flash_surface.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_ADD)
                surface.blit(flash_surface, self.rect)
            else:
                # Draw the asteroid image
                surface.blit(self.image, self.rect)
            
            # Draw hitbox if debug mode is enabled
            if DEBUG_HITBOXES:
                pygame.draw.rect(surface, (150, 150, 0), self.hitbox, 1)
    def should_drop_powerup(self):
        """Determine if the asteroid should drop a powerup based on the current chance."""
        return random.random() < self.powerup_drop_chance
