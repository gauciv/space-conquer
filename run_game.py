#!/usr/bin/env python3
"""
One-click launcher for Space Conquer.
This script sets up a virtual environment if needed and runs the game.
"""
import os
import sys
import subprocess
import platform

def is_venv_installed():
    """Check if the virtual environment is already installed."""
    return os.path.exists('venv')

def create_venv():
    """Create a virtual environment."""
    print("Setting up virtual environment...")
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
        return True
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment.")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    # Determine the pip and python commands based on the platform
    if platform.system() == "Windows":
        pip_cmd = os.path.join("venv", "Scripts", "pip")
        python_cmd = os.path.join("venv", "Scripts", "python")
    else:
        pip_cmd = os.path.join("venv", "bin", "pip")
        python_cmd = os.path.join("venv", "bin", "python")
    
    try:
        subprocess.check_call([pip_cmd, 'install', '--upgrade', 'pip'])
        subprocess.check_call([pip_cmd, 'install', 'pygame', 'numpy'])
        return True, python_cmd
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        return False, None

def run_game(python_cmd):
    """Run the game."""
    print("Starting Space Conquer...")
    try:
        subprocess.check_call([python_cmd, 'main.py'])
        return True
    except subprocess.CalledProcessError:
        print("Failed to start the game.")
        return False

def main():
    """Main function."""
    print("Space Conquer Launcher")
    print("=====================")
    
    # Check if virtual environment exists
    if not is_venv_installed():
        if not create_venv():
            print("Error: Could not create virtual environment.")
            input("Press Enter to exit...")
            return
        
        success, python_cmd = install_dependencies()
        if not success:
            print("Error: Could not install dependencies.")
            input("Press Enter to exit...")
            return
    else:
        # Virtual environment exists, just get the python command
        if platform.system() == "Windows":
            python_cmd = os.path.join("venv", "Scripts", "python")
        else:
            python_cmd = os.path.join("venv", "bin", "python")
    
    # Run the game
    if not run_game(python_cmd):
        print("Error: Could not run the game.")
        input("Press Enter to exit...")
        return

if __name__ == "__main__":
    main()
