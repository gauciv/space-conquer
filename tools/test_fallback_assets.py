#!/usr/bin/env python3
"""
Script to test the fallback asset system.
This will attempt to load non-existent assets to verify that fallbacks are used.
"""
import os
import sys
import pygame
from pathlib import Path

# Add the parent directory to the path so we can import the src package
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.utils.asset_manager import AssetManager

def main():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create a window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Fallback Asset Test")
    
    # Create the asset manager
    asset_manager = AssetManager()
    
    # Test loading non-existent assets
    print("\nTesting fallback system...")
    
    # Test loading a non-existent image
    print("\nTesting non-existent image:")
    non_existent_image = asset_manager.get_image("non_existent_image")
    print(f"Image loaded: {non_existent_image is not None}")
    
    # Test loading a non-existent sound
    print("\nTesting non-existent sound:")
    non_existent_sound = asset_manager.get_sound("non_existent_sound")
    print(f"Sound loaded: {non_existent_sound is not None}")
    
    # Test loading a non-existent music track
    print("\nTesting non-existent music:")
    non_existent_music = asset_manager.get_music_path("non_existent_music")
    print(f"Music path: {non_existent_music}")
    
    # Test loading a non-existent map
    print("\nTesting non-existent map:")
    non_existent_map = asset_manager.get_map("non_existent_map")
    print(f"Map loaded: {non_existent_map is not None}")
    if non_existent_map:
        print(f"Map name: {non_existent_map.get('name')}")
    
    # Get fallback usage information
    print("\nFallback usage:")
    fallback_usage = asset_manager.get_fallback_usage()
    for asset_type, used_ids in fallback_usage.items():
        print(f"  {asset_type}: {', '.join(used_ids)}")
    
    # Display the non-existent image
    if non_existent_image:
        screen.fill((0, 0, 0))
        screen.blit(non_existent_image, (400 - non_existent_image.get_width() // 2, 300 - non_existent_image.get_height() // 2))
        pygame.display.flip()
    
    # Play the non-existent sound
    if non_existent_sound:
        non_existent_sound.play()
    
    # Wait for user to close the window
    print("\nPress any key to exit...")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
