#!/usr/bin/env python3
"""
Script to update the manifest.json file with standardized size dimensions
for all game entities, establishing a clear visual hierarchy.
"""
import json
from pathlib import Path

# Define base directory
base_dir = Path(__file__).resolve().parent.parent
manifest_path = base_dir / "assets" / "images" / "manifest.json"

# Load the existing manifest
with open(manifest_path, "r") as f:
    manifest = json.load(f)

# Define standard sizes
sizes = {
    "player": [50, 30],        # Baseline
    "bullet": [10, 5],         # Small projectile
    "lower": [40, 25],         # 0.8x player size
    "elite": [60, 35],         # 1.2x player size
    "super": [80, 45],         # 1.6x player size
    "mini-boss": [120, 70],    # 2.4x player size
    "boss": [180, 100],        # 3.6x player size
    "powerup": [25, 25],       # Standard powerup size
    "heart": [32, 32],         # UI element
    "health-bar": [100, 10],   # UI element
    "settings": [30, 30],      # UI element
    "slider-bar": [100, 10],   # UI element
    "slider-handle": [20, 20], # UI element
}

# Update manifest with standardized sizes
for asset_id, asset_data in manifest.items():
    # Player assets
    if asset_id == "player" or asset_id == "player-default" or "player-variant" in asset_id:
        asset_data["scale"] = sizes["player"]
    
    # Bullet assets
    elif asset_id == "bullet" or "bullet" in asset_id:
        asset_data["scale"] = sizes["bullet"]
    
    # Monster assets - Starlights End
    elif "SE-monster-lower" in asset_id or "normal_enemy" in asset_id:
        asset_data["scale"] = sizes["lower"]
    elif "SE-monster-elite" in asset_id or "fast_enemy" in asset_id:
        asset_data["scale"] = sizes["elite"]
    elif "SE-monster-super" in asset_id or "tank_enemy" in asset_id:
        asset_data["scale"] = sizes["super"]
    elif "SE-monster-mini-boss" in asset_id or "mini_boss" in asset_id:
        asset_data["scale"] = sizes["mini-boss"]
    elif "SE-monster-boss" in asset_id or "main_boss" in asset_id:
        asset_data["scale"] = sizes["boss"]
    
    # Monster assets - Crimson Frontier
    elif "CF-monster-lower" in asset_id:
        asset_data["scale"] = sizes["lower"]
    elif "CF-monster-elite" in asset_id:
        asset_data["scale"] = sizes["elite"]
    elif "CF-monster-super" in asset_id:
        asset_data["scale"] = sizes["super"]
    elif "CF-monster-mini-boss" in asset_id:
        asset_data["scale"] = sizes["mini-boss"]
    elif "CF-monster-boss" in asset_id:
        asset_data["scale"] = sizes["boss"]
    
    # Monster assets - Oblivion Veil
    elif "OV-monster-lower" in asset_id:
        asset_data["scale"] = sizes["lower"]
    elif "OV-monster-elite" in asset_id:
        asset_data["scale"] = sizes["elite"]
    elif "OV-monster-super" in asset_id:
        asset_data["scale"] = sizes["super"]
    elif "OV-monster-mini-boss" in asset_id:
        asset_data["scale"] = sizes["mini-boss"]
    elif "OV-monster-boss" in asset_id:
        asset_data["scale"] = sizes["boss"]
    
    # Powerup assets
    elif "powerup" in asset_id:
        asset_data["scale"] = sizes["powerup"]
    
    # UI assets
    elif "heart" in asset_id:
        asset_data["scale"] = sizes["heart"]
    elif "health-bar" in asset_id or "health_bar" in asset_id:
        asset_data["scale"] = sizes["health-bar"]
    elif "settings" in asset_id:
        asset_data["scale"] = sizes["settings"]
    elif "slider-bar" in asset_id or "slider_bar" in asset_id:
        asset_data["scale"] = sizes["slider-bar"]
    elif "slider-handle" in asset_id or "slider_handle" in asset_id:
        asset_data["scale"] = sizes["slider-handle"]

# Save the updated manifest
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=4)

print(f"Updated manifest at {manifest_path} with standardized size dimensions")
print("Size hierarchy established:")
print(f"  Player:     {sizes['player'][0]}x{sizes['player'][1]} (baseline)")
print(f"  Lower:      {sizes['lower'][0]}x{sizes['lower'][1]} (0.8x player size)")
print(f"  Elite:      {sizes['elite'][0]}x{sizes['elite'][1]} (1.2x player size)")
print(f"  Super:      {sizes['super'][0]}x{sizes['super'][1]} (1.6x player size)")
print(f"  Mini-Boss:  {sizes['mini-boss'][0]}x{sizes['mini-boss'][1]} (2.4x player size)")
print(f"  Boss:       {sizes['boss'][0]}x{sizes['boss'][1]} (3.6x player size)")
