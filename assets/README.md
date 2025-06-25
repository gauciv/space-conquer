# Space Conquer Asset System

This directory contains the asset management system for Space Conquer. The system is designed to be flexible and extensible, allowing for easy customization of the game's appearance and sounds.

## Directory Structure

- `images/`: Contains game images and sprites
- `sounds/`: Contains sound effects
- `music/`: Contains background music tracks
- `maps/`: Contains map definitions
- `themes/`: Contains theme definitions
- `packs/`: Contains asset packs that can be installed

## Asset Manifests

Each asset type has a manifest file that defines the available assets:

- `images/manifest.json`: Defines available images and their properties
- `sounds/manifest.json`: Defines available sound effects and their properties
- `music/manifest.json`: Defines available music tracks and their properties
- `maps/manifest.json`: Defines available maps and their properties

## Adding New Assets

### Images

To add a new image:

1. Place the image file in the `images/` directory
2. Add an entry to `images/manifest.json`:

```json
"my_new_image": {
    "file": "my_image.png",
    "scale": [50, 50]
}
```

### Sounds

To add a new sound effect:

1. Place the sound file in the `sounds/` directory
2. Add an entry to `sounds/manifest.json`:

```json
"my_new_sound": {
    "file": "my_sound.wav",
    "volume": 0.7
}
```

### Music

To add a new music track:

1. Place the music file in the `music/` directory
2. Add an entry to `music/manifest.json`:

```json
"my_new_music": {
    "file": "my_music.wav",
    "volume": 0.5
}
```

### Maps

To add a new map:

1. Add an entry to `maps/manifest.json`:

```json
{
    "id": "my_new_map",
    "name": "My New Map",
    "description": "Description of my new map",
    "background": "my_map_bg.png",
    "music": "my_map_music",
    "enemy_spawn_rate": 1200,
    "enemy_types": ["normal", "fast", "tank"],
    "boss": "mini_boss",
    "difficulty": 2
}
```

2. Add the background image to the `images/` directory and update `images/manifest.json`
3. Add the music track to the `music/` directory and update `music/manifest.json`

## Themes

Themes allow you to customize the game's appearance. To create a new theme:

1. Create a new JSON file in the `themes/` directory (e.g., `themes/my_theme.json`)
2. Define the theme properties:

```json
{
    "name": "my_theme",
    "description": "My custom theme",
    "ui": {
        "font_main": "Arial",
        "font_title": "Arial",
        "color_primary": [150, 150, 255],
        "color_secondary": [100, 100, 180],
        "color_background": [20, 20, 40],
        "color_text": [220, 220, 255],
        "color_highlight": [180, 180, 255],
        "button_style": "space"
    },
    "overrides": {
        "images": {
            "player": "my_player_ship.png"
        },
        "sounds": {
            "shoot": "my_shoot_sound.wav"
        },
        "music": {
            "menu": "my_menu_music.wav"
        }
    }
}
```

## Asset Packs

Asset packs are collections of assets that can be installed as a unit. See the `packs/README.md` file for more information on creating and installing asset packs.

## Asset Manager API

The asset manager provides a simple API for accessing assets:

```python
# Get an image
image = asset_manager.get_image("player")

# Get a sound
sound = asset_manager.get_sound("shoot")

# Play a sound
asset_manager.play_sound("shoot")

# Get a music track path
music_path = asset_manager.get_music_path("menu")

# Get a map
map_data = asset_manager.get_map("starlight_end")

# Get all maps
maps = asset_manager.get_all_maps()

# Set a theme
asset_manager.set_theme("my_theme")

# Get a UI color
color = asset_manager.get_ui_color("primary")

# Get a font
font = asset_manager.get_font("main", 20)

# Reload assets
asset_manager.reload_assets()
```
