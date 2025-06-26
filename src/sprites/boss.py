"""
Boss sprites for the Space Impact game.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES
from .bullet import Bullet

class Boss(pygame.sprite.Sprite):
    """Base class for boss enemies."""
    def __init__(self, boss_type, asset_loader, sound_manager):
        super().__init__()
        self.boss_type = boss_type
        self.sound_manager = sound_manager
        
        # Set image based on boss type
        if boss_type == 'mini':
            self.image = asset_loader.get_image('mini_boss')
            self.name = "Vanguard"
            self.max_health = 50  # Doubled from 25 to 50
            self.health = self.max_health
            self.speed = 2
            self.shoot_delay = 1000  # milliseconds
            self.bullet_speed = -8  # Negative because bullets move left
            self.bullet_damage = 1
            self.score_value = 250
            self.movement_pattern = "sine"
        else:  # main boss
            self.image = asset_loader.get_image('main_boss')
            self.name = "Dreadnought"
            self.max_health = 100  # Doubled from 50 to 100
            self.health = self.max_health
            self.speed = 1.5
            self.shoot_delay = 800  # milliseconds
            self.bullet_speed = -10
            self.bullet_damage = 2
            self.score_value = 500
            self.movement_pattern = "complex"
        
        # Common properties
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 50  # Start off-screen
        self.rect.centery = SCREEN_HEIGHT // 2
        
        # Create a custom hitbox based on boss type (85% of sprite size for better gameplay)
        hitbox_width = int(self.rect.width * 0.85)
        hitbox_height = int(self.rect.height * 0.85)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.entry_complete = False
        self.movement_timer = 0
        self.movement_direction = 1  # 1 for down, -1 for up
        self.movement_change_delay = 120  # frames before changing direction
        
        # Health bar images
        self.health_bar_bg = asset_loader.get_image('health_bar_bg')
        self.health_bar_fill = asset_loader.get_image('health_bar_fill')
        
        # For complex movement pattern
        self.angle = 0
        self.center_y = SCREEN_HEIGHT // 2
        self.amplitude = 100  # How far up/down the boss moves
        self.frequency = 0.02  # How fast the boss moves up/down
        
        # Death animation properties
        self.dying = False
        self.death_animation_start = 0
        self.death_animation_duration = 1500  # 1.5 seconds
        self.explosion_particles = []
    
    def update(self):
        """Update the boss state."""
        # If dying, update death animation
        if self.dying:
            # Update death animation and check if it's complete
            animation_complete = self.update_death_animation()
            return animation_complete
            
        # Entry movement - move from right edge to battle position
        if not self.entry_complete:
            self.rect.x -= 3
            if self.rect.right < SCREEN_WIDTH - 100:
                self.entry_complete = True
                self.last_shot = pygame.time.get_ticks()  # Reset shot timer when entry is complete
        else:
            # Different movement patterns based on boss type
            if self.movement_pattern == "sine":
                # Sine wave movement
                self.movement_timer += 1
                self.rect.centery = self.center_y + math.sin(self.movement_timer * 0.05) * self.amplitude
            
            elif self.movement_pattern == "complex":
                # More complex movement with occasional direction changes
                self.movement_timer += 1
                
                # Change direction occasionally
                if self.movement_timer % self.movement_change_delay == 0:
                    self.movement_direction = random.choice([-1, 1])
                    self.movement_change_delay = random.randint(60, 180)  # Random delay before next change
                
                # Move up/down with some randomness
                self.rect.y += self.speed * self.movement_direction
                
                # Ensure boss stays on screen
                if self.rect.top < 50:
                    self.rect.top = 50
                    self.movement_direction = 1
                elif self.rect.bottom > SCREEN_HEIGHT - 50:
                    self.rect.bottom = SCREEN_HEIGHT - 50
                    self.movement_direction = -1
            
            # Shoot bullets
            self.shoot()
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Update bullets
        self.bullets.update()
        
        return False  # Not finished dying
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            if self.boss_type == 'mini':
                # Mini boss shoots 2 bullets
                bullet1 = BossBullet(self.rect.left, self.rect.centery - 10, self.bullet_speed, self.bullet_damage)
                bullet2 = BossBullet(self.rect.left, self.rect.centery + 10, self.bullet_speed, self.bullet_damage)
                self.bullets.add(bullet1, bullet2)
            else:
                # Main boss shoots 3 bullets in a spread pattern
                bullet1 = BossBullet(self.rect.left, self.rect.centery, self.bullet_speed, self.bullet_damage)
                bullet2 = BossBullet(self.rect.left, self.rect.centery - 15, self.bullet_speed, self.bullet_damage)
                bullet3 = BossBullet(self.rect.left, self.rect.centery + 15, self.bullet_speed, self.bullet_damage)
                
                # Add some vertical velocity to the top and bottom bullets
                bullet2.vy = -1
                bullet3.vy = 1
                
                self.bullets.add(bullet1, bullet2, bullet3)
            
            # Play sound
            self.sound_manager.play_sound('shoot')
    
    def take_damage(self, damage=1):
        """Handle boss taking damage."""
        # Prevent damage during entrance
        if not self.entry_complete:
            return False
            
        self.health -= damage
        self.sound_manager.play_sound('explosion')
        
        # Check if boss is defeated
        if self.health <= 0 and not self.dying:
            self.destroy()
            return True
        return False
    
    def destroy(self):
        """Handle boss destruction with animation."""
        # Set dying state
        self.dying = True
        self.death_animation_start = pygame.time.get_ticks()
        self.explosion_particles = []
        
        # Create explosion particles
        for _ in range(20):
            particle = {
                'x': self.rect.centerx + random.randint(-self.rect.width//2, self.rect.width//2),
                'y': self.rect.centery + random.randint(-self.rect.height//2, self.rect.height//2),
                'size': random.randint(5, 15),
                'speed_x': random.uniform(-3, 3),
                'speed_y': random.uniform(-3, 3),
                'color': random.choice([(255, 100, 0), (255, 200, 0), (255, 50, 0), (200, 0, 0)]),
                'lifetime': random.randint(30, 60)  # frames
            }
            self.explosion_particles.append(particle)
        
        # Play explosion sound
        self.sound_manager.play_sound('explosion')
        
    def update_death_animation(self):
        """Update the death animation."""
        # Update explosion particles
        for particle in self.explosion_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
        
        # Check if animation is complete
        current_time = pygame.time.get_ticks()
        if current_time - self.death_animation_start > self.death_animation_duration:
            # Clear any remaining bullets
            for bullet in list(self.bullets):
                bullet.kill()
            self.bullets.empty()
            return True  # Animation complete, boss can be removed
        return False
    
    def draw_health_bar(self, surface):
        """Draw the boss health bar at the top of the screen."""
        # Don't draw health bar if dying
        if self.dying:
            return
            
        # Position the health bar at the top center
        bar_x = (SCREEN_WIDTH - self.health_bar_bg.get_width()) // 2
        bar_y = 10
        
        # Draw the background
        surface.blit(self.health_bar_bg, (bar_x, bar_y))
        
        # Calculate the width of the fill based on current health
        fill_width = int((self.health / self.max_health) * (self.health_bar_bg.get_width() - 2))
        
        # Create a subsurface of the fill image with the correct width
        if fill_width > 0:
            fill_rect = pygame.Rect(0, 0, fill_width, self.health_bar_fill.get_height())
            fill_surface = self.health_bar_fill.subsurface(fill_rect)
            surface.blit(fill_surface, (bar_x + 1, bar_y + 1))
        
        # Draw the boss name and health
        font = pygame.font.SysFont('Arial', 16)
        text = font.render(f"{self.name}: {self.health}/{self.max_health}", True, (255, 255, 255))
        surface.blit(text, (bar_x + (self.health_bar_bg.get_width() - text.get_width()) // 2, bar_y + 16))
    
    def draw(self, surface):
        """Draw the boss and its bullets."""
        if self.dying:
            self.draw_death_animation(surface)
        else:
            surface.blit(self.image, self.rect)
            
            # Draw hitbox if debug mode is enabled
            if DEBUG_HITBOXES:
                pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Always draw bullets
        self.bullets.draw(surface)
        
        # Draw health bar if not dying
        if not self.dying:
            self.draw_health_bar(surface)
            
    def draw_death_animation(self, surface):
        """Draw the death animation."""
        # Draw explosion particles
        for particle in self.explosion_particles:
            pygame.draw.circle(
                surface, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
            
        # Draw fading boss sprite
        alpha = 255 * (1 - (pygame.time.get_ticks() - self.death_animation_start) / self.death_animation_duration)
        if alpha > 0:
            # Create a copy of the image with transparency
            temp_image = self.image.copy()
            temp_image.set_alpha(int(alpha))
            surface.blit(temp_image, self.rect)


class BossBullet(pygame.sprite.Sprite):
    """Bullets fired by bosses."""
    def __init__(self, x, y, speed, damage):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 100, 100))  # Red bullet
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speed = speed
        self.damage = damage
        self.vx = speed
        self.vy = 0  # Can be set for angled shots
        
        # Create a smaller hitbox for more precise collision detection
        self.hitbox = self.rect.inflate(-2, -1)  # 2px smaller on width, 1px smaller on height
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Remove if off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
