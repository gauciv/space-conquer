#!/usr/bin/env python3
"""
Script to create basic fallback assets for the game.
These assets will be used when the requested assets cannot be loaded.
"""
import os
import pygame
import numpy as np
import wave
import struct
from pathlib import Path

def main():
    # Initialize pygame
    pygame.init()
    
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    fallback_dir = base_dir / "assets" / "fallback"
    
    # Create fallback directories if they don't exist
    for subdir in ["images", "sounds", "music", "maps"]:
        (fallback_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Create fallback images
    create_fallback_images(fallback_dir / "images")
    
    # Create fallback sounds
    create_fallback_sounds(fallback_dir / "sounds")
    
    # Create fallback music
    create_fallback_music(fallback_dir / "music")
    
    # Create fallback maps
    create_fallback_maps(fallback_dir / "maps")
    
    print("Fallback assets created successfully!")

def create_fallback_images(image_dir):
    """Create basic fallback images."""
    # List of images to create
    images = {
        # Player and enemies
        "player_ship.png": (50, 30, (0, 255, 0)),
        "normal_enemy.png": (40, 30, (255, 0, 0)),
        "fast_enemy.png": (30, 20, (255, 100, 0)),
        "tank_enemy.png": (50, 40, (255, 0, 100)),
        "drone_enemy.png": (35, 25, (255, 0, 255)),
        "bomber_enemy.png": (45, 35, (200, 0, 0)),
        "mini_boss.png": (80, 60, (255, 100, 100)),
        "main_boss.png": (120, 90, (255, 50, 50)),
        
        # Projectiles
        "bullet.png": (10, 5, (255, 255, 0)),
        
        # Power-ups
        "health_powerup.png": (20, 20, (0, 255, 0)),
        "speed_powerup.png": (20, 20, (0, 0, 255)),
        "rapid_fire_powerup.png": (20, 20, (255, 255, 0)),
        "score_multiplier.png": (20, 20, (255, 0, 255)),
        
        # UI elements
        "full_heart.png": (32, 32, (255, 0, 0)),
        "empty_heart.png": (32, 32, (100, 0, 0)),
        "health_bar_bg.png": (100, 10, (50, 50, 50)),
        "health_bar_fill.png": (100, 10, (0, 255, 0)),
        "settings_cog.png": (30, 30, (200, 200, 200)),
        "slider_bar.png": (100, 10, (100, 100, 100)),
        "slider_handle.png": (20, 20, (150, 150, 150)),
        
        # Backgrounds
        "starlight_end_bg.png": (800, 600, (10, 10, 40)),
        "nebula_ruins_bg.png": (800, 600, (40, 10, 40)),
    }
    
    # Create each image
    for filename, (width, height, color) in images.items():
        # Create a surface
        surface = pygame.Surface((width, height))
        
        # Fill with the specified color
        surface.fill(color)
        
        # Add "FALLBACK" text if the image is large enough
        if width >= 50 and height >= 20:
            font = pygame.font.SysFont("Arial", min(height - 4, 14))
            text = font.render("FALLBACK", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            surface.blit(text, text_rect)
        
        # Add a border
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 1)
        
        # Save the image
        pygame.image.save(surface, image_dir / filename)
        print(f"Created fallback image: {filename}")

def create_fallback_sounds(sound_dir):
    """Create basic fallback sounds."""
    # List of sounds to create
    sounds = {
        "shoot.wav": {"duration": 0.2, "frequency": 440, "volume": 0.5},
        "explosion.wav": {"duration": 0.5, "frequency": 220, "volume": 0.7},
        "powerup.wav": {"duration": 0.3, "frequency": 880, "volume": 0.5},
        "game_start.wav": {"duration": 1.0, "frequency": 660, "volume": 0.6},
        "game_over.wav": {"duration": 1.5, "frequency": 330, "volume": 0.7},
        "select.wav": {"duration": 0.1, "frequency": 550, "volume": 0.4},
        "boss_hit.wav": {"duration": 0.3, "frequency": 110, "volume": 0.7},
    }
    
    # Create each sound
    for filename, params in sounds.items():
        create_simple_sound(sound_dir / filename, **params)
        print(f"Created fallback sound: {filename}")

def create_simple_sound(filepath, duration=0.5, frequency=440, volume=0.5):
    """Create a simple sound file with the given parameters."""
    # Parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate a simple sine wave
    t = np.linspace(0, duration, num_samples, False)
    tone = np.sin(2 * np.pi * frequency * t) * volume
    
    # Add a simple envelope
    envelope = np.ones_like(tone)
    attack = int(sample_rate * 0.02)
    release = int(sample_rate * 0.1)
    
    # Apply attack
    if attack > 0:
        envelope[:attack] = np.linspace(0, 1, attack)
    
    # Apply release
    if release > 0 and num_samples > release:
        envelope[-release:] = np.linspace(1, 0, release)
    
    # Apply envelope
    tone = tone * envelope
    
    # Convert to 16-bit PCM
    audio = (tone * 32767).astype(np.int16)
    
    # Create stereo audio
    stereo = np.column_stack((audio, audio))
    
    # Write to WAV file
    with wave.open(str(filepath), 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for sample in stereo:
            f.writeframes(struct.pack('<hh', sample[0], sample[1]))

def create_fallback_music(music_dir):
    """Create basic fallback music."""
    # List of music tracks to create
    tracks = {
        "background_music.wav": {"duration": 10, "base_freq": 220, "volume": 0.4},
        "starlight_end.wav": {"duration": 10, "base_freq": 165, "volume": 0.4},
        "boss_battle.wav": {"duration": 10, "base_freq": 330, "volume": 0.5},
        "nebula_ruins.wav": {"duration": 10, "base_freq": 196, "volume": 0.4},
    }
    
    # Create each track
    for filename, params in tracks.items():
        create_simple_music(music_dir / filename, **params)
        print(f"Created fallback music: {filename}")

def create_simple_music(filepath, duration=10, base_freq=220, volume=0.4):
    """Create a simple music file with the given parameters."""
    # Parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate a simple melody
    t = np.linspace(0, duration, num_samples, False)
    
    # Create a simple chord progression
    chord1 = np.sin(2 * np.pi * base_freq * t) * 0.5
    chord2 = np.sin(2 * np.pi * (base_freq * 1.25) * t) * 0.3
    chord3 = np.sin(2 * np.pi * (base_freq * 1.5) * t) * 0.2
    
    # Combine chords
    melody = chord1 + chord2 + chord3
    
    # Add a simple bass line
    bass_freq = base_freq / 2
    bass = np.sin(2 * np.pi * bass_freq * t) * 0.4
    
    # Combine melody and bass
    music = (melody + bass) * volume
    
    # Add a simple rhythm
    rhythm_freq = 4  # 4 beats per second
    rhythm = np.sin(2 * np.pi * rhythm_freq * t)
    rhythm = (rhythm > 0.7).astype(float) * 0.1
    
    # Combine everything
    music = music + rhythm
    
    # Normalize
    max_val = np.max(np.abs(music))
    if max_val > 0:
        music = music / max_val * 0.9
    
    # Convert to 16-bit PCM
    audio = (music * 32767).astype(np.int16)
    
    # Create stereo audio
    stereo = np.column_stack((audio, audio))
    
    # Write to WAV file
    with wave.open(str(filepath), 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for sample in stereo:
            f.writeframes(struct.pack('<hh', sample[0], sample[1]))

def create_fallback_maps(maps_dir):
    """Create fallback map definitions."""
    # Create a basic map manifest
    manifest = {
        "maps": [
            {
                "id": "fallback_map",
                "name": "Fallback Map",
                "description": "This is a fallback map used when the requested map cannot be loaded.",
                "background": "starlight_end_bg.png",
                "music": "background_music",
                "enemy_spawn_rate": 1500,
                "enemy_types": ["normal", "fast"],
                "boss": "mini_boss",
                "difficulty": 1
            }
        ]
    }
    
    # Write the manifest to a file
    import json
    with open(maps_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print("Created fallback map manifest")

if __name__ == "__main__":
    main()
