"""
Enemy sprites for the Space Impact game.
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
            self.image = images.get('normal_enemy')
            self.health = 1
            self.speed = 3
            self.points = 10
            self.movement_pattern = "straight"
            # Normal enemy has a slightly smaller hitbox (80% of sprite size)
            self.hitbox_ratio = 0.8
        elif enemy_type == 'fast':
            self.image = images.get('fast_enemy')
            self.health = 1
            self.speed = 5
            self.points = 15
            self.movement_pattern = "zigzag"
            # Fast enemy has an even smaller hitbox (70% of sprite size) since it's harder to hit
            self.hitbox_ratio = 0.7
        elif enemy_type == 'tank':
            self.image = images.get('tank_enemy')
            self.health = 3
            self.speed = 2
            self.points = 25
            self.movement_pattern = "straight"
            # Tank enemy has a larger hitbox (90% of sprite size) since it's a bigger target
            self.hitbox_ratio = 0.9
        elif enemy_type == 'drone':
            # Fallback to normal enemy if drone image is not available
            self.image = images.get('normal_enemy')
            self.health = 1
            self.speed = 4
            self.points = 20
            self.movement_pattern = "sine"
            # Drone enemy has a medium hitbox (75% of sprite size)
            self.hitbox_ratio = 0.75
        elif enemy_type == 'bomber':
            # Fallback to tank enemy if bomber image is not available
            self.image = images.get('tank_enemy')
            self.health = 2
            self.speed = 2
            self.points = 30
            self.movement_pattern = "dive"
            # Bomber enemy has a larger hitbox (85% of sprite size)
            self.hitbox_ratio = 0.85
        else:
            # Default to normal enemy for any unknown type
            self.image = images.get('normal_enemy')
            self.health = 1
            self.speed = 3
            self.points = 10
            self.movement_pattern = "straight"
            self.hitbox_ratio = 0.8
        
        # Check if image is None and provide a fallback
        if self.image is None:
            # Create a default colored surface
            self.image = pygame.Surface((50, 30))
            if enemy_type == 'normal':
                self.image.fill((255, 0, 0))  # Red for normal
            elif enemy_type == 'fast':
                self.image.fill((255, 255, 0))  # Yellow for fast
            elif enemy_type == 'tank':
                self.image.fill((0, 0, 255))  # Blue for tank
            elif enemy_type == 'drone':
                self.image.fill((0, 255, 0))  # Green for drone
            elif enemy_type == 'bomber':
                self.image.fill((255, 0, 255))  # Purple for bomber
            else:
                self.image.fill((128, 128, 128))  # Gray for unknown
        
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
    
    def update(self):
        # Move based on movement pattern
        if self.movement_pattern == "straight":
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
        """Draw the enemy with enhanced visual effects."""
        # Draw the enemy ship
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Add engine glow effect based on enemy type
        engine_x = self.rect.right
        engine_y = self.rect.centery
        
        # Create pulsing effect
        pulse_factor = 0.7 + 0.3 * abs(math.sin(pygame.time.get_ticks() * 0.01))
        
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
        
        # Draw engine glow
        glow_radius = int(6 * pulse_factor)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Create gradient glow
        for r in range(glow_radius, 0, -1):
            alpha = int(150 * (r / glow_radius))
            color = (glow_color[0], glow_color[1], glow_color[2], alpha)
            pygame.draw.circle(glow_surface, color, (glow_radius, glow_radius), r)
        
        # Draw the glow behind the ship
        surface.blit(glow_surface, (engine_x - glow_radius, engine_y - glow_radius))
        
        # Add health indicator for enemies with more than 1 health
        if self.health > 1:
            health_width = 20
            health_height = 3
            health_x = self.rect.centerx - health_width // 2
            health_y = self.rect.top - 8
            
            # Draw health background
            pygame.draw.rect(surface, (50, 50, 50, 150), 
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
            
        # Add special effects for different movement patterns
        if self.movement_pattern == "zigzag":
            # Add motion trail
            trail_alpha = 100
            for i in range(3):
                offset = (i + 1) * self.speed
                trail_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                trail_surface.fill((255, 100, 0, trail_alpha // (i + 1)))
                trail_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(trail_surface, (self.rect.x + offset, self.rect.y))
                
        elif self.movement_pattern == "dive" and self.dive_state == "dive":
            # Add dive effect
            pygame.draw.line(surface, (255, 255, 0, 150), 
                           (self.rect.centerx, self.rect.centery), 
                           (self.rect.centerx + 20, self.rect.centery), 2)
