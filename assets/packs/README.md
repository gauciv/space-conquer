# Asset Packs for Space Conquer

This directory contains asset packs that can be used to customize the game's appearance and sounds.

## Installing Asset Packs

To install an asset pack:

1. Place the asset pack folder in this directory
2. Start the game
3. Go to Options > Themes and select the new theme

## Creating Asset Packs

To create a new asset pack:

1. Use the in-game asset pack creator (Options > Create Asset Pack)
2. Or manually create a directory with the following structure:

```
my_asset_pack/
├── manifest.json
├── images/
│   ├── player_ship.png
│   ├── normal_enemy.png
│   └── ...
├── sounds/
│   ├── shoot.wav
│   ├── explosion.wav
│   └── ...
├── music/
│   ├── background_music.wav
│   ├── starlight_end.wav
│   └── ...
└── maps/
    └── custom_maps.json
```

The `manifest.json` file should contain:

```json
{
    "name": "My Asset Pack",
    "description": "Description of your asset pack",
    "version": "1.0.0",
    "author": "Your Name",
    "theme": {
        "name": "my_theme",
        "ui": {
            "font_main": "Arial",
            "font_title": "Arial",
            "color_primary": [150, 150, 255],
            "color_secondary": [100, 100, 180],
            "color_background": [20, 20, 40],
            "color_text": [220, 220, 255],
            "color_highlight": [180, 180, 255]
        }
    },
    "assets": {
        "images": {
            "player": "player_ship.png",
            "normal_enemy": "normal_enemy.png"
        },
        "sounds": {
            "shoot": "shoot.wav",
            "explosion": "explosion.wav"
        },
        "music": {
            "menu": "background_music.wav",
            "starlight_end": "starlight_end.wav"
        }
    }
}
```
