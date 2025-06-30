#!/usr/bin/env python3
"""
Music Tester Tool for Space Conquer

This tool helps you easily test different music files by copying them
to the correct locations and updating the game's music system.

Usage:
    python tools/music_tester.py --menu path/to/menu_music.wav
    python tools/music_tester.py --gameplay path/to/gameplay_music.wav
    python tools/music_tester.py --boss path/to/boss_music.wav
    python tools/music_tester.py --list  # List current music files
"""

import argparse
import shutil
import os
from pathlib import Path

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent

def get_music_dir():
    """Get the music assets directory."""
    return get_project_root() / "assets" / "music"

def list_current_music():
    """List currently available music files."""
    music_dir = get_music_dir()
    print(f"Current music files in {music_dir}:")
    
    music_files = {
        'menu': 'background_music.wav',
        'gameplay': 'gameplay_music.wav', 
        'boss': 'boss_music.wav'
    }
    
    for track_type, filename in music_files.items():
        file_path = music_dir / filename
        status = "✓ EXISTS" if file_path.exists() else "✗ MISSING"
        print(f"  {track_type.upper()}: {filename} - {status}")

def copy_music_file(source_path, track_type):
    """Copy a music file to the appropriate location."""
    music_dir = get_music_dir()
    
    # Ensure music directory exists
    music_dir.mkdir(parents=True, exist_ok=True)
    
    # Define target filenames
    target_files = {
        'menu': 'background_music.wav',
        'gameplay': 'gameplay_music.wav',
        'boss': 'boss_music.wav'
    }
    
    if track_type not in target_files:
        print(f"Error: Invalid track type '{track_type}'. Use: menu, gameplay, or boss")
        return False
    
    source = Path(source_path)
    if not source.exists():
        print(f"Error: Source file '{source_path}' does not exist")
        return False
    
    target = music_dir / target_files[track_type]
    
    try:
        shutil.copy2(source, target)
        print(f"✓ Copied {source.name} to {target}")
        print(f"  Track type: {track_type.upper()}")
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def backup_current_music():
    """Create backups of current music files."""
    music_dir = get_music_dir()
    backup_dir = music_dir / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    music_files = ['background_music.wav', 'gameplay_music.wav', 'boss_music.wav']
    
    for filename in music_files:
        source = music_dir / filename
        if source.exists():
            backup_path = backup_dir / f"{filename}.backup"
            shutil.copy2(source, backup_path)
            print(f"✓ Backed up {filename}")

def main():
    parser = argparse.ArgumentParser(description="Test different music files in Space Conquer")
    parser.add_argument('--menu', help='Path to menu music file')
    parser.add_argument('--gameplay', help='Path to gameplay music file')
    parser.add_argument('--boss', help='Path to boss music file')
    parser.add_argument('--list', action='store_true', help='List current music files')
    parser.add_argument('--backup', action='store_true', help='Backup current music files')
    
    args = parser.parse_args()
    
    if args.list:
        list_current_music()
        return
    
    if args.backup:
        backup_current_music()
        return
    
    if not any([args.menu, args.gameplay, args.boss]):
        print("No action specified. Use --help for usage information.")
        list_current_music()
        return
    
    success_count = 0
    
    if args.menu:
        if copy_music_file(args.menu, 'menu'):
            success_count += 1
    
    if args.gameplay:
        if copy_music_file(args.gameplay, 'gameplay'):
            success_count += 1
    
    if args.boss:
        if copy_music_file(args.boss, 'boss'):
            success_count += 1
    
    if success_count > 0:
        print(f"\n✓ Successfully updated {success_count} music file(s)")
        print("You can now run the game to test the new music!")
        print("\nTip: Use 'python tools/music_tester.py --backup' to backup your current files first")

if __name__ == "__main__":
    main()