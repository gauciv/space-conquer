"""
Player sprite for the Space Impact game.
"""
import pygame
import time
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_SPEED, PLAYER_SHOOT_DELAY, DEBUG_HITBOXES
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, image, sound_manager):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        
        # Create a smaller hitbox for more precise collision detection
        self.hitbox = self.rect.inflate(-30, -20)  # 30px smaller on width, 20px smaller on height
        
        self.speed = PLAYER_INITIAL_SPEED
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()
        self.health = PLAYER_INITIAL_HEALTH
        self.max_health = PLAYER_INITIAL_HEALTH
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.sound_manager = sound_manager
        
        # Score multiplier
        self.score_multiplier = 1
        self.score_multiplier_timer = 0
        self.score_multiplier_duration = 600  # 10 seconds at 60 FPS
        
        # Invulnerability properties
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1500  # 1.5 seconds in milliseconds
        self.blink_timer = 0
        self.blink_interval = 100  # Blink every 100ms
        self.visible = True
        self.blink_color = (255, 255, 255)  # White for contrast
    
    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Shoot bullets
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Update bullets
        self.bullets.update()
        
        # Check rapid fire timer
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False
                self.shoot_delay = PLAYER_SHOOT_DELAY
        
        # Check score multiplier timer
        if self.score_multiplier > 1:
            self.score_multiplier_timer -= 1
            if self.score_multiplier_timer <= 0:
                self.score_multiplier = 1
        
        # Update invulnerability
        current_time = pygame.time.get_ticks()
        if self.invulnerable:
            # Check if invulnerability period is over
            if current_time - self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                self.visible = True
                self.image = self.original_image
            else:
                # Handle blinking effect
                if current_time - self.blink_timer > self.blink_interval:
                    self.blink_timer = current_time
                    self.visible = not self.visible
                    
                    if self.visible:
                        self.image = self.original_image
                    else:
                        # Create a colored version of the image for blinking
                        colored_image = self.original_image.copy()
                        colored_image.fill(self.blink_color, special_flags=pygame.BLEND_ADD)
                        self.image = colored_image
    
    def shoot(self, bullet_image=None):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery, bullet_image)
            self.bullets.add(bullet)
            
            # Add a second bullet if rapid fire is active
            if self.rapid_fire:
                bullet2 = Bullet(self.rect.right, self.rect.centery - 10, bullet_image)
                self.bullets.add(bullet2)
            
            # Play sound
            self.sound_manager.play_sound('shoot')
    
    def apply_powerup(self, powerup_type):
        if powerup_type == 'health':
            if self.health < self.max_health:
                self.health += 1
        elif powerup_type == 'speed':
            self.speed += 1
        elif powerup_type == 'rapid_fire':
            self.rapid_fire = True
            self.shoot_delay = 100
            self.rapid_fire_timer = 300  # Lasts for 300 frames (5 seconds at 60 FPS)
        elif powerup_type == 'score_multiplier':
            self.score_multiplier = 2
            self.score_multiplier_timer = self.score_multiplier_duration
    
    def take_damage(self):
        """Handle player taking damage with invulnerability period."""
        if not self.invulnerable:
            self.health -= 1
            self.sound_manager.play_sound('explosion')
            
            # Start invulnerability period
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            self.blink_timer = pygame.time.get_ticks()
            
            return True  # Damage was applied
        return False  # Player was invulnerable, no damage applied
    
    def draw(self, surface):
        """Draw the player with enhanced visual effects."""
        # Only draw if visible or not invulnerable
        if self.visible or not self.invulnerable:
            # Draw the player ship
            surface.blit(self.image, self.rect)
            
            # Draw hitbox if debug mode is enabled
            if DEBUG_HITBOXES:
                pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
            
            # Add engine glow effect
            engine_x = self.rect.left
            engine_y = self.rect.centery
            
            # Create pulsing effect
            pulse_factor = 0.7 + 0.3 * abs(math.sin(pygame.time.get_ticks() * 0.01))
            
            # Draw engine glow
            glow_radius = int(8 * pulse_factor)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            
            # Create gradient glow
            for r in range(glow_radius, 0, -1):
                alpha = int(200 * (r / glow_radius))
                color = (50, 100, 255, alpha)
                pygame.draw.circle(glow_surface, color, (glow_radius, glow_radius), r)
            
            # Draw the glow behind the ship
            surface.blit(glow_surface, (engine_x - glow_radius, engine_y - glow_radius))
            
            # Add shield effect when invulnerable
            if self.invulnerable:
                shield_radius = max(self.rect.width, self.rect.height) + 5
                shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
                
                # Create pulsing shield effect
                shield_pulse = 0.5 + 0.5 * abs(math.sin(pygame.time.get_ticks() * 0.01))
                shield_alpha = int(100 * shield_pulse)
                
                # Draw shield
                pygame.draw.circle(shield_surface, (100, 150, 255, shield_alpha), 
                                  (shield_radius, shield_radius), shield_radius)
                pygame.draw.circle(shield_surface, (150, 200, 255, shield_alpha), 
                                  (shield_radius, shield_radius), shield_radius, 2)
                
                # Draw the shield around the ship
                surface.blit(shield_surface, 
                            (self.rect.centerx - shield_radius, self.rect.centery - shield_radius))
        
        # Draw bullets with enhanced effects
        for bullet in self.bullets:
            bullet.draw(surface)
        
        # Draw rapid fire indicator if active
        if self.rapid_fire:
            # Create pulsing effect for the indicator
            pulse = 0.7 + 0.3 * abs(math.sin(pygame.time.get_ticks() * 0.01))
            indicator_color = (int(200 * pulse), int(200 * pulse), int(50 * pulse))
            
            # Draw indicator
            pygame.draw.circle(surface, indicator_color, (self.rect.right + 10, self.rect.top - 5), 5)
            pygame.draw.circle(surface, (255, 255, 100), (self.rect.right + 10, self.rect.top - 5), 5, 1)
