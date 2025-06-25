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
        
        # Create a hitbox (90% of sprite size)
        hitbox_width = int(self.rect.width * 0.9)
        hitbox_height = int(self.rect.height * 0.9)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # Asteroid properties
        self.health = 3  # Takes 3 hits to destroy
        self.speed = 1   # Very slow movement
        self.points = 15  # Points awarded for destroying
        
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
            
            # Update hitbox position to follow the rect
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
        """Draw the asteroid with visual effects."""
        if self.is_exploding:
            # Draw explosion animation
            explosion_size = int(self.rect.width * (1 + self.explosion_frame * 0.2))
            
            # Create explosion surface with transparency
            explosion_surface = pygame.Surface((explosion_size, explosion_size), pygame.SRCALPHA)
            
            # Draw explosion circle with fading opacity
            max_alpha = 255
            current_alpha = max(0, max_alpha - (self.explosion_frame * 30))
            
            # White core
            pygame.draw.circle(explosion_surface, (255, 255, 255, current_alpha), 
                             (explosion_size // 2, explosion_size // 2), 
                             explosion_size // 4)
            
            # Orange middle
            pygame.draw.circle(explosion_surface, (255, 165, 0, current_alpha), 
                             (explosion_size // 2, explosion_size // 2), 
                             explosion_size // 3)
            
            # Red outer
            pygame.draw.circle(explosion_surface, (255, 0, 0, current_alpha // 2), 
                             (explosion_size // 2, explosion_size // 2), 
                             explosion_size // 2)
            
            # Add particles
            for _ in range(10):
                particle_angle = random.uniform(0, math.pi * 2)
                particle_distance = random.uniform(0, explosion_size // 2)
                particle_x = explosion_size // 2 + math.cos(particle_angle) * particle_distance
                particle_y = explosion_size // 2 + math.sin(particle_angle) * particle_distance
                particle_size = random.randint(2, 5)
                particle_color = (255, 255, 200, 150)  # Light yellow with transparency
                
                pygame.draw.circle(explosion_surface, particle_color, 
                                 (int(particle_x), int(particle_y)), 
                                 particle_size)
            
            # Draw the explosion centered on the asteroid
            explosion_rect = explosion_surface.get_rect(center=self.rect.center)
            surface.blit(explosion_surface, explosion_rect)
        else:
            # Draw the asteroid
            if self.hit_flash:
                # Create a white flash effect when hit
                flash_surface = self.image.copy()
                flash_surface.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_ADD)
                surface.blit(flash_surface, self.rect)
            else:
                surface.blit(self.image, self.rect)
            
            # Add a subtle glow effect
            glow_size = self.rect.width + 10
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Pulsating glow
            time = pygame.time.get_ticks() * 0.001
            glow_alpha = 30 + 20 * math.sin(time * 2)
            
            # Draw the glow
            pygame.draw.circle(glow_surface, (100, 100, 150, int(glow_alpha)), 
                             (glow_size // 2, glow_size // 2), 
                             glow_size // 2)
            
            # Draw the glow centered on the asteroid
            glow_rect = glow_surface.get_rect(center=self.rect.center)
            surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)
            
            # Draw hitbox if debug mode is enabled
            if DEBUG_HITBOXES:
                pygame.draw.rect(surface, (150, 150, 0), self.hitbox, 1)
