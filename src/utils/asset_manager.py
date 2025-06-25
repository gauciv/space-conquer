"""
Asset Manager for Space Conquer.
Provides a structured system for loading and managing game assets.
Includes fallback assets to ensure the game never crashes due to missing assets.
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
    Provides fallback assets when requested assets cannot be loaded.
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
        
        # Asset directories
        self.asset_dirs = {
            "images": self.base_dir / "assets" / "images",
            "sounds": self.base_dir / "assets" / "sounds",
            "music": self.base_dir / "assets" / "music",
            "maps": self.base_dir / "assets" / "maps",
        }
        
        # Fallback asset directories
        self.fallback_dirs = {
            "images": self.base_dir / "assets" / "fallback" / "images",
            "sounds": self.base_dir / "assets" / "fallback" / "sounds",
            "music": self.base_dir / "assets" / "fallback" / "music",
            "maps": self.base_dir / "assets" / "fallback" / "maps",
        }
        
        # Create directories if they don't exist
        for dir_path in self.asset_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Load asset manifests
        self._load_asset_manifests()
        
        # Track fallback usage
        self.fallback_used = {
            "images": set(),
            "sounds": set(),
            "music": set(),
            "maps": set(),
        }
        
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
        
        # Load fallback manifests
        self._load_fallback_manifests()
    
    def _load_fallback_manifests(self):
        """Load fallback asset manifests."""
        self.fallback_image_manifest = {}
        self.fallback_sound_manifest = {}
        self.fallback_music_manifest = {}
        self.fallback_map_manifest = {"maps": []}
        
        # Try to load fallback manifests
        try:
            fallback_image_path = self.fallback_dirs["images"] / "manifest.json"
            if fallback_image_path.exists():
                with open(fallback_image_path, "r") as f:
                    self.fallback_image_manifest = json.load(f)
            
            fallback_sound_path = self.fallback_dirs["sounds"] / "manifest.json"
            if fallback_sound_path.exists():
                with open(fallback_sound_path, "r") as f:
                    self.fallback_sound_manifest = json.load(f)
            
            fallback_music_path = self.fallback_dirs["music"] / "manifest.json"
            if fallback_music_path.exists():
                with open(fallback_music_path, "r") as f:
                    self.fallback_music_manifest = json.load(f)
            
            fallback_map_path = self.fallback_dirs["maps"] / "manifest.json"
            if fallback_map_path.exists():
                with open(fallback_map_path, "r") as f:
                    self.fallback_map_manifest = json.load(f)
            
            logger.info("Fallback manifests loaded successfully")
        except Exception as e:
            logger.error(f"Error loading fallback manifests: {e}")
    
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
    
    def load_all_assets(self):
        """Load all game assets."""
        self.load_all_images()
        self.load_all_sounds()
        self.load_all_music()
        self.load_all_maps()
        logger.info("All assets loaded successfully")
        
        # Log any fallbacks used
        self._log_fallbacks()
    
    def _log_fallbacks(self):
        """Log information about fallback assets that were used."""
        for asset_type, used_ids in self.fallback_used.items():
            if used_ids:
                logger.warning(f"Used fallback {asset_type} for: {', '.join(used_ids)}")
    
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
            The loaded pygame Surface, or a fallback surface if loading fails
        """
        # Check if image is already loaded
        if image_id in self.images:
            return self.images[image_id]
        
        # Check if image is in manifest
        if image_id not in self.image_manifest:
            logger.warning(f"Image '{image_id}' not found in manifest")
            return self._load_fallback_image(image_id)
        
        # Get image data from manifest
        image_data = self.image_manifest[image_id]
        image_file = image_data["file"]
        
        # Try to load image from different possible locations
        image_paths = [
            self.asset_dirs["images"] / image_file,  # New nested structure
            self.base_dir / "images" / Path(image_file).name,  # Old structure with just filename
            self.base_dir / "assets" / image_file  # Alternative path
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
        
        # If all paths fail, use fallback
        return self._load_fallback_image(image_id)
    
    def _load_fallback_image(self, image_id):
        """
        Load a fallback image when the requested image cannot be loaded.
        
        Args:
            image_id: The ID of the image to load
            
        Returns:
            A fallback image or a default surface
        """
        # Track that we're using a fallback
        self.fallback_used["images"].add(image_id)
        
        # Try to load a specific fallback for this image
        fallback_path = self.fallback_dirs["images"] / f"{image_id}.png"
        if not fallback_path.exists():
            # If no specific fallback, try the generic filename
            image_data = self.image_manifest.get(image_id, {})
            image_file = image_data.get("file")
            if image_file:
                # For nested paths, just use the filename part
                fallback_path = self.fallback_dirs["images"] / Path(image_file).name
        
        # Try to load the fallback
        if fallback_path.exists():
            try:
                self.images[image_id] = pygame.image.load(str(fallback_path))
                
                # Scale if specified
                image_data = self.image_manifest.get(image_id, {})
                if "scale" in image_data:
                    width, height = image_data["scale"]
                    self.images[image_id] = pygame.transform.scale(
                        self.images[image_id], (width, height)
                    )
                
                logger.warning(f"Using fallback image for '{image_id}' from {fallback_path}")
                return self.images[image_id]
            except pygame.error as e:
                logger.error(f"Error loading fallback image for '{image_id}': {e}")
        
        # If all else fails, create a default surface
        width, height = self.image_manifest.get(image_id, {}).get("scale", (30, 30))
        surface = pygame.Surface((width, height))
        surface.fill((255, 0, 255))  # Magenta for visibility
        
        # Add "FALLBACK" text if the image is large enough
        if width >= 50 and height >= 20:
            font = pygame.font.SysFont("Arial", min(height - 4, 14))
            text = font.render("FALLBACK", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            surface.blit(text, text_rect)
        
        # Add a border
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 1)
        
        self.images[image_id] = surface
        logger.warning(f"Created default surface for '{image_id}'")
        return surface
    
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
            return self._load_fallback_sound(sound_id)
        
        # Get sound data from manifest
        sound_data = self.sound_manifest[sound_id]
        sound_file = sound_data["file"]
        
        # Try to load sound from different possible locations
        sound_paths = [
            self.asset_dirs["sounds"] / sound_file,
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
        
        # If all paths fail, use fallback
        return self._load_fallback_sound(sound_id)
    
    def _load_fallback_sound(self, sound_id):
        """
        Load a fallback sound when the requested sound cannot be loaded.
        
        Args:
            sound_id: The ID of the sound to load
            
        Returns:
            A fallback sound or None
        """
        # Track that we're using a fallback
        self.fallback_used["sounds"].add(sound_id)
        
        # Try to load a specific fallback for this sound
        fallback_path = self.fallback_dirs["sounds"] / f"{sound_id}.wav"
        if not fallback_path.exists():
            # If no specific fallback, try the generic filename
            sound_data = self.sound_manifest.get(sound_id, {})
            sound_file = sound_data.get("file")
            if sound_file:
                fallback_path = self.fallback_dirs["sounds"] / sound_file
        
        # Try to load the fallback
        if fallback_path.exists():
            try:
                self.sounds[sound_id] = pygame.mixer.Sound(str(fallback_path))
                
                # Set volume if specified
                sound_data = self.sound_manifest.get(sound_id, {})
                if "volume" in sound_data:
                    self.sounds[sound_id].set_volume(sound_data["volume"])
                
                logger.warning(f"Using fallback sound for '{sound_id}' from {fallback_path}")
                return self.sounds[sound_id]
            except pygame.error as e:
                logger.error(f"Error loading fallback sound for '{sound_id}': {e}")
        
        # If all else fails, return None
        logger.warning(f"No fallback sound available for '{sound_id}'")
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
            return self._get_fallback_music_path(music_id)
        
        # Get music data from manifest
        music_data = self.music_manifest[music_id]
        music_file = music_data["file"]
        
        # Try to find music file in different possible locations
        music_paths = [
            self.asset_dirs["music"] / music_file,
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
        
        # If all paths fail, use fallback
        return self._get_fallback_music_path(music_id)
    
    def _get_fallback_music_path(self, music_id):
        """
        Get the path to a fallback music file when the requested music cannot be found.
        
        Args:
            music_id: The ID of the music to load
            
        Returns:
            The path to a fallback music file or None
        """
        # Track that we're using a fallback
        self.fallback_used["music"].add(music_id)
        
        # Try to load a specific fallback for this music
        fallback_path = self.fallback_dirs["music"] / f"{music_id}.wav"
        if not fallback_path.exists():
            # If no specific fallback, try the generic filename
            music_data = self.music_manifest.get(music_id, {})
            music_file = music_data.get("file")
            if music_file:
                fallback_path = self.fallback_dirs["music"] / music_file
        
        # Try to load the fallback
        if fallback_path.exists():
            # Store the path
            self.music[music_id] = {
                "path": str(fallback_path),
                "volume": self.music_manifest.get(music_id, {}).get("volume", 0.5)
            }
            logger.warning(f"Using fallback music for '{music_id}' from {fallback_path}")
            return str(fallback_path)
        
        # If all else fails, use the default background music
        default_path = self.fallback_dirs["music"] / "background_music.wav"
        if default_path.exists():
            self.music[music_id] = {
                "path": str(default_path),
                "volume": 0.5
            }
            logger.warning(f"Using default background music for '{music_id}'")
            return str(default_path)
        
        # If even that fails, return None
        logger.warning(f"No fallback music available for '{music_id}'")
        return None
    
    def load_all_maps(self):
        """Load all maps defined in the manifest."""
        self.maps = {}
        
        if "maps" not in self.map_manifest:
            logger.warning("No maps defined in manifest")
            self._load_fallback_maps()
            return
        
        for map_data in self.map_manifest["maps"]:
            if "id" in map_data:
                map_id = map_data["id"]
                self.maps[map_id] = map_data
                logger.info(f"Map '{map_id}' loaded from manifest")
            else:
                logger.warning(f"Map without ID found in manifest: {map_data}")
        
        # If no maps were loaded, use fallbacks
        if not self.maps:
            self._load_fallback_maps()
    
    def _load_fallback_maps(self):
        """Load fallback maps when no maps are available."""
        # Track that we're using fallbacks
        self.fallback_used["maps"].add("all")
        
        if "maps" in self.fallback_map_manifest:
            for map_data in self.fallback_map_manifest["maps"]:
                if "id" in map_data:
                    map_id = map_data["id"]
                    self.maps[map_id] = map_data
                    logger.warning(f"Using fallback map '{map_id}'")
        
        # If still no maps, create a default map
        if not self.maps:
            default_map = {
                "id": "default_map",
                "name": "Default Map",
                "background": "starlight_end_bg.png",
                "music": "background_music",
                "enemy_spawn_rate": 1500,
                "enemy_types": ["normal"],
                "boss": None,
                "difficulty": 1
            }
            self.maps["default_map"] = default_map
            logger.warning("Using generated default map")
    
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
            # Return the first available map as a fallback
            if self.maps:
                fallback_map_id = next(iter(self.maps.keys()))
                logger.warning(f"Using '{fallback_map_id}' as fallback map")
                return self.maps[fallback_map_id]
            return None
        return self.maps[map_id]
    
    def get_all_maps(self):
        """
        Get all available maps.
        
        Returns:
            A list of map data dictionaries
        """
        return list(self.maps.values())
    
    def reload_assets(self):
        """Reload all assets from disk."""
        # Reload manifests
        self._load_asset_manifests()
        
        # Clear cached assets
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.maps = {}
        
        # Reset fallback tracking
        self.fallback_used = {
            "images": set(),
            "sounds": set(),
            "music": set(),
            "maps": set(),
        }
        
        # Reload assets
        self.load_all_assets()
        
        logger.info("All assets reloaded")
    
    def get_fallback_usage(self):
        """
        Get information about fallback assets that were used.
        
        Returns:
            A dictionary with lists of asset IDs that used fallbacks
        """
        return {
            asset_type: list(used_ids)
            for asset_type, used_ids in self.fallback_used.items()
            if used_ids
        }
