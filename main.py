#!/usr/bin/env python3
"""
Space Impact Game - Main Entry Point

A Python recreation of the classic Space Impact game that was popular on Nokia phones.
"""
from space_impact.game_manager import GameManager

def main():
    """Main entry point for the game."""
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()
