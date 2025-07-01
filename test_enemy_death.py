"""
Test script for enemy death animations.
This script runs a simple test to verify that enemy death animations work correctly.
"""
import os
import sys
import pygame
import time
import random
from src.sprites.enemy_enhanced import EnhancedEnemy
from src.utils.sound_manager import SoundManager
from src.utils.asset_loader import AssetLoader

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enemy Death Animation Test")

# Load assets
asset_loader = AssetLoader()
sound_manager = SoundManager()

# Create enemies
enemies = pygame.sprite.Group()

# Create different enemy types
enemy_types = ['low', 'elite', 'super']
for i in range(3):
    for enemy_type in enemy_types:
        enemy = EnhancedEnemy(enemy_type, asset_loader.images)
        enemy.rect.x = 200 + i * 200
        enemy.rect.y = 100 + enemy_types.index(enemy_type) * 150
        enemy.game_manager = type('obj', (object,), {'sound_manager': sound_manager})
        enemies.add(enemy)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kill enemy on click
            pos = pygame.mouse.get_pos()
            for enemy in enemies:
                if enemy.rect.collidepoint(pos):
                    enemy.take_damage(enemy.health)  # Kill with one click
    
    # Update enemies
    enemies.update()
    
    # Draw
    screen.fill((0, 0, 30))  # Dark blue background
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw instructions
    font = pygame.font.SysFont('Arial', 24)
    text = font.render("Click on enemies to test death animations", True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 20))
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
