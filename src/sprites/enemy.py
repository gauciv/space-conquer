"""
Enemy sprites for the Space Impact game.
Five enemy types: low-type, elite-type, super-type, mini-boss, and boss.
"""
import pygame
import random
import math
import time
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, images):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Set image based on enemy type
        if enemy_type == 'low':
            self.image = images.get('normal_enemy')
            self.health = 1
            self.base_speed = 3
            self.points = 30  # Already includes 3x multiplier
            self.movement_pattern = "oscillate"  # New movement pattern for low-type
            # Low-type enemy has a slightly smaller hitbox (80% of sprite size)
            self.hitbox_ratio = 0.8
            
            # Special properties for low-type enemy
            self.oscillation_amplitude = random.randint(10, 20)  # Horizontal oscillation range
            self.oscillation_speed = random.uniform(0.05, 0.1)  # How fast it oscillates
            self.oscillation_angle = random.random() * 6.28  # Random start angle
            
            # Stutter behavior (periodically slows down)
            self.stutter_timer = random.uniform(3.0, 5.0)  # Time until next stutter
            self.stutter_duration = 0.0  # Current stutter duration
            self.is_stuttering = False
            self.last_time = time.time()
            
            # Attack pattern
            self.fire_rate = random.uniform(2.0, 3.0)  # Time between shots
            self.time_since_last_shot = random.uniform(0, 1.5)  # Randomize initial shot timing
            self.is_telegraphing = False  # Whether it's about to shoot
            self.telegraph_duration = 0.3  # How long the telegraph lasts
            self.telegraph_timer = 0.0
            
        elif enemy_type == 'elite':
            self.image = images.get('fast_enemy')
            self.health = 1
            self.base_speed = 5
            self.points = 45  # Already includes 3x multiplier
            self.movement_pattern = "zigzag"
            # Elite enemy has an even smaller hitbox (70% of sprite size) since it's harder to hit
            self.hitbox_ratio = 0.7
            
        elif enemy_type == 'super':
            self.image = images.get('tank_enemy')
            self.health = 3
            self.base_speed = 2
            self.points = 75  # Already includes 3x multiplier
            self.movement_pattern = "straight"
            # Super enemy has a larger hitbox (90% of sprite size) since it's a bigger target
            self.hitbox_ratio = 0.9
            
        else:
            # Default to low-type enemy for any unknown type
            self.image = images.get('normal_enemy')
            self.health = 1
            self.base_speed = 3
            self.points = 30
            self.movement_pattern = "straight"
            self.hitbox_ratio = 0.8
            self.base_speed = 3
            self.points = 10
            self.movement_pattern = "straight"
            self.hitbox_ratio = 0.8
        
        # Speed multiplier (for time-based difficulty)
        self.speed_multiplier = 1.0
        self.speed = self.base_speed
        
        # Check if image is None and provide a fallback
        if self.image is None:
            # Create a default colored surface
            self.image = pygame.Surface((50, 30))
            if enemy_type == 'low':
                self.image.fill((255, 0, 0))  # Red for low-type
            elif enemy_type == 'elite':
                self.image.fill((255, 255, 0))  # Yellow for elite-type
            elif enemy_type == 'super':
                self.image.fill((0, 0, 255))  # Blue for super-type
            else:
                self.image.fill((128, 128, 128))  # Gray for unknown
        
        # Store the original image for the low-type enemy's telegraph effect
        self.original_image = self.image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create a custom hitbox based on enemy type
        hitbox_width = int(self.rect.width * self.hitbox_ratio)
        hitbox_height = int(self.rect.height * self.hitbox_ratio)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # For zigzag movement
        self.direction = 1  # 1 for down, -1 for up
        self.direction_change_timer = 0
        self.direction_change_delay = random.randint(20, 40)  # frames before changing direction
        
        # For sine wave movement
        self.angle = random.random() * 6.28  # Random start angle
        self.center_y = self.rect.centery
        self.amplitude = random.randint(30, 70)  # How far up/down the enemy moves
        self.frequency = random.uniform(0.05, 0.1)  # How fast the enemy moves up/down
        
        # For dive movement
        self.dive_state = "approach"  # approach, dive, retreat
        self.target_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.dive_speed = self.speed * 1.5
        
        # For bullet firing (low-type enemy)
        self.bullets = []  # Store bullets here
        
    def update(self):
        # Get current time for time-based behaviors
        current_time = time.time()
        delta_time = current_time - self.last_time if hasattr(self, 'last_time') else 0.016
        self.last_time = current_time
        
        # Apply speed multiplier
        self.speed = self.base_speed * self.speed_multiplier
        
        # Update low-type enemy specific behaviors
        if self.enemy_type == 'low' and self.movement_pattern == "oscillate":
            # Update stutter timer
            if not self.is_stuttering:
                self.stutter_timer -= delta_time
                if self.stutter_timer <= 0:
                    # Start stuttering
                    self.is_stuttering = True
                    self.stutter_duration = 0.5  # Stutter for 0.5 seconds
                    self.stutter_timer = random.uniform(3.0, 5.0)  # Reset timer for next stutter
            else:
                # Currently stuttering
                self.stutter_duration -= delta_time
                if self.stutter_duration <= 0:
                    self.is_stuttering = False
            
            # Calculate actual speed based on stutter state
            actual_speed = self.speed * 0.5 if self.is_stuttering else self.speed
            
            # Move horizontally with oscillation
            self.rect.x -= actual_speed
            
            # Update oscillation angle
            self.oscillation_angle += self.oscillation_speed
            
            # Apply horizontal oscillation
            oscillation = math.sin(self.oscillation_angle) * self.oscillation_amplitude
            self.rect.x += oscillation * delta_time * 60  # Scale by delta_time and target 60 FPS
            
            # Update attack pattern
            self.time_since_last_shot += delta_time
            
            # Check if it's time to telegraph the shot
            if not self.is_telegraphing and self.time_since_last_shot >= self.fire_rate - self.telegraph_duration:
                self.is_telegraphing = True
                self.telegraph_timer = self.telegraph_duration
                
                # Create a brightened version of the image for telegraph effect
                bright_image = self.original_image.copy()
                bright_overlay = pygame.Surface(bright_image.get_size(), pygame.SRCALPHA)
                bright_overlay.fill((50, 50, 100, 0))
                bright_image.blit(bright_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                self.image = bright_image
            
            # Update telegraph timer
            if self.is_telegraphing:
                self.telegraph_timer -= delta_time
                if self.telegraph_timer <= 0:
                    self.is_telegraphing = False
                    self.image = self.original_image.copy()  # Reset image
                    
                    # Fire a shot
                    if self.time_since_last_shot >= self.fire_rate:
                        self.fire_shot()
                        self.time_since_last_shot = 0
                        self.fire_rate = random.uniform(2.0, 3.0)  # Randomize next shot timing
        
        # Other movement patterns remain the same
        elif self.movement_pattern == "straight":
            self.rect.x -= self.speed
        
        elif self.movement_pattern == "zigzag":
            self.rect.x -= self.speed
            self.rect.y += self.speed * self.direction
            
            # Change direction periodically
            self.direction_change_timer += 1
            if self.direction_change_timer >= self.direction_change_delay:
                self.direction *= -1
                self.direction_change_timer = 0
                self.direction_change_delay = random.randint(20, 40)
            
            # Keep within screen bounds
            if self.rect.top < 10:
                self.rect.top = 10
                self.direction = 1
            elif self.rect.bottom > SCREEN_HEIGHT - 10:
                self.rect.bottom = SCREEN_HEIGHT - 10
                self.direction = -1
        
        elif self.movement_pattern == "sine":
            self.rect.x -= self.speed
            self.angle += self.frequency
            self.rect.centery = self.center_y + int(self.amplitude * math.sin(self.angle))
            
            # Keep within screen bounds
            if self.rect.top < 10:
                self.rect.top = 10
            elif self.rect.bottom > SCREEN_HEIGHT - 10:
                self.rect.bottom = SCREEN_HEIGHT - 10
        
        elif self.movement_pattern == "dive":
            if self.dive_state == "approach":
                # Move towards the screen
                self.rect.x -= self.speed
                
                # When reaching a certain x position, start diving
                if self.rect.x < SCREEN_WIDTH * 0.7:
                    self.dive_state = "dive"
            
            elif self.dive_state == "dive":
                # Dive towards the target y position
                self.rect.x -= self.speed * 0.5  # Slow down x movement during dive
                
                if self.rect.centery < self.target_y:
                    self.rect.y += self.dive_speed
                    if self.rect.centery >= self.target_y:
                        self.dive_state = "retreat"
                else:
                    self.rect.y -= self.dive_speed
                    if self.rect.centery <= self.target_y:
                        self.dive_state = "retreat"
            
            elif self.dive_state == "retreat":
                # Retreat after dive
                self.rect.x -= self.speed * 1.5  # Faster x movement during retreat
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
            
    def draw(self, surface):
        """Draw the enemy with simplified visual effects for better performance."""
        # Draw the enemy ship
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Add simplified engine glow effect
        engine_x = self.rect.right
        engine_y = self.rect.centery
        
        # Different colors for different enemy types
        if self.enemy_type == 'normal':
            glow_color = (255, 50, 50)  # Red
        elif self.enemy_type == 'fast':
            glow_color = (255, 150, 0)  # Orange
        elif self.enemy_type == 'tank':
            glow_color = (150, 0, 255)  # Purple
        elif self.enemy_type == 'drone':
            glow_color = (0, 255, 150)  # Cyan
        elif self.enemy_type == 'bomber':
            glow_color = (255, 255, 0)  # Yellow
        else:
            glow_color = (255, 0, 0)  # Default red
        
        # Draw simplified engine glow (just a rectangle)
        glow_rect = pygame.Rect(engine_x - 2, engine_y - 3, 6, 6)
        pygame.draw.rect(surface, glow_color, glow_rect)
        
        # Add health indicator for enemies with more than 1 health (simplified)
        if self.health > 1:
            health_width = 20
            health_height = 3
            health_x = self.rect.centerx - health_width // 2
            health_y = self.rect.top - 8
            
            # Draw health background
            pygame.draw.rect(surface, (50, 50, 50), 
                           (health_x, health_y, health_width, health_height))
            
            # Draw health bar
            health_percent = self.health / 3  # Assuming max health is 3
            health_fill_width = int(health_width * health_percent)
            
            # Health color based on percentage
            if health_percent > 0.7:
                health_color = (0, 255, 0)  # Green
            elif health_percent > 0.3:
                health_color = (255, 255, 0)  # Yellow
            else:
                health_color = (255, 0, 0)  # Red
                
            pygame.draw.rect(surface, health_color, 
                           (health_x, health_y, health_fill_width, health_height))
