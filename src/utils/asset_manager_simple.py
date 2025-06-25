"""
Simplified Asset Manager for Space Conquer.
Provides a basic system for loading and managing game assets.
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
        
        # Create directories if they don't exist
        for dir_path in self.asset_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Load asset manifests
        self._load_asset_manifests()
        
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
            # Create empty manifests if loading fails
            self.image_manifest = {}
            self.sound_manifest = {}
            self.music_manifest = {}
            self.map_manifest = {"maps": []}
    
    def load_all_assets(self):
        """Load all game assets."""
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
            return self._create_default_surface(image_id)
        
        # Get image data from manifest
        image_data = self.image_manifest[image_id]
        image_file = image_data["file"]
        
        # Try to load image from the assets directory
        image_path = self.asset_dirs["images"] / image_file
        
        try:
            if image_path.exists():
                self.images[image_id] = pygame.image.load(str(image_path))
                
                # Scale if specified
                if "scale" in image_data:
                    width, height = image_data["scale"]
                    self.images[image_id] = pygame.transform.scale(
                        self.images[image_id], (width, height)
                    )
                
                logger.info(f"Image '{image_id}' loaded from {image_path}")
                return self.images[image_id]
            else:
                logger.warning(f"Image file not found: {image_path}")
                return self._create_default_surface(image_id)
        except pygame.error as e:
            logger.error(f"Error loading image '{image_id}' from {image_path}: {e}")
            return self._create_default_surface(image_id)
    
    def _create_default_surface(self, image_id):
        """Create a default surface for an image that couldn't be loaded."""
        # Determine size based on image ID
        width, height = 30, 30
        
        # Try to get size from manifest
        if image_id in self.image_manifest and "scale" in self.image_manifest[image_id]:
            width, height = self.image_manifest[image_id]["scale"]
        
        # Create a colored surface
        surface = pygame.Surface((width, height))
        surface.fill((255, 0, 255))  # Magenta for visibility
        
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
            return None
        
        # Get sound data from manifest
        sound_data = self.sound_manifest[sound_id]
        sound_file = sound_data["file"]
        
        # Try to load sound from the assets directory
        sound_path = self.asset_dirs["sounds"] / sound_file
        
        try:
            if sound_path.exists():
                self.sounds[sound_id] = pygame.mixer.Sound(str(sound_path))
                
                # Set volume if specified
                if "volume" in sound_data:
                    self.sounds[sound_id].set_volume(sound_data["volume"])
                
                logger.info(f"Sound '{sound_id}' loaded from {sound_path}")
                return self.sounds[sound_id]
            else:
                logger.warning(f"Sound file not found: {sound_path}")
                return None
        except pygame.error as e:
            logger.error(f"Error loading sound '{sound_id}' from {sound_path}: {e}")
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
        music_file = music_data["file"]
        
        # Try to find music file in the assets directory
        music_path = self.asset_dirs["music"] / music_file
        
        if music_path.exists():
            # Store the path
            self.music[music_id] = {
                "path": str(music_path),
                "volume": music_data.get("volume", 0.5)
            }
            logger.info(f"Music '{music_id}' found at {music_path}")
            return str(music_path)
        else:
            logger.warning(f"Music file not found: {music_path}")
            return None
    
    def load_all_maps(self):
        """Load all maps defined in the manifest."""
        self.maps = {}
        
        if "maps" not in self.map_manifest:
            logger.warning("No maps defined in manifest")
            return
        
        for map_data in self.map_manifest["maps"]:
            if "id" in map_data:
                map_id = map_data["id"]
                self.maps[map_id] = map_data
                logger.info(f"Map '{map_id}' loaded from manifest")
            else:
                logger.warning(f"Map without ID found in manifest: {map_data}")
    
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
        
        # Reload assets
        self.load_all_assets()
        
        logger.info("All assets reloaded")
