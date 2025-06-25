#!/usr/bin/env python3
"""
Script to fix the manifest.json file to include the new asset IDs.
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
    
    # Load the existing manifest
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    # Add new asset IDs
    new_assets = {
        # Player assets
        "player-default": {
            "file": "player/player-default.png",
            "scale": [50, 30]
        },
        "player-bullet-default": {
            "file": "player/player-bullet-default.png",
            "scale": [10, 5]
        },
        
        # Powerup assets
        "powerup-health": {
            "file": "powerups/powerup-health.png",
            "scale": [20, 20]
        },
        "powerup-speed": {
            "file": "powerups/powerup-speed.png",
            "scale": [20, 20]
        },
        "powerup-rapid-fire": {
            "file": "powerups/powerup-rapid-fire.png",
            "scale": [20, 20]
        },
        "powerup-score-multiplier": {
            "file": "powerups/powerup-score-multiplier.png",
            "scale": [20, 20]
        },
        
        # UI assets
        "ui-heart-full": {
            "file": "ui/ui-heart-full.png",
            "scale": [32, 32]
        },
        "ui-heart-empty": {
            "file": "ui/ui-heart-empty.png",
            "scale": [32, 32]
        },
        "ui-health-bar-bg": {
            "file": "ui/ui-health-bar-bg.png",
            "scale": [100, 10]
        },
        "ui-health-bar-fill": {
            "file": "ui/ui-health-bar-fill.png",
            "scale": [100, 10]
        },
        "ui-settings-cog": {
            "file": "ui/ui-settings-cog.png",
            "scale": [30, 30]
        },
        "ui-slider-bar": {
            "file": "ui/ui-slider-bar.png",
            "scale": [100, 10]
        },
        "ui-slider-handle": {
            "file": "ui/ui-slider-handle.png",
            "scale": [20, 20]
        },
        
        # Starlights End monsters
        "SE-monster-lower": {
            "file": "starlights_end/monsters/SE-monster-lower.png",
            "scale": [30, 20]
        },
        "SE-monster-elite": {
            "file": "starlights_end/monsters/SE-monster-elite.png",
            "scale": [40, 30]
        },
        "SE-monster-super": {
            "file": "starlights_end/monsters/SE-monster-super.png",
            "scale": [45, 35]
        },
        "SE-monster-mini-boss": {
            "file": "starlights_end/monsters/SE-monster-mini-boss.png",
            "scale": [80, 60]
        },
        "SE-monster-boss": {
            "file": "starlights_end/monsters/SE-monster-boss.png",
            "scale": [120, 90]
        },
        
        # Crimson Frontier monsters
        "CF-monster-lower": {
            "file": "crimson_frontier/monsters/CF-monster-lower.png",
            "scale": [30, 20]
        },
        "CF-monster-elite": {
            "file": "crimson_frontier/monsters/CF-monster-elite.png",
            "scale": [40, 30]
        },
        "CF-monster-super": {
            "file": "crimson_frontier/monsters/CF-monster-super.png",
            "scale": [45, 35]
        },
        "CF-monster-mini-boss": {
            "file": "crimson_frontier/monsters/CF-monster-mini-boss.png",
            "scale": [80, 60]
        },
        "CF-monster-boss": {
            "file": "crimson_frontier/monsters/CF-monster-boss.png",
            "scale": [120, 90]
        },
        
        # Oblivion Veil monsters
        "OV-monster-lower": {
            "file": "oblivion_veil/monsters/OV-monster-lower.png",
            "scale": [30, 20]
        },
        "OV-monster-elite": {
            "file": "oblivion_veil/monsters/OV-monster-elite.png",
            "scale": [40, 30]
        },
        "OV-monster-super": {
            "file": "oblivion_veil/monsters/OV-monster-super.png",
            "scale": [45, 35]
        },
        "OV-monster-mini-boss": {
            "file": "oblivion_veil/monsters/OV-monster-mini-boss.png",
            "scale": [80, 60]
        },
        "OV-monster-boss": {
            "file": "oblivion_veil/monsters/OV-monster-boss.png",
            "scale": [120, 90]
        }
    }
    
    # Add the new assets to the manifest
    manifest.update(new_assets)
    
    # Save the updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    
    print(f"Updated manifest at {manifest_path}")
    print(f"Added {len(new_assets)} new asset IDs to the manifest")

if __name__ == "__main__":
    main()
