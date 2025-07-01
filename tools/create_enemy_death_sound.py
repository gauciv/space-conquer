"""
Create a satisfying enemy death sound effect.
This script generates a sound effect for when low-type enemies are destroyed.
"""
import os
import numpy as np
from scipy.io import wavfile
import random

def create_enemy_death_sound():
    """Create a satisfying enemy death sound effect."""
    # Sound parameters
    sample_rate = 44100  # Standard sample rate
    duration = 0.4  # Sound duration in seconds
    
    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create base explosion sound (white noise with exponential decay)
    noise = np.random.normal(0, 1, len(t))
    decay = np.exp(-5 * t)  # Exponential decay
    explosion = noise * decay
    
    # Add a metallic impact component
    impact_freq = 220  # Base frequency
    impact = np.sin(2 * np.pi * impact_freq * t) * np.exp(-15 * t)
    
    # Add some higher frequency components for "crunch" effect
    crunch_freq1 = 1200
    crunch_freq2 = 1800
    crunch1 = np.sin(2 * np.pi * crunch_freq1 * t) * np.exp(-25 * t) * 0.3
    crunch2 = np.sin(2 * np.pi * crunch_freq2 * t) * np.exp(-30 * t) * 0.2
    
    # Add a low frequency "boom" component
    boom_freq = 80
    boom = np.sin(2 * np.pi * boom_freq * t) * np.exp(-8 * t) * 0.8
    
    # Combine all components
    sound = explosion * 0.3 + impact * 0.4 + crunch1 + crunch2 + boom
    
    # Add some distortion for a more aggressive sound
    distortion_amount = 0.2
    sound = sound * (1 + distortion_amount * np.sign(sound) * np.abs(sound))
    
    # Normalize to prevent clipping
    sound = sound / np.max(np.abs(sound))
    
    # Convert to 16-bit PCM
    sound = (sound * 32767).astype(np.int16)
    
    # Create stereo sound
    stereo_sound = np.column_stack((sound, sound))
    
    # Create sounds directory if it doesn't exist
    sounds_dir = os.path.join('..', 'sounds')
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    
    # Save the sound
    output_path = os.path.join(sounds_dir, 'enemy_death.wav')
    wavfile.write(output_path, sample_rate, stereo_sound)
    print(f"Enemy death sound created at: {output_path}")

if __name__ == "__main__":
    create_enemy_death_sound()
