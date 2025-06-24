import pygame
import os
import math

# Initialize pygame
pygame.init()

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create a cog icon
def create_cog_icon():
    # Create a transparent surface
    size = 30  # Size of the icon
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    gray = (180, 180, 180)
    dark_gray = (100, 100, 100)
    
    # Draw the outer circle
    center = (size // 2, size // 2)
    outer_radius = size // 2 - 2
    inner_radius = size // 3
    pygame.draw.circle(surface, gray, center, outer_radius)
    pygame.draw.circle(surface, dark_gray, center, outer_radius, 2)
    
    # Draw the inner circle
    pygame.draw.circle(surface, dark_gray, center, inner_radius)
    
    # Draw the teeth of the cog
    num_teeth = 8
    tooth_length = size // 6
    
    for i in range(num_teeth):
        angle = 2 * math.pi * i / num_teeth
        x1 = center[0] + (outer_radius - 2) * math.cos(angle)
        y1 = center[1] + (outer_radius - 2) * math.sin(angle)
        x2 = center[0] + (outer_radius + tooth_length) * math.cos(angle)
        y2 = center[1] + (outer_radius + tooth_length) * math.sin(angle)
        
        # Calculate points for a wider tooth
        angle_width = 0.2
        x1a = center[0] + (outer_radius - 2) * math.cos(angle - angle_width)
        y1a = center[1] + (outer_radius - 2) * math.sin(angle - angle_width)
        x2a = center[0] + (outer_radius + tooth_length) * math.cos(angle - angle_width)
        y2a = center[1] + (outer_radius + tooth_length) * math.sin(angle - angle_width)
        
        x1b = center[0] + (outer_radius - 2) * math.cos(angle + angle_width)
        y1b = center[1] + (outer_radius - 2) * math.sin(angle + angle_width)
        x2b = center[0] + (outer_radius + tooth_length) * math.cos(angle + angle_width)
        y2b = center[1] + (outer_radius + tooth_length) * math.sin(angle + angle_width)
        
        # Draw the tooth as a polygon
        pygame.draw.polygon(surface, gray, [(x1a, y1a), (x2a, y2a), (x2b, y2b), (x1b, y1b)])
        pygame.draw.polygon(surface, dark_gray, [(x1a, y1a), (x2a, y2a), (x2b, y2b), (x1b, y1b)], 1)
    
    # Save the image
    pygame.image.save(surface, "images/settings_cog.png")
    print("Settings cog icon created successfully!")
    return surface

# Create the cog icon
create_cog_icon()
