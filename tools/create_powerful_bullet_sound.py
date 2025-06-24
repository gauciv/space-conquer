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
total_duration = 0.15  # short, punchy sound

# Create a powerful bullet sound
print("Creating powerful bullet sound...")

# Create the WAV file
with wave.open('sounds/shoot.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    
    # Calculate samples
    num_samples = int(total_duration * sample_rate)
    
    # Create a buffer
    buffer = []
    
    # Generate a powerful laser-like sound
    for i in range(num_samples):
        t = i / sample_rate
        
        # Start with a high frequency that drops slightly (laser effect)
        freq = 1200 - (i / num_samples) * 600
        
        # Main tone (square wave for sharpness)
        if (t * freq) % 1 > 0.5:
            value = 0.7
        else:
            value = -0.7
        
        # Add a lower frequency component for body
        if (t * (freq/3)) % 1 > 0.5:
            value += 0.2
        else:
            value -= 0.2
            
        # Add some noise for texture
        value += np.random.normal(0, 0.1) * (1 - i/num_samples)
        
        # Apply envelope
        if i < num_samples // 10:
            # Very quick attack
            value *= i / (num_samples // 10)
        elif i > num_samples * 0.4:
            # Longer decay for a "whoosh" effect
            value *= (num_samples - i) / (num_samples * 0.6)
        
        # Clip to prevent distortion
        value = max(min(value, 0.9), -0.9)
        
        # Convert to 16-bit sample
        sample = int(value * 32767)
        buffer.append(struct.pack('h', sample))
    
    # Write to the WAV file
    wav_file.writeframes(b''.join(buffer))

print("Powerful bullet sound created successfully!")
