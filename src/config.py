"""
Configuration settings for the Space Impact game.
"""
import pygame
import os
from pathlib import Path

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

# Debug settings
DEBUG_HITBOXES = False  # Set to False by default, can be toggled in test mode

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Asset paths - try both the new assets directory and the original structure
def get_asset_path(subdir, filename):
    # First try the assets directory
    assets_path = BASE_DIR / "assets" / subdir / filename
    if assets_path.exists():
        return str(assets_path)
    
    # Then try the original structure
    original_path = BASE_DIR / subdir / filename
    if original_path.exists():
        return str(original_path)
    
    # If neither exists, return the assets path (will fail gracefully later)
    return str(assets_path)

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
