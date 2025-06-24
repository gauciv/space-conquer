#!/usr/bin/env python3
"""
Create boss images for Space Conquer.
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

# Create a mini-boss image
def create_mini_boss():
    """Create the mini-boss 'Vanguard' image."""
    # Create a larger surface for the mini-boss
    width, height = 80, 60
    mini_boss = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base color for the mini-boss - dark red with metallic feel
    base_color = (180, 30, 30)
    highlight_color = (220, 60, 60)
    shadow_color = (100, 10, 10)
    
    # Draw the main body - a larger, more complex ship
    # Main hull
    points = [
        (10, height//2),  # Nose
        (25, height//4),   # Top front
        (60, height//4),   # Top rear
        (70, height//2),   # Rear
        (60, height*3//4), # Bottom rear
        (25, height*3//4), # Bottom front
    ]
    pygame.draw.polygon(mini_boss, base_color, points)
    
    # Engine glow
    pygame.draw.circle(mini_boss, (255, 150, 50), (70, height//2), 8)
    pygame.draw.circle(mini_boss, (255, 220, 150), (70, height//2), 4)
    
    # Cockpit/command center
    pygame.draw.circle(mini_boss, highlight_color, (25, height//2), 10)
    pygame.draw.circle(mini_boss, (100, 200, 255), (25, height//2), 6)  # Blue glow
    
    # Wing details
    pygame.draw.line(mini_boss, highlight_color, (30, height//4), (55, height//4), 3)
    pygame.draw.line(mini_boss, highlight_color, (30, height*3//4), (55, height*3//4), 3)
    
    # Weapon mounts
    pygame.draw.rect(mini_boss, shadow_color, (35, height//4-8, 10, 8))
    pygame.draw.rect(mini_boss, shadow_color, (35, height*3//4, 10, 8))
    
    # Save the image
    pygame.image.save(mini_boss, 'images/mini_boss.png')
    
    # Also save to the space_impact/assets directory
    if not os.path.exists('space_impact/assets'):
        os.makedirs('space_impact/assets')
    pygame.image.save(mini_boss, 'space_impact/assets/mini_boss.png')
    
    print("Mini-boss 'Vanguard' image created successfully!")
    return mini_boss

# Create a main boss image
def create_main_boss():
    """Create the main boss 'Dreadnought' image."""
    # Create a much larger surface for the main boss
    width, height = 120, 90
    main_boss = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base color for the main boss - dark purple with menacing feel
    base_color = (80, 20, 100)
    highlight_color = (150, 50, 200)
    shadow_color = (40, 10, 60)
    energy_color = (200, 100, 255)
    
    # Draw the main body - a massive, intimidating battleship
    # Main hull - more complex shape
    points = [
        (10, height//2),    # Nose
        (30, height//3),    # Top front
        (90, height//3),    # Top rear
        (110, height//2),   # Rear
        (90, height*2//3),  # Bottom rear
        (30, height*2//3),  # Bottom front
    ]
    pygame.draw.polygon(main_boss, base_color, points)
    
    # Additional hull details - armored plates
    for i in range(3):
        x_offset = 35 + i * 20
        pygame.draw.rect(main_boss, shadow_color, (x_offset, height//3, 15, height//3))
        pygame.draw.rect(main_boss, highlight_color, (x_offset+2, height//3+2, 11, height//3-4))
    
    # Massive engine glow
    pygame.draw.circle(main_boss, (255, 100, 50), (110, height//2), 12)
    pygame.draw.circle(main_boss, (255, 200, 100), (110, height//2), 6)
    
    # Command center with menacing "eye"
    pygame.draw.circle(main_boss, shadow_color, (25, height//2), 15)
    pygame.draw.circle(main_boss, (200, 0, 0), (25, height//2), 10)  # Red eye
    pygame.draw.circle(main_boss, (255, 150, 150), (25, height//2), 5)  # Glowing center
    
    # Wing structures
    pygame.draw.polygon(main_boss, highlight_color, [
        (40, height//3), (70, height//6), (90, height//6), (90, height//3)
    ])
    pygame.draw.polygon(main_boss, highlight_color, [
        (40, height*2//3), (70, height*5//6), (90, height*5//6), (90, height*2//3)
    ])
    
    # Energy weapon ports
    for i in range(2):
        y_offset = height//3 - 10 if i == 0 else height*2//3 + 10
        pygame.draw.circle(main_boss, energy_color, (50, y_offset), 5)
        pygame.draw.circle(main_boss, energy_color, (70, y_offset), 5)
        pygame.draw.circle(main_boss, energy_color, (90, y_offset), 5)
    
    # Save the image
    pygame.image.save(main_boss, 'images/main_boss.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(main_boss, 'space_impact/assets/main_boss.png')
    
    print("Main boss 'Dreadnought' image created successfully!")
    return main_boss

# Create a new tank enemy image that fits the space theme better
def create_space_tank():
    """Create a new tank enemy that fits the space theme better."""
    # Create a surface for the space tank
    width, height = 50, 40
    space_tank = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base color for the space tank - metallic blue
    base_color = (40, 70, 120)
    highlight_color = (80, 120, 180)
    shadow_color = (20, 40, 80)
    
    # Draw the main body - a heavily armored space cruiser
    # Main hull
    pygame.draw.rect(space_tank, base_color, (10, 10, 30, 20))
    
    # Front armor
    points = [
        (10, 10),   # Top left of hull
        (0, 20),    # Front point
        (10, 30),   # Bottom left of hull
    ]
    pygame.draw.polygon(space_tank, shadow_color, points)
    
    # Rear engines
    pygame.draw.rect(space_tank, highlight_color, (40, 15, 10, 10))
    pygame.draw.circle(space_tank, (255, 150, 50), (50, 20), 5)  # Engine glow
    
    # Top and bottom armor plates
    pygame.draw.rect(space_tank, highlight_color, (15, 5, 20, 5))
    pygame.draw.rect(space_tank, highlight_color, (15, 30, 20, 5))
    
    # Weapon turret
    pygame.draw.circle(space_tank, shadow_color, (25, 20), 8)
    pygame.draw.rect(space_tank, shadow_color, (25, 16, 15, 8))
    
    # Save the image
    pygame.image.save(space_tank, 'images/tank_enemy.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(space_tank, 'space_impact/assets/tank_enemy.png')
    
    print("Space tank enemy image created successfully!")
    return space_tank

# Create a health bar image
def create_health_bar():
    """Create health bar images for bosses."""
    # Create surfaces for the health bar
    width, height = 200, 15
    bar_bg = pygame.Surface((width, height))
    bar_fill = pygame.Surface((width-2, height-2))
    
    # Colors
    bg_color = (60, 60, 60)
    fill_color = (220, 50, 50)
    
    # Draw the background
    bar_bg.fill(bg_color)
    bar_fill.fill(fill_color)
    
    # Save the images
    pygame.image.save(bar_bg, 'images/health_bar_bg.png')
    pygame.image.save(bar_fill, 'images/health_bar_fill.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(bar_bg, 'space_impact/assets/health_bar_bg.png')
    pygame.image.save(bar_fill, 'space_impact/assets/health_bar_fill.png')
    
    print("Health bar images created successfully!")
    return bar_bg, bar_fill

if __name__ == "__main__":
    create_mini_boss()
    create_main_boss()
    create_space_tank()
    create_health_bar()
    pygame.quit()
