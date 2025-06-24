# Space Impact Game

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/space-impact/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python recreation of the classic Space Impact game that was popular on Nokia phones.

## Description

Space Impact is a side-scrolling shooter game where you control a spaceship and must destroy enemy ships while avoiding collisions. This version includes:

- Multiple enemy types with different behaviors
- Custom designed spaceship graphics
- Power-ups to enhance your ship
- Increasing difficulty over time
- Score tracking
- Sound effects with adjustable volume
- Background music with separate volume control
- Settings menu

## Project Structure

The project follows a modular structure for better maintainability:

```
space-impact/
├── main.py                  # Main entry point
├── setup.py                 # Setup script for installation
├── tools/                   # Utility scripts for development
├── images/                  # Original game images
├── sounds/                  # Original sound effects
├── music/                   # Original background music
└── space_impact/            # Main package
    ├── __init__.py
    ├── config.py            # Game configuration
    ├── game_manager.py      # Main game manager
    ├── version.py           # Version information
    ├── assets/              # Game images
    ├── sounds/              # Sound effects
    ├── music/               # Background music
    ├── sprites/             # Game sprites
    │   ├── __init__.py
    │   ├── player.py        # Player sprite
    │   ├── bullet.py        # Bullet sprite
    │   ├── enemy.py         # Enemy sprites
    │   ├── powerup.py       # Power-up sprites
    │   └── star.py          # Background stars
    └── utils/               # Utility modules
        ├── __init__.py
        ├── asset_loader.py  # Asset loading
        ├── sound_manager.py # Sound management
        └── ui_manager.py    # UI management
```

## How to Run the Game

### Method 1: Direct Execution

1. Make sure you have Python and Pygame installed
2. Run the game with:
   ```
   python main.py
   ```
   or
   ```
   python3 main.py
   ```

### Method 2: Using a Virtual Environment

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install required packages:
   ```
   pip install pygame numpy
   ```

4. Run the game:
   ```
   python main.py
   ```

### Method 3: Installation as a Package

1. Install the package in development mode:
   ```
   pip install -e .
   ```

2. Run the game:
   ```
   python -m space_impact
   ```

## Controls

- Arrow keys: Move your ship
- SPACE: Shoot
- SPACE (at start/game over screen): Start/restart game
- ESC: Close settings menu
- Mouse: Interact with settings menu and volume sliders

## Game Features

### Power-ups

- Green cross: Extra health
- Blue triangle: Speed boost
- White/red square: Rapid fire (temporary)

### Enemy Types

- Normal (red): Basic enemy
- Fast (triangular): Moves quickly but has low health
- Tank (armored): Slow but requires multiple hits to destroy

### Audio

The game includes both sound effects and background music:
- Sound effects: Shooting, explosions, and power-up collection
- Background music: Chiptune-style music that loops continuously
- Both sound effects and music have separate volume controls in the settings menu
- Setting music volume to 0% automatically turns off the background music

## Development

### Tools Directory

The `tools` directory contains utility scripts for development:
- Sound creation scripts
- Image generation scripts
- Testing utilities

These are not required to run the game but are useful for development and customization.

## Versioning

This project uses [Semantic Versioning](https://semver.org/). See the [CHANGELOG.md](CHANGELOG.md) file for details on changes between versions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created as a learning project for Python game development with Pygame.
