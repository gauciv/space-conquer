# Music Files

Place your music files here:

- `background_music.wav` - Main menu music
- `gameplay_music.wav` - Normal gameplay music  
- `boss_music.wav` - Boss battle music (optional)

## Quick Setup

Use the music tester tool to easily add your files:

```bash
# Add menu music
python tools/music_tester.py --menu path/to/your/menu_music.wav

# Add gameplay music
python tools/music_tester.py --gameplay path/to/your/gameplay_music.wav

# Add boss music
python tools/music_tester.py --boss path/to/your/boss_music.wav
```

All files should be in WAV format for best compatibility.