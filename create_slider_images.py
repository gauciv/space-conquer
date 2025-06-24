import pygame
import os

# Initialize pygame
pygame.init()

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create slider bar
def create_slider_bar():
    width, height = 200, 10
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw the slider background
    pygame.draw.rect(surface, (80, 80, 80), (0, 0, width, height))
    pygame.draw.rect(surface, (120, 120, 120), (0, 0, width, height), 1)
    
    # Save the image
    pygame.image.save(surface, "images/slider_bar.png")
    print("Slider bar created successfully!")
    return surface

# Create slider handle
def create_slider_handle():
    width, height = 20, 20
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw the slider handle
    pygame.draw.circle(surface, (200, 200, 200), (width//2, height//2), width//2)
    pygame.draw.circle(surface, (150, 150, 150), (width//2, height//2), width//2, 2)
    
    # Save the image
    pygame.image.save(surface, "images/slider_handle.png")
    print("Slider handle created successfully!")
    return surface

# Create the slider images
create_slider_bar()
create_slider_handle()
