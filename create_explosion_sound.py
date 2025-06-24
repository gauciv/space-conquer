import pygame
import numpy as np
import wave
import struct
import os

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

# Create sounds directory if it doesn't exist
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Parameters
sample_rate = 44100
total_duration = 0.4  # medium length explosion

# Create an impactful explosion sound
print("Creating explosion sound...")

# Create the WAV file
with wave.open('sounds/explosion.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    
    # Calculate samples
    num_samples = int(total_duration * sample_rate)
    
    # Create a buffer
    buffer = []
    
    # Generate an explosion sound (noise + tonal components)
    for i in range(num_samples):
        progress = i / num_samples
        
        # Start with white noise (main explosion component)
        value = np.random.normal(0, 0.8) * (1 - progress*0.7)
        
        # Add some low frequency rumble
        t = i / sample_rate
        rumble_freq = 80 - progress * 30  # Decreasing frequency
        value += 0.4 * np.sin(2 * np.pi * rumble_freq * t) * (1 - progress)
        
        # Add some mid-frequency components for "debris" sound
        if progress > 0.1:
            debris_freq = 300 - progress * 200
            value += 0.2 * np.sin(2 * np.pi * debris_freq * t) * (1 - progress)
        
        # Apply envelope
        if i < num_samples // 20:
            # Very quick attack (explosion is sudden)
            value *= i / (num_samples // 20)
        elif i > num_samples * 0.2:
            # Longer decay
            value *= (1.0 - (progress - 0.2) / 0.8)
        
        # Clip to prevent distortion
        value = max(min(value, 0.9), -0.9)
        
        # Convert to 16-bit sample
        sample = int(value * 32767)
        buffer.append(struct.pack('h', sample))
    
    # Write to the WAV file
    wav_file.writeframes(b''.join(buffer))

print("Explosion sound created successfully!")
