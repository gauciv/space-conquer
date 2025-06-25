#!/usr/bin/env python3
"""
Script to consolidate the directory structure by moving Python modules from space_impact/ to the root directory
and removing redundant directories.
"""
import os
import shutil
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Consolidate directory structure")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually doing it")
    args = parser.parse_args()
    
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    space_impact_dir = base_dir / "space_impact"
    
    # Create new directories in root if they don't exist
    new_dirs = ["src", "src/sprites", "src/utils"]
    for new_dir in new_dirs:
        dir_path = base_dir / new_dir
        if not dir_path.exists():
            if args.dry_run:
                print(f"Would create directory: {dir_path}")
            else:
                print(f"Creating directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
    
    # Move Python files from space_impact/ to src/
    python_files = list(space_impact_dir.glob("*.py"))
    for file_path in python_files:
        if file_path.name != "__init__.py":  # Skip __init__.py for now
            dest_path = base_dir / "src" / file_path.name
            if args.dry_run:
                print(f"Would move: {file_path} -> {dest_path}")
            else:
                print(f"Moving: {file_path} -> {dest_path}")
                shutil.copy2(file_path, dest_path)
    
    # Create __init__.py files
    init_files = ["src/__init__.py", "src/sprites/__init__.py", "src/utils/__init__.py"]
    for init_file in init_files:
        init_path = base_dir / init_file
        if args.dry_run:
            print(f"Would create: {init_path}")
        else:
            print(f"Creating: {init_path}")
            with open(init_path, "w") as f:
                f.write('"""Module initialization."""\n')
    
    # Move sprite files
    sprite_files = list((space_impact_dir / "sprites").glob("*.py"))
    for file_path in sprite_files:
        if file_path.name != "__init__.py":  # Skip __init__.py
            dest_path = base_dir / "src" / "sprites" / file_path.name
            if args.dry_run:
                print(f"Would move: {file_path} -> {dest_path}")
            else:
                print(f"Moving: {file_path} -> {dest_path}")
                shutil.copy2(file_path, dest_path)
    
    # Move utility files
    util_files = list((space_impact_dir / "utils").glob("*.py"))
    for file_path in util_files:
        if file_path.name != "__init__.py":  # Skip __init__.py
            dest_path = base_dir / "src" / "utils" / file_path.name
            if args.dry_run:
                print(f"Would move: {file_path} -> {dest_path}")
            else:
                print(f"Moving: {file_path} -> {dest_path}")
                shutil.copy2(file_path, dest_path)
    
    # Update main.py
    main_py_path = base_dir / "main.py"
    if main_py_path.exists():
        if args.dry_run:
            print(f"Would update imports in: {main_py_path}")
        else:
            print(f"Updating imports in: {main_py_path}")
            with open(main_py_path, "r") as f:
                content = f.read()
            
            # Replace import
            content = content.replace("from space_impact.game_manager", "from src.game_manager")
            
            with open(main_py_path, "w") as f:
                f.write(content)
    
    # Update imports in all Python files
    if not args.dry_run:
        print("\nUpdating imports in Python files...")
        update_imports(base_dir / "src")
    
    # Move asset files from space_impact to root assets directory
    asset_dirs = {
        "assets": "assets",
        "sounds": "assets/sounds",
        "music": "assets/music",
        "maps": "assets/maps"
    }
    
    for src_dir, dest_dir in asset_dirs.items():
        src_path = space_impact_dir / src_dir
        dest_path = base_dir / dest_dir
        
        if src_path.exists() and dest_path.exists():
            # Copy files from src_path to dest_path
            for file_path in src_path.glob("*"):
                if file_path.is_file():
                    dest_file = dest_path / file_path.name
                    if not dest_file.exists():
                        if args.dry_run:
                            print(f"Would copy: {file_path} -> {dest_file}")
                        else:
                            print(f"Copying: {file_path} -> {dest_file}")
                            shutil.copy2(file_path, dest_file)
    
    # Remove space_impact directory if not in dry-run mode
    if not args.dry_run:
        print(f"\nRemoving space_impact directory...")
        # Don't actually remove it yet, just to be safe
        print("IMPORTANT: Please manually remove the space_impact directory after verifying everything works.")
    else:
        print(f"\nWould remove space_impact directory")
    
    # Print summary
    if args.dry_run:
        print("\nDry run complete. No changes were made.")
    else:
        print("\nConsolidation complete. Please verify everything works before removing the space_impact directory.")

def update_imports(src_dir):
    """Update import statements in all Python files."""
    for file_path in src_dir.glob("**/*.py"):
        with open(file_path, "r") as f:
            content = f.read()
        
        # Replace imports
        content = content.replace("from ..config", "from src.config")
        content = content.replace("from ..utils", "from src.utils")
        content = content.replace("from ..sprites", "from src.sprites")
        content = content.replace("from ..", "from src")
        
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"Updated imports in: {file_path}")

if __name__ == "__main__":
    main()
