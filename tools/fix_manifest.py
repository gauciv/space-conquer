#!/usr/bin/env python3
"""
Script to fix the manifest.json file to include all the new asset IDs.
"""
import os
import sys
import json
from pathlib import Path

def main():
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    images_dir = base_dir / "assets" / "images"
    manifest_path = images_dir / "manifest.json"
    
    # Create a new manifest
    manifest = {}
    
    # Add player assets
    player_dir = images_dir / "player"
    if player_dir.exists():
        for file_path in player_dir.glob("*.png"):
            asset_id = file_path.stem
            manifest[asset_id] = {
                "file": f"player/{file_path.name}",
                "scale": [50, 30] if "bullet" not in file_path.name else [10, 5]
            }
    
    # Add powerup assets
    powerups_dir = images_dir / "powerups"
    if powerups_dir.exists():
        for file_path in powerups_dir.glob("*.png"):
            asset_id = file_path.stem
            manifest[asset_id] = {
                "file": f"powerups/{file_path.name}",
                "scale": [20, 20]
            }
    
    # Add UI assets
    ui_dir = images_dir / "ui"
    if ui_dir.exists():
        for file_path in ui_dir.glob("*.png"):
            asset_id = file_path.stem
            
            # Determine scale based on asset type
            if "heart" in file_path.name:
                scale = [32, 32]
            elif "health-bar" in file_path.name or "slider-bar" in file_path.name:
                scale = [100, 10]
            elif "slider-handle" in file_path.name:
                scale = [20, 20]
            elif "button" in file_path.name:
                scale = [100, 40]
            elif "background" in file_path.name:
                scale = [800, 600]
            else:
                scale = [30, 30]
            
            manifest[asset_id] = {
                "file": f"ui/{file_path.name}",
                "scale": scale
            }
    
    # Add map assets for each map
    map_dirs = {
        "SE": "starlights_end",
        "CF": "crimson_frontier",
        "OV": "oblivion_veil"
    }
    
    for prefix, map_dir_name in map_dirs.items():
        map_dir = images_dir / map_dir_name
        if map_dir.exists():
            # Add map visuals
            for file_path in map_dir.glob("*.png"):
                if file_path.parent == map_dir:  # Only include files directly in the map directory
                    asset_id = file_path.stem
                    manifest[asset_id] = {
                        "file": f"{map_dir_name}/{file_path.name}",
                        "scale": [800, 600]
                    }
            
            # Add monsters
            monsters_dir = map_dir / "monsters"
            if monsters_dir.exists():
                for file_path in monsters_dir.glob("*.png"):
                    asset_id = file_path.stem
                    
                    # Determine scale based on monster type
                    if "boss" in file_path.name and "mini" not in file_path.name:
                        scale = [120, 90]
                    elif "mini-boss" in file_path.name:
                        scale = [80, 60]
                    elif "super" in file_path.name:
                        scale = [45, 35]
                    elif "elite" in file_path.name:
                        scale = [40, 30]
                    else:  # lower
                        scale = [30, 20]
                    
                    manifest[asset_id] = {
                        "file": f"{map_dir_name}/monsters/{file_path.name}",
                        "scale": scale
                    }
            
            # Add additional assets
            additional_assets_dir = map_dir / "additional_assets"
            if additional_assets_dir.exists():
                for file_path in additional_assets_dir.glob("*.png"):
                    asset_id = file_path.stem
                    
                    # Determine scale based on asset type
                    if "asteroid" in file_path.name or "debris" in file_path.name:
                        scale = [40, 40]
                    elif "turret" in file_path.name:
                        scale = [30, 30]
                    else:
                        scale = [50, 50]
                    
                    manifest[asset_id] = {
                        "file": f"{map_dir_name}/additional_assets/{file_path.name}",
                        "scale": scale
                    }
    
    # Save the manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    
    print(f"Updated manifest at {manifest_path}")
    print(f"Added {len(manifest)} assets to the manifest")

if __name__ == "__main__":
    main()
