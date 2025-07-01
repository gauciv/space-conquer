"""
Create a simple enemy death sound effect.
This script generates a basic sound effect for when low-type enemies are destroyed.
"""
import os
import shutil

def create_simple_enemy_death_sound():
    """Create a simple enemy death sound effect by copying the explosion sound."""
    # Create sounds directory if it doesn't exist
    sounds_dir = os.path.join('assets', 'sounds')
    if not os.path.exists(sounds_dir):
        print(f"Sounds directory not found at: {sounds_dir}")
        return
    
    # Output path
    output_path = os.path.join(sounds_dir, 'enemy_death.wav')
    
    # Check if the file already exists
    if os.path.exists(output_path):
        print(f"Sound file already exists at: {output_path}")
        return
    
    # Copy the explosion sound
    explosion_path = os.path.join(sounds_dir, 'explosion.wav')
    if os.path.exists(explosion_path):
        # Copy the explosion sound
        shutil.copy(explosion_path, output_path)
        print(f"Created enemy death sound at: {output_path}")
    else:
        print(f"Explosion sound not found at: {explosion_path}")
        print("Cannot create enemy death sound")

if __name__ == "__main__":
    create_simple_enemy_death_sound()
