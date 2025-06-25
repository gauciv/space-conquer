#!/usr/bin/env python3
"""
Script to clean up old asset files after consolidation.
This will remove asset files from the old locations that have been consolidated into the new assets directory.
"""
import os
import shutil
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Clean up old asset files after consolidation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without actually deleting")
    args = parser.parse_args()
    
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    # Define old asset directories
    old_asset_dirs = [
        base_dir / "images",
        base_dir / "sounds",
        base_dir / "music",
        base_dir / "space_impact" / "assets",
        base_dir / "space_impact" / "sounds",
        base_dir / "space_impact" / "music"
    ]
    
    # Define asset file extensions
    asset_extensions = [".png", ".jpg", ".jpeg", ".gif", ".wav", ".ogg", ".mp3"]
    
    # Count files to be deleted
    total_files = 0
    
    # Process each directory
    for dir_path in old_asset_dirs:
        if not dir_path.exists():
            print(f"Directory {dir_path} does not exist, skipping.")
            continue
        
        print(f"Processing directory: {dir_path}")
        
        # Find asset files
        for file_path in dir_path.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in asset_extensions:
                total_files += 1
                
                if args.dry_run:
                    print(f"Would delete: {file_path}")
                else:
                    print(f"Deleting: {file_path}")
                    os.remove(file_path)
    
    # Print summary
    if args.dry_run:
        print(f"\nDry run complete. {total_files} files would be deleted.")
    else:
        print(f"\nCleanup complete. {total_files} files deleted.")

if __name__ == "__main__":
    main()
