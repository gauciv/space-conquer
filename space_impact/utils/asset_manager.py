"""
Asset Manager for Space Conquer.
Provides a flexible system for loading, managing, and hot-swapping game assets.
"""
import os
import json
import pygame
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AssetManager')

class AssetManager:
    """
    Manages all game assets including images, sounds, music, and maps.
    Supports themes, asset packs, and hot-swapping.
    """
    
    def __init__(self, base_dir=None):
        """
        Initialize the asset manager.
        
        Args:
            base_dir: Base directory for assets. If None, uses the default directory structure.
        """
        # Set base directory
        if base_dir is None:
            self.base_dir = self._get_base_dir()
        else:
            self.base_dir = Path(base_dir)
        
        # Initialize asset containers
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.maps = {}
        self.themes = {}
        self.current_theme = "default"
        
        # Asset directories
        self.asset_dirs = {
            "images": self.base_dir / "assets" / "images",
            "sounds": self.base_dir / "assets" / "sounds",
            "music": self.base_dir / "assets" / "music",
            "maps": self.base_dir / "assets" / "maps",
            "themes": self.base_dir / "assets" / "themes",
        }
        
        # Create directories if they don't exist
        for dir_path in self.asset_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Load asset manifests
        self._load_asset_manifests()
        
        # Load default theme
        self._load_theme("default")
        
        logger.info(f"Asset Manager initialized with base directory: {self.base_dir}")
    
    def _get_base_dir(self):
        """Determine the base directory for assets."""
        # Try to find the project root
        current_dir = Path(__file__).resolve().parent.parent.parent
        
        # Check if we're in the expected directory structure
        if (current_dir / "assets").exists():
            return current_dir
        
        # If not, use the module directory
        return Path(__file__).resolve().parent.parent
    
    def _load_asset_manifests(self):
        """Load asset manifests from JSON files."""
        # Create default manifests if they don't exist
        self._create_default_manifests()
        
        # Load manifests
        try:
            with open(self.asset_dirs["images"] / "manifest.json", "r") as f:
                self.image_manifest = json.load(f)
            
            with open(self.asset_dirs["sounds"] / "manifest.json", "r") as f:
                self.sound_manifest = json.load(f)
            
            with open(self.asset_dirs["music"] / "manifest.json", "r") as f:
                self.music_manifest = json.load(f)
            
            with open(self.asset_dirs["maps"] / "manifest.json", "r") as f:
                self.map_manifest = json.load(f)
            
            logger.info("Asset manifests loaded successfully")
        except Exception as e:
            logger.error(f"Error loading asset manifests: {e}")
            # Create default manifests if loading fails
            self._create_default_manifests()
    
    def _create_default_manifests(self):
        """Create default asset manifests if they don't exist."""
        # Default image manifest
        image_manifest = {
            "player": {"file": "player_ship.png", "scale": [50, 30]},
            "normal_enemy": {"file": "normal_enemy.png", "scale": [40, 30]},
            "fast_enemy": {"file": "fast_enemy.png", "scale": [30, 20]},
            "tank_enemy": {"file": "tank_enemy.png", "scale": [50, 40]},
            "drone_enemy": {"file": "drone_enemy.png", "scale": [35, 25]},
            "bomber_enemy": {"file": "bomber_enemy.png", "scale": [45, 35]},
            "bullet": {"file": "bullet.png", "scale": [10, 5]},
            "health_powerup": {"file": "health_powerup.png", "scale": [20, 20]},
            "speed_powerup": {"file": "speed_powerup.png", "scale": [20, 20]},
            "rapid_fire_powerup": {"file": "rapid_fire_powerup.png", "scale": [20, 20]},
            "score_multiplier": {"file": "score_multiplier.png", "scale": [20, 20]},
            "full_heart": {"file": "full_heart.png", "scale": [32, 32]},
            "empty_heart": {"file": "empty_heart.png", "scale": [32, 32]},
            "mini_boss": {"file": "mini_boss.png", "scale": [80, 60]},
            "main_boss": {"file": "main_boss.png", "scale": [120, 90]},
        }
        
        # Default sound manifest
        sound_manifest = {
            "shoot": {"file": "shoot.wav", "volume": 0.7},
            "explosion": {"file": "explosion.wav", "volume": 0.7},
            "powerup": {"file": "powerup.wav", "volume": 0.7},
            "game_start": {"file": "game_start.wav", "volume": 0.7},
            "game_over": {"file": "game_over.wav", "volume": 0.7},
            "select": {"file": "select.wav", "volume": 0.5},
            "boss_hit": {"file": "boss_hit.wav", "volume": 0.7},
        }
        
        # Default music manifest
        music_manifest = {
            "menu": {"file": "background_music.wav", "volume": 0.5},
            "starlight_end": {"file": "starlight_end.wav", "volume": 0.5},
            "boss_battle": {"file": "boss_battle.wav", "volume": 0.6},
        }
        
        # Default map manifest
        map_manifest = {
            "maps": [
                {
                    "id": "starlight_end",
                    "name": "Starlight's End",
                    "background": "starlight_end_bg.png",
                    "music": "starlight_end",
                    "enemy_spawn_rate": 1500,
                    "enemy_types": ["normal", "fast", "tank", "drone", "bomber"],
                    "boss": "mini_boss"
                },
                {
                    "id": "nebula_ruins",
                    "name": "Nebula Ruins",
                    "background": "nebula_ruins_bg.png",
                    "music": "nebula_ruins",
                    "enemy_spawn_rate": 1200,
                    "enemy_types": ["normal", "fast", "tank", "drone", "bomber"],
                    "boss": "main_boss"
                }
            ]
        }
        
        # Save manifests
        self._save_manifest(self.asset_dirs["images"] / "manifest.json", image_manifest)
        self._save_manifest(self.asset_dirs["sounds"] / "manifest.json", sound_manifest)
        self._save_manifest(self.asset_dirs["music"] / "manifest.json", music_manifest)
        self._save_manifest(self.asset_dirs["maps"] / "manifest.json", map_manifest)
        
        # Update instance variables
        self.image_manifest = image_manifest
        self.sound_manifest = sound_manifest
        self.music_manifest = music_manifest
        self.map_manifest = map_manifest
    
    def _save_manifest(self, path, data):
        """Save a manifest to a JSON file."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Manifest saved to {path}")
        except Exception as e:
            logger.error(f"Error saving manifest to {path}: {e}")
    
    def _load_theme(self, theme_name):
        """Load a theme configuration."""
        theme_path = self.asset_dirs["themes"] / f"{theme_name}.json"
        
        # Create default theme if it doesn't exist
        if not theme_path.exists():
            self._create_default_theme(theme_name)
        
        # Load theme
        try:
            with open(theme_path, "r") as f:
                self.themes[theme_name] = json.load(f)
            
            self.current_theme = theme_name
            logger.info(f"Theme '{theme_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Error loading theme '{theme_name}': {e}")
            # Create and load default theme
            self._create_default_theme(theme_name)
            with open(theme_path, "r") as f:
                self.themes[theme_name] = json.load(f)
    
    def _create_default_theme(self, theme_name):
        """Create a default theme configuration."""
        default_theme = {
            "name": theme_name,
            "description": "Default game theme",
            "ui": {
                "font_main": "Arial",
                "font_title": "Arial",
                "color_primary": [150, 150, 255],
                "color_secondary": [100, 100, 180],
                "color_background": [20, 20, 40],
                "color_text": [220, 220, 255],
                "color_highlight": [180, 180, 255],
                "button_style": "space"
            },
            "overrides": {
                "images": {},
                "sounds": {},
                "music": {}
            }
        }
        
        # Save theme
        theme_path = self.asset_dirs["themes"] / f"{theme_name}.json"
        self._save_manifest(theme_path, default_theme)
        
        # Update instance variable
        self.themes[theme_name] = default_theme
    
    def load_all_assets(self):
        """Load all game assets according to current theme."""
        self.load_all_images()
        self.load_all_sounds()
        self.load_all_music()
        self.load_all_maps()
        logger.info("All assets loaded successfully")
    
    def load_all_images(self):
        """Load all images defined in the manifest."""
        for image_id, image_data in self.image_manifest.items():
            self.load_image(image_id)
    
    def load_image(self, image_id):
        """
        Load an image by its ID from the manifest.
        
        Args:
            image_id: The ID of the image in the manifest
            
        Returns:
            The loaded pygame Surface, or a default surface if loading fails
        """
        # Check if image is already loaded
        if image_id in self.images:
            return self.images[image_id]
        
        # Check if image is in manifest
        if image_id not in self.image_manifest:
            logger.warning(f"Image '{image_id}' not found in manifest")
            self.images[image_id] = pygame.Surface((30, 30))
            return self.images[image_id]
        
        # Get image data from manifest
        image_data = self.image_manifest[image_id]
        
        # Check for theme override
        theme_data = self.themes.get(self.current_theme, {})
        theme_overrides = theme_data.get("overrides", {}).get("images", {})
        
        if image_id in theme_overrides:
            # Use theme override
            image_file = theme_overrides[image_id]
        else:
            # Use default from manifest
            image_file = image_data["file"]
        
        # Try to load image from different possible locations
        image_paths = [
            self.asset_dirs["images"] / image_file,
            self.asset_dirs["images"] / self.current_theme / image_file,
            self.base_dir / "images" / image_file,
            self.base_dir / "assets" / image_file
        ]
        
        # Try each path
        for path in image_paths:
            if path.exists():
                try:
                    self.images[image_id] = pygame.image.load(str(path))
                    
                    # Scale if specified
                    if "scale" in image_data:
                        width, height = image_data["scale"]
                        self.images[image_id] = pygame.transform.scale(
                            self.images[image_id], (width, height)
                        )
                    
                    logger.info(f"Image '{image_id}' loaded from {path}")
                    return self.images[image_id]
                except pygame.error as e:
                    logger.error(f"Error loading image '{image_id}' from {path}: {e}")
        
        # If all paths fail, create a default surface
        logger.warning(f"Could not load image '{image_id}', using default surface")
        self.images[image_id] = pygame.Surface((30, 30))
        return self.images[image_id]
    
    def load_all_sounds(self):
        """Load all sounds defined in the manifest."""
        for sound_id, sound_data in self.sound_manifest.items():
            self.load_sound(sound_id)
    
    def load_sound(self, sound_id):
        """
        Load a sound by its ID from the manifest.
        
        Args:
            sound_id: The ID of the sound in the manifest
            
        Returns:
            The loaded pygame Sound, or None if loading fails
        """
        # Check if sound is already loaded
        if sound_id in self.sounds:
            return self.sounds[sound_id]
        
        # Check if sound is in manifest
        if sound_id not in self.sound_manifest:
            logger.warning(f"Sound '{sound_id}' not found in manifest")
            return None
        
        # Get sound data from manifest
        sound_data = self.sound_manifest[sound_id]
        
        # Check for theme override
        theme_data = self.themes.get(self.current_theme, {})
        theme_overrides = theme_data.get("overrides", {}).get("sounds", {})
        
        if sound_id in theme_overrides:
            # Use theme override
            sound_file = theme_overrides[sound_id]
        else:
            # Use default from manifest
            sound_file = sound_data["file"]
        
        # Try to load sound from different possible locations
        sound_paths = [
            self.asset_dirs["sounds"] / sound_file,
            self.asset_dirs["sounds"] / self.current_theme / sound_file,
            self.base_dir / "sounds" / sound_file,
            self.base_dir / "assets" / sound_file
        ]
        
        # Try each path
        for path in sound_paths:
            if path.exists():
                try:
                    self.sounds[sound_id] = pygame.mixer.Sound(str(path))
                    
                    # Set volume if specified
                    if "volume" in sound_data:
                        self.sounds[sound_id].set_volume(sound_data["volume"])
                    
                    logger.info(f"Sound '{sound_id}' loaded from {path}")
                    return self.sounds[sound_id]
                except pygame.error as e:
                    logger.error(f"Error loading sound '{sound_id}' from {path}: {e}")
        
        # If all paths fail
        logger.warning(f"Could not load sound '{sound_id}'")
        return None
    
    def load_all_music(self):
        """Load all music tracks defined in the manifest."""
        for music_id in self.music_manifest:
            self.get_music_path(music_id)
    
    def get_music_path(self, music_id):
        """
        Get the path to a music file by its ID from the manifest.
        
        Args:
            music_id: The ID of the music track in the manifest
            
        Returns:
            The path to the music file, or None if not found
        """
        # Check if music is in manifest
        if music_id not in self.music_manifest:
            logger.warning(f"Music '{music_id}' not found in manifest")
            return None
        
        # Get music data from manifest
        music_data = self.music_manifest[music_id]
        
        # Check for theme override
        theme_data = self.themes.get(self.current_theme, {})
        theme_overrides = theme_data.get("overrides", {}).get("music", {})
        
        if music_id in theme_overrides:
            # Use theme override
            music_file = theme_overrides[music_id]
        else:
            # Use default from manifest
            music_file = music_data["file"]
        
        # Try to find music file in different possible locations
        music_paths = [
            self.asset_dirs["music"] / music_file,
            self.asset_dirs["music"] / self.current_theme / music_file,
            self.base_dir / "music" / music_file,
            self.base_dir / "assets" / music_file
        ]
        
        # Try each path
        for path in music_paths:
            if path.exists():
                # Store the path
                self.music[music_id] = {
                    "path": str(path),
                    "volume": music_data.get("volume", 0.5)
                }
                logger.info(f"Music '{music_id}' found at {path}")
                return str(path)
        
        # If all paths fail
        logger.warning(f"Could not find music '{music_id}'")
        return None
    
    def load_all_maps(self):
        """Load all maps defined in the manifest."""
        self.maps = {}
        
        if "maps" not in self.map_manifest:
            logger.warning("No maps defined in manifest")
            return
        
        for map_data in self.map_manifest["maps"]:
            map_id = map_data["id"]
            self.maps[map_id] = map_data
            logger.info(f"Map '{map_id}' loaded from manifest")
    
    def get_image(self, image_id):
        """
        Get an image by its ID.
        
        Args:
            image_id: The ID of the image
            
        Returns:
            The pygame Surface for the image
        """
        if image_id not in self.images:
            return self.load_image(image_id)
        return self.images[image_id]
    
    def get_sound(self, sound_id):
        """
        Get a sound by its ID.
        
        Args:
            sound_id: The ID of the sound
            
        Returns:
            The pygame Sound object
        """
        if sound_id not in self.sounds:
            return self.load_sound(sound_id)
        return self.sounds[sound_id]
    
    def play_sound(self, sound_id):
        """
        Play a sound by its ID.
        
        Args:
            sound_id: The ID of the sound to play
        """
        sound = self.get_sound(sound_id)
        if sound:
            sound.play()
    
    def get_map(self, map_id):
        """
        Get a map by its ID.
        
        Args:
            map_id: The ID of the map
            
        Returns:
            The map data dictionary
        """
        if map_id not in self.maps:
            logger.warning(f"Map '{map_id}' not found")
            return None
        return self.maps[map_id]
    
    def get_all_maps(self):
        """
        Get all available maps.
        
        Returns:
            A list of map data dictionaries
        """
        return list(self.maps.values())
    
    def set_theme(self, theme_name):
        """
        Set the current theme and reload assets.
        
        Args:
            theme_name: The name of the theme to set
        """
        if theme_name == self.current_theme:
            return
        
        # Load the new theme
        self._load_theme(theme_name)
        
        # Clear cached assets
        self.images = {}
        self.sounds = {}
        self.music = {}
        
        # Reload assets with new theme
        self.load_all_assets()
        
        logger.info(f"Theme changed to '{theme_name}'")
    
    def get_ui_color(self, color_name):
        """
        Get a UI color from the current theme.
        
        Args:
            color_name: The name of the color (e.g., 'primary', 'secondary')
            
        Returns:
            The color as an RGB tuple
        """
        theme_data = self.themes.get(self.current_theme, {})
        ui_data = theme_data.get("ui", {})
        
        color_key = f"color_{color_name}"
        if color_key in ui_data:
            return tuple(ui_data[color_key])
        
        # Default colors
        defaults = {
            "primary": (150, 150, 255),
            "secondary": (100, 100, 180),
            "background": (20, 20, 40),
            "text": (220, 220, 255),
            "highlight": (180, 180, 255)
        }
        
        return defaults.get(color_name, (255, 255, 255))
    
    def get_font(self, font_type="main", size=20):
        """
        Get a font from the current theme.
        
        Args:
            font_type: The type of font ('main' or 'title')
            size: The font size
            
        Returns:
            A pygame Font object
        """
        theme_data = self.themes.get(self.current_theme, {})
        ui_data = theme_data.get("ui", {})
        
        font_key = f"font_{font_type}"
        font_name = ui_data.get(font_key, "Arial")
        
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            return pygame.font.SysFont("Arial", size)
    
    def reload_assets(self):
        """Reload all assets from disk."""
        # Reload manifests
        self._load_asset_manifests()
        
        # Clear cached assets
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.maps = {}
        
        # Reload assets
        self.load_all_assets()
        
        logger.info("All assets reloaded")
    
    def create_asset_pack_template(self, pack_name):
        """
        Create a template for a new asset pack.
        
        Args:
            pack_name: The name of the asset pack
        """
        pack_dir = self.base_dir / "assets" / "packs" / pack_name
        pack_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (pack_dir / "images").mkdir(exist_ok=True)
        (pack_dir / "sounds").mkdir(exist_ok=True)
        (pack_dir / "music").mkdir(exist_ok=True)
        (pack_dir / "maps").mkdir(exist_ok=True)
        
        # Create manifest
        manifest = {
            "name": pack_name,
            "description": f"Asset pack for Space Conquer",
            "version": "1.0.0",
            "author": "Your Name",
            "theme": {
                "name": pack_name,
                "ui": {
                    "font_main": "Arial",
                    "font_title": "Arial",
                    "color_primary": [150, 150, 255],
                    "color_secondary": [100, 100, 180],
                    "color_background": [20, 20, 40],
                    "color_text": [220, 220, 255],
                    "color_highlight": [180, 180, 255]
                }
            },
            "assets": {
                "images": {},
                "sounds": {},
                "music": {}
            }
        }
        
        # Save manifest
        self._save_manifest(pack_dir / "manifest.json", manifest)
        
        # Create README
        readme_text = f"""# {pack_name} Asset Pack

This is an asset pack for Space Conquer.

## Installation

1. Place this directory in the `assets/packs` directory of your Space Conquer installation.
2. Start the game and select this theme from the options menu.

## Contents

- Images: Place your image files in the `images` directory
- Sounds: Place your sound files in the `sounds` directory
- Music: Place your music files in the `music` directory
- Maps: Place your map files in the `maps` directory

## Customization

Edit the `manifest.json` file to customize the asset pack.
"""
        
        # Save README
        with open(pack_dir / "README.md", "w") as f:
            f.write(readme_text)
        
        logger.info(f"Asset pack template created at {pack_dir}")
        return str(pack_dir)
    
    def install_asset_pack(self, pack_path):
        """
        Install an asset pack from a directory.
        
        Args:
            pack_path: Path to the asset pack directory
            
        Returns:
            True if installation was successful, False otherwise
        """
        pack_path = Path(pack_path)
        
        # Check if manifest exists
        manifest_path = pack_path / "manifest.json"
        if not manifest_path.exists():
            logger.error(f"Asset pack manifest not found at {manifest_path}")
            return False
        
        try:
            # Load manifest
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            
            # Get pack name
            pack_name = manifest.get("name", pack_path.name)
            
            # Create destination directory
            dest_dir = self.base_dir / "assets" / "packs" / pack_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            import shutil
            shutil.copytree(pack_path, dest_dir, dirs_exist_ok=True)
            
            # Install theme if present
            if "theme" in manifest:
                theme_name = manifest["theme"].get("name", pack_name)
                theme_path = self.asset_dirs["themes"] / f"{theme_name}.json"
                self._save_manifest(theme_path, manifest["theme"])
            
            logger.info(f"Asset pack '{pack_name}' installed successfully")
            return True
        except Exception as e:
            logger.error(f"Error installing asset pack: {e}")
            return False
