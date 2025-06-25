#!/usr/bin/env python3
"""
Script to refactor the monster assets to have exactly 5 types per map:
1. Lower
2. Elite
3. Super
4. Mini-boss
5. Boss
"""
import os
import sys
import json
import shutil
from pathlib import Path
import pygame

def main():
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    images_dir = base_dir / "assets" / "images"
    
    # Define map directories
    map_dirs = {
        "SE": images_dir / "starlights_end",
        "CF": images_dir / "crimson_frontier",
        "OV": images_dir / "oblivion_veil"
    }
    
    # Define the 5 monster types for each map
    monster_types = {
        "SE": {
            "lower": "SE-monster-lower.png",
            "elite": "SE-monster-elite.png",
            "super": "SE-monster-super.png",
            "mini-boss": "SE-monster-mini-boss.png",
            "boss": "SE-monster-boss.png"
        },
        "CF": {
            "lower": "CF-monster-lower.png",
            "elite": "CF-monster-elite.png",
            "super": "CF-monster-super.png",
            "mini-boss": "CF-monster-mini-boss.png",
            "boss": "CF-monster-boss.png"
        },
        "OV": {
            "lower": "OV-monster-lower.png",
            "elite": "OV-monster-elite.png",
            "super": "OV-monster-super.png",
            "mini-boss": "OV-monster-mini-boss.png",
            "boss": "OV-monster-boss.png"
        }
    }
    
    # Create monster directories if they don't exist
    for map_prefix, map_dir in map_dirs.items():
        monster_dir = map_dir / "monsters"
        monster_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder images for each monster type
        for monster_type, filename in monster_types[map_prefix].items():
            file_path = monster_dir / filename
            if not file_path.exists():
                print(f"Creating placeholder for {map_prefix} {monster_type}: {file_path}")
                create_placeholder_image(file_path, map_prefix, monster_type)
    
    # Update the manifest file
    manifest_path = images_dir / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    else:
        manifest = {}
    
    # Remove old monster entries
    keys_to_remove = []
    for key in manifest.keys():
        if any(f"{prefix}-monster-" in key for prefix in ["SE", "CF", "OV"]):
            if not any(f"{prefix}-monster-{monster_type}" in key for prefix in ["SE", "CF", "OV"] for monster_type in ["lower", "elite", "super", "mini-boss", "boss"]):
                keys_to_remove.append(key)
    
    for key in keys_to_remove:
        if key in manifest:
            del manifest[key]
    
    # Add new monster entries
    for map_prefix, monsters in monster_types.items():
        for monster_type, filename in monsters.items():
            asset_id = f"{map_prefix}-monster-{monster_type}"
            
            # Determine scale based on monster type
            if monster_type == "boss":
                scale = [120, 90]
            elif monster_type == "mini-boss":
                scale = [80, 60]
            elif monster_type == "super":
                scale = [45, 35]
            elif monster_type == "elite":
                scale = [40, 30]
            else:  # lower
                scale = [30, 20]
            
            manifest[asset_id] = {
                "file": f"{map_prefix.lower()}_map/monsters/{filename}",
                "scale": scale
            }
    
    # Save the updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    
    print(f"Updated manifest at {manifest_path}")
    
    # Update the asset loader to use the new monster types
    update_asset_loader(base_dir)
    
    print("Monster refactoring complete!")

def create_placeholder_image(path, map_prefix, monster_type):
    """Create a simple placeholder image for a monster."""
    # Initialize pygame if not already initialized
    if not pygame.get_init():
        pygame.init()
    
    # Determine size based on monster type
    if monster_type == "boss":
        width, height = 120, 90
    elif monster_type == "mini-boss":
        width, height = 80, 60
    elif monster_type == "super":
        width, height = 45, 35
    elif monster_type == "elite":
        width, height = 40, 30
    else:  # lower
        width, height = 30, 20
    
    # Create a surface
    surface = pygame.Surface((width, height))
    
    # Determine color based on map
    if map_prefix == "SE":
        color = (100, 100, 255)  # Blue-ish for Starlights End
    elif map_prefix == "CF":
        color = (255, 100, 100)  # Red-ish for Crimson Frontier
    elif map_prefix == "OV":
        color = (100, 0, 100)  # Purple for Oblivion Veil
    else:
        color = (150, 150, 150)  # Default gray
    
    # Adjust color based on monster type
    if monster_type == "boss":
        color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
    elif monster_type == "mini-boss":
        color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
    elif monster_type == "lower":
        color = (max(color[0] - 30, 0), max(color[1] - 30, 0), max(color[2] - 30, 0))
    
    surface.fill(color)
    
    # Add a border
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 1)
    
    # Add the monster type as text
    font_size = min(height // 3, 12)
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(f"{map_prefix} {monster_type}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface, text_rect)
    
    # Add "PLACEHOLDER" text
    font = pygame.font.SysFont("Arial", max(font_size - 2, 6))
    text_surface = font.render("PLACEHOLDER", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + font_size + 2))
    surface.blit(text_surface, text_rect)
    
    # Save the image
    pygame.image.save(surface, path)

def update_asset_loader(base_dir):
    """Update the asset loader to use the new monster types."""
    asset_loader_path = base_dir / "src" / "utils" / "asset_loader.py"
    
    with open(asset_loader_path, "r") as f:
        content = f.read()
    
    # Update the image_ids dictionary to use the new monster types
    old_image_ids = """        image_ids = {
            'player': 'player-default',
            'normal_enemy': 'SE-monster-low-normal',
            'fast_enemy': 'SE-monster-low-fast',
            'tank_enemy': 'SE-monster-elite-tank',
            'drone_enemy': 'SE-monster-elite-drone',
            'bomber_enemy': 'SE-monster-super-bomber',
            'bullet': 'player-bullet-default',
            'health_powerup': 'powerup-health',
            'speed_powerup': 'powerup-speed',
            'rapid_fire_powerup': 'powerup-rapid-fire',
            'score_multiplier': 'powerup-score-multiplier',
            'settings_cog': 'ui-settings-cog',
            'slider_bar': 'ui-slider-bar',
            'slider_handle': 'ui-slider-handle',
            'full_heart': 'ui-heart-full',
            'empty_heart': 'ui-heart-empty',
            'mini_boss': 'SE-monster-mini-boss',
            'main_boss': 'SE-monster-boss',
            'health_bar_bg': 'ui-health-bar-bg',
            'health_bar_fill': 'ui-health-bar-fill'
        }"""
    
    new_image_ids = """        image_ids = {
            'player': 'player-default',
            'normal_enemy': 'SE-monster-lower',
            'fast_enemy': 'SE-monster-elite',
            'tank_enemy': 'SE-monster-super',
            'bullet': 'player-bullet-default',
            'health_powerup': 'powerup-health',
            'speed_powerup': 'powerup-speed',
            'rapid_fire_powerup': 'powerup-rapid-fire',
            'score_multiplier': 'powerup-score-multiplier',
            'settings_cog': 'ui-settings-cog',
            'slider_bar': 'ui-slider-bar',
            'slider_handle': 'ui-slider-handle',
            'full_heart': 'ui-heart-full',
            'empty_heart': 'ui-heart-empty',
            'mini_boss': 'SE-monster-mini-boss',
            'main_boss': 'SE-monster-boss',
            'health_bar_bg': 'ui-health-bar-bg',
            'health_bar_fill': 'ui-health-bar-fill'
        }"""
    
    # Update the load_image method to handle the new monster types
    old_load_image = """        # Special cases for the new naming convention
        if filename == 'player_ship.png':
            asset_id = 'player-default'
        elif filename == 'bullet.png':
            asset_id = 'player-bullet-default'
        elif filename.startswith('normal_'):
            asset_id = 'SE-monster-low-normal'
        elif filename.startswith('fast_'):
            asset_id = 'SE-monster-low-fast'
        elif filename.startswith('tank_'):
            asset_id = 'SE-monster-elite-tank'
        elif filename.startswith('drone_'):
            asset_id = 'SE-monster-elite-drone'
        elif filename.startswith('bomber_'):
            asset_id = 'SE-monster-super-bomber'
        elif filename.startswith('mini_boss'):
            asset_id = 'SE-monster-mini-boss'
        elif filename.startswith('main_boss'):
            asset_id = 'SE-monster-boss'"""
    
    new_load_image = """        # Special cases for the new naming convention
        if filename == 'player_ship.png':
            asset_id = 'player-default'
        elif filename == 'bullet.png':
            asset_id = 'player-bullet-default'
        elif filename.startswith('normal_'):
            asset_id = 'SE-monster-lower'
        elif filename.startswith('fast_'):
            asset_id = 'SE-monster-elite'
        elif filename.startswith('tank_'):
            asset_id = 'SE-monster-super'
        elif filename.startswith('mini_boss'):
            asset_id = 'SE-monster-mini-boss'
        elif filename.startswith('main_boss'):
            asset_id = 'SE-monster-boss'"""
    
    # Replace the old code with the new code
    content = content.replace(old_image_ids, new_image_ids)
    content = content.replace(old_load_image, new_load_image)
    
    # Write the updated content back to the file
    with open(asset_loader_path, "w") as f:
        f.write(content)
    
    print(f"Updated asset loader at {asset_loader_path}")

if __name__ == "__main__":
    main()
