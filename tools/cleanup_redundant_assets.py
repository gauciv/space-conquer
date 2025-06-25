#!/usr/bin/env python3
"""
Script to clean up redundant asset directories and files.
This will ensure all assets are properly consolidated in the assets/ directory.
"""
import os
import sys
import shutil
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Clean up redundant asset directories and files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually doing it")
    args = parser.parse_args()
    
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    # Define asset directories
    asset_dirs = {
        "images": base_dir / "assets" / "images",
        "sounds": base_dir / "assets" / "sounds",
        "music": base_dir / "assets" / "music",
        "maps": base_dir / "assets" / "maps",
    }
    
    # Define old directories to remove
    old_dirs = [
        base_dir / "images",
        base_dir / "sounds",
        base_dir / "music",
    ]
    
    # Ensure all assets are in the new structure
    for old_dir in old_dirs:
        if old_dir.exists():
            print(f"Checking {old_dir}...")
            
            # Determine the corresponding new directory
            dir_name = old_dir.name
            new_dir = asset_dirs.get(dir_name)
            
            if new_dir and new_dir.exists():
                # Copy any missing files
                for file_path in old_dir.glob("*"):
                    if file_path.is_file():
                        dest_path = new_dir / file_path.name
                        
                        # Check if the file exists in the new directory
                        if not dest_path.exists():
                            if args.dry_run:
                                print(f"Would copy: {file_path} -> {dest_path}")
                            else:
                                print(f"Copying: {file_path} -> {dest_path}")
                                shutil.copy2(file_path, dest_path)
                        else:
                            # Check if the files are different
                            if file_path.stat().st_size != dest_path.stat().st_size:
                                print(f"Warning: {file_path} and {dest_path} have different sizes")
                                print(f"  Old: {file_path.stat().st_size} bytes")
                                print(f"  New: {dest_path.stat().st_size} bytes")
            else:
                print(f"Warning: No corresponding directory for {old_dir}")
    
    # Remove old directories
    for old_dir in old_dirs:
        if old_dir.exists():
            if args.dry_run:
                print(f"Would remove directory: {old_dir}")
            else:
                print(f"Removing directory: {old_dir}")
                shutil.rmtree(old_dir)
    
    # Check for any other redundant asset directories
    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)
        
        # Skip certain directories
        if any(skip in str(root_path) for skip in ["venv", ".git", "fallback", "assets"]):
            continue
        
        # Check for asset directories
        for dir_name in dirs:
            if dir_name in ["images", "sounds", "music", "maps"]:
                dir_path = root_path / dir_name
                print(f"Found potential redundant directory: {dir_path}")
                
                # Check if it contains files
                files = list(dir_path.glob("*"))
                if files:
                    print(f"  Contains {len(files)} files")
                    
                    # Check if we should remove it
                    if args.dry_run:
                        print(f"  Would remove directory: {dir_path}")
                    else:
                        print(f"  Removing directory: {dir_path}")
                        shutil.rmtree(dir_path)
    
    # Print summary
    if args.dry_run:
        print("\nDry run complete. No changes were made.")
    else:
        print("\nCleanup complete.")

if __name__ == "__main__":
    main()
