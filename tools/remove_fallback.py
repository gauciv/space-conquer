#!/usr/bin/env python3
"""
Script to remove the fallback asset system and update the asset manager.
"""
import os
import sys
import shutil
from pathlib import Path

def main():
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    # Remove fallback directory
    fallback_dir = base_dir / "assets" / "fallback"
    if fallback_dir.exists():
        print(f"Removing fallback directory: {fallback_dir}")
        shutil.rmtree(fallback_dir)
    
    # Update asset manager
    asset_manager_path = base_dir / "src" / "utils" / "asset_manager.py"
    
    # Read the current asset manager file
    with open(asset_manager_path, "r") as f:
        content = f.read()
    
    # Remove fallback-related code
    content = content.replace("self.fallback_dirs = {", "# Removed fallback dirs\n        # self.fallback_dirs = {")
    content = content.replace("self.fallback_used = {", "# Removed fallback tracking\n        # self.fallback_used = {")
    content = content.replace("self._load_fallback_manifests()", "# Removed fallback manifests loading\n        # self._load_fallback_manifests()")
    content = content.replace("def _load_fallback_manifests", "def _removed_load_fallback_manifests")
    content = content.replace("def _load_fallback_image", "def _removed_load_fallback_image")
    content = content.replace("def _load_fallback_sound", "def _removed_load_fallback_sound")
    content = content.replace("def _get_fallback_music_path", "def _removed_get_fallback_music_path")
    content = content.replace("def _load_fallback_maps", "def _removed_load_fallback_maps")
    content = content.replace("return self._load_fallback_image", "return self._create_default_surface")
    content = content.replace("return self._load_fallback_sound", "return None")
    content = content.replace("return self._get_fallback_music_path", "return None")
    content = content.replace("self._load_fallback_maps()", "# Removed fallback maps loading")
    content = content.replace("self._log_fallbacks()", "# Removed fallback logging")
    content = content.replace("def _log_fallbacks", "def _removed_log_fallbacks")
    content = content.replace("def get_fallback_usage", "def _removed_get_fallback_usage")
    
    # Add a simple default surface creation method
    default_surface_method = """
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
    """
    
    # Check if the method already exists
    if "_create_default_surface" not in content:
        # Find a good place to insert the method
        insert_pos = content.find("def load_all_sounds")
        if insert_pos > 0:
            content = content[:insert_pos] + default_surface_method + content[insert_pos:]
    
    # Write the updated content back to the file
    with open(asset_manager_path, "w") as f:
        f.write(content)
    
    print(f"Updated asset manager at {asset_manager_path}")
    print("Fallback asset system removed.")

if __name__ == "__main__":
    main()
