"""
Script to update the asset manager to work with the new directory structure.
This will modify the asset_manager.py file to handle the new nested directory structure.
"""
import os
import sys
from pathlib import Path

def main():
    # Define base directory
    base_dir = Path(__file__).resolve().parent.parent.parent
    asset_manager_path = base_dir / "src" / "utils" / "asset_manager.py"
    
    # Read the current asset manager file
    with open(asset_manager_path, "r") as f:
        content = f.read()
    
    # Update the load_image method to handle nested directories
    old_load_image = """    def load_image(self, image_id):
        \"\"\"
        Load an image by its ID from the manifest.
        
        Args:
            image_id: The ID of the image in the manifest
            
        Returns:
            The loaded pygame Surface, or a fallback surface if loading fails
        \"\"\"
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
            self.asset_dirs["images"] / image_file,
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
        
        # If all paths fail, use fallback
        return self._load_fallback_image(image_id)"""
    
    new_load_image = """    def load_image(self, image_id):
        \"\"\"
        Load an image by its ID from the manifest.
        
        Args:
            image_id: The ID of the image in the manifest
            
        Returns:
            The loaded pygame Surface, or a fallback surface if loading fails
        \"\"\"
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
        return self._load_fallback_image(image_id)"""
    
    # Update the _load_fallback_image method to handle nested directories
    old_fallback_image = """    def _load_fallback_image(self, image_id):
        \"\"\"
        Load a fallback image when the requested image cannot be loaded.
        
        Args:
            image_id: The ID of the image to load
            
        Returns:
            A fallback image or a default surface
        \"\"\"
        # Track that we're using a fallback
        self.fallback_used["images"].add(image_id)
        
        # Try to load a specific fallback for this image
        fallback_path = self.fallback_dirs["images"] / f"{image_id}.png"
        if not fallback_path.exists():
            # If no specific fallback, try the generic filename
            image_data = self.image_manifest.get(image_id, {})
            image_file = image_data.get("file")
            if image_file:
                fallback_path = self.fallback_dirs["images"] / image_file
        
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
        return surface"""
    
    new_fallback_image = """    def _load_fallback_image(self, image_id):
        \"\"\"
        Load a fallback image when the requested image cannot be loaded.
        
        Args:
            image_id: The ID of the image to load
            
        Returns:
            A fallback image or a default surface
        \"\"\"
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
        return surface"""
    
    # Replace the methods in the content
    content = content.replace(old_load_image, new_load_image)
    content = content.replace(old_fallback_image, new_fallback_image)
    
    # Write the updated content back to the file
    with open(asset_manager_path, "w") as f:
        f.write(content)
    
    print(f"Updated asset manager at {asset_manager_path}")

if __name__ == "__main__":
    main()
