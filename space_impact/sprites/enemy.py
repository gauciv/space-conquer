"""
Enemy sprites for the Space Impact game.
"""
import pygame
import random
import math
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

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
        elif enemy_type == 'fast':
            self.image = images.get('fast_enemy')
            self.health = 1
            self.speed = 5
            self.points = 15
            self.movement_pattern = "zigzag"
        elif enemy_type == 'tank':
            self.image = images.get('tank_enemy')
            self.health = 3
            self.speed = 2
            self.points = 25
            self.movement_pattern = "straight"
        elif enemy_type == 'drone':
            self.image = images.get('drone_enemy')
            self.health = 1
            self.speed = 4
            self.points = 20
            self.movement_pattern = "sine"
        elif enemy_type == 'bomber':
            self.image = images.get('bomber_enemy')
            self.health = 2
            self.speed = 2
            self.points = 30
            self.movement_pattern = "dive"
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
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
        
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()
