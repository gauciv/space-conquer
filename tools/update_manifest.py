#!/usr/bin/env python3
"""
Script to update the manifest.json file to use the new directory structure.
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
    new_manifest = {}
    
    # Add player assets
    player_dir = images_dir / "player"
    if player_dir.exists():
        for file_path in player_dir.glob("*.png"):
            asset_id = file_path.stem
            new_manifest[asset_id] = {
                "file": f"player/{file_path.name}",
                "scale": [50, 30] if "bullet" not in file_path.name else [10, 5]
            }
            
            # Add legacy IDs
            if file_path.name == "player-default.png":
                new_manifest["player"] = {
                    "file": f"player/{file_path.name}",
                    "scale": [50, 30]
                }
            elif file_path.name == "player-bullet-default.png":
                new_manifest["bullet"] = {
                    "file": f"player/{file_path.name}",
                    "scale": [10, 5]
                }
    
    # Add powerup assets
    powerups_dir = images_dir / "powerups"
    if powerups_dir.exists():
        for file_path in powerups_dir.glob("*.png"):
            asset_id = file_path.stem
            new_manifest[asset_id] = {
                "file": f"powerups/{file_path.name}",
                "scale": [20, 20]
            }
            
            # Add legacy IDs
            if file_path.name == "powerup-health.png":
                new_manifest["health_powerup"] = {
                    "file": f"powerups/{file_path.name}",
                    "scale": [20, 20]
                }
            elif file_path.name == "powerup-speed.png":
                new_manifest["speed_powerup"] = {
                    "file": f"powerups/{file_path.name}",
                    "scale": [20, 20]
                }
            elif file_path.name == "powerup-rapid-fire.png":
                new_manifest["rapid_fire_powerup"] = {
                    "file": f"powerups/{file_path.name}",
                    "scale": [20, 20]
                }
            elif file_path.name == "powerup-score-multiplier.png":
                new_manifest["score_multiplier"] = {
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
            
            new_manifest[asset_id] = {
                "file": f"ui/{file_path.name}",
                "scale": scale
            }
            
            # Add legacy IDs
            if file_path.name == "ui-heart-full.png":
                new_manifest["full_heart"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [32, 32]
                }
            elif file_path.name == "ui-heart-empty.png":
                new_manifest["empty_heart"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [32, 32]
                }
            elif file_path.name == "ui-health-bar-bg.png":
                new_manifest["health_bar_bg"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [100, 10]
                }
            elif file_path.name == "ui-health-bar-fill.png":
                new_manifest["health_bar_fill"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [100, 10]
                }
            elif file_path.name == "ui-settings-cog.png":
                new_manifest["settings_cog"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [30, 30]
                }
            elif file_path.name == "ui-slider-bar.png":
                new_manifest["slider_bar"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [100, 10]
                }
            elif file_path.name == "ui-slider-handle.png":
                new_manifest["slider_handle"] = {
                    "file": f"ui/{file_path.name}",
                    "scale": [20, 20]
                }
    
    # Add Starlights End monsters
    se_monsters_dir = images_dir / "starlights_end" / "monsters"
    if se_monsters_dir.exists():
        for file_path in se_monsters_dir.glob("*.png"):
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
            
            new_manifest[asset_id] = {
                "file": f"starlights_end/monsters/{file_path.name}",
                "scale": scale
            }
            
            # Add legacy IDs
            if file_path.name == "SE-monster-lower.png":
                new_manifest["normal_enemy"] = {
                    "file": f"starlights_end/monsters/{file_path.name}",
                    "scale": [30, 20]
                }
            elif file_path.name == "SE-monster-elite.png":
                new_manifest["fast_enemy"] = {
                    "file": f"starlights_end/monsters/{file_path.name}",
                    "scale": [40, 30]
                }
            elif file_path.name == "SE-monster-super.png":
                new_manifest["tank_enemy"] = {
                    "file": f"starlights_end/monsters/{file_path.name}",
                    "scale": [45, 35]
                }
            elif file_path.name == "SE-monster-mini-boss.png":
                new_manifest["mini_boss"] = {
                    "file": f"starlights_end/monsters/{file_path.name}",
                    "scale": [80, 60]
                }
            elif file_path.name == "SE-monster-boss.png":
                new_manifest["main_boss"] = {
                    "file": f"starlights_end/monsters/{file_path.name}",
                    "scale": [120, 90]
                }
    
    # Save the updated manifest
    with open(manifest_path, "w") as f:
        json.dump(new_manifest, f, indent=4)
    
    print(f"Updated manifest at {manifest_path}")
    print(f"Added {len(new_manifest)} entries to the manifest")

if __name__ == "__main__":
    main()
