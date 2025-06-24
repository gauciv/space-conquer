"""
Configuration settings for the Space Impact game.
"""
import pygame
import os

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)

# Asset paths
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")
MUSIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music")

# Game settings
DEFAULT_SFX_VOLUME = 0.7  # 70% for sound effects
DEFAULT_MUSIC_VOLUME = 0.5  # 50% for music

# Enemy settings
ENEMY_SPAWN_DELAY = 1000  # milliseconds
POWERUP_SPAWN_DELAY = 10000  # milliseconds

# Player settings
PLAYER_INITIAL_HEALTH = 3
PLAYER_INITIAL_SPEED = 5
PLAYER_SHOOT_DELAY = 250  # milliseconds

# Difficulty settings
FAST_ENEMY_APPEAR_TIME = 1200  # frames (20 seconds at 60 FPS)
TANK_ENEMY_APPEAR_TIME = 3600  # frames (60 seconds at 60 FPS)
