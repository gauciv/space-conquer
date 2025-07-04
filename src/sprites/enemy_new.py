"""
Enemy sprites for the Space Impact game.
Only includes the three main enemy types: normal (low-type), fast (elite-type), and tank (super-type).
Mini-boss and boss are handled separately.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, images):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Set image based on enemy type
        if enemy_type == 'normal':
            self.image = images.get('normal_enemy')  # SE-monster-lower
            self.health = 1
            self.speed = 3
            self.points = 10
            self.movement_pattern = "straight"
            # Normal enemy has a slightly smaller hitbox (80% of sprite size)
            self.hitbox_ratio = 0.8
        elif enemy_type == 'fast':
            self.image = images.get('fast_enemy')  # SE-monster-elite
            self.health = 1
            self.speed = 5
            self.points = 15
            self.movement_pattern = "zigzag"
            # Fast enemy has an even smaller hitbox (70% of sprite size) since it's harder to hit
            self.hitbox_ratio = 0.7
        elif enemy_type == 'tank':
            self.image = images.get('tank_enemy')  # SE-monster-super
            self.health = 3
            self.speed = 2
            self.points = 25
            self.movement_pattern = "straight"
            # Tank enemy has a larger hitbox (90% of sprite size) since it's a bigger target
            self.hitbox_ratio = 0.9
        else:
            # Default to normal enemy if type is not recognized
            self.image = images.get('normal_enemy')
            self.health = 1
            self.speed = 3
            self.points = 10
            self.movement_pattern = "straight"
            self.hitbox_ratio = 0.8
        
        # Check if image is None and provide a fallback
        if self.image is None:
            # Create a default colored surface
            self.image = pygame.Surface((40, 30))
            if enemy_type == 'normal':
                self.image.fill((255, 0, 0))  # Red for normal
            elif enemy_type == 'fast':
                self.image.fill((255, 165, 0))  # Orange for fast
            elif enemy_type == 'tank':
                self.image.fill((128, 0, 128))  # Purple for tank
            else:
                self.image.fill((255, 0, 0))  # Default red
        
        self.rect = self.image.get_rect()
        
        # Position the enemy at a random position on the right side of the screen
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create a hitbox based on the ratio
        hitbox_width = int(self.rect.width * self.hitbox_ratio)
        hitbox_height = int(self.rect.height * self.hitbox_ratio)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # Movement pattern variables
        if self.movement_pattern == "zigzag":
            self.zigzag_direction = 1  # 1 for down, -1 for up
            self.zigzag_counter = 0
            self.zigzag_change = random.randint(10, 20)  # Change direction every 10-20 frames
        elif self.movement_pattern == "sine":
            self.sine_offset = random.uniform(0, 6.28)  # Random starting point in the sine wave
            self.sine_speed = random.uniform(0.05, 0.1)  # Speed of the sine wave
            self.sine_amplitude = random.randint(20, 40)  # Amplitude of the sine wave
            self.original_y = self.rect.y  # Store original y position
        elif self.movement_pattern == "dive":
            self.dive_state = "approach"  # States: approach, dive, retreat
            self.dive_speed = random.randint(4, 7)
            self.target_y = random.randint(100, SCREEN_HEIGHT - 100)  # Target y position for dive
    
    def update(self):
        """Update enemy position based on movement pattern."""
        if self.movement_pattern == "straight":
            # Simple left movement
            self.rect.x -= self.speed
        elif self.movement_pattern == "zigzag":
            # Zigzag movement
            self.rect.x -= self.speed
            self.rect.y += self.zigzag_direction * self.speed
            
            # Change direction periodically
            self.zigzag_counter += 1
            if self.zigzag_counter >= self.zigzag_change:
                self.zigzag_direction *= -1
                self.zigzag_counter = 0
                self.zigzag_change = random.randint(10, 20)
            
            # Ensure enemy stays within screen bounds
            if self.rect.top < 10:
                self.rect.top = 10
                self.zigzag_direction = 1
            elif self.rect.bottom > SCREEN_HEIGHT - 10:
                self.rect.bottom = SCREEN_HEIGHT - 10
                self.zigzag_direction = -1
        elif self.movement_pattern == "sine":
            # Sine wave movement
            self.rect.x -= self.speed
            time = pygame.time.get_ticks() * self.sine_speed + self.sine_offset
            self.rect.y = self.original_y + math.sin(time) * self.sine_amplitude
        elif self.movement_pattern == "dive":
            # Dive movement pattern
            if self.dive_state == "approach":
                # Move towards the right side of the screen
                self.rect.x -= self.speed
                
                # Start dive when reaching a certain point
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
    
    def take_damage(self, damage=1):
        """Handle enemy taking damage."""
        self.health -= damage
        return self.health <= 0  # Return True if destroyed
