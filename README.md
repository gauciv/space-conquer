# Space Impact Game

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
├── images/                  # Game images
├── sounds/                  # Sound effects
├── music/                   # Background music
└── space_impact/            # Main package
    ├── __init__.py
    ├── config.py            # Game configuration
    ├── game_manager.py      # Main game manager
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

## How to Play

1. Make sure you have Python and Pygame installed
2. Run the game with `python main.py` or `python3 main.py`
3. Use the arrow keys to move your ship
4. Press SPACE to shoot
5. Avoid enemy ships and collect power-ups
6. Click the settings (cog) icon in the top-right corner to adjust volume

## Controls

- Arrow keys: Move your ship
- SPACE: Shoot
- SPACE (at start/game over screen): Start/restart game
- ESC: Close settings menu
- Mouse: Interact with settings menu and volume sliders

## Power-ups

- Green cross: Extra health
- Blue triangle: Speed boost
- White/red square: Rapid fire (temporary)

## Enemy Types

- Normal (red): Basic enemy
- Fast (triangular): Moves quickly but has low health
- Tank (armored): Slow but requires multiple hits to destroy

## Graphics

The game features custom-designed spaceship graphics:
- Player ship: Blue and green spaceship with engine effects
- Enemy ships: Different designs for each enemy type
- Power-ups: Distinct visual indicators for each power-up type
- Bullets: Yellow projectiles with orange tips

## Audio

The game includes both sound effects and background music:
- Sound effects: Shooting, explosions, and power-up collection
- Background music: Chiptune-style music that loops continuously
- Both sound effects and music have separate volume controls in the settings menu
- Setting music volume to 0% automatically turns off the background music

## Settings

The game includes a settings menu accessible by clicking the cog icon in the top-right corner:
- Sound Effects Volume: Adjust the volume of game sound effects (default: 70%)
- Music Volume: Adjust the volume of background music (default: 50%)
- Close button: Return to the game

## Requirements

- Python 3.6+
- Pygame
- NumPy (for sound generation)

## Installation

### Method 1: Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/space-impact.git
cd space-impact

# Install the game and dependencies
pip install -e .
```

### Method 2: Manual setup

1. Create a virtual environment:
   ```
   python3 -m venv venv
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

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

Created as a learning project for Python game development with Pygame.
