# Space Impact Game

A Python recreation of the classic Space Impact game that was popular on Nokia phones.

## Description

Space Impact is a side-scrolling shooter game where you control a spaceship and must destroy enemy ships while avoiding collisions. This version includes:

- Multiple enemy types with different behaviors
- Power-ups to enhance your ship
- Increasing difficulty over time
- Score tracking
- Sound effects

## How to Play

1. Make sure you have Python and Pygame installed
2. Run the game with `python main.py` or `python3 main.py`
3. Use the arrow keys to move your ship
4. Press SPACE to shoot
5. Avoid enemy ships and collect power-ups

## Controls

- Arrow keys: Move your ship
- SPACE: Shoot
- SPACE (at start/game over screen): Start/restart game

## Power-ups

- Green cross: Extra health
- Blue triangle: Speed boost
- White/red square: Rapid fire (temporary)

## Enemy Types

- Normal (red square): Basic enemy
- Fast (red triangle): Moves quickly but has low health
- Tank (red circle): Slow but requires multiple hits to destroy

## Requirements

- Python 3.x
- Pygame

## Installation

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install Pygame:
   ```
   pip install pygame
   ```

4. Run the game:
   ```
   python main.py
   ```

## Credits

Created as a learning project for Python game development with Pygame.
