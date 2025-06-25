#!/usr/bin/env python3
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
}

# Update manifest with standardized sizes
for asset_id, asset_data in manifest.items():
    # Player assets
    if "player" in asset_id and "bullet" not in asset_id:
        asset_data["scale"] = sizes["player"]
    # Bullet assets
    elif "bullet" in asset_id:
        asset_data["scale"] = sizes["bullet"]
    # Monster assets - Lower tier
    elif "lower" in asset_id or "normal_enemy" in asset_id:
        asset_data["scale"] = sizes["lower"]
    # Monster assets - Elite tier
    elif "elite" in asset_id or "fast_enemy" in asset_id:
        asset_data["scale"] = sizes["elite"]
    # Monster assets - Super tier
    elif "super" in asset_id or "tank_enemy" in asset_id:
        asset_data["scale"] = sizes["super"]
    # Monster assets - Mini-boss
    elif "mini-boss" in asset_id or "mini_boss" in asset_id:
        asset_data["scale"] = sizes["mini-boss"]
    # Monster assets - Boss
    elif "boss" in asset_id and "mini" not in asset_id:
        asset_data["scale"] = sizes["boss"]
    # Powerup assets
    elif "powerup" in asset_id:
        asset_data["scale"] = sizes["powerup"]

# Save the updated manifest
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=4)

print("Updated manifest with standardized size dimensions")
