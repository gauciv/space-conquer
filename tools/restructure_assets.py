#!/usr/bin/env python3
"""
Script to restructure assets according to the new directory structure.
This will:
1. Move existing assets to their appropriate directories
2. Create placeholder files for missing assets
3. Update the asset manifest to reflect the new structure
"""
import os
import sys
import json
import shutil
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Restructure assets according to the new directory structure")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually doing it")
    args = parser.parse_args()
    
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    images_dir = assets_dir / "images"
    
    # Define new directory structure
    new_dirs = {
        "player": images_dir / "player",
        "powerups": images_dir / "powerups",
        "ui": images_dir / "ui",
        "se_monsters": images_dir / "starlights_end" / "monsters",
        "se_assets": images_dir / "starlights_end" / "additional_assets",
        "cf_monsters": images_dir / "crimson_frontier" / "monsters",
        "cf_assets": images_dir / "crimson_frontier" / "additional_assets",
        "ov_monsters": images_dir / "oblivion_veil" / "monsters",
        "ov_assets": images_dir / "oblivion_veil" / "additional_assets",
    }
    
    # Create directories if they don't exist
    for dir_path in new_dirs.values():
        if not dir_path.exists():
            if args.dry_run:
                print(f"Would create directory: {dir_path}")
            else:
                print(f"Creating directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
    
    # Define asset mappings (old_name -> new_location)
    asset_mappings = {
        # Player assets
        "player_ship.png": ("player", "player-default.png"),
        
        # Powerup assets
        "health_powerup.png": ("powerups", "powerup-health.png"),
        "speed_powerup.png": ("powerups", "powerup-speed.png"),
        "rapid_fire_powerup.png": ("powerups", "powerup-rapid-fire.png"),
        "score_multiplier.png": ("powerups", "powerup-score-multiplier.png"),
        
        # UI assets
        "full_heart.png": ("ui", "ui-heart-full.png"),
        "empty_heart.png": ("ui", "ui-heart-empty.png"),
        "health_bar_bg.png": ("ui", "ui-health-bar-bg.png"),
        "health_bar_fill.png": ("ui", "ui-health-bar-fill.png"),
        "settings_cog.png": ("ui", "ui-settings-cog.png"),
        "slider_bar.png": ("ui", "ui-slider-bar.png"),
        "slider_handle.png": ("ui", "ui-slider-handle.png"),
        "bullet.png": ("player", "player-bullet-default.png"),
        
        # Starlights End monsters
        "normal_enemy.png": ("se_monsters", "SE-monster-low-normal.png"),
        "fast_enemy.png": ("se_monsters", "SE-monster-low-fast.png"),
        "tank_enemy.png": ("se_monsters", "SE-monster-elite-tank.png"),
        "drone_enemy.png": ("se_monsters", "SE-monster-elite-drone.png"),
        "bomber_enemy.png": ("se_monsters", "SE-monster-super-bomber.png"),
        "mini_boss.png": ("se_monsters", "SE-monster-mini-boss.png"),
        "main_boss.png": ("se_monsters", "SE-monster-boss.png"),
    }
    
    # Define placeholder assets to create
    placeholders = {
        # Player variants
        "player": [
            "player-variant1.png",
            "player-variant2.png",
            "player-variant3.png",
            "player-bullet-enhanced.png",
            "player-bullet-special.png",
        ],
        
        # Additional powerups
        "powerups": [
            "powerup-shield.png",
            "powerup-bomb.png",
            "powerup-special.png",
        ],
        
        # Additional UI elements
        "ui": [
            "ui-button-start.png",
            "ui-button-exit.png",
            "ui-background-menu.png",
            "ui-background-gameover.png",
        ],
        
        # Map visuals
        "starlights_end": [
            "SE-map-visual.png",
            "SE-map-background.png",
        ],
        "crimson_frontier": [
            "CF-map-visual.png",
            "CF-map-background.png",
        ],
        "oblivion_veil": [
            "OV-map-visual.png",
            "OV-map-background.png",
        ],
        
        # Crimson Frontier monsters
        "cf_monsters": [
            "CF-monster-low-scout.png",
            "CF-monster-low-fighter.png",
            "CF-monster-elite-destroyer.png",
            "CF-monster-elite-carrier.png",
            "CF-monster-super-dreadnought.png",
            "CF-monster-mini-boss.png",
            "CF-monster-boss.png",
        ],
        
        # Oblivion Veil monsters
        "ov_monsters": [
            "OV-monster-low-phantom.png",
            "OV-monster-low-specter.png",
            "OV-monster-elite-wraith.png",
            "OV-monster-elite-harbinger.png",
            "OV-monster-super-annihilator.png",
            "OV-monster-mini-boss.png",
            "OV-monster-boss.png",
        ],
        
        # Additional map assets
        "se_assets": [
            "SE-asset-asteroid.png",
            "SE-asset-debris.png",
            "SE-asset-nebula.png",
        ],
        "cf_assets": [
            "CF-asset-minefield.png",
            "CF-asset-turret.png",
            "CF-asset-forcefield.png",
        ],
        "ov_assets": [
            "OV-asset-void-rift.png",
            "OV-asset-gravity-well.png",
            "OV-asset-dark-matter.png",
        ],
    }
    
    # Move existing assets to new locations
    for old_name, (dir_key, new_name) in asset_mappings.items():
        old_path = images_dir / old_name
        new_path = new_dirs[dir_key] / new_name
        
        if old_path.exists():
            if args.dry_run:
                print(f"Would move: {old_path} -> {new_path}")
            else:
                print(f"Moving: {old_path} -> {new_path}")
                shutil.copy2(old_path, new_path)
    
    # Create placeholder files
    for dir_key, filenames in placeholders.items():
        if dir_key in new_dirs:
            dir_path = new_dirs[dir_key]
        else:
            dir_path = images_dir / dir_key
            if not dir_path.exists():
                if args.dry_run:
                    print(f"Would create directory: {dir_path}")
                else:
                    print(f"Creating directory: {dir_path}")
                    dir_path.mkdir(parents=True, exist_ok=True)
        
        for filename in filenames:
            file_path = dir_path / filename
            if not file_path.exists():
                if args.dry_run:
                    print(f"Would create placeholder: {file_path}")
                else:
                    print(f"Creating placeholder: {file_path}")
                    create_placeholder_image(file_path, filename)
    
    # Create a new asset manifest
    manifest = create_new_manifest(images_dir, new_dirs)
    
    # Save the manifest
    manifest_path = images_dir / "manifest.json"
    if args.dry_run:
        print(f"Would update manifest: {manifest_path}")
    else:
        print(f"Updating manifest: {manifest_path}")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
    
    # Remove old assets if they've been moved
    if not args.dry_run:
        print("\nRemoving old assets...")
        for old_name in asset_mappings.keys():
            old_path = images_dir / old_name
            if old_path.exists():
                print(f"Removing: {old_path}")
                os.remove(old_path)
    
    # Print summary
    if args.dry_run:
        print("\nDry run complete. No changes were made.")
    else:
        print("\nRestructuring complete.")

def create_placeholder_image(path, name):
    """Create a simple placeholder image with the filename as text."""
    import pygame
    
    # Initialize pygame if not already initialized
    if not pygame.get_init():
        pygame.init()
    
    # Create a surface
    width, height = 100, 100
    surface = pygame.Surface((width, height))
    
    # Fill with a color based on the filename
    if "player" in name:
        color = (0, 255, 0)  # Green for player
    elif "powerup" in name:
        color = (0, 0, 255)  # Blue for powerups
    elif "ui" in name:
        color = (200, 200, 200)  # Gray for UI
    elif "SE" in name:
        color = (100, 100, 255)  # Blue-ish for Starlights End
    elif "CF" in name:
        color = (255, 100, 100)  # Red-ish for Crimson Frontier
    elif "OV" in name:
        color = (100, 0, 100)  # Purple for Oblivion Veil
    else:
        color = (150, 150, 150)  # Default gray
    
    surface.fill(color)
    
    # Add a border
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 1)
    
    # Add the filename as text
    font = pygame.font.SysFont("Arial", 10)
    text_surface = font.render(name, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface, text_rect)
    
    # Add "PLACEHOLDER" text
    font = pygame.font.SysFont("Arial", 8)
    text_surface = font.render("PLACEHOLDER", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + 15))
    surface.blit(text_surface, text_rect)
    
    # Save the image
    pygame.image.save(surface, path)

def create_new_manifest(images_dir, new_dirs):
    """Create a new asset manifest based on the new directory structure."""
    manifest = {}
    
    # Add player assets
    for file_path in new_dirs["player"].glob("*.png"):
        asset_id = file_path.stem
        manifest[asset_id] = {
            "file": f"player/{file_path.name}",
            "scale": [50, 30]
        }
    
    # Add powerup assets
    for file_path in new_dirs["powerups"].glob("*.png"):
        asset_id = file_path.stem
        manifest[asset_id] = {
            "file": f"powerups/{file_path.name}",
            "scale": [20, 20]
        }
    
    # Add UI assets
    for file_path in new_dirs["ui"].glob("*.png"):
        asset_id = file_path.stem
        if "heart" in file_path.name:
            scale = [32, 32]
        elif "bar" in file_path.name:
            scale = [100, 10]
        elif "slider" in file_path.name:
            scale = [100, 10] if "bar" in file_path.name else [20, 20]
        else:
            scale = [30, 30]
        
        manifest[asset_id] = {
            "file": f"ui/{file_path.name}",
            "scale": scale
        }
    
    # Add Starlights End monsters
    for file_path in new_dirs["se_monsters"].glob("*.png"):
        asset_id = file_path.stem
        
        if "boss" in file_path.name:
            if "mini" in file_path.name:
                scale = [80, 60]
            else:
                scale = [120, 90]
        elif "super" in file_path.name:
            scale = [45, 35]
        elif "elite" in file_path.name:
            scale = [40, 30]
        else:
            scale = [30, 20]
        
        manifest[asset_id] = {
            "file": f"starlights_end/monsters/{file_path.name}",
            "scale": scale
        }
    
    # Add Crimson Frontier monsters
    for file_path in new_dirs["cf_monsters"].glob("*.png"):
        asset_id = file_path.stem
        
        if "boss" in file_path.name:
            if "mini" in file_path.name:
                scale = [80, 60]
            else:
                scale = [120, 90]
        elif "super" in file_path.name:
            scale = [45, 35]
        elif "elite" in file_path.name:
            scale = [40, 30]
        else:
            scale = [30, 20]
        
        manifest[asset_id] = {
            "file": f"crimson_frontier/monsters/{file_path.name}",
            "scale": scale
        }
    
    # Add Oblivion Veil monsters
    for file_path in new_dirs["ov_monsters"].glob("*.png"):
        asset_id = file_path.stem
        
        if "boss" in file_path.name:
            if "mini" in file_path.name:
                scale = [80, 60]
            else:
                scale = [120, 90]
        elif "super" in file_path.name:
            scale = [45, 35]
        elif "elite" in file_path.name:
            scale = [40, 30]
        else:
            scale = [30, 20]
        
        manifest[asset_id] = {
            "file": f"oblivion_veil/monsters/{file_path.name}",
            "scale": scale
        }
    
    # Add map visuals
    for map_dir in ["starlights_end", "crimson_frontier", "oblivion_veil"]:
        map_path = images_dir / map_dir
        if map_path.exists():
            for file_path in map_path.glob("*.png"):
                if file_path.parent == map_path:  # Only include files directly in the map directory
                    asset_id = file_path.stem
                    manifest[asset_id] = {
                        "file": f"{map_dir}/{file_path.name}",
                        "scale": [800, 600]
                    }
    
    # Add additional assets
    for dir_key in ["se_assets", "cf_assets", "ov_assets"]:
        for file_path in new_dirs[dir_key].glob("*.png"):
            asset_id = file_path.stem
            
            if "asteroid" in file_path.name or "debris" in file_path.name:
                scale = [40, 40]
            elif "turret" in file_path.name:
                scale = [30, 30]
            else:
                scale = [50, 50]
            
            manifest[asset_id] = {
                "file": f"{dir_key.split('_')[0]}_{dir_key.split('_')[1]}/{file_path.name}",
                "scale": scale
            }
    
    return manifest

if __name__ == "__main__":
    main()
