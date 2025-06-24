import pygame
import numpy as np
import wave
import struct
import os

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

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
            # Create a rising tone effect
            if i < num_samples // 3:
                freq = frequency * (1 + i / (num_samples // 3) * 0.5)  # Increase frequency by 50%
            else:
                freq = frequency * 1.5
            
            # Apply volume envelope
            if i < num_samples // 10:
                vol = volume * (i / (num_samples // 10))  # Fade in
            elif i > num_samples * 0.8:
                vol = volume * (1 - (i - num_samples * 0.8) / (num_samples * 0.2))  # Fade out
            else:
                vol = volume
            
            sample = int(vol * 32767.0 * np.sin(2 * np.pi * freq * i / sample_rate))
            # Pack the sample as a 16-bit signed integer
            packed_sample = struct.pack('h', sample)
            samples.append(packed_sample)
        
        # Write the samples to the WAV file
        wav_file.writeframes(b''.join(samples))

# Create a triumphant start game sound
print("Creating start game sound...")
create_tone_file('sounds/game_start.wav', 440, 1.0, 0.7)  # A4 note, 1 second, 70% volume

print("Start game sound created successfully!")
