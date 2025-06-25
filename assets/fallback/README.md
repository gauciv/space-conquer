# Fallback Assets

This directory contains fallback assets that are used when the requested assets cannot be loaded.
These assets ensure that the game continues to function even if some assets are missing or corrupted.

## Structure

The fallback directory mirrors the main assets directory structure:

```
fallback/
├── images/     # Fallback images
├── sounds/     # Fallback sounds
├── music/      # Fallback music
└── maps/       # Fallback map definitions
```

## Usage

The asset manager will automatically use these fallback assets when it cannot load the requested assets.
This ensures that the game will never crash due to missing assets.

## Customizing Fallbacks

You can customize the fallback assets by replacing the files in this directory.
Make sure to keep the same filenames and formats to ensure compatibility.
