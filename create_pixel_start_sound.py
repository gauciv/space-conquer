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
total_duration = 1.2  # seconds

# Create a space adventure start sound
print("Creating pixel space adventure start sound...")

# Create the WAV file
with wave.open('sounds/game_start.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    
    # Create a sequence of ascending notes (arpeggio)
    base_freqs = [150, 200, 250, 300, 350, 400]
    note_duration = 0.15  # seconds
    
    for freq in base_freqs:
        # Calculate samples for this note
        num_samples = int(note_duration * sample_rate)
        
        # Create a buffer for this note
        buffer = []
        
        # Generate a square wave (8-bit sound)
        for i in range(num_samples):
            # Square wave with some noise for texture
            t = i / sample_rate
            
            # Main square wave
            if (t * freq) % 1 > 0.5:
                value = 0.7
            else:
                value = -0.7
                
            # Add a higher frequency component for richness
            if (t * freq * 2) % 1 > 0.5:
                value += 0.2
            else:
                value -= 0.2
                
            # Add some noise for texture
            value += np.random.normal(0, 0.05)
            
            # Apply envelope
            if i < num_samples // 10:
                # Fade in
                value *= i / (num_samples // 10)
            elif i > num_samples * 0.8:
                # Fade out
                value *= (num_samples - i) / (num_samples * 0.2)
            
            # Clip to prevent distortion
            value = max(min(value, 0.9), -0.9)
            
            # Convert to 16-bit sample
            sample = int(value * 32767)
            buffer.append(struct.pack('h', sample))
        
        # Write the note to the WAV file
        wav_file.writeframes(b''.join(buffer))
    
    # Add a final sweep up (power-up sound)
    sweep_duration = 0.3  # seconds
    sweep_samples = int(sweep_duration * sample_rate)
    sweep_buffer = []
    
    start_freq = 300
    end_freq = 900
    
    for i in range(sweep_samples):
        # Calculate current frequency (linear sweep)
        progress = i / sweep_samples
        current_freq = start_freq + (end_freq - start_freq) * progress
        
        # Generate sample
        t = i / sample_rate
        
        # Mix of square and sawtooth waves
        if (t * current_freq) % 1 > 0.5:
            value = 0.6
        else:
            value = -0.6
            
        # Add sawtooth component
        value += 0.3 * ((t * current_freq * 2) % 1 * 2 - 1)
        
        # Apply envelope
        if i < sweep_samples // 5:
            # Fade in
            value *= i / (sweep_samples // 5)
        elif i > sweep_samples * 0.7:
            # Fade out
            value *= (sweep_samples - i) / (sweep_samples * 0.3)
        
        # Clip to prevent distortion
        value = max(min(value, 0.9), -0.9)
        
        # Convert to 16-bit sample
        sample = int(value * 32767)
        sweep_buffer.append(struct.pack('h', sample))
    
    # Write the sweep to the WAV file
    wav_file.writeframes(b''.join(sweep_buffer))

print("Pixel space adventure start sound created successfully!")
