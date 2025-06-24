import numpy as np
import wave
import struct
import os

# Create music directory if it doesn't exist
if not os.path.exists('music'):
    os.makedirs('music')

# Parameters
sample_rate = 44100
duration = 30  # seconds for the loop
bpm = 120
beats_per_bar = 4
bars = 16

# Calculate timing
beat_duration = 60 / bpm  # in seconds
samples_per_beat = int(beat_duration * sample_rate)
total_samples = int(duration * sample_rate)

# Function to generate a note with given frequency and duration
def generate_note(frequency, duration_samples, volume=0.3, decay=0.8):
    t = np.linspace(0, duration_samples / sample_rate, duration_samples, False)
    # Apply decay to make the note fade out
    decay_factor = np.exp(-decay * t)
    # Generate a square wave with some harmonics for a more "chiptune" sound
    note = volume * decay_factor * (
        0.5 * np.sign(np.sin(2 * np.pi * frequency * t)) +
        0.3 * np.sign(np.sin(2 * np.pi * frequency * 2 * t)) +
        0.2 * np.sign(np.sin(2 * np.pi * frequency * 3 * t))
    )
    return note

# Define a simple melody (frequencies in Hz)
# Using pentatonic scale for a space-like feel
melody_notes = [
    196.00,  # G3
    246.94,  # B3
    293.66,  # D4
    392.00,  # G4
    493.88,  # B4
    587.33,  # D5
    493.88,  # B4
    392.00,  # G4
    293.66,  # D4
    246.94,  # B3
    196.00,  # G3
    246.94,  # B3
    293.66,  # D4
    392.00,  # G4
    493.88,  # B4
    587.33   # D5
]

# Define a simple bass line
bass_notes = [
    98.00,   # G2
    98.00,   # G2
    123.47,  # B2
    146.83,  # D3
    98.00,   # G2
    98.00,   # G2
    123.47,  # B2
    146.83,  # D3
]

# Create the audio data
audio_data = np.zeros(total_samples)

# Add melody
note_duration = samples_per_beat // 2  # eighth notes
for i, freq in enumerate(melody_notes * 4):  # Repeat melody 4 times
    start_sample = (i * note_duration) % total_samples
    end_sample = min(start_sample + note_duration, total_samples)
    note = generate_note(freq, end_sample - start_sample, volume=0.3)
    audio_data[start_sample:end_sample] += note

# Add bass line
bass_duration = samples_per_beat * 2  # half notes
for i, freq in enumerate(bass_notes * 8):  # Repeat bass line 8 times
    start_sample = (i * bass_duration) % total_samples
    end_sample = min(start_sample + bass_duration, total_samples)
    note = generate_note(freq, end_sample - start_sample, volume=0.2, decay=0.4)
    audio_data[start_sample:end_sample] += note

# Add a simple drum beat
drum_pattern = [1, 0, 0.5, 0, 1, 0, 0.5, 0.5]  # Simple drum pattern
drum_duration = samples_per_beat // 2
for bar in range(bars * 2):  # Double the number of bars for the drum
    for beat in range(len(drum_pattern)):
        if drum_pattern[beat] > 0:
            start_sample = (bar * samples_per_beat * beats_per_bar + beat * drum_duration) % total_samples
            end_sample = min(start_sample + drum_duration // 4, total_samples)
            # White noise for drum sound
            drum = np.random.uniform(-0.3 * drum_pattern[beat], 0.3 * drum_pattern[beat], end_sample - start_sample)
            audio_data[start_sample:end_sample] += drum

# Normalize to prevent clipping
max_amplitude = np.max(np.abs(audio_data))
if max_amplitude > 1.0:
    audio_data = audio_data / max_amplitude * 0.9

# Convert to 16-bit PCM
audio_data_int = (audio_data * 32767).astype(np.int16)

# Write to WAV file
with wave.open('music/background_music.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes (16 bits)
    wav_file.setframerate(sample_rate)
    for sample in audio_data_int:
        wav_file.writeframes(struct.pack('h', sample))

print("Background music created successfully!")
