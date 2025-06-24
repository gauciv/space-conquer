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
total_duration = 1.5  # longer for dramatic effect

# Create a dramatic game over sound
print("Creating game over sound...")

# Create the WAV file
with wave.open('sounds/game_over.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    
    # Calculate samples
    num_samples = int(total_duration * sample_rate)
    
    # Create a buffer
    buffer = []
    
    # Generate a descending pattern (sad/dramatic effect)
    base_freqs = [400, 350, 300, 250, 200, 150]
    note_duration = 0.2  # seconds
    
    for idx, freq in enumerate(base_freqs):
        # Calculate samples for this note
        note_samples = int(note_duration * sample_rate)
        start_sample = idx * note_samples
        end_sample = start_sample + note_samples
        
        if end_sample > num_samples:
            end_sample = num_samples
            
        # Generate a complex tone for each note
        for i in range(start_sample, end_sample):
            local_i = i - start_sample
            t = local_i / sample_rate
            
            # Main tone (mix of square and triangle for richness)
            if (t * freq) % 1 > 0.5:
                value = 0.5
            else:
                value = -0.5
                
            # Add triangle component
            cycle_pos = (t * freq) % 1
            if cycle_pos < 0.5:
                value += 0.3 * (cycle_pos * 4 - 1)
            else:
                value += 0.3 * (3 - cycle_pos * 4)
                
            # Add a subtle vibrato for dramatic effect
            vibrato = 0.2 * np.sin(2 * np.pi * 5 * t)  # 5 Hz vibrato
            value += vibrato * 0.1
            
            # Apply note envelope
            if local_i < note_samples // 10:
                # Fade in
                value *= local_i / (note_samples // 10)
            elif local_i > note_samples * 0.7:
                # Fade out
                value *= (note_samples - local_i) / (note_samples * 0.3)
            
            # Apply overall envelope (get quieter toward the end)
            overall_progress = i / num_samples
            if overall_progress > 0.7:
                value *= (1.0 - (overall_progress - 0.7) / 0.3)
            
            # Clip to prevent distortion
            value = max(min(value, 0.9), -0.9)
            
            # Convert to 16-bit sample
            sample = int(value * 32767)
            buffer.append(struct.pack('h', sample))
    
    # Fill any remaining samples with silence
    remaining = num_samples - len(buffer)
    if remaining > 0:
        for _ in range(remaining):
            buffer.append(struct.pack('h', 0))
    
    # Write to the WAV file
    wav_file.writeframes(b''.join(buffer))

print("Game over sound created successfully!")
