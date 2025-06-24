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
total_duration = 0.6  # shorter duration (600ms)

# Create a brief but exciting start sound
print("Creating brief game start sound...")

# Create the WAV file
with wave.open('sounds/game_start.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    
    # Create a quick ascending pattern (3 notes)
    base_freqs = [300, 450, 600]
    note_duration = 0.15  # seconds
    
    for freq in base_freqs:
        # Calculate samples for this note
        num_samples = int(note_duration * sample_rate)
        
        # Create a buffer for this note
        buffer = []
        
        # Generate a square wave with harmonics for richness
        for i in range(num_samples):
            t = i / sample_rate
            
            # Main square wave
            if (t * freq) % 1 > 0.5:
                value = 0.6
            else:
                value = -0.6
                
            # Add a higher frequency component for excitement
            if (t * freq * 1.5) % 1 > 0.5:
                value += 0.25
            else:
                value -= 0.25
                
            # Apply envelope
            if i < num_samples // 8:
                # Quick fade in
                value *= i / (num_samples // 8)
            elif i > num_samples * 0.75:
                # Fade out
                value *= (num_samples - i) / (num_samples * 0.25)
            
            # Clip to prevent distortion
            value = max(min(value, 0.9), -0.9)
            
            # Convert to 16-bit sample
            sample = int(value * 32767)
            buffer.append(struct.pack('h', sample))
        
        # Write the note to the WAV file
        wav_file.writeframes(b''.join(buffer))
    
    # Add a final quick sweep up (excitement peak)
    sweep_duration = 0.15  # seconds
    sweep_samples = int(sweep_duration * sample_rate)
    sweep_buffer = []
    
    start_freq = 600
    end_freq = 900
    
    for i in range(sweep_samples):
        # Calculate current frequency (exponential sweep for more excitement)
        progress = i / sweep_samples
        current_freq = start_freq + (end_freq - start_freq) * (progress ** 0.7)
        
        # Generate sample
        t = i / sample_rate
        
        # Mix of square and triangle waves for a triumphant sound
        if (t * current_freq) % 1 > 0.5:
            value = 0.7
        else:
            value = -0.7
            
        # Add triangle component
        cycle_pos = (t * current_freq * 2) % 1
        if cycle_pos < 0.5:
            value += 0.3 * (cycle_pos * 4 - 1)
        else:
            value += 0.3 * (3 - cycle_pos * 4)
        
        # Apply envelope
        if i < sweep_samples // 10:
            # Quick fade in
            value *= i / (sweep_samples // 10)
        elif i > sweep_samples * 0.8:
            # Fade out
            value *= (sweep_samples - i) / (sweep_samples * 0.2)
        
        # Clip to prevent distortion
        value = max(min(value, 0.9), -0.9)
        
        # Convert to 16-bit sample
        sample = int(value * 32767)
        sweep_buffer.append(struct.pack('h', sample))
    
    # Write the sweep to the WAV file
    wav_file.writeframes(b''.join(sweep_buffer))

print("Brief game start sound created successfully!")
