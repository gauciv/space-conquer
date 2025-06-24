import pygame
import os

# Initialize pygame
pygame.init()

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_BLUE = (0, 200, 255)
ORANGE = (255, 165, 0)

# Create player ship
def create_player_ship():
    # Create a more detailed player ship
    surface = pygame.Surface((60, 40), pygame.SRCALPHA)
    
    # Main body (blue)
    pygame.draw.polygon(surface, BLUE, [(0, 20), (40, 10), (40, 30)])
    
    # Cockpit (light blue)
    pygame.draw.polygon(surface, LIGHT_BLUE, [(25, 20), (35, 15), (35, 25)])
    
    # Wings (green)
    pygame.draw.polygon(surface, GREEN, [(20, 10), (50, 5), (60, 10), (40, 15)])
    pygame.draw.polygon(surface, GREEN, [(20, 30), (50, 35), (60, 30), (40, 25)])
    
    # Engine (orange glow)
    pygame.draw.rect(surface, ORANGE, (5, 15, 5, 10))
    pygame.draw.rect(surface, YELLOW, (0, 17, 5, 6))
    
    # Save the image
    pygame.image.save(surface, "images/player_ship.png")
    return surface

# Create normal enemy ship
def create_normal_enemy():
    surface = pygame.Surface((50, 30), pygame.SRCALPHA)
    
    # Main body (red)
    pygame.draw.polygon(surface, RED, [(10, 15), (40, 5), (50, 15), (40, 25)])
    
    # Cockpit (dark gray)
    pygame.draw.circle(surface, DARK_GRAY, (30, 15), 5)
    
    # Wings (darker red)
    pygame.draw.polygon(surface, (200, 0, 0), [(20, 5), (30, 0), (40, 5)])
    pygame.draw.polygon(surface, (200, 0, 0), [(20, 25), (30, 30), (40, 25)])
    
    # Engine (yellow glow)
    pygame.draw.rect(surface, YELLOW, (5, 12, 5, 6))
    pygame.draw.rect(surface, ORANGE, (0, 13, 5, 4))
    
    # Save the image
    pygame.image.save(surface, "images/normal_enemy.png")
    return surface

# Create fast enemy ship
def create_fast_enemy():
    surface = pygame.Surface((40, 20), pygame.SRCALPHA)
    
    # Main body (red triangle shape)
    pygame.draw.polygon(surface, RED, [(0, 10), (30, 0), (40, 10), (30, 20)])
    
    # Cockpit (dark gray)
    pygame.draw.circle(surface, DARK_GRAY, (25, 10), 3)
    
    # Engine (yellow glow)
    pygame.draw.rect(surface, YELLOW, (5, 8, 3, 4))
    pygame.draw.rect(surface, ORANGE, (0, 9, 5, 2))
    
    # Save the image
    pygame.image.save(surface, "images/fast_enemy.png")
    return surface

# Create tank enemy ship
def create_tank_enemy():
    surface = pygame.Surface((60, 50), pygame.SRCALPHA)
    
    # Main body (dark red)
    pygame.draw.rect(surface, (150, 0, 0), (10, 10, 40, 30))
    
    # Armor plating (lighter red)
    pygame.draw.rect(surface, RED, (5, 5, 50, 40), 5)
    
    # Cockpit (dark gray)
    pygame.draw.rect(surface, DARK_GRAY, (35, 20, 10, 10))
    
    # Cannons (gray)
    pygame.draw.rect(surface, DARK_GRAY, (50, 15, 10, 5))
    pygame.draw.rect(surface, DARK_GRAY, (50, 30, 10, 5))
    
    # Engine (yellow glow)
    pygame.draw.rect(surface, YELLOW, (5, 20, 5, 10))
    pygame.draw.rect(surface, ORANGE, (0, 22, 5, 6))
    
    # Save the image
    pygame.image.save(surface, "images/tank_enemy.png")
    return surface

# Create power-up images
def create_powerups():
    # Health power-up
    health = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.rect(health, GREEN, (0, 0, 20, 20))
    pygame.draw.rect(health, WHITE, (8, 3, 4, 14))
    pygame.draw.rect(health, WHITE, (3, 8, 14, 4))
    pygame.image.save(health, "images/health_powerup.png")
    
    # Speed power-up
    speed = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.rect(speed, BLUE, (0, 0, 20, 20))
    pygame.draw.polygon(speed, WHITE, [(5, 10), (15, 5), (15, 15)])
    pygame.image.save(speed, "images/speed_powerup.png")
    
    # Rapid fire power-up
    rapid_fire = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.rect(rapid_fire, WHITE, (0, 0, 20, 20))
    pygame.draw.rect(rapid_fire, RED, (5, 5, 10, 10))
    pygame.image.save(rapid_fire, "images/rapid_fire_powerup.png")

# Create bullet image
def create_bullet():
    bullet = pygame.Surface((15, 5), pygame.SRCALPHA)
    pygame.draw.rect(bullet, YELLOW, (0, 0, 10, 5))
    pygame.draw.rect(bullet, ORANGE, (10, 0, 5, 5))
    pygame.image.save(bullet, "images/bullet.png")

# Create all images
create_player_ship()
create_normal_enemy()
create_fast_enemy()
create_tank_enemy()
create_powerups()
create_bullet()

print("All sprite images have been created in the 'images' directory.")
