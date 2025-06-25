# Space Conquer Asset Structure

This document explains the new asset structure for the Space Conquer game.

## Directory Structure

```
assets/
├── images/                     # All game images
│   ├── player/                 # Player ships and bullets
│   │   ├── player-default.png  # Default player ship
│   │   ├── player-variant1.png # Player ship variant 1
│   │   ├── player-variant2.png # Player ship variant 2
│   │   ├── player-variant3.png # Player ship variant 3
│   │   ├── player-bullet-default.png  # Default bullet
│   │   ├── player-bullet-enhanced.png # Enhanced bullet
│   │   └── player-bullet-special.png  # Special bullet
│   │
│   ├── powerups/               # Power-up items
│   │   ├── powerup-health.png        # Health power-up
│   │   ├── powerup-speed.png         # Speed power-up
│   │   ├── powerup-rapid-fire.png    # Rapid fire power-up
│   │   ├── powerup-score-multiplier.png # Score multiplier power-up
│   │   ├── powerup-shield.png        # Shield power-up
│   │   ├── powerup-bomb.png          # Bomb power-up
│   │   └── powerup-special.png       # Special power-up
│   │
│   ├── ui/                     # UI elements
│   │   ├── ui-heart-full.png         # Full heart for health display
│   │   ├── ui-heart-empty.png        # Empty heart for health display
│   │   ├── ui-health-bar-bg.png      # Health bar background
│   │   ├── ui-health-bar-fill.png    # Health bar fill
│   │   ├── ui-settings-cog.png       # Settings button
│   │   ├── ui-slider-bar.png         # Slider bar
│   │   ├── ui-slider-handle.png      # Slider handle
│   │   ├── ui-button-start.png       # Start button
│   │   ├── ui-button-exit.png        # Exit button
│   │   ├── ui-background-menu.png    # Menu background
│   │   └── ui-background-gameover.png # Game over background
│   │
│   ├── starlights_end/         # Starlights End map assets
│   │   ├── SE-map-visual.png         # Map visual
│   │   ├── SE-map-background.png     # Map background
│   │   ├── monsters/                 # Monsters for this map
│   │   │   ├── SE-monster-low-normal.png    # Normal enemy (low tier)
│   │   │   ├── SE-monster-low-fast.png      # Fast enemy (low tier)
│   │   │   ├── SE-monster-elite-tank.png    # Tank enemy (elite tier)
│   │   │   ├── SE-monster-elite-drone.png   # Drone enemy (elite tier)
│   │   │   ├── SE-monster-super-bomber.png  # Bomber enemy (super tier)
│   │   │   ├── SE-monster-mini-boss.png     # Mini boss
│   │   │   └── SE-monster-boss.png          # Main boss
│   │   │
│   │   └── additional_assets/        # Additional map-specific assets
│   │       ├── SE-asset-asteroid.png       # Asteroid obstacle
│   │       ├── SE-asset-debris.png         # Space debris
│   │       └── SE-asset-nebula.png         # Nebula effect
│   │
│   ├── crimson_frontier/       # Crimson Frontier map assets
│   │   ├── CF-map-visual.png         # Map visual
│   │   ├── CF-map-background.png     # Map background
│   │   ├── monsters/                 # Monsters for this map
│   │   │   ├── CF-monster-low-scout.png     # Scout enemy (low tier)
│   │   │   ├── CF-monster-low-fighter.png   # Fighter enemy (low tier)
│   │   │   ├── CF-monster-elite-destroyer.png # Destroyer enemy (elite tier)
│   │   │   ├── CF-monster-elite-carrier.png # Carrier enemy (elite tier)
│   │   │   ├── CF-monster-super-dreadnought.png # Dreadnought enemy (super tier)
│   │   │   ├── CF-monster-mini-boss.png     # Mini boss
│   │   │   └── CF-monster-boss.png          # Main boss
│   │   │
│   │   └── additional_assets/        # Additional map-specific assets
│   │       ├── CF-asset-minefield.png      # Minefield obstacle
│   │       ├── CF-asset-turret.png         # Defense turret
│   │       └── CF-asset-forcefield.png     # Force field effect
│   │
│   └── oblivion_veil/          # Oblivion Veil map assets
│       ├── OV-map-visual.png         # Map visual
│       ├── OV-map-background.png     # Map background
│       ├── monsters/                 # Monsters for this map
│       │   ├── OV-monster-low-phantom.png  # Phantom enemy (low tier)
│       │   ├── OV-monster-low-specter.png  # Specter enemy (low tier)
│       │   ├── OV-monster-elite-wraith.png # Wraith enemy (elite tier)
│       │   ├── OV-monster-elite-harbinger.png # Harbinger enemy (elite tier)
│       │   ├── OV-monster-super-annihilator.png # Annihilator enemy (super tier)
│       │   ├── OV-monster-mini-boss.png    # Mini boss
│       │   └── OV-monster-boss.png         # Main boss
│       │
│       └── additional_assets/        # Additional map-specific assets
│           ├── OV-asset-void-rift.png      # Void rift obstacle
│           ├── OV-asset-gravity-well.png   # Gravity well effect
│           └── OV-asset-dark-matter.png    # Dark matter effect
│
├── sounds/                     # Sound effects
│   ├── shoot.wav               # Shooting sound
│   ├── explosion.wav           # Explosion sound
│   ├── powerup.wav             # Power-up collection sound
│   ├── game_start.wav          # Game start sound
│   └── game_over.wav           # Game over sound
│
├── music/                      # Background music
│   ├── background_music.wav    # Main menu music
│   ├── starlight_end.wav       # Starlights End map music
│   └── boss_battle.wav         # Boss battle music
│
├── maps/                       # Map definitions
│   └── manifest.json           # Map configuration
│
├── fallback/                   # Fallback assets
│   ├── images/                 # Fallback images
│   ├── sounds/                 # Fallback sounds
│   ├── music/                  # Fallback music
│   └── maps/                   # Fallback map definitions
│
└── themes/                     # Theme definitions
```

## Naming Conventions

### Player Assets
- `player-default.png`: Default player ship
- `player-variant1.png`, `player-variant2.png`, etc.: Player ship variants
- `player-bullet-default.png`: Default bullet
- `player-bullet-enhanced.png`: Enhanced bullet
- `player-bullet-special.png`: Special bullet

### Power-up Assets
- `powerup-health.png`: Health power-up
- `powerup-speed.png`: Speed power-up
- `powerup-rapid-fire.png`: Rapid fire power-up
- `powerup-score-multiplier.png`: Score multiplier power-up
- `powerup-shield.png`: Shield power-up
- `powerup-bomb.png`: Bomb power-up
- `powerup-special.png`: Special power-up

### UI Assets
- `ui-heart-full.png`: Full heart for health display
- `ui-heart-empty.png`: Empty heart for health display
- `ui-health-bar-bg.png`: Health bar background
- `ui-health-bar-fill.png`: Health bar fill
- `ui-settings-cog.png`: Settings button
- `ui-slider-bar.png`: Slider bar
- `ui-slider-handle.png`: Slider handle
- `ui-button-start.png`: Start button
- `ui-button-exit.png`: Exit button
- `ui-background-menu.png`: Menu background
- `ui-background-gameover.png`: Game over background

### Map Assets
- `SE-map-visual.png`: Starlights End map visual
- `SE-map-background.png`: Starlights End map background
- `CF-map-visual.png`: Crimson Frontier map visual
- `CF-map-background.png`: Crimson Frontier map background
- `OV-map-visual.png`: Oblivion Veil map visual
- `OV-map-background.png`: Oblivion Veil map background

### Monster Assets
- `SE-monster-low-normal.png`: Normal enemy (low tier) for Starlights End
- `SE-monster-low-fast.png`: Fast enemy (low tier) for Starlights End
- `SE-monster-elite-tank.png`: Tank enemy (elite tier) for Starlights End
- `SE-monster-elite-drone.png`: Drone enemy (elite tier) for Starlights End
- `SE-monster-super-bomber.png`: Bomber enemy (super tier) for Starlights End
- `SE-monster-mini-boss.png`: Mini boss for Starlights End
- `SE-monster-boss.png`: Main boss for Starlights End

Similar naming conventions apply for Crimson Frontier (CF-) and Oblivion Veil (OV-) monsters.

### Additional Map Assets
- `SE-asset-asteroid.png`: Asteroid obstacle for Starlights End
- `SE-asset-debris.png`: Space debris for Starlights End
- `SE-asset-nebula.png`: Nebula effect for Starlights End

Similar naming conventions apply for Crimson Frontier (CF-) and Oblivion Veil (OV-) additional assets.

## Asset Manifest

The `manifest.json` file in each asset directory defines the available assets and their properties. For example, the `images/manifest.json` file contains:

```json
{
  "player-default": {
    "file": "player/player-default.png",
    "scale": [50, 30]
  },
  "SE-monster-low-normal": {
    "file": "starlights_end/monsters/SE-monster-low-normal.png",
    "scale": [40, 30]
  },
  ...
}
```

## Fallback Assets

The game includes a fallback asset system that provides default assets when the requested assets cannot be loaded. This ensures that the game never crashes due to missing assets.

Fallback assets are stored in the `assets/fallback/` directory, which mirrors the main assets directory structure.

## Adding New Assets

To add new assets:

1. Place the asset file in the appropriate directory
2. Update the corresponding manifest file to include the new asset
3. Use the asset in your code by referencing its ID

For example, to add a new player ship variant:

1. Place the image file in `assets/images/player/player-variant4.png`
2. Add an entry to `assets/images/manifest.json`:
   ```json
   "player-variant4": {
     "file": "player/player-variant4.png",
     "scale": [50, 30]
   }
   ```
3. Use the asset in your code:
   ```python
   player_image = asset_manager.get_image("player-variant4")
   ```
