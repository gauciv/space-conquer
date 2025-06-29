"""
Enemy Behavior Manager for Space Conquer.
Handles different enemy movement and attack patterns.
"""
import pygame
import random
import math
import time
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class EnemyBehaviorManager:
    """Manages different enemy behaviors and movement patterns."""
    
    def __init__(self):
        """Initialize the behavior manager."""
        # Dictionary of available behaviors
        self.behaviors = {
            "drifter": self.drifter_behavior,
            "oscillate": self.oscillate_behavior,
            "zigzag": self.zigzag_behavior,
            "straight": self.straight_behavior,
            "sine": self.sine_behavior,
            "dive": self.dive_behavior,
            "juggernaut": self.juggernaut_behavior  # Add new juggernaut behavior
        }
    
    def initialize_behavior(self, enemy, behavior_type):
        """Initialize behavior-specific properties for an enemy."""
        if behavior_type == "drifter":
            self._init_drifter(enemy)
        elif behavior_type == "oscillate":
            self._init_oscillate(enemy)
        elif behavior_type == "zigzag":
            self._init_zigzag(enemy)
        elif behavior_type == "sine":
            self._init_sine(enemy)
        elif behavior_type == "dive":
            self._init_dive(enemy)
        elif behavior_type == "juggernaut":
            self._init_juggernaut(enemy)
        # Default to straight behavior if not specified
        else:
            self._init_straight(enemy)
    
    def update_behavior(self, enemy, delta_time):
        """Update enemy based on its behavior type."""
        behavior_func = self.behaviors.get(enemy.movement_pattern, self.straight_behavior)
        behavior_func(enemy, delta_time)
        
        # Update hitbox position to follow the rect
        enemy.hitbox.center = enemy.rect.center
    
    def _init_drifter(self, enemy):
        """Initialize drifter behavior (low-type enemy)."""
        # Horizontal movement properties (primary movement) - reduced by 25%
        base_speed = random.uniform(1.5, 2.0)
        enemy.horizontal_speed = base_speed * 0.75  # 25% reduction in speed
        
        # Dash properties (rare vertical movement)
        enemy.dash_chance = 0.005  # 0.5% chance per frame to initiate a dash
        enemy.is_dashing = False
        enemy.dash_direction = 0  # 0 = no dash, 1 = up, -1 = down
        enemy.dash_duration = 0
        enemy.dash_speed = enemy.horizontal_speed * 0.8  # Dash speed slightly slower than horizontal
        enemy.dash_cooldown = 0  # Cooldown after a dash
        enemy.dash_trail = []  # Store positions for trail effect
        enemy.dash_warning = 0  # Warning time before dash
        
        # Shooting properties
        enemy.has_shot = False  # Can only shoot once
        enemy.can_shoot = False  # Will be set to true when within range
        enemy.is_preparing_shot = False
        enemy.shot_preparation_time = 0
        enemy.shot_preparation_duration = 0.8  # Time to prepare shot (flash warning)
        enemy.shot_flash_intensity = 0  # Flash intensity (0-100)
        enemy.targeting_line_visible = False  # Whether to show targeting line
        
        # Stutter behavior
        enemy.stutter_timer = random.uniform(3.0, 5.0)  # Time until next stutter
        enemy.stutter_duration = 0.0  # Current stutter duration
        enemy.is_stuttering = False
        enemy.last_time = time.time()
        enemy.stutter_warning = 0  # Warning time before stutter
        
        # Flickering light properties
        enemy.light_flicker_speed = random.uniform(0.1, 0.2)
        enemy.light_flicker_angle = random.random() * 6.28
        enemy.light_brightness = 50  # Base brightness
        enemy.light_size = 3
        enemy.light_color_shift = random.choice([
            (255, 100, 100),  # Red
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
            (100, 255, 100),  # Green
            (255, 100, 255),  # Purple
        ])  # Different colors for variety
        
        # Visual effect properties
        enemy.engine_glow = 0  # Engine glow intensity
        enemy.hit_flash = 0  # Flash when taking damage
        enemy.variant = random.randint(0, 2)  # Visual variant (0-2)
        
        # Position at the right edge of the screen with random y position
        enemy.rect.x = SCREEN_WIDTH + random.randint(10, 30)  # Just off the right edge
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 100)  # Random vertical position
        
        # Set light position after rect is positioned
        enemy.light_position = (enemy.rect.centerx, enemy.rect.centery - 5)
    
    def _init_oscillate(self, enemy):
        """Initialize oscillating behavior."""
        enemy.oscillation_amplitude = random.randint(10, 20)
        enemy.oscillation_speed = random.uniform(0.05, 0.1)
        enemy.oscillation_angle = random.random() * 6.28
        
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def _init_zigzag(self, enemy):
        """Initialize elite-type enemy behavior with burst speed capability."""
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Elite-type enemies have higher speed with burst capability
        if enemy.enemy_type == 'elite':
            # Base movement properties
            enemy.base_speed = 5  # Normal speed (still faster than most enemies)
            enemy.burst_speed = 12  # Burst speed (more than double normal speed)
            enemy.burst_available = True  # Can use burst once
            enemy.burst_duration = 0.0  # Current burst duration
            enemy.burst_max_duration = 0.6  # Maximum burst duration in seconds
            enemy.burst_cooldown = 0.0  # Cooldown after burst
            enemy.is_bursting = False  # Currently in burst mode
            enemy.target_acquired = False  # Whether a target position has been selected
            enemy.target_y = 0  # Target Y position for burst
            enemy.detection_range = 250  # How far ahead the enemy can detect the player
            enemy.lane_change_cooldown = 0.0  # Cooldown for changing lanes
            enemy.pre_burst_delay = 0.0  # Telegraph delay before bursting
    
    def _init_sine(self, enemy):
        """Initialize sine wave behavior."""
        enemy.angle = random.random() * 6.28
        enemy.center_y = enemy.rect.centery
        enemy.amplitude = random.randint(30, 70)
        enemy.frequency = random.uniform(0.05, 0.1)
        
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def _init_dive(self, enemy):
        """Initialize dive behavior."""
        enemy.dive_state = "approach"
        enemy.target_y = random.randint(100, SCREEN_HEIGHT - 100)
        enemy.dive_speed = enemy.speed * 1.5
        
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def _init_straight(self, enemy):
        """Initialize straight behavior."""
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def drifter_behavior(self, enemy, delta_time):
        """Update drifter behavior (low-type enemy)."""
        # Update stutter timer
        if not enemy.is_stuttering:
            enemy.stutter_timer -= delta_time
            if enemy.stutter_timer <= 0:
                # Add warning before stuttering
                if enemy.stutter_warning <= 0:
                    enemy.stutter_warning = 0.3  # 0.3 second warning
                else:
                    enemy.stutter_warning -= delta_time
                    if enemy.stutter_warning <= 0:
                        # Start stuttering
                        enemy.is_stuttering = True
                        enemy.stutter_duration = 0.5  # Stutter for 0.5 seconds
                        enemy.stutter_timer = random.uniform(3.0, 5.0)  # Reset timer for next stutter
                        enemy.stutter_warning = 0
            else:
                enemy.stutter_warning = 0
        else:
            # Currently stuttering
            enemy.stutter_duration -= delta_time
            if enemy.stutter_duration <= 0:
                enemy.is_stuttering = False
        
        # Calculate actual speed based on stutter state
        speed_multiplier = 0.5 if enemy.is_stuttering else 1.0
        
        # Check if we're within shooting range (15 pixels from right edge)
        if not enemy.can_shoot and enemy.rect.right <= SCREEN_WIDTH - 15:
            enemy.can_shoot = True
        
        # Handle dash cooldown
        if enemy.dash_cooldown > 0:
            enemy.dash_cooldown -= delta_time
        
        # Determine if we should start a dash warning
        if (not enemy.is_dashing and not enemy.is_preparing_shot and enemy.dash_cooldown <= 0 and 
            enemy.dash_warning <= 0 and random.random() < enemy.dash_chance):
            enemy.dash_warning = 0.4  # 0.4 second warning before dash
            # Choose dash direction based on player position if available
            if hasattr(enemy, 'game_manager') and enemy.game_manager and enemy.game_manager.player:
                player = enemy.game_manager.player
                # Dash toward player if they're above or below
                if player.rect.centery < enemy.rect.centery - 50:
                    enemy.dash_direction = -1  # Dash up
                elif player.rect.centery > enemy.rect.centery + 50:
                    enemy.dash_direction = 1  # Dash down
                else:
                    enemy.dash_direction = random.choice([-1, 1])  # Random direction
            else:
                enemy.dash_direction = random.choice([-1, 1])  # Random direction
        
        # Update dash warning
        if enemy.dash_warning > 0:
            enemy.dash_warning -= delta_time
            if enemy.dash_warning <= 0:
                # Start dash
                enemy.is_dashing = True
                enemy.dash_duration = random.uniform(0.4, 0.8)  # Slightly longer dash
                enemy.dash_cooldown = random.uniform(2.0, 4.0)  # Long cooldown between dashes
                enemy.dash_trail = []  # Clear trail
        
        # Handle dashing
        if enemy.is_dashing:
            # Store position for trail effect
            if len(enemy.dash_trail) < 5:  # Limit to 5 positions
                enemy.dash_trail.append((enemy.rect.centerx, enemy.rect.centery))
            else:
                enemy.dash_trail.pop(0)
                enemy.dash_trail.append((enemy.rect.centerx, enemy.rect.centery))
            
            # Move vertically based on dash direction
            enemy.rect.y += enemy.dash_direction * enemy.dash_speed * speed_multiplier * delta_time * 60
            
            # Update dash duration
            enemy.dash_duration -= delta_time
            if enemy.dash_duration <= 0:
                enemy.is_dashing = False
        
        # Get player reference
        player = None
        if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
            player = enemy.game_manager.player
        
        # Check if player is in shooting range
        player_in_range = False
        if player:
            # Check if player is within vertical bounds with some leeway
            vertical_range = 30  # Pixels above/below enemy to consider in range
            if (player.rect.centery >= enemy.rect.top - vertical_range and 
                player.rect.centery <= enemy.rect.bottom + vertical_range):
                player_in_range = True
                
                # Show targeting line when player is in range
                enemy.targeting_line_visible = True
            else:
                enemy.targeting_line_visible = False
        
        # Handle shooting preparation and execution
        if (enemy.can_shoot and not enemy.has_shot and not enemy.is_preparing_shot and 
            not enemy.is_dashing and player_in_range):
            # Start preparing to shoot
            enemy.is_preparing_shot = True
            enemy.shot_preparation_time = enemy.shot_preparation_duration
        
        if enemy.is_preparing_shot:
            # Stop horizontal movement during shot preparation
            pass  # Don't move horizontally
            
            # Update preparation timer
            enemy.shot_preparation_time -= delta_time
            
            # Calculate flash intensity (0 to 100, peaking at the end)
            progress = 1.0 - (enemy.shot_preparation_time / enemy.shot_preparation_duration)
            enemy.shot_flash_intensity = min(100, int(progress * 150))  # Increased max intensity
            
            # When preparation is complete, fire the shot
            if enemy.shot_preparation_time <= 0:
                self._fire_shot_left(enemy)  # Fire shot to the left
                enemy.has_shot = True
                enemy.is_preparing_shot = False
                enemy.shot_flash_intensity = 0
                enemy.targeting_line_visible = False
        else:
            # Normal horizontal movement if not preparing to shoot
            if not enemy.is_preparing_shot:
                enemy.rect.x -= enemy.horizontal_speed * speed_multiplier * delta_time * 60
        
        # Update flickering light
        enemy.light_flicker_angle += enemy.light_flicker_speed
        
        # Base brightness plus flash intensity during shot preparation
        if enemy.is_preparing_shot:
            enemy.light_brightness = 70 + enemy.shot_flash_intensity
            enemy.light_size = 3 + int(enemy.shot_flash_intensity / 20)  # Grow light during preparation
        elif enemy.dash_warning > 0:
            # Pulsing light during dash warning
            pulse_factor = math.sin(enemy.dash_warning * 20) * 0.5 + 0.5  # 0-1 pulsing
            enemy.light_brightness = 50 + int(100 * pulse_factor)
            enemy.light_size = 3 + int(3 * pulse_factor)
        elif enemy.stutter_warning > 0:
            # Flickering light during stutter warning
            flicker_factor = math.sin(enemy.stutter_warning * 30) * 0.5 + 0.5  # 0-1 flickering
            enemy.light_brightness = 50 + int(50 * flicker_factor)
        else:
            # Normal flicker with more variation
            enemy.light_brightness = 50 + int(30 * math.sin(enemy.light_flicker_angle))
        
        # Update engine glow based on speed
        if enemy.is_dashing:
            enemy.engine_glow = min(1.0, enemy.engine_glow + delta_time * 5)  # Quickly increase
        else:
            target_glow = 0.3 if enemy.is_stuttering else 0.7  # Lower glow when stuttering
            if enemy.engine_glow < target_glow:
                enemy.engine_glow += delta_time * 2  # Gradually increase
            elif enemy.engine_glow > target_glow:
                enemy.engine_glow -= delta_time * 2  # Gradually decrease
        
        # Update hit flash
        if enemy.hit_flash > 0:
            enemy.hit_flash -= delta_time * 5
        
        # Update light position
        enemy.light_position = (enemy.rect.centerx, enemy.rect.centery - 5)
        
        # Keep within screen bounds
        if enemy.rect.top < 10:
            enemy.rect.top = 10
            if enemy.is_dashing and enemy.dash_direction == -1:
                enemy.is_dashing = False  # Stop dashing if hit top
        elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
            enemy.rect.bottom = SCREEN_HEIGHT - 10
            if enemy.is_dashing and enemy.dash_direction == 1:
                enemy.is_dashing = False  # Stop dashing if hit bottom
        
        # Remove if it goes off the left side of the screen
        if enemy.rect.right < 0:
            enemy.kill()
    
    def oscillate_behavior(self, enemy, delta_time):
        """Update oscillating behavior."""
        # Update stutter timer if it exists
        if hasattr(enemy, 'is_stuttering'):
            if not enemy.is_stuttering:
                enemy.stutter_timer -= delta_time
                if enemy.stutter_timer <= 0:
                    enemy.is_stuttering = True
                    enemy.stutter_duration = 0.5
                    enemy.stutter_timer = random.uniform(3.0, 5.0)
            else:
                enemy.stutter_duration -= delta_time
                if enemy.stutter_duration <= 0:
                    enemy.is_stuttering = False
            
            # Calculate actual speed based on stutter state
            actual_speed = enemy.speed * 0.5 if enemy.is_stuttering else enemy.speed
        else:
            actual_speed = enemy.speed
        
        # Move horizontally with oscillation
        enemy.rect.x -= actual_speed
        
        # Update oscillation angle
        enemy.oscillation_angle += enemy.oscillation_speed
        
        # Apply horizontal oscillation
        oscillation = math.sin(enemy.oscillation_angle) * enemy.oscillation_amplitude
        enemy.rect.x += oscillation * delta_time * 60
        
        # Update attack pattern if it exists
        if hasattr(enemy, 'time_since_last_shot'):
            enemy.time_since_last_shot += delta_time
            
            # Check if it's time to telegraph the shot
            if not enemy.is_telegraphing and enemy.time_since_last_shot >= enemy.fire_rate - enemy.telegraph_duration:
                enemy.is_telegraphing = True
                enemy.telegraph_timer = enemy.telegraph_duration
                
                # Create a brightened version of the image for telegraph effect
                bright_image = enemy.original_image.copy()
                bright_overlay = pygame.Surface(bright_image.get_size(), pygame.SRCALPHA)
                bright_overlay.fill((50, 50, 100, 0))
                bright_image.blit(bright_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                enemy.image = bright_image
            
            # Update telegraph timer
            if enemy.is_telegraphing:
                enemy.telegraph_timer -= delta_time
                if enemy.telegraph_timer <= 0:
                    enemy.is_telegraphing = False
                    enemy.image = enemy.original_image.copy()  # Reset image
                    
                    # Fire a shot
                    if enemy.time_since_last_shot >= enemy.fire_rate:
                        self._fire_shot(enemy)
                        enemy.time_since_last_shot = 0
                        enemy.fire_rate = random.uniform(2.0, 3.0)
        
        # Remove if it goes off-screen
        if enemy.rect.right < 0:
            enemy.kill()
    
    def zigzag_behavior(self, enemy, delta_time):
        """Update elite-type enemy behavior with burst speed and targeting."""
        # For elite-type enemies, implement the enhanced behavior
        if enemy.enemy_type == 'elite':
            # Apply speed multiplier for time-based difficulty
            base_speed = enemy.base_speed * enemy.speed_multiplier
            
            # Check if player exists and get reference
            player = None
            if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
                player = enemy.game_manager.player
            
            # Update lane change cooldown
            if enemy.lane_change_cooldown > 0:
                enemy.lane_change_cooldown -= delta_time
            
            # Handle burst cooldown
            if enemy.burst_cooldown > 0:
                enemy.burst_cooldown -= delta_time
            
            # Handle pre-burst delay (telegraph)
            if enemy.pre_burst_delay > 0:
                # During telegraph, flash the enemy to indicate imminent burst
                enemy.pre_burst_delay -= delta_time
                
                # Visual telegraph effect - flash between normal and bright
                flash_intensity = int(abs(math.sin(enemy.pre_burst_delay * 20)) * 100)
                bright_image = enemy.original_image.copy()
                bright_overlay = pygame.Surface(bright_image.get_size(), pygame.SRCALPHA)
                bright_overlay.fill((flash_intensity, flash_intensity, 0, 0))
                bright_image.blit(bright_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                enemy.image = bright_image
                
                # When telegraph is complete, start the burst
                if enemy.pre_burst_delay <= 0:
                    enemy.is_bursting = True
                    enemy.burst_duration = enemy.burst_max_duration
                    # Reset image
                    enemy.image = enemy.original_image.copy()
                
                # Move at reduced speed during telegraph
                enemy.rect.x -= base_speed * 0.5
                
                # If we have a target Y position, gradually move toward it
                if enemy.target_acquired and enemy.target_y != enemy.rect.centery:
                    # Calculate direction to move (up or down)
                    direction = 1 if enemy.target_y > enemy.rect.centery else -1
                    # Move at a moderate speed toward target
                    enemy.rect.y += direction * base_speed * 0.8 * delta_time * 60
                    
                    # Check if we've reached the target
                    if (direction == 1 and enemy.rect.centery >= enemy.target_y) or \
                       (direction == -1 and enemy.rect.centery <= enemy.target_y):
                        enemy.rect.centery = enemy.target_y  # Snap to exact position
            
            # Handle burst mode
            elif enemy.is_bursting:
                # Move at burst speed
                enemy.rect.x -= enemy.burst_speed * delta_time * 60
                
                # Update burst duration
                enemy.burst_duration -= delta_time
                if enemy.burst_duration <= 0:
                    enemy.is_bursting = False
                    enemy.burst_available = False  # Can only burst once
                    enemy.burst_cooldown = 1.0  # Cooldown after burst
                
                # Intensify trail effect during burst
                enemy.has_trail = True
                if not hasattr(enemy, 'trail_intensity'):
                    enemy.trail_intensity = 2.0  # Double intensity during burst
            
            # Normal movement (not bursting or telegraphing)
            else:
                # Move at normal speed
                enemy.rect.x -= base_speed * delta_time * 60
                
                # Reset trail intensity if it was set
                if hasattr(enemy, 'trail_intensity'):
                    enemy.trail_intensity = 1.0
                
                # Check if we can detect the player for a potential burst
                if player and enemy.burst_available and enemy.burst_cooldown <= 0 and enemy.lane_change_cooldown <= 0:
                    # Calculate horizontal distance to player
                    distance_x = enemy.rect.x - player.rect.x
                    
                    # Only consider bursting if player is within detection range and ahead of us
                    if 0 < distance_x < enemy.detection_range:
                        # Determine if player is in one of three lanes relative to enemy
                        player_lane = 0  # 0 = same lane, -1 = above, 1 = below
                        lane_threshold = 80  # Vertical distance to consider a different lane
                        
                        if player.rect.centery < enemy.rect.centery - lane_threshold:
                            player_lane = -1  # Player is above
                        elif player.rect.centery > enemy.rect.centery + lane_threshold:
                            player_lane = 1  # Player is below
                        
                        # 70% chance to target player's lane, 30% chance to predict movement
                        if random.random() < 0.7 or player_lane == 0:
                            # Target player's current position
                            enemy.target_y = player.rect.centery
                        else:
                            # Try to predict where player is moving
                            if hasattr(player, 'last_y'):
                                # Calculate player's vertical movement direction
                                player_moving_down = player.rect.centery > player.last_y
                                # Predict further movement in that direction
                                prediction_offset = random.randint(30, 70) * (1 if player_moving_down else -1)
                                enemy.target_y = player.rect.centery + prediction_offset
                                # Keep within screen bounds
                                enemy.target_y = max(50, min(SCREEN_HEIGHT - 50, enemy.target_y))
                            else:
                                # If we can't predict, just target current position
                                enemy.target_y = player.rect.centery
                        
                        # Set flags for burst
                        enemy.target_acquired = True
                        enemy.pre_burst_delay = 0.4  # Telegraph for 0.4 seconds before burst
                        enemy.lane_change_cooldown = 2.0  # Prevent rapid lane changes
            
            # Keep within screen bounds
            if enemy.rect.top < 10:
                enemy.rect.top = 10
            elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
                enemy.rect.bottom = SCREEN_HEIGHT - 10
            
            # Remove if it goes off-screen
            if enemy.rect.right < 0:
                enemy.kill()
        else:
            # Legacy zigzag behavior for other enemy types (fallback)
            enemy.rect.x -= enemy.speed
            
            # Keep within screen bounds
            if enemy.rect.top < 10:
                enemy.rect.top = 10
            elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
                enemy.rect.bottom = SCREEN_HEIGHT - 10
            
            # Remove if it goes off-screen
            if enemy.rect.right < 0:
                enemy.kill()
    
    def sine_behavior(self, enemy, delta_time):
        """Update sine wave behavior."""
        enemy.rect.x -= enemy.speed
        enemy.angle += enemy.frequency
        enemy.rect.centery = enemy.center_y + int(enemy.amplitude * math.sin(enemy.angle))
        
        # Keep within screen bounds
        if enemy.rect.top < 10:
            enemy.rect.top = 10
        elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
            enemy.rect.bottom = SCREEN_HEIGHT - 10
        
        # Remove if it goes off-screen
        if enemy.rect.right < 0:
            enemy.kill()
    
    def dive_behavior(self, enemy, delta_time):
        """Update dive behavior."""
        if enemy.dive_state == "approach":
            # Move towards the screen
            enemy.rect.x -= enemy.speed
            
            # When reaching a certain x position, start diving
            if enemy.rect.x < SCREEN_WIDTH * 0.7:
                enemy.dive_state = "dive"
        
        elif enemy.dive_state == "dive":
            # Dive towards the target y position
            enemy.rect.x -= enemy.speed * 0.5  # Slow down x movement during dive
            
            if enemy.rect.centery < enemy.target_y:
                enemy.rect.y += enemy.dive_speed
                if enemy.rect.centery >= enemy.target_y:
                    enemy.dive_state = "retreat"
            else:
                enemy.rect.y -= enemy.dive_speed
                if enemy.rect.centery <= enemy.target_y:
                    enemy.dive_state = "retreat"
        
        elif enemy.dive_state == "retreat":
            # Retreat after dive
            enemy.rect.x -= enemy.speed * 1.5  # Faster x movement during retreat
        
        # Remove if it goes off-screen
        if enemy.rect.right < 0:
            enemy.kill()
    
    def straight_behavior(self, enemy, delta_time):
        """Update straight behavior."""
        enemy.rect.x -= enemy.speed
        
        # Remove if it goes off-screen
        if enemy.rect.right < 0:
            enemy.kill()
    
    def _fire_shot(self, enemy):
        """Fire a projectile from the enemy."""
        if enemy.movement_pattern == "drifter":
            # Dim energy bolt for drifter
            bullet = {
                'x': enemy.rect.centerx,
                'y': enemy.rect.bottom,
                'speed': 2,  # Slower-moving projectile
                'width': 3,
                'height': 7,
                'color': (180, 80, 80),  # Dimmer red energy bolt
                'damage': 1
            }
        else:
            # Default bullet
            bullet = {
                'x': enemy.rect.centerx,
                'y': enemy.rect.bottom,
                'speed': 3,  # Slow-moving projectile
                'width': 4,
                'height': 8,
                'color': (255, 100, 100),  # Red energy bolt
                'damage': 1
            }
        enemy.bullets.append(bullet)
    
    def update_bullets(self, enemy):
        """Update enemy bullets."""
        if hasattr(enemy, 'bullets'):
            # Get player reference for homing missiles
            player = None
            if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
                player = enemy.game_manager.player
            
            for bullet in list(enemy.bullets):
                # Check if this is a juggernaut bullet with velocity components
                if 'vx' in bullet and 'vy' in bullet:
                    # Update position using velocity components
                    bullet['x'] += bullet['vx']
                    bullet['y'] += bullet['vy']
                    
                    # Handle homing missiles
                    if 'homing' in bullet and bullet['homing'] and player:
                        # Calculate direction to player
                        dx = player.rect.centerx - bullet['x']
                        dy = player.rect.centery - bullet['y']
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        if distance > 0:
                            # Normalize direction
                            dx /= distance
                            dy /= distance
                            
                            # Adjust velocity toward player (homing effect)
                            bullet['vx'] += dx * bullet['homing_strength']
                            bullet['vy'] += dy * bullet['homing_strength']
                            
                            # Normalize velocity to maintain constant speed
                            velocity = math.sqrt(bullet['vx']**2 + bullet['vy']**2)
                            if velocity > 0:
                                bullet['vx'] = (bullet['vx'] / velocity) * bullet['speed']
                                bullet['vy'] = (bullet['vy'] / velocity) * bullet['speed']
                        
                        # Update missile lifetime
                        if 'lifetime' in bullet:
                            bullet['lifetime'] -= 0.016  # Approximate for one frame
                            if bullet['lifetime'] <= 0:
                                enemy.bullets.remove(bullet)
                                continue
                        
                        # Store trail positions for rendering
                        if 'trail' in bullet:
                            bullet['trail'].append((bullet['x'], bullet['y']))
                            # Keep only the last 10 positions
                            if len(bullet['trail']) > 10:
                                bullet['trail'] = bullet['trail'][-10:]
                    
                    # Remove bullets that go off screen
                    if (bullet['x'] < -50 or bullet['x'] > SCREEN_WIDTH + 50 or
                        bullet['y'] < -50 or bullet['y'] > SCREEN_HEIGHT + 50):
                        enemy.bullets.remove(bullet)
                
                # Handle standard direction-based bullets
                elif 'direction' in bullet and bullet['direction'] == 'left':
                    # Horizontal bullet (moving left)
                    bullet['x'] += bullet['speed']
                    
                    # Remove bullets that go off the left side of the screen
                    if bullet['x'] + bullet['width'] < 0:
                        enemy.bullets.remove(bullet)
                else:
                    # Vertical bullet (moving down)
                    bullet['y'] += bullet['speed']
                    
                    # Remove bullets that go off the bottom of the screen
                    if bullet['y'] > SCREEN_HEIGHT:
                        enemy.bullets.remove(bullet)
    def _fire_shot_left(self, enemy):
        """Fire a projectile to the left (for low-type enemy)."""
        # More pronounced bullet for better visibility
        bullet = {
            'x': enemy.rect.centerx - 5,  # Start slightly to the left of center
            'y': enemy.rect.centery,
            'speed': -6,  # Faster negative speed means moving left quickly
            'width': 8,   # Wider bullet
            'height': 3,  # Shorter but wider for better visibility
            'color': (255, 80, 80),  # Brighter red for better visibility
            'damage': 1,
            'direction': 'left'  # Mark this as a horizontal bullet
        }
        enemy.bullets.append(bullet)
    def _init_juggernaut(self, enemy):
        """Initialize juggernaut behavior for super-type enemy."""
        # Position far to the right of the screen for dramatic entrance
        # Note: For SuperEnemy class, this is already set in the constructor
        if not hasattr(enemy, 'is_exploding'):  # Only set if not a SuperEnemy
            enemy.rect.x = SCREEN_WIDTH + 300
            enemy.rect.y = random.randint(80, SCREEN_HEIGHT - 80)
        
        # Movement direction (always start moving left)
        enemy.direction = -1
        
        # Dynamic positioning behavior - more aggressive
        enemy.preferred_distance = random.randint(180, 250)  # Closer preferred distance to be more threatening
        enemy.min_distance = 120   # Can get closer to player
        enemy.max_distance = 300   # Don't get too far
        enemy.position_update_timer = 0  # Timer for position recalculation
        enemy.position_update_interval = random.uniform(0.8, 1.5)  # More frequent position updates
        enemy.current_target_x = None  # Target X position (will be calculated)
        
        # Screen boundary limits
        enemy.min_x = 100  # Increased minimum X to give more room for maneuvering
        enemy.max_x = SCREEN_WIDTH - enemy.rect.width - 20  # Don't go off right edge
        
        # Vertical movement properties - more dynamic and aggressive
        enemy.bob_angle = random.random() * 6.28
        enemy.bob_speed = random.uniform(0.02, 0.04)
        enemy.bob_amplitude = random.randint(4, 7)
        enemy.target_y = enemy.rect.y
        
        # Attack properties - more aggressive
        enemy.last_attack_time = time.time()
        enemy.attack_warning = False
        enemy.warning_duration = 0
        enemy.attack_type = None
        enemy.attack_cooldown = 1.2  # Reduced initial cooldown
        
        # Tracking properties - improved for more aggressive movement
        enemy.tracking_speed = 0.7  # Increased for more responsive movement
        enemy.tracking_enabled = True
        enemy.horizontal_speed = 1.0  # Increased for more aggressive movement
        
        # Charge properties - more aggressive
        enemy.charge_speed = 3.5  # Increased for more impactful charges
        enemy.charge_duration = 0
        enemy.charge_cooldown = random.uniform(4.0, 7.0)  # Reduced cooldown for more frequent charges
        
        # Shield properties
        enemy.shield_opacity = 255
        enemy.shield_pulse_speed = 0
        enemy.shield_regen_time = 5.0  # Faster shield regeneration
        
        # Visual effect properties - minimized
        enemy.damage_flash = 0
        enemy.engine_flare = 0
        
        # Bobbing offset (for visual effect)
        enemy.bob_offset = 0
        
        # Vertical movement limits with more freedom
        enemy.min_y = 50  # Less restriction at the top
        enemy.max_y = SCREEN_HEIGHT - 50  # Less restriction at the bottom
        
        # Player targeting
        enemy.target_player = True  # Always target the player
        
        # Debug flag - removed
        enemy.debug_attack = False  # Don't force attack on first update
    def juggernaut_behavior(self, enemy, delta_time):
        """Update juggernaut behavior for super-type enemy."""
        # Skip behavior if enemy is exploding (for SuperEnemy class)
        if hasattr(enemy, 'is_exploding') and enemy.is_exploding:
            return
            
        # Get player reference if available
        player = None
        if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
            player = enemy.game_manager.player
        
        # Update attack phase based on health
        if enemy.health <= 1:
            enemy.attack_phase = 3  # Critical phase
            if not enemy.berserk_mode:
                enemy.berserk_mode = True
                enemy.base_speed *= 1.2  # 20% speed increase in berserk mode (reduced from 30%)
                # Visual indication of berserk mode
                enemy.damage_flash = 10
        elif enemy.health <= 2:
            enemy.attack_phase = 2  # Damaged phase
        else:
            enemy.attack_phase = 1  # Normal phase
        
        # Update position target timer
        enemy.position_update_timer -= delta_time
        
        # Dynamic positioning based on player location
        if player and enemy.position_update_timer <= 0:
            # Recalculate preferred position
            enemy.position_update_timer = enemy.position_update_interval
            
            # Calculate distance to player
            distance_to_player = player.rect.centerx - enemy.rect.centerx
            abs_distance = abs(distance_to_player)
            
            # Determine if we need to adjust position
            if abs_distance < enemy.min_distance:
                # Too close to player, move away
                enemy.current_target_x = player.rect.centerx - enemy.preferred_distance * (1 if distance_to_player > 0 else -1)
                enemy.direction = -1 if distance_to_player > 0 else 1
            elif abs_distance > enemy.max_distance:
                # Too far from player, move closer
                enemy.current_target_x = player.rect.centerx - enemy.preferred_distance * (1 if distance_to_player > 0 else -1)
                enemy.direction = 1 if distance_to_player > 0 else -1
            else:
                # Within acceptable range, occasionally adjust position for more dynamic movement
                if random.random() < 0.3:  # 30% chance to adjust position even when in acceptable range
                    # Choose a new position within the acceptable range
                    offset = random.randint(enemy.min_distance, enemy.max_distance)
                    enemy.current_target_x = player.rect.centerx - offset * (1 if distance_to_player > 0 else -1)
                    enemy.direction = 1 if enemy.rect.centerx < enemy.current_target_x else -1
            
            # Ensure target position is within screen bounds
            enemy.current_target_x = max(enemy.min_x, min(enemy.max_x, enemy.current_target_x))
        
        # Calculate actual speed based on current state
        if enemy.is_charging:
            actual_speed = enemy.charge_speed * enemy.direction
        elif enemy.retreat_active:
            actual_speed = -enemy.base_speed * 0.5 * enemy.direction  # Slower retreat
        else:
            # Tank-like movement: deliberate but with purpose
            base_speed = enemy.horizontal_speed * enemy.speed_multiplier * 0.7
            
            # Adjust speed based on distance to target position
            if enemy.current_target_x is not None:
                distance_to_target = enemy.current_target_x - enemy.rect.centerx
                # If very close to target, slow down
                if abs(distance_to_target) < 20:
                    base_speed *= 0.5
                # Set direction based on target position
                enemy.direction = 1 if distance_to_target > 0 else -1
            
            actual_speed = base_speed * enemy.direction
        
        # Always move left initially (toward the player)
        if enemy.rect.x > SCREEN_WIDTH - 100:
            # When first entering the screen, always move left
            enemy.direction = -1
            actual_speed = enemy.horizontal_speed * enemy.speed_multiplier * enemy.direction
        
        # Apply horizontal movement
        enemy.rect.x += actual_speed * delta_time * 60
        
        # Keep within horizontal bounds
        if enemy.rect.x < enemy.min_x:
            enemy.rect.x = enemy.min_x
            enemy.direction = 1  # Reverse direction if hitting left boundary
        elif enemy.rect.x > enemy.max_x:
            enemy.rect.x = enemy.max_x
            enemy.direction = -1  # Reverse direction if hitting right boundary
        
        # Handle bobbing motion - more natural effect
        enemy.bob_angle += enemy.bob_speed
        enemy.bob_offset = math.sin(enemy.bob_angle) * enemy.bob_amplitude
        
        # Track player vertically - more deliberate tracking with some randomness
        if player and enemy.tracking_enabled:
            # Calculate vertical distance to player
            distance_y = player.rect.centery - enemy.rect.centery
            
            # Add some randomness to vertical positioning
            vertical_offset = random.randint(-40, 40)
            adjusted_player_y = player.rect.centery + vertical_offset
            adjusted_distance_y = adjusted_player_y - enemy.rect.centery
            
            # Only track if significantly above or below
            if abs(adjusted_distance_y) > 30:  # Moderate threshold for vertical movement
                # Set target Y to adjusted player position
                enemy.target_y = adjusted_player_y
                
                # Move toward target Y position deliberately
                direction = 1 if adjusted_distance_y > 0 else -1
                
                # Vary tracking speed based on distance and phase
                tracking_speed = enemy.tracking_speed
                if abs(adjusted_distance_y) > 100:
                    tracking_speed *= 1.2  # Speed up if far away
                if enemy.attack_phase >= 2:
                    tracking_speed *= 1.1  # Slightly faster tracking in later phases
                
                enemy.rect.y += direction * tracking_speed * delta_time * 40  # Deliberate movement
        
        # Apply bobbing offset for more natural movement
        enemy.rect.y += enemy.bob_offset * delta_time * 30
        
        # Keep within vertical bounds with improved edge handling
        if hasattr(enemy, 'min_y') and hasattr(enemy, 'max_y'):
            if enemy.rect.top < enemy.min_y:
                enemy.rect.top = enemy.min_y
                # Force movement away from top edge
                if enemy.tracking_enabled and enemy.rect.top <= enemy.min_y + 10:
                    enemy.rect.y += 0.8  # Stronger downward nudge
            elif enemy.rect.bottom > enemy.max_y:
                enemy.rect.bottom = enemy.max_y
                # Force movement away from bottom edge
                if enemy.tracking_enabled and enemy.rect.bottom >= enemy.max_y - 10:
                    enemy.rect.y -= 0.8  # Stronger upward nudge
        else:
            # Fallback to standard screen bounds
            if enemy.rect.top < 10:
                enemy.rect.top = 10
            elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
                enemy.rect.bottom = SCREEN_HEIGHT - 10
        
        # Handle charge behavior - less frequent, slower charges
        if enemy.is_charging:
            enemy.charge_duration -= delta_time
            if enemy.charge_duration <= 0:
                enemy.is_charging = False
                enemy.retreat_active = True
                enemy.charge_cooldown = random.uniform(6.0, 9.0)  # Longer cooldown
                # Retreat duration is proportional to how far we charged
                retreat_duration = enemy.charge_duration * 0.7
                enemy.retreat_duration = max(0.8, min(1.8, retreat_duration))
        elif enemy.retreat_active:
            enemy.retreat_duration -= delta_time
            if enemy.retreat_duration <= 0:
                enemy.retreat_active = False
        elif enemy.charge_cooldown > 0:
            enemy.charge_cooldown -= delta_time
            # Only charge if player is in front of us and we're in phase 2 or 3
            if enemy.charge_cooldown <= 0 and enemy.attack_phase >= 2 and player:
                # Check if player is in front of us (in the direction we're facing)
                player_in_front = (enemy.direction == -1 and player.rect.x < enemy.rect.x) or \
                                 (enemy.direction == 1 and player.rect.x > enemy.rect.x)
                
                if player_in_front and random.random() < 0.7:  # 70% chance to charge when conditions are met
                    self._prepare_charge(enemy)
        
        # Handle shield regeneration
        if not enemy.has_shield and enemy.shield_regen_cooldown > 0:
            enemy.shield_regen_cooldown -= delta_time
            if enemy.shield_regen_cooldown <= 0 and enemy.attack_phase == 1:
                # Only regenerate shield in phase 1
                enemy.has_shield = True
                enemy.shield_health = 1
                enemy.shield_opacity = 255
        
        # Handle shield pulse
        if enemy.shield_pulse_active:
            enemy.shield_pulse_radius += enemy.shield_pulse_speed * delta_time * 60
            if enemy.shield_pulse_radius > 100:
                enemy.shield_pulse_active = False
                enemy.shield_pulse_radius = 0
                enemy.shield_pulse_cooldown = random.uniform(3.0, 5.0)  # Longer cooldown
        elif enemy.shield_pulse_cooldown > 0:
            enemy.shield_pulse_cooldown -= delta_time
            if enemy.shield_pulse_cooldown <= 0 and enemy.has_shield and player:
                # Only pulse if player is nearby
                distance_to_player = math.sqrt((player.rect.centerx - enemy.rect.centerx)**2 + 
                                             (player.rect.centery - enemy.rect.centery)**2)
                if distance_to_player < 200:  # Only pulse when player is within range
                    self._activate_shield_pulse(enemy)
                else:
                    # Reset cooldown to a short value to check again soon
                    enemy.shield_pulse_cooldown = 0.5
        
        # Handle attack cooldown - more deliberate attacks
        if enemy.attack_cooldown > 0:
            enemy.attack_cooldown -= delta_time
            if enemy.attack_cooldown <= 0 or enemy.debug_attack:
                if hasattr(enemy, 'debug_attack') and enemy.debug_attack:
                    enemy.debug_attack = False  # Only force attack once
                
                # Only attack if player is in front of us
                if player:
                    # Check if player is in front of us (in the direction we're facing)
                    player_in_front = (enemy.direction == -1 and player.rect.x < enemy.rect.x) or \
                                     (enemy.direction == 1 and player.rect.x > enemy.rect.x)
                    
                    if player_in_front:
                        self._prepare_attack(enemy)
                    else:
                        # If player is behind us, turn around to face them
                        enemy.direction *= -1
                        # Short cooldown before attacking
                        enemy.attack_cooldown = 0.5
        
        # Handle attack warning
        if enemy.attack_warning:
            enemy.warning_duration -= delta_time
            if enemy.warning_duration <= 0:
                enemy.attack_warning = False
                self._execute_attack(enemy)
        
        # Update damage flash effect
        if enemy.damage_flash > 0:
            enemy.damage_flash -= delta_time * 10
        
        # Update engine flare effect
        if enemy.is_charging:
            enemy.engine_flare = min(1.0, enemy.engine_flare + delta_time * 2)
        else:
            enemy.engine_flare = max(0.0, enemy.engine_flare - delta_time)
    def _prepare_attack(self, enemy):
        """Prepare an attack for the juggernaut enemy."""
        # Choose attack type based on phase and tactical situation
        if enemy.attack_phase == 1:
            # Phase 1: Shield pulse if shield is active, otherwise single shot
            if enemy.has_shield:
                # Check if player is close enough for shield pulse to be effective
                if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
                    player = enemy.game_manager.player
                    distance_to_player = math.sqrt((player.rect.centerx - enemy.rect.centerx)**2 + 
                                                 (player.rect.centery - enemy.rect.centery)**2)
                    
                    if distance_to_player < 180:  # Only use shield pulse when player is close enough
                        enemy.attack_type = "shield_pulse"
                    else:
                        enemy.attack_type = "single_shot"  # Use single shot if player is too far for shield pulse
                else:
                    enemy.attack_type = "shield_pulse"
            else:
                enemy.attack_type = "single_shot"
        elif enemy.attack_phase == 2:
            # Phase 2: Twin cannons with occasional single shot for variety
            if random.random() < 0.8:  # 80% chance for twin shot
                enemy.attack_type = "twin_shot"
            else:
                enemy.attack_type = "single_shot"  # 20% chance for single shot
        else:
            # Phase 3: Missile barrage or desperate twin shot if player is very close
            if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
                player = enemy.game_manager.player
                distance_to_player = math.sqrt((player.rect.centerx - enemy.rect.centerx)**2 + 
                                             (player.rect.centery - enemy.rect.centery)**2)
                
                if distance_to_player < 120:  # Player is very close
                    # 50% chance for twin shot (faster) when player is close
                    enemy.attack_type = "twin_shot" if random.random() < 0.5 else "missile_barrage"
                else:
                    enemy.attack_type = "missile_barrage"
            else:
                enemy.attack_type = "missile_barrage"
        
        # Set warning duration - reduced for surprise attacks
        enemy.attack_warning = True
        if enemy.attack_type == "missile_barrage":
            enemy.warning_duration = 0.4  # Shorter warning for more surprise
        elif enemy.attack_type == "shield_pulse":
            enemy.warning_duration = 0.3  # Very short warning for shield pulse
        else:
            enemy.warning_duration = 0.35  # Short warning for shots
        
        # No visual indication of attack preparation
        enemy.damage_flash = 0
        
        # Disable tracking during attack preparation
        enemy.tracking_enabled = False
        
        # Adjust vertical position to better target player if needed
        if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
            player = enemy.game_manager.player
            
            # For non-shield pulse attacks, try to align with player vertically
            if enemy.attack_type != "shield_pulse" and abs(player.rect.centery - enemy.rect.centery) > 30:
                # Move toward player's vertical position
                direction = 1 if player.rect.centery > enemy.rect.centery else -1
                enemy.rect.y += direction * 15  # Quick adjustment before attack
        
        # No debug message needed
    
    def _execute_attack(self, enemy):
        """Execute the prepared attack for the juggernaut enemy."""
        if enemy.attack_type == "shield_pulse":
            self._activate_shield_pulse(enemy)
        elif enemy.attack_type == "single_shot":
            self._fire_juggernaut_shot(enemy, 0)
        elif enemy.attack_type == "twin_shot":
            self._fire_juggernaut_shot(enemy, -10)
            self._fire_juggernaut_shot(enemy, 10)
        elif enemy.attack_type == "missile_barrage":
            # Fire multiple homing missiles
            for angle in [-20, -10, 0, 10, 20]:
                self._fire_juggernaut_missile(enemy, angle)
        
        # Reset attack cooldown based on phase - more aggressive
        if enemy.attack_phase == 1:
            enemy.attack_cooldown = random.uniform(2.0, 3.0)  # Faster attacks
        elif enemy.attack_phase == 2:
            enemy.attack_cooldown = random.uniform(1.8, 2.5)  # Even faster
        else:
            enemy.attack_cooldown = random.uniform(1.5, 2.0)  # Very aggressive in phase 3
        
        # Re-enable tracking after attack
        enemy.tracking_enabled = True
    
    def _activate_shield_pulse(self, enemy):
        """Activate the shield pulse attack."""
        enemy.shield_pulse_active = True
        enemy.shield_pulse_radius = 20
        enemy.shield_pulse_speed = 4  # Faster pulse expansion
        
        # Check for player collision with pulse
        if hasattr(enemy, 'game_manager') and enemy.game_manager and enemy.game_manager.player:
            player = enemy.game_manager.player
            # Calculate distance to player
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            # If player is close, apply knockback
            if distance < 150:  # Increased range
                # Calculate knockback direction
                knockback_x = dx / distance if distance > 0 else 0
                knockback_y = dy / distance if distance > 0 else 0
                
                # Apply knockback to player position
                player.rect.x += knockback_x * 50  # Stronger knockback
                player.rect.y += knockback_y * 50
    
    def _prepare_charge(self, enemy):
        """Prepare a charge attack."""
        enemy.is_charging = True
        enemy.charge_duration = random.uniform(0.9, 1.4)  # Longer charges
        enemy.engine_flare = 0  # No visual flare
        
        # No visual indication of charge
        enemy.damage_flash = 0
        
        # More aggressive charging behavior
        if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
            player = enemy.game_manager.player
            
            # Calculate distance to player
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Determine charge strategy based on distance and phase
            if enemy.attack_phase == 3 or distance < 200:
                # In critical phase or player is close - direct charge
                if player.rect.centerx < enemy.rect.centerx:
                    enemy.direction = -1  # Charge left toward player
                else:
                    enemy.direction = 1   # Charge right toward player
            else:
                # More tactical charge - sometimes charge past player or to a strategic position
                tactical_choice = random.random()
                
                if tactical_choice < 0.7:  # 70% chance for direct charge (increased from 60%)
                    # Direct charge toward player
                    if player.rect.centerx < enemy.rect.centerx:
                        enemy.direction = -1  # Charge left toward player
                    else:
                        enemy.direction = 1   # Charge right toward player
                elif tactical_choice < 0.9:  # 20% chance for positioning charge
                    # Charge to a position that gives better attack angle
                    target_x = player.rect.centerx + random.randint(100, 200) * (1 if random.random() < 0.5 else -1)
                    enemy.direction = 1 if target_x > enemy.rect.centerx else -1
                else:  # 10% chance for feint
                    # Feint in opposite direction of player
                    enemy.direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                    enemy.charge_duration *= 0.7  # Shorter feint charge
            
            # Also adjust vertical position to better target player
            if abs(player.rect.centery - enemy.rect.centery) > 30:
                # Move toward player's vertical position with minimal randomness
                vertical_offset = random.randint(-15, 15)  # Reduced randomness for more accurate targeting
                enemy.target_y = player.rect.centery + vertical_offset
                
                # Adjust position immediately to better aim
                direction = 1 if enemy.target_y > enemy.rect.centery else -1
                enemy.rect.y += direction * 25  # Quicker adjustment before charge
    
    def _fire_juggernaut_shot(self, enemy, angle_offset=0):
        """Fire a projectile from the juggernaut enemy."""
        # Calculate angle in radians
        angle_rad = math.radians(angle_offset)
        
        # Calculate velocity components - aim toward player if possible
        speed = 4.5  # Slower projectiles (was 6)
        
        # Try to aim at player
        player = None
        if hasattr(enemy, 'game_manager') and enemy.game_manager and hasattr(enemy.game_manager, 'player'):
            player = enemy.game_manager.player
        
        # Determine firing position based on direction
        if hasattr(enemy, 'direction') and enemy.direction == 1:
            # Moving right, fire from right side
            fire_x = enemy.rect.right
        else:
            # Moving left, fire from left side
            fire_x = enemy.rect.left
        
        if player:
            # Calculate direction to player
            dx = player.rect.centerx - fire_x
            dy = player.rect.centery - enemy.rect.centery
            
            # Add some randomness to make it not perfect
            dy += random.randint(-30, 30)
            
            # Normalize direction
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                
                # Apply angle offset
                cos_offset = math.cos(angle_rad)
                sin_offset = math.sin(angle_rad)
                
                # Rotate direction vector by offset angle
                vx = dx * cos_offset - dy * sin_offset
                vy = dx * sin_offset + dy * cos_offset
                
                # Scale by speed
                vx *= speed
                vy *= speed
            else:
                # Fallback if distance is zero
                vx = speed * enemy.direction * math.cos(angle_rad)
                vy = speed * math.sin(angle_rad)
        else:
            # Default direction if no player
            vx = speed * enemy.direction * math.cos(angle_rad)
            vy = speed * math.sin(angle_rad)
        
        # Create bullet with angle - larger, more powerful projectiles
        bullet = {
            'x': fire_x,
            'y': enemy.rect.centery,
            'vx': vx,
            'vy': vy,
            'speed': speed,
            'width': 14,  # Even larger projectiles (was 10)
            'height': 7,  # Taller projectiles (was 5)
            'color': (200, 50, 200),  # Purple energy bolt
            'damage': 1,
            'angle': angle_offset
        }
        
        if not hasattr(enemy, 'bullets'):
            enemy.bullets = []
        
        enemy.bullets.append(bullet)
    
    def _fire_juggernaut_missile(self, enemy, angle_offset=0):
        """Fire a homing missile from the juggernaut enemy."""
        # Calculate initial angle in radians
        angle_rad = math.radians(angle_offset)
        
        # Determine firing position based on direction
        if hasattr(enemy, 'direction') and enemy.direction == 1:
            # Moving right, fire from right side
            fire_x = enemy.rect.right
            base_vx = math.cos(angle_rad) * 2.5  # Slower base velocity (was 3.5)
        else:
            # Moving left, fire from left side
            fire_x = enemy.rect.left
            base_vx = -math.cos(angle_rad) * 2.5  # Slower base velocity (was 3.5)
        
        # Calculate velocity components
        speed = 2.5  # Slower missiles (was 3.5)
        vx = base_vx
        vy = math.sin(angle_rad) * speed
        
        # Create missile with homing properties - larger, more powerful missiles
        missile = {
            'x': fire_x,
            'y': enemy.rect.centery,
            'vx': vx,
            'vy': vy,
            'speed': speed,
            'width': 16,  # Even larger missiles (was 12)
            'height': 8,  # Taller missiles (was 6)
            'color': (255, 100, 0),  # Orange missile
            'damage': 1,
            'angle': angle_offset,
            'homing': True,
            'homing_strength': 0.05,  # Weaker homing (was 0.08) for slower turning
            'lifetime': 5.0,  # Longer lifetime (was 4.0) since they're slower
            'trail': []  # Store trail positions
        }
        
        if not hasattr(enemy, 'bullets'):
            enemy.bullets = []
        
        enemy.bullets.append(missile)
