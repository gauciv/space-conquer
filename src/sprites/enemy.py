"""
Enemy sprites for the Space Impact game.
Five enemy types: low-type, elite-type, super-type, mini-boss, and boss.

Enemy Types:
- Low-type: Basic enemy with drifting movement and single shot capability
- Elite-type: Fast enemy with burst speed capability and player targeting
- Super-type: Tanky enemy with high health
- Mini-boss: Appears at 1:30 mark
- Boss: Final boss at 3:00 mark
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
            self.original_image = self.image.copy()
            self.health = 4  # Increased from 3 to 4
            self.base_speed = 1.5  # Slightly slower base speed
            self.points = 100  # Increased from 75 to 100 due to enhanced difficulty
            self.movement_pattern = "juggernaut"  # New custom movement pattern
            # Super enemy has a larger hitbox (90% of sprite size) since it's a bigger target
            self.hitbox_ratio = 0.9
            
            # Shield system
            self.has_shield = True
            self.shield_health = 1  # One-hit shield
            self.shield_regen_cooldown = 0
            self.shield_pulse_cooldown = 0
            self.shield_pulse_active = False
            self.shield_pulse_radius = 0
            
            # Attack system
            self.attack_cooldown = random.uniform(3.0, 5.0)  # Initial cooldown
            self.attack_phase = 1  # Current attack phase (1-3)
            self.is_charging = False
            self.charge_cooldown = 0
            self.retreat_active = False
            self.berserk_mode = False
            
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
        # Handle shield for super-type enemy
        if self.enemy_type == 'super' and hasattr(self, 'has_shield') and self.has_shield:
            # Damage shield first
            self.shield_health -= damage
            
            # Set damage flash effect
            if hasattr(self, 'damage_flash'):
                self.damage_flash = 5.0
            
            # Check if shield is destroyed
            if self.shield_health <= 0:
                self.has_shield = False
                self.shield_regen_cooldown = getattr(self, 'shield_regen_time', 8.0)
                return False  # Not destroyed, just shield broken
            
            return False  # Not destroyed, shield absorbed damage
        
        # Normal damage handling
        self.health -= damage
        
        # Set damage flash effect for super-type
        if self.enemy_type == 'super' and hasattr(self, 'damage_flash'):
            self.damage_flash = 10.0
        
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
        
        # Draw special effects for super-type enemy (shield, etc.)
        if self.enemy_type == 'super':
            self.draw_super_effects(surface)
        
        # Draw the enemy ship (only if not a flashing super-type)
        if not (self.enemy_type == 'super' and hasattr(self, 'damage_flash') and self.damage_flash > 0):
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
    def draw_super_effects(self, surface):
        """Draw special effects for super-type enemy."""
        if self.enemy_type != 'super':
            return
            
        # Draw shield if active
        if hasattr(self, 'has_shield') and self.has_shield:
            # Create shield surface with transparency
            shield_radius = max(self.rect.width, self.rect.height) // 2 + 5
            shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
            
            # Get shield opacity
            shield_opacity = getattr(self, 'shield_opacity', 255)
            
            # Draw shield with gradient effect
            for i in range(3):
                thickness = 3 - i
                radius = shield_radius - i*2
                alpha = min(255, shield_opacity - i*30)
                shield_color = (100, 150, 255, alpha)  # Blue shield
                pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), radius, thickness)
            
            # Draw shield on surface
            shield_rect = shield_surface.get_rect(center=self.rect.center)
            surface.blit(shield_surface, shield_rect)
        
        # Draw shield pulse if active
        if hasattr(self, 'shield_pulse_active') and self.shield_pulse_active:
            pulse_radius = getattr(self, 'shield_pulse_radius', 0)
            if pulse_radius > 0:
                # Calculate pulse opacity (fades as it expands)
                pulse_opacity = max(0, 255 - int(pulse_radius * 2.5))
                pulse_color = (100, 150, 255, pulse_opacity)
                
                # Create pulse surface
                pulse_surface = pygame.Surface((pulse_radius*2, pulse_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(pulse_surface, pulse_color, (pulse_radius, pulse_radius), pulse_radius, 2)
                
                # Draw pulse on surface
                pulse_rect = pulse_surface.get_rect(center=self.rect.center)
                surface.blit(pulse_surface, pulse_rect)
        
        # Get engine position based on direction
        if hasattr(self, 'direction') and self.direction == 1:
            # Moving right, engine on left
            engine_x = self.rect.left
            engine_y = self.rect.centery
        else:
            # Moving left or default, engine on right
            engine_x = self.rect.right
            engine_y = self.rect.centery
        
        # Draw engine flare for juggernaut
        if hasattr(self, 'engine_flare') and self.engine_flare > 0:
            flare_intensity = self.engine_flare
            flare_size = int(10 * flare_intensity)
            
            # Draw engine flare
            pygame.draw.circle(surface, (255, 100, 0), (engine_x, engine_y), flare_size)
            pygame.draw.circle(surface, (255, 200, 0), (engine_x, engine_y), flare_size // 2)
            
            # Add particles during high flare
            if flare_intensity > 0.7:
                for _ in range(2):
                    particle_size = random.randint(2, 4)
                    offset_x = random.randint(5, 15)
                    offset_y = random.randint(-5, 5)
                    particle_x = engine_x + offset_x
                    particle_y = engine_y + offset_y
                    particle_color = (255, 150 + random.randint(0, 105), 0)
                    pygame.draw.circle(surface, particle_color, (particle_x, particle_y), particle_size)
        
        # Draw attack warning if active
        if hasattr(self, 'attack_warning') and self.attack_warning:
            # Get attack type
            attack_type = getattr(self, 'attack_type', None)
            
            if attack_type == "shield_pulse":
                # Draw charging shield pulse
                warning_color = (100, 150, 255, 150)  # Blue warning
                warning_radius = 30
                warning_surface = pygame.Surface((warning_radius*2, warning_radius*2), pygame.SRCALPHA)
                
                # Pulsing effect
                pulse = abs(math.sin(time.time() * 10)) * 5
                pygame.draw.circle(warning_surface, warning_color, (warning_radius, warning_radius), warning_radius - pulse, 2)
                
                # Draw warning on surface
                warning_rect = warning_surface.get_rect(center=self.rect.center)
                surface.blit(warning_surface, warning_rect)
            
            elif attack_type == "single_shot" or attack_type == "twin_shot":
                # Draw charging cannon
                warning_color = (200, 50, 200, 150)  # Purple warning
                
                # Draw warning line
                start_pos = (self.rect.left, self.rect.centery)
                end_pos = (self.rect.left - 20, self.rect.centery)
                pygame.draw.line(surface, warning_color, start_pos, end_pos, 3)
                
                # Draw pulsing dot at end
                pulse = abs(math.sin(time.time() * 10)) * 2
                pygame.draw.circle(surface, warning_color, end_pos, 3 + pulse)
            
            elif attack_type == "missile_barrage":
                # Draw multiple missile warnings
                warning_color = (255, 100, 0, 150)  # Orange warning
                
                for angle in [-20, -10, 0, 10, 20]:
                    # Calculate angle in radians
                    angle_rad = math.radians(angle)
                    
                    # Calculate end position
                    dx = -math.cos(angle_rad) * 25
                    dy = math.sin(angle_rad) * 25
                    start_pos = (self.rect.left, self.rect.centery)
                    end_pos = (self.rect.left + dx, self.rect.centery + dy)
                    
                    # Draw warning line
                    pygame.draw.line(surface, warning_color, start_pos, end_pos, 2)
                    
                    # Draw pulsing dot at end
                    pulse = abs(math.sin(time.time() * 10 + angle)) * 2
                    pygame.draw.circle(surface, warning_color, end_pos, 2 + pulse)
        
        # Draw damage flash effect
        if hasattr(self, 'damage_flash') and self.damage_flash > 0:
            # Create a copy of the image with damage flash
            flash_image = self.image.copy()
            flash_overlay = pygame.Surface(flash_image.get_size(), pygame.SRCALPHA)
            
            # Calculate flash intensity
            flash_intensity = int(min(255, self.damage_flash * 25))
            
            # Different colors based on phase
            if hasattr(self, 'attack_phase'):
                if self.attack_phase == 3:
                    # Red flash for critical phase
                    flash_color = (flash_intensity, 0, 0, 0)
                elif self.attack_phase == 2:
                    # Orange flash for damaged phase
                    flash_color = (flash_intensity, flash_intensity // 2, 0, 0)
                else:
                    # White flash for normal phase
                    flash_color = (flash_intensity, flash_intensity, flash_intensity, 0)
            else:
                # Default white flash
                flash_color = (flash_intensity, flash_intensity, flash_intensity, 0)
            
            flash_overlay.fill(flash_color)
            flash_image.blit(flash_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Draw the flashed image
            surface.blit(flash_image, self.rect)
        
        # Draw damage state visual effects
        if hasattr(self, 'attack_phase'):
            if self.attack_phase == 3:
                # Critical damage: add sparks
                for _ in range(2):
                    if random.random() < 0.3:  # 30% chance per frame
                        spark_x = self.rect.x + random.randint(0, self.rect.width)
                        spark_y = self.rect.y + random.randint(0, self.rect.height)
                        spark_size = random.randint(1, 3)
                        spark_color = (255, 200, 50)
                        pygame.draw.circle(surface, spark_color, (spark_x, spark_y), spark_size)
            
            elif self.attack_phase == 2:
                # Moderate damage: add occasional spark
                if random.random() < 0.1:  # 10% chance per frame
                    spark_x = self.rect.x + random.randint(0, self.rect.width)
                    spark_y = self.rect.y + random.randint(0, self.rect.height)
                    spark_size = random.randint(1, 2)
                    spark_color = (255, 200, 50)
                    pygame.draw.circle(surface, spark_color, (spark_x, spark_y), spark_size)
