"""
Player sprite for the Space Impact game.
"""
import pygame
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_SPEED, PLAYER_SHOOT_DELAY
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, image, sound_manager):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed = PLAYER_INITIAL_SPEED
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()
        self.health = PLAYER_INITIAL_HEALTH
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.sound_manager = sound_manager
    
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
            self.health += 1
        elif powerup_type == 'speed':
            self.speed += 1
        elif powerup_type == 'rapid_fire':
            self.rapid_fire = True
            self.shoot_delay = 100
            self.rapid_fire_timer = 300  # Lasts for 300 frames (5 seconds at 60 FPS)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)
