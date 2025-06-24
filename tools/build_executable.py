#!/usr/bin/env python3
"""
Build script to create standalone executables for Space Impact.
"""
import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Version from the package
sys.path.insert(0, str(ROOT_DIR))
from space_impact.version import __version__

# Output directory for builds
BUILD_DIR = ROOT_DIR / "dist"
RELEASE_DIR = ROOT_DIR / "releases"

# Path to PyInstaller in virtual environment
VENV_DIR = ROOT_DIR / "venv"
if platform.system().lower() == "windows":
    PYINSTALLER = VENV_DIR / "Scripts" / "pyinstaller.exe"
else:
    PYINSTALLER = VENV_DIR / "bin" / "pyinstaller"

def clean_build_dirs():
    """Clean build directories before building."""
    for directory in [BUILD_DIR, RELEASE_DIR]:
        if directory.exists():
            print(f"Cleaning {directory}...")
            shutil.rmtree(directory)
        directory.mkdir(exist_ok=True)

def copy_assets():
    """Copy necessary assets to the build directory."""
    # This is handled by PyInstaller's data files, but we can add extra files here if needed
    pass

def build_executable():
    """Build the executable using PyInstaller."""
    system = platform.system().lower()
    
    # Check if PyInstaller exists
    if not PYINSTALLER.exists():
        print(f"Error: PyInstaller not found at {PYINSTALLER}")
        print("Make sure you've activated the virtual environment and installed PyInstaller.")
        return False
    
    # Base PyInstaller command
    cmd = [
        str(PYINSTALLER),
        "--name=SpaceImpact",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window on Windows
        "--icon=images/player_ship.png",  # Use player ship as icon
        "--add-data=images:images",  # Include images directory
        "--add-data=sounds:sounds",  # Include sounds directory
        "--add-data=music:music",    # Include music directory
        "main.py"
    ]
    
    # Adjust path separator for Windows
    if system == "windows":
        cmd = [arg.replace(":", ";") for arg in cmd]
    
    # Run PyInstaller
    print("Building executable...")
    subprocess.run(cmd, cwd=str(ROOT_DIR), check=True)
    
    # Create version-specific release directory
    release_version_dir = RELEASE_DIR / f"SpaceImpact-v{__version__}"
    release_version_dir.mkdir(exist_ok=True)
    
    # Copy the executable to the release directory
    if system == "windows":
        executable = BUILD_DIR / "SpaceImpact.exe"
        target = release_version_dir / "SpaceImpact.exe"
    elif system == "darwin":  # macOS
        executable = BUILD_DIR / "SpaceImpact"
        target = release_version_dir / "SpaceImpact"
    else:  # Linux
        executable = BUILD_DIR / "SpaceImpact"
        target = release_version_dir / "SpaceImpact"
    
    if executable.exists():
        shutil.copy2(executable, target)
        print(f"Executable copied to {target}")
    else:
        print(f"Error: Executable not found at {executable}")
        return False
    
    # Copy README, LICENSE, etc.
    for file in ["README.md", "LICENSE", "CHANGELOG.md"]:
        src = ROOT_DIR / file
        if src.exists():
            shutil.copy2(src, release_version_dir / file)
    
    # Create a simple launcher script for Linux/macOS
    if system != "windows":
        with open(release_version_dir / "run_game.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("chmod +x ./SpaceImpact\n")
            f.write("./SpaceImpact\n")
        os.chmod(release_version_dir / "run_game.sh", 0o755)
    
    # Create ZIP archive
    archive_name = f"SpaceImpact-v{__version__}-{system}"
    shutil.make_archive(
        str(RELEASE_DIR / archive_name),
        "zip",
        root_dir=str(RELEASE_DIR),
        base_dir=f"SpaceImpact-v{__version__}"
    )
    
    print(f"Release archive created: {archive_name}.zip")
    return True

if __name__ == "__main__":
    clean_build_dirs()
    copy_assets()
    success = build_executable()
    sys.exit(0 if success else 1)
