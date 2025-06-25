#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Define base directory
base_dir = Path(__file__).resolve().parent.parent
manifest_path = base_dir / "assets" / "images" / "manifest.json"

# Create a new manifest
new_manifest = {
    # Player assets
    "player": {"file": "player/player-default.png", "scale": [50, 30]},
    "normal_enemy": {"file": "starlights_end/monsters/SE-monster-lower.png", "scale": [30, 20]},
    "fast_enemy": {"file": "starlights_end/monsters/SE-monster-elite.png", "scale": [40, 30]},
    "tank_enemy": {"file": "starlights_end/monsters/SE-monster-super.png", "scale": [45, 35]},
    "bullet": {"file": "player/player-bullet-default.png", "scale": [10, 5]},
    "health_powerup": {"file": "powerups/powerup-health.png", "scale": [20, 20]},
    "speed_powerup": {"file": "powerups/powerup-speed.png", "scale": [20, 20]},
    "rapid_fire_powerup": {"file": "powerups/powerup-rapid-fire.png", "scale": [20, 20]},
    "score_multiplier": {"file": "powerups/powerup-score-multiplier.png", "scale": [20, 20]},
    "full_heart": {"file": "ui/ui-heart-full.png", "scale": [32, 32]},
    "empty_heart": {"file": "ui/ui-heart-empty.png", "scale": [32, 32]},
    "mini_boss": {"file": "starlights_end/monsters/SE-monster-mini-boss.png", "scale": [80, 60]},
    "main_boss": {"file": "starlights_end/monsters/SE-monster-boss.png", "scale": [120, 90]},
    "settings_cog": {"file": "ui/ui-settings-cog.png", "scale": [30, 30]},
    "slider_bar": {"file": "ui/ui-slider-bar.png", "scale": [100, 10]},
    "slider_handle": {"file": "ui/ui-slider-handle.png", "scale": [20, 20]},
    "health_bar_bg": {"file": "ui/ui-health-bar-bg.png", "scale": [100, 10]},
    "health_bar_fill": {"file": "ui/ui-health-bar-fill.png", "scale": [100, 10]},
}

# Add new asset IDs
new_manifest.update({
    "player-default": {"file": "player/player-default.png", "scale": [50, 30]},
    "player-bullet-default": {"file": "player/player-bullet-default.png", "scale": [10, 5]},
    "powerup-health": {"file": "powerups/powerup-health.png", "scale": [20, 20]},
    "powerup-speed": {"file": "powerups/powerup-speed.png", "scale": [20, 20]},
    "powerup-rapid-fire": {"file": "powerups/powerup-rapid-fire.png", "scale": [20, 20]},
    "powerup-score-multiplier": {"file": "powerups/powerup-score-multiplier.png", "scale": [20, 20]},
    "ui-heart-full": {"file": "ui/ui-heart-full.png", "scale": [32, 32]},
    "ui-heart-empty": {"file": "ui/ui-heart-empty.png", "scale": [32, 32]},
    "ui-health-bar-bg": {"file": "ui/ui-health-bar-bg.png", "scale": [100, 10]},
    "ui-health-bar-fill": {"file": "ui/ui-health-bar-fill.png", "scale": [100, 10]},
    "ui-settings-cog": {"file": "ui/ui-settings-cog.png", "scale": [30, 30]},
    "ui-slider-bar": {"file": "ui/ui-slider-bar.png", "scale": [100, 10]},
    "ui-slider-handle": {"file": "ui/ui-slider-handle.png", "scale": [20, 20]},
    "SE-monster-lower": {"file": "starlights_end/monsters/SE-monster-lower.png", "scale": [30, 20]},
    "SE-monster-elite": {"file": "starlights_end/monsters/SE-monster-elite.png", "scale": [40, 30]},
    "SE-monster-super": {"file": "starlights_end/monsters/SE-monster-super.png", "scale": [45, 35]},
    "SE-monster-mini-boss": {"file": "starlights_end/monsters/SE-monster-mini-boss.png", "scale": [80, 60]},
    "SE-monster-boss": {"file": "starlights_end/monsters/SE-monster-boss.png", "scale": [120, 90]}
})

# Save the updated manifest
with open(manifest_path, "w") as f:
    json.dump(new_manifest, f, indent=4)

print(f"Updated manifest at {manifest_path}")
print(f"Added {len(new_manifest)} entries to the manifest")
