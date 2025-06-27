"""
Enemy sprites for the Space Impact game.
Five enemy types: low-type, elite-type, super-type, mini-boss, and boss.
"""
import pygame
import random
import math
import time
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, images, behavior_manager=None):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Set image based on enemy type
        if enemy_type == 'low':
            self.image = images.get('low_enemy') or images.get('normal_enemy')
            self.health = 1
            self.base_speed = 2  # Slower base speed for downward movement
            self.points = 30  # Already includes 3x multiplier
            self.movement_pattern = "drifter"  # New movement pattern for low-type
            # Low-type enemy has a slightly smaller hitbox (80% of sprite size)
            self.hitbox_ratio = 0.8
            
        elif enemy_type == 'elite':
            self.image = images.get('elite_enemy') or images.get('fast_enemy')
            self.health = 1
            self.base_speed = 8  # Increased from 5 to 8 for even faster movement
            self.points = 45  # Already includes 3x multiplier
            self.movement_pattern = "zigzag"  # We keep this name but changed the behavior
            # Elite enemy has an even smaller hitbox (70% of sprite size) since it's harder to hit
            self.hitbox_ratio = 0.7
            
        elif enemy_type == 'super':
            self.image = images.get('super_enemy') or images.get('tank_enemy')
            self.health = 3
            self.base_speed = 2
            self.points = 75  # Already includes 3x multiplier
            self.movement_pattern = "straight"
            # Super enemy has a larger hitbox (90% of sprite size) since it's a bigger target
            self.hitbox_ratio = 0.9
            
        else:
            # Default to low-type enemy for any unknown type
            self.image = images.get('normal_enemy')
            self.health = 1
            self.base_speed = 3
            self.points = 30
            self.movement_pattern = "straight"
            self.hitbox_ratio = 0.8
        
        # Speed multiplier (for time-based difficulty)
        self.speed_multiplier = 1.0
        self.speed = self.base_speed
        
        # Store the original image for the enemy's telegraph effect
        self.original_image = self.image.copy()
        
        # Create the rect
        self.rect = self.image.get_rect()
        
        # Create a custom hitbox based on enemy type
        hitbox_width = int(self.rect.width * self.hitbox_ratio)
        hitbox_height = int(self.rect.height * self.hitbox_ratio)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # For bullet firing
        self.bullets = []  # Store bullets here
        
        # Initialize time tracking
        self.last_time = time.time()
        
        # Initialize behavior using the behavior manager
        self.behavior_manager = behavior_manager
        if self.behavior_manager:
            self.behavior_manager.initialize_behavior(self, self.movement_pattern)
    
    def update(self):
        """Update the enemy based on its behavior pattern."""
        # Get current time for time-based behaviors
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Apply speed multiplier
        self.speed = self.base_speed * self.speed_multiplier
        
        # Use behavior manager if available
        if self.behavior_manager:
            self.behavior_manager.update_behavior(self, delta_time)
            self.behavior_manager.update_bullets(self)
        else:
            # Fallback to basic movement if no behavior manager
            self.rect.x -= self.speed
            
            # Update hitbox position
            self.hitbox.center = self.rect.center
            
            # Remove if it goes off-screen
            if self.rect.right < 0:
                self.kill()
    
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed."""
        self.health -= damage
        if self.health <= 0:
            return True
        return False
    
    def fire_shot(self):
        """Fire a projectile (for enemies that can shoot)."""
        if self.behavior_manager:
            self.behavior_manager._fire_shot(self)
        else:
            # Default bullet behavior
            bullet = {
                'x': self.rect.centerx,
                'y': self.rect.bottom,
                'speed': 3,
                'width': 4,
                'height': 8,
                'color': (255, 100, 100),
                'damage': 1
            }
            self.bullets.append(bullet)
    
    def draw(self, surface):
        """Draw the enemy with visual effects."""
        # Add trail effect for elite-type enemy
        if self.enemy_type == 'elite' and hasattr(self, 'has_trail') and self.has_trail:
            # Get trail intensity multiplier (default to 1.0 if not set)
            trail_intensity = getattr(self, 'trail_intensity', 1.0)
            
            # Create a trail effect to emphasize speed
            trail_length = int(4 * trail_intensity)  # Number of trail segments, increased during burst
            alpha_step = 180 // (trail_length + 1)  # Decreasing alpha for each segment
            
            # Determine if we're in burst mode for special effects
            is_bursting = hasattr(self, 'is_bursting') and self.is_bursting
            
            for i in range(trail_length):
                # Calculate position and alpha for this trail segment
                segment_spacing = 5 if not is_bursting else 8  # Wider spacing during burst
                trail_x = self.rect.x + (i + 1) * segment_spacing
                
                # Higher base alpha during burst
                base_alpha = 180 if not is_bursting else 220
                trail_alpha = base_alpha - (i + 1) * alpha_step
                
                # Create a semi-transparent copy of the image
                trail_image = self.image.copy()
                trail_image.set_alpha(trail_alpha)
                
                # During burst, add color tint to trail
                if is_bursting:
                    # Create a colored overlay
                    overlay = pygame.Surface(trail_image.get_size(), pygame.SRCALPHA)
                    overlay_color = (255, 200, 0, min(150, int(80 * (trail_length - i) / trail_length)))
                    overlay.fill(overlay_color)
                    trail_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                
                # Draw the trail segment
                trail_rect = self.rect.copy()
                trail_rect.x = trail_x
                surface.blit(trail_image, trail_rect)
        
        # Draw the enemy ship
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Add simplified engine glow effect
        if self.enemy_type == 'low' and self.movement_pattern == "drifter":
            # For drifter, engine is on the left side (since it moves right)
            engine_x = self.rect.left
            engine_y = self.rect.centery
        else:
            # For other enemies, engine is on the right side (since they move left)
            engine_x = self.rect.right
            engine_y = self.rect.centery
        
        # Different colors for different enemy types
        if self.enemy_type == 'low':
            glow_color = (255, 50, 50)  # Red
        elif self.enemy_type == 'elite':
            # Check if we're in burst mode
            is_bursting = hasattr(self, 'is_bursting') and self.is_bursting
            is_preparing_burst = hasattr(self, 'pre_burst_delay') and self.pre_burst_delay > 0
            
            if is_bursting:
                # Intense yellow-white glow during burst
                glow_color = (255, 220, 100)  # Bright yellow-orange
                
                # For elite-type in burst mode, add an extra intense engine glow
                if hasattr(self, 'has_trail') and self.has_trail:
                    # Create a larger engine glow with pulsing effect
                    pulse_factor = 0.7 + 0.3 * abs(math.sin(time.time() * 15))  # Fast pulsing
                    glow_size = int(12 * pulse_factor)  # Larger, pulsing glow
                    
                    # Outer glow (large)
                    pygame.draw.circle(surface, glow_color, (engine_x, engine_y), glow_size)
                    
                    # Middle glow (medium)
                    pygame.draw.circle(surface, (255, 240, 150), (engine_x, engine_y), glow_size * 0.7)
                    
                    # Inner bright core (small)
                    pygame.draw.circle(surface, (255, 255, 255), (engine_x, engine_y), glow_size * 0.4)
                    
                    # Add energy particles during burst
                    for _ in range(3):
                        particle_size = random.randint(2, 4)
                        offset_x = random.randint(10, 25)
                        offset_y = random.randint(-8, 8)
                        particle_x = engine_x + offset_x
                        particle_y = engine_y + offset_y
                        particle_color = (255, 220 + random.randint(0, 35), 100 + random.randint(0, 155))
                        pygame.draw.circle(surface, particle_color, (particle_x, particle_y), particle_size)
                    
                    # Skip the regular engine glow
                    glow_color = None
            elif is_preparing_burst:
                # Charging glow during pre-burst telegraph
                glow_color = (255, 180, 0)  # Orange
                
                # For elite-type preparing to burst, add a charging effect
                if hasattr(self, 'has_trail') and self.has_trail:
                    # Create a pulsing engine glow that grows as we approach burst
                    progress = 1.0 - (self.pre_burst_delay / 0.4)  # Assuming 0.4s telegraph time
                    pulse_factor = 0.5 + 0.5 * abs(math.sin(time.time() * 10))  # Medium pulsing
                    base_size = 8 + int(4 * progress)  # Grows as we approach burst
                    glow_size = int(base_size * pulse_factor)
                    
                    # Draw the charging glow
                    pygame.draw.circle(surface, glow_color, (engine_x, engine_y), glow_size)
                    
                    # Inner bright core
                    pygame.draw.circle(surface, (255, 255, 200), (engine_x, engine_y), glow_size // 2)
                    
                    # Skip the regular engine glow
                    glow_color = None
            else:
                # Normal elite enemy glow
                glow_color = (255, 150, 0)  # Orange
                
                # For elite-type, add a more intense engine glow to emphasize speed
                if hasattr(self, 'has_trail') and self.has_trail:
                    # Create a larger engine glow
                    glow_size = 8
                    pygame.draw.circle(surface, glow_color, (engine_x, engine_y), glow_size)
                    
                    # Add inner bright core
                    pygame.draw.circle(surface, (255, 255, 200), (engine_x, engine_y), glow_size // 2)
                    
                    # Skip the regular engine glow
                    glow_color = None
                
                # Skip the regular engine glow for elite-type
                glow_color = None
        elif self.enemy_type == 'super':
            glow_color = (150, 0, 255)  # Purple
        else:
            glow_color = (255, 0, 0)  # Default red
        
        # Draw simplified engine glow (just a rectangle) for non-elite types
        if glow_color:
            glow_rect = pygame.Rect(engine_x - 2, engine_y - 3, 6, 6)
            pygame.draw.rect(surface, glow_color, glow_rect)
        
        # Draw flickering light for drifter enemy
        if self.enemy_type == 'low' and self.movement_pattern == "drifter" and hasattr(self, 'light_brightness'):
            # Calculate light color based on brightness
            light_color = (
                min(255, self.light_brightness),
                min(255, int(self.light_brightness * 0.7)),
                min(255, int(self.light_brightness * 0.5)),
                255
            )
            
            # Draw the light
            light_pos = (self.rect.centerx, self.rect.centery - 5)
            light_size = self.light_size
            
            # Draw a small circle for the light
            pygame.draw.circle(surface, light_color, light_pos, light_size)
            
            # Add shot preparation effect (red flash)
            if hasattr(self, 'is_preparing_shot') and self.is_preparing_shot:
                # Create a subtle red glow around the enemy
                flash_surface = pygame.Surface((self.rect.width + 6, self.rect.height + 6), pygame.SRCALPHA)
                flash_intensity = min(100, self.shot_flash_intensity)
                pygame.draw.rect(flash_surface, (255, 0, 0, flash_intensity), 
                               (3, 3, self.rect.width, self.rect.height), 2)  # Just an outline
                surface.blit(flash_surface, (self.rect.x - 3, self.rect.y - 3))
                
                # Add a small red dot that grows brighter
                dot_size = 2 + int(self.shot_flash_intensity / 20)  # Small dot that grows slightly
                dot_pos = (self.rect.centerx + self.rect.width // 4, self.rect.centery)
                dot_color = (255, 50, 50, min(255, self.shot_flash_intensity * 3))
                
                # Draw the dot
                pygame.draw.circle(surface, dot_color, dot_pos, dot_size)
                
                # Add a small glow around the dot
                if self.shot_flash_intensity > 40:  # Only add glow when intensity is high enough
                    glow_surface = pygame.Surface((dot_size * 4, dot_size * 4), pygame.SRCALPHA)
                    glow_color = (255, 50, 50, min(150, self.shot_flash_intensity * 2))
                    pygame.draw.circle(glow_surface, glow_color, 
                                     (dot_size * 2, dot_size * 2), dot_size * 2)
                    surface.blit(glow_surface, 
                               (dot_pos[0] - dot_size * 2, dot_pos[1] - dot_size * 2))
            
            # Add a subtle glow effect for normal flickering
            elif hasattr(self, 'is_telegraphing') and self.is_telegraphing:
                # Larger glow when telegraphing
                glow_surface = pygame.Surface((light_size * 6, light_size * 6), pygame.SRCALPHA)
                glow_color_alpha = (light_color[0], light_color[1], light_color[2], 100)
                pygame.draw.circle(glow_surface, glow_color_alpha, 
                                 (light_size * 3, light_size * 3), light_size * 2)
                surface.blit(glow_surface, 
                           (light_pos[0] - light_size * 3, light_pos[1] - light_size * 3))
        
        # Draw bullets
        for bullet in self.bullets:
            # Adjust bullet drawing based on direction (horizontal or vertical)
            if 'speed' in bullet and bullet['speed'] < 0:  # Horizontal bullet (moving left)
                bullet_rect = pygame.Rect(
                    bullet['x'] - bullet['width'] // 2,
                    bullet['y'] - bullet['height'] // 2,
                    bullet['width'],
                    bullet['height']
                )
                
                # Draw a more pronounced bullet
                pygame.draw.rect(surface, bullet['color'], bullet_rect)
                
                # Add a bright core to the bullet
                core_rect = pygame.Rect(
                    bullet['x'] - bullet['width'] // 4,
                    bullet['y'] - bullet['height'] // 4,
                    bullet['width'] // 2,
                    bullet['height'] // 2
                )
                pygame.draw.rect(surface, (255, 200, 200), core_rect)
                
                # Add a larger glow effect for horizontal bullets
                glow_width = bullet['width'] * 2
                glow_height = bullet['height'] * 2
                glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
                
                # Create an elongated glow in the direction of travel
                glow_color = (*bullet['color'][:3], 100)
                pygame.draw.ellipse(glow_surface, glow_color, (0, 0, glow_width, glow_height))
                
                # Add a trail effect
                trail_length = bullet['width'] * 1.5
                trail_surface = pygame.Surface((int(trail_length), bullet['height']), pygame.SRCALPHA)
                for i in range(int(trail_length)):
                    alpha = 150 * (1 - i / trail_length)
                    trail_color = (*bullet['color'][:3], int(alpha))
                    pygame.draw.line(trail_surface, trail_color, 
                                   (i, bullet['height'] // 2), 
                                   (i, bullet['height'] // 2), 
                                   1)
                
                # Position the glow and trail
                surface.blit(glow_surface, 
                           (bullet['x'] - glow_width // 2, 
                            bullet['y'] - glow_height // 2))
                surface.blit(trail_surface,
                           (bullet['x'] + bullet['width'] // 2,
                            bullet['y'] - bullet['height'] // 2))
            else:  # Vertical bullet (moving down)
                bullet_rect = pygame.Rect(
                    bullet['x'] - bullet['width'] // 2,
                    bullet['y'],
                    bullet['width'],
                    bullet['height']
                )
                pygame.draw.rect(surface, bullet['color'], bullet_rect)
                
                # Add a small glow effect to the bullet
                glow_surface = pygame.Surface((bullet['width'] + 4, bullet['height'] + 4), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surface, (*bullet['color'][:3], 100), 
                                  (0, 0, bullet['width'] + 4, bullet['height'] + 4))
                surface.blit(glow_surface, 
                       (bullet['x'] - (bullet['width'] + 4) // 2, 
                        bullet['y'] - 2))
        
        # Add health indicator for enemies with more than 1 health
        if self.health > 1:
            health_width = 20
            health_height = 3
            health_x = self.rect.centerx - health_width // 2
            health_y = self.rect.top - 8
            
            # Draw health background
            pygame.draw.rect(surface, (50, 50, 50), 
                           (health_x, health_y, health_width, health_height))
            
            # Draw health bar
            health_percent = self.health / 3  # Assuming max health is 3
            health_fill_width = int(health_width * health_percent)
            
            # Health color based on percentage
            if health_percent > 0.7:
                health_color = (0, 255, 0)  # Green
            elif health_percent > 0.3:
                health_color = (255, 255, 0)  # Yellow
            else:
                health_color = (255, 0, 0)  # Red
                
            pygame.draw.rect(surface, health_color, 
                           (health_x, health_y, health_fill_width, health_height))
    
    def get_bullets(self):
        """Return the enemy's bullets for collision detection."""
        return self.bullets
