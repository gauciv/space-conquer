#!/usr/bin/env python3
"""
Create new enemy types for Space Conquer.
"""
import pygame
import os
import sys
import random

# Add the parent directory to the path so we can import from space_impact
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize pygame
pygame.init()

# Create the images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create a drone enemy image
def create_drone_enemy():
    """Create a drone enemy image."""
    # Create a surface for the drone
    width, height = 40, 20
    drone = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base color for the drone - metallic green
    base_color = (30, 150, 80)
    highlight_color = (50, 200, 100)
    shadow_color = (20, 80, 40)
    
    # Draw the main body - a sleek, fast drone
    # Main hull
    pygame.draw.ellipse(drone, base_color, (5, 5, 30, 10))
    
    # Wings
    pygame.draw.polygon(drone, highlight_color, [
        (15, 5),  # Top front
        (25, 0),  # Top tip
        (35, 5),  # Top back
    ])
    pygame.draw.polygon(drone, highlight_color, [
        (15, 15),  # Bottom front
        (25, 20),  # Bottom tip
        (35, 15),  # Bottom back
    ])
    
    # Cockpit/sensor array
    pygame.draw.circle(drone, shadow_color, (10, 10), 5)
    pygame.draw.circle(drone, (100, 255, 150), (10, 10), 2)  # Green glow
    
    # Engine glow
    pygame.draw.circle(drone, (200, 255, 100), (35, 10), 3)
    
    # Save the image
    pygame.image.save(drone, 'images/drone_enemy.png')
    
    # Also save to the space_impact/assets directory
    if not os.path.exists('space_impact/assets'):
        os.makedirs('space_impact/assets')
    pygame.image.save(drone, 'space_impact/assets/drone_enemy.png')
    
    print("Drone enemy image created successfully!")
    return drone

# Create a bomber enemy image
def create_bomber_enemy():
    """Create a bomber enemy image."""
    # Create a surface for the bomber
    width, height = 60, 50
    bomber = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base color for the bomber - dark purple
    base_color = (100, 30, 120)
    highlight_color = (150, 50, 180)
    shadow_color = (60, 20, 80)
    
    # Draw the main body - a heavy bomber
    # Main hull
    pygame.draw.rect(bomber, base_color, (10, 15, 40, 20))
    
    # Front section
    pygame.draw.polygon(bomber, shadow_color, [
        (10, 15),  # Top left
        (0, 25),   # Front point
        (10, 35),  # Bottom left
    ])
    
    # Wings
    pygame.draw.polygon(bomber, highlight_color, [
        (20, 15),  # Top front
        (15, 5),   # Top tip
        (40, 5),   # Top back
        (50, 15),  # Wing back
    ])
    pygame.draw.polygon(bomber, highlight_color, [
        (20, 35),  # Bottom front
        (15, 45),  # Bottom tip
        (40, 45),  # Bottom back
        (50, 35),  # Wing back
    ])
    
    # Engine glow
    pygame.draw.rect(bomber, (255, 100, 50), (50, 20, 10, 10))
    pygame.draw.circle(bomber, (255, 200, 100), (60, 25), 5)
    
    # Bomb bay
    pygame.draw.rect(bomber, shadow_color, (25, 35, 10, 5))
    
    # Cockpit
    pygame.draw.rect(bomber, (150, 150, 200), (15, 20, 10, 10))
    
    # Save the image
    pygame.image.save(bomber, 'images/bomber_enemy.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(bomber, 'space_impact/assets/bomber_enemy.png')
    
    print("Bomber enemy image created successfully!")
    return bomber

# Create a score multiplier powerup image
def create_score_multiplier():
    """Create a score multiplier powerup image."""
    # Create a surface for the powerup
    width, height = 30, 30
    powerup = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw a golden star shape
    color = (255, 215, 0)  # Gold color
    glow_color = (255, 255, 200)
    
    # Draw a star shape
    points = []
    for i in range(10):
        angle = i * 36  # 360 / 10 = 36 degrees per point
        radius = 15 if i % 2 == 0 else 7  # Alternate between outer and inner points
        x = width // 2 + int(radius * pygame.math.Vector2(1, 0).rotate(angle).x)
        y = height // 2 + int(radius * pygame.math.Vector2(1, 0).rotate(angle).y)
        points.append((x, y))
    
    pygame.draw.polygon(powerup, color, points)
    
    # Add a glow effect
    pygame.draw.circle(powerup, glow_color, (width // 2, height // 2), 5)
    
    # Draw a "2x" in the center
    font = pygame.font.SysFont('Arial', 12, bold=True)
    text = font.render("2x", True, (0, 0, 0))
    powerup.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    
    # Save the image
    pygame.image.save(powerup, 'images/score_multiplier.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(powerup, 'space_impact/assets/score_multiplier.png')
    
    print("Score multiplier powerup image created successfully!")
    return powerup

if __name__ == "__main__":
    create_drone_enemy()
    create_bomber_enemy()
    create_score_multiplier()
    pygame.quit()
