#!/usr/bin/env python3
"""
Script to consolidate assets into the new structure.
This will copy all assets from various locations into the new assets directory structure.
"""
import os
import shutil
from pathlib import Path

def main():
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    # Define asset directories
    asset_dirs = {
        "images": base_dir / "assets" / "images",
        "sounds": base_dir / "assets" / "sounds",
        "music": base_dir / "assets" / "music",
        "maps": base_dir / "assets" / "maps",
    }
    
    # Create directories if they don't exist
    for dir_path in asset_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Copy images
    print("Copying images...")
    copy_assets(base_dir / "images", asset_dirs["images"], [".png", ".jpg", ".jpeg", ".gif"])
    copy_assets(base_dir / "space_impact" / "assets", asset_dirs["images"], [".png", ".jpg", ".jpeg", ".gif"])
    
    # Copy sounds
    print("Copying sounds...")
    copy_assets(base_dir / "sounds", asset_dirs["sounds"], [".wav", ".ogg", ".mp3"])
    copy_assets(base_dir / "space_impact" / "sounds", asset_dirs["sounds"], [".wav", ".ogg", ".mp3"])
    
    # Copy music
    print("Copying music...")
    copy_assets(base_dir / "music", asset_dirs["music"], [".wav", ".ogg", ".mp3"])
    copy_assets(base_dir / "space_impact" / "music", asset_dirs["music"], [".wav", ".ogg", ".mp3"])
    
    print("Asset consolidation complete!")

def copy_assets(source_dir, target_dir, extensions):
    """Copy assets from source directory to target directory."""
    if not source_dir.exists():
        print(f"Source directory {source_dir} does not exist, skipping.")
        return
    
    for file_path in source_dir.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            target_path = target_dir / file_path.name
            if not target_path.exists():
                shutil.copy2(file_path, target_path)
                print(f"Copied {file_path} to {target_path}")
            else:
                print(f"File {target_path} already exists, skipping.")

if __name__ == "__main__":
    main()
