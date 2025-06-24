#!/usr/bin/env python3
"""
Create heart images for the health display in Space Conquer.
"""
import pygame
import os
import sys

# Add the parent directory to the path so we can import from space_impact
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize pygame
pygame.init()

# Create the images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create a full heart image
def create_full_heart():
    # Create a transparent surface
    heart = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw the heart shape
    color = (255, 0, 0)  # Red
    
    # Draw the heart shape using polygons
    # Left half of the heart
    pygame.draw.polygon(heart, color, [(16, 8), (8, 4), (4, 8), (4, 16), (16, 28)])
    # Right half of the heart
    pygame.draw.polygon(heart, color, [(16, 8), (24, 4), (28, 8), (28, 16), (16, 28)])
    
    # Save the image
    pygame.image.save(heart, 'images/full_heart.png')
    
    # Also save to the space_impact/assets directory
    if not os.path.exists('space_impact/assets'):
        os.makedirs('space_impact/assets')
    pygame.image.save(heart, 'space_impact/assets/full_heart.png')
    
    print("Full heart image created successfully!")
    return heart

# Create an empty heart image
def create_empty_heart():
    # Create a transparent surface
    heart = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw the heart shape outline
    color = (100, 100, 100)  # Gray
    
    # Draw the heart shape using polygons with thicker lines
    # Left half of the heart
    pygame.draw.polygon(heart, color, [(16, 8), (8, 4), (4, 8), (4, 16), (16, 28)], 2)
    # Right half of the heart
    pygame.draw.polygon(heart, color, [(16, 8), (24, 4), (28, 8), (28, 16), (16, 28)], 2)
    
    # Save the image
    pygame.image.save(heart, 'images/empty_heart.png')
    
    # Also save to the space_impact/assets directory
    pygame.image.save(heart, 'space_impact/assets/empty_heart.png')
    
    print("Empty heart image created successfully!")
    return heart

if __name__ == "__main__":
    create_full_heart()
    create_empty_heart()
    pygame.quit()
