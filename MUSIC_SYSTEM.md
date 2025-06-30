# Music System Guide

Space Conquer now supports multiple music tracks that automatically switch based on game state.

## Music Tracks

The game supports three types of music:

1. **Menu Music** (`background_music.wav`) - Plays on the main menu
2. **Gameplay Music** (`gameplay_music.wav`) - Plays during normal gameplay
3. **Boss Music** (`boss_music.wav`) - Plays during boss encounters (optional)

## File Locations

All music files should be placed in: `assets/music/`

- `assets/music/background_music.wav` - Menu music (required)
- `assets/music/gameplay_music.wav` - Gameplay music (falls back to menu music if missing)
- `assets/music/boss_music.wav` - Boss music (falls back to gameplay music if missing)

## Music Switching Behavior

- **Menu → Gameplay**: When starting a new game, music switches from menu to gameplay
- **Gameplay → Boss**: When a boss spawns, music switches to boss music (if available)
- **Boss → Gameplay**: When boss is defeated, music switches back to gameplay
- **Game Over → Menu**: When returning to menu, music switches back to menu music

## Testing Different Music Files

### Using the Music Tester Tool

The easiest way to test different music files:

```bash
# Test a new gameplay music file
python tools/music_tester.py --gameplay path/to/your/music.wav

# Test a new menu music file  
python tools/music_tester.py --menu path/to/your/menu_music.wav

# Test boss music
python tools/music_tester.py --boss path/to/your/boss_music.wav

# List current music files
python tools/music_tester.py --list

# Backup current music files before testing
python tools/music_tester.py --backup
```

### Manual Method

1. Copy your music file to `assets/music/`
2. Rename it to the appropriate filename:
   - Menu music: `background_music.wav`
   - Gameplay music: `gameplay_music.wav`
   - Boss music: `boss_music.wav`
3. Run the game to test

## Supported Audio Formats

- **Primary**: WAV files (recommended for best compatibility)
- **Secondary**: MP3, OGG (may work depending on pygame installation)

## Volume Control

- Music volume can be controlled separately from sound effects
- Use the settings menu in-game to adjust music volume
- Setting music volume to 0% will pause the music

## Fallback System

The music system includes intelligent fallbacks:

- If `gameplay_music.wav` is missing, it uses `background_music.wav`
- If `boss_music.wav` is missing, it uses `gameplay_music.wav`
- If no music files are found, the game runs without music

## Development Notes

### Adding New Music Types

To add new music types (e.g., victory music):

1. Add the filename to `SoundManager._load_music_tracks()`
2. Add switching logic in `GameManager` where appropriate
3. Update this documentation

### Music Transition Effects

- Smooth transitions use `pygame.mixer.music.fadeout(500)` for 500ms fade
- Immediate switches use direct `load()` and `play()` calls
- Volume is preserved across track switches

## Troubleshooting

### Music Not Playing
- Check if files exist in `assets/music/`
- Verify file format is supported (WAV recommended)
- Check volume settings in-game
- Look for error messages in console

### Music Not Switching
- Ensure all required music files are present
- Check console for "Playing music track: X" messages
- Verify game state transitions are working correctly

### Performance Issues
- Use compressed audio formats (MP3/OGG) for large files
- Keep music files under 10MB for best performance
- Consider shorter loop lengths for boss music