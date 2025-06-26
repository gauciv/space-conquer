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
        
        # Damage cooldown system
        self.damage_cooldown = {}  # Dictionary to track cooldown for different damage sources
        self.damage_cooldown_duration = 1000  # 1 second cooldown between damage from same source
    
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
        
        # Handle shooting with SPACE key
        if keys[pygame.K_SPACE]:
            # Get bullet image from asset loader if available
            bullet_image = None
            if hasattr(self, 'asset_loader'):
                bullet_image = self.asset_loader.get_image('bullet')
            self.shoot(bullet_image)
        
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
        
        # Update bullets
        self.bullets.update()
        
        # Check for rapid fire timer
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False
        
        # Check for score multiplier timer
        if self.score_multiplier > 1:
            self.score_multiplier_timer -= 1
            if self.score_multiplier_timer <= 0:
                self.score_multiplier = 1
        
        # Check for invulnerability timer
        current_time = pygame.time.get_ticks()
        if self.invulnerable:
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
        
        # Update damage cooldowns
        current_time = pygame.time.get_ticks()
        for source_id in list(self.damage_cooldown.keys()):
            if current_time - self.damage_cooldown[source_id] > self.damage_cooldown_duration:
                del self.damage_cooldown[source_id]
    
    def shoot(self, bullet_image=None):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Create bullet with proper image
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
                return True
            return False
        elif powerup_type == 'speed':
            self.speed += 1
            return True
        elif powerup_type == 'rapid_fire':
            self.rapid_fire = True
            self.rapid_fire_timer = 300  # 5 seconds at 60 FPS
            return True
        elif powerup_type == 'score_multiplier':
            self.score_multiplier = 2
            self.score_multiplier_timer = self.score_multiplier_duration
            return True
        return False
    
    def take_damage(self, god_mode=False, source_id=None):
        """
        Apply damage to the player with cooldown system.
        
        Args:
            god_mode (bool): If True, player takes no damage
            source_id: Unique identifier for the damage source (enemy, boss, etc.)
                      Used to track cooldown for each source separately
        
        Returns:
            bool: True if damage was applied, False otherwise
        """
        if god_mode:
            return False
            
        # If no source_id provided, generate a random one (not ideal but prevents errors)
        if source_id is None:
            source_id = f"unknown_{pygame.time.get_ticks()}"
            
        # Check if this source is on cooldown
        current_time = pygame.time.get_ticks()
        if source_id in self.damage_cooldown:
            return False  # Still on cooldown, no damage applied
            
        # Check if player is invulnerable
        if self.invulnerable:
            self.blink_timer = pygame.time.get_ticks()
            return False  # No actual damage applied
            
        # Apply damage and start cooldown
        self.health -= 1
        self.sound_manager.play_sound('explosion')
        
        # Start invulnerability period
        self.invulnerable = True
        self.invulnerable_timer = pygame.time.get_ticks()
        self.blink_timer = pygame.time.get_ticks()
        
        # Set cooldown for this damage source
        self.damage_cooldown[source_id] = current_time
        
        return True  # Damage was applied
    
    def draw(self, surface):
        """Draw the player with simplified visual effects for better performance."""
        # Only draw if visible or not invulnerable
        if self.visible or not self.invulnerable:
            # Draw the player ship
            surface.blit(self.image, self.rect)
            
            # Draw hitbox if debug mode is enabled
            if DEBUG_HITBOXES:
                pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
            
            # Add simplified engine glow effect
            engine_x = self.rect.left
            engine_y = self.rect.centery
            
            # Draw simplified engine glow (just a rectangle)
            glow_width = 10
            glow_height = 6
            glow_rect = pygame.Rect(engine_x - glow_width, engine_y - glow_height//2, glow_width, glow_height)
            pygame.draw.rect(surface, (255, 150, 50), glow_rect)
            
            # Draw a smaller, brighter inner glow
            inner_glow_rect = pygame.Rect(engine_x - glow_width//2, engine_y - glow_height//4, glow_width//2, glow_height//2)
            pygame.draw.rect(surface, (255, 255, 150), inner_glow_rect)
