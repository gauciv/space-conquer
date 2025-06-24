import pygame
import numpy as np
import os
import wave
import struct

# Initialize pygame
pygame.init()

# Create sounds directory if it doesn't exist
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Function to create a WAV file with a simple tone
def create_tone_file(filename, frequency, duration, volume=0.5):
    # Parameters for the WAV file
    sample_rate = 44100
    num_samples = int(round(duration * sample_rate))
    
    # Open the WAV file for writing
    with wave.open(filename, 'w') as wav_file:
        # Set the WAV file parameters
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        
        # Create the samples
        samples = []
        for i in range(num_samples):
            sample = int(volume * 32767.0 * np.sin(2 * np.pi * frequency * i / sample_rate))
            # Pack the sample as a 16-bit signed integer
            packed_sample = struct.pack('h', sample)
            samples.append(packed_sample)
        
        # Write the samples to the WAV file
        wav_file.writeframes(b''.join(samples))

# Create shoot sound (higher pitch, short duration)
print("Creating shoot sound...")
create_tone_file('sounds/shoot.wav', 440, 0.1, 0.3)  # A4 note, 0.1 seconds

# Create explosion sound (lower pitch, longer duration with decay)
print("Creating explosion sound...")
sample_rate = 44100
duration = 0.5
num_samples = int(round(duration * sample_rate))

with wave.open('sounds/explosion.wav', 'w') as wav_file:
    wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
    
    samples = []
    for i in range(num_samples):
        # Decreasing volume over time
        volume = 0.8 * (1.0 - i / num_samples)
        # Mix of frequencies for a more complex sound
        sample = int(volume * 32767.0 * (
            0.6 * np.sin(2 * np.pi * 100 * i / sample_rate) +  # Base frequency
            0.3 * np.sin(2 * np.pi * 80 * i / sample_rate) +   # Lower frequency
            0.1 * np.random.rand()                             # Noise component
        ))
        packed_sample = struct.pack('h', sample)
        samples.append(packed_sample)
    
    wav_file.writeframes(b''.join(samples))

# Create powerup sound (ascending tone)
print("Creating powerup sound...")
duration = 0.3
num_samples = int(round(duration * sample_rate))

with wave.open('sounds/powerup.wav', 'w') as wav_file:
    wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
    
    samples = []
    for i in range(num_samples):
        # Increasing frequency over time
        freq = 300 + (i / num_samples) * 500
        sample = int(0.4 * 32767.0 * np.sin(2 * np.pi * freq * i / sample_rate))
        packed_sample = struct.pack('h', sample)
        samples.append(packed_sample)
    
    wav_file.writeframes(b''.join(samples))

print("Sound files created successfully!")
