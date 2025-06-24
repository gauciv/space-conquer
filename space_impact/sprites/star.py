"""
Star background elements for the Space Impact game.
"""
import pygame
import random
import math
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 5)  # Increased speed range for more dynamic background
        
        # Randomize star colors for more visual interest
        color_choice = random.randint(0, 10)
        if color_choice < 7:  # 70% white stars
            self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        elif color_choice < 9:  # 20% blue stars
            self.color = (random.randint(100, 150), random.randint(150, 200), random.randint(200, 255))
        else:  # 10% red/yellow stars
            self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(50, 100))
        
        # Add twinkling effect
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_offset = random.uniform(0, 6.28)  # Random starting phase
        self.base_size = self.size
        
        # Add occasional shooting stars
        self.is_shooting_star = random.random() < 0.02  # 2% chance
        if self.is_shooting_star:
            self.shooting_length = random.randint(20, 50)
            self.shooting_angle = random.uniform(-0.2, 0.2)  # Slight angle variation
            self.shooting_speed = random.randint(8, 15)
            self.trail_alpha = 200
    
    def update(self):
        self.x -= self.speed
        
        # Update twinkling effect
        if not self.is_shooting_star:
            twinkle_factor = 0.3 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset) + 0.7
            self.size = self.base_size * twinkle_factor
        
        # Reset when off-screen
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)
            
            # Chance to become a shooting star when respawning
            self.is_shooting_star = random.random() < 0.02
            if self.is_shooting_star:
                self.shooting_length = random.randint(20, 50)
                self.shooting_angle = random.uniform(-0.2, 0.2)
                self.shooting_speed = random.randint(8, 15)
                self.trail_alpha = 200
    
    def draw(self, surface):
        if self.is_shooting_star:
            # Draw shooting star with trail
            trail_points = []
            for i in range(self.shooting_length):
                trail_x = self.x + i * math.cos(self.shooting_angle)
                trail_y = self.y - i * math.sin(self.shooting_angle)
                trail_points.append((trail_x, trail_y))
            
            # Draw trail with gradient alpha
            for i in range(len(trail_points) - 1):
                alpha = int(self.trail_alpha * (1 - i / len(trail_points)))
                color = (self.color[0], self.color[1], self.color[2], alpha)
                pygame.draw.line(surface, color, trail_points[i], trail_points[i+1], 1)
            
            # Draw the star head
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size) + 1)
        else:
            # Draw regular star with slight glow for larger stars
            if self.base_size >= 2:
                # Draw glow
                glow_size = self.size * 2
                glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
                
                # Create gradient glow
                for r in range(int(glow_size), 0, -1):
                    alpha = int(50 * (r / glow_size))
                    color = (self.color[0], self.color[1], self.color[2], alpha)
                    pygame.draw.circle(glow_surface, color, (int(glow_size), int(glow_size)), r)
                
                # Draw the glow
                surface.blit(glow_surface, (int(self.x - glow_size), int(self.y - glow_size)))
            
            # Draw the star
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
