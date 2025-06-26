#!/usr/bin/env python3
"""
Space Conquer - Main Entry Point

A Python recreation of the classic Space Impact game that was popular on Nokia phones.
"""
import pygame
from src.game_manager import GameManager

def main():
    """Main entry point for the game."""
    game = GameManager()
    # Store a reference to the game manager for global access
    pygame.app = type('', (), {})()
    pygame.app.game_manager = game
    game.run()

if __name__ == "__main__":
    main()
