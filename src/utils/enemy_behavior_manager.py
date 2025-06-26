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
            "dive": self.dive_behavior
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
        
        # Shooting properties
        enemy.has_shot = False  # Can only shoot once
        enemy.can_shoot = False  # Will be set to true when within range
        enemy.is_preparing_shot = False
        enemy.shot_preparation_time = 0
        enemy.shot_preparation_duration = 0.8  # Time to prepare shot (flash warning)
        enemy.shot_flash_intensity = 0  # Flash intensity (0-100)
        
        # Stutter behavior
        enemy.stutter_timer = random.uniform(3.0, 5.0)  # Time until next stutter
        enemy.stutter_duration = 0.0  # Current stutter duration
        enemy.is_stuttering = False
        enemy.last_time = time.time()
        
        # Flickering light properties
        enemy.light_flicker_speed = random.uniform(0.1, 0.2)
        enemy.light_flicker_angle = random.random() * 6.28
        enemy.light_brightness = 50  # Base brightness
        enemy.light_size = 3
        
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
        """Initialize zigzag behavior."""
        enemy.direction = 1  # 1 for down, -1 for up
        enemy.direction_change_timer = 0
        enemy.direction_change_delay = random.randint(20, 40)
        
        # Position from the right side
        enemy.rect.x = SCREEN_WIDTH + random.randint(50, 200)
        enemy.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
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
                # Start stuttering
                enemy.is_stuttering = True
                enemy.stutter_duration = 0.5  # Stutter for 0.5 seconds
                enemy.stutter_timer = random.uniform(3.0, 5.0)  # Reset timer for next stutter
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
        
        # Determine if we should start a dash (only if not already dashing, not preparing to shoot, and cooldown expired)
        if (not enemy.is_dashing and not enemy.is_preparing_shot and enemy.dash_cooldown <= 0 and 
            random.random() < enemy.dash_chance):
            enemy.is_dashing = True
            enemy.dash_direction = random.choice([-1, 1])  # Random up or down
            enemy.dash_duration = random.uniform(0.3, 0.6)  # Short dash
            enemy.dash_cooldown = random.uniform(2.0, 4.0)  # Long cooldown between dashes
        
        # Handle dashing
        if enemy.is_dashing:
            # Move vertically based on dash direction
            enemy.rect.y += enemy.dash_direction * enemy.dash_speed * speed_multiplier * delta_time * 60
            
            # Update dash duration
            enemy.dash_duration -= delta_time
            if enemy.dash_duration <= 0:
                enemy.is_dashing = False
        
        # Check if player is on the same horizontal line (for shooting)
        player_on_same_line = False
        if hasattr(enemy, 'game_manager') and enemy.game_manager and enemy.game_manager.player:
            player = enemy.game_manager.player
            # Check if player's center is within the vertical bounds of the enemy
            if (player.rect.centery >= enemy.rect.top and 
                player.rect.centery <= enemy.rect.bottom):
                player_on_same_line = True
        
        # Handle shooting preparation and execution
        if (enemy.can_shoot and not enemy.has_shot and not enemy.is_preparing_shot and 
            not enemy.is_dashing and player_on_same_line):
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
            enemy.shot_flash_intensity = min(70, int(progress * 100))  # Reduced max intensity to 70
            
            # When preparation is complete, fire the shot
            if enemy.shot_preparation_time <= 0:
                self._fire_shot_left(enemy)  # Fire shot to the left
                enemy.has_shot = True
                enemy.is_preparing_shot = False
                enemy.shot_flash_intensity = 0
        else:
            # Normal horizontal movement if not preparing to shoot
            if not enemy.is_preparing_shot:
                enemy.rect.x -= enemy.horizontal_speed * speed_multiplier * delta_time * 60
        
        # Update flickering light
        enemy.light_flicker_angle += enemy.light_flicker_speed
        
        # Base brightness plus flash intensity during shot preparation
        if enemy.is_preparing_shot:
            enemy.light_brightness = 50 + enemy.shot_flash_intensity
        else:
            enemy.light_brightness = 50 + int(20 * math.sin(enemy.light_flicker_angle))  # Normal flicker
        
        enemy.light_position = (enemy.rect.centerx, enemy.rect.centery - 5)  # Update light position
        
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
        """Update zigzag behavior."""
        enemy.rect.x -= enemy.speed
        enemy.rect.y += enemy.speed * enemy.direction
        
        # Change direction periodically
        enemy.direction_change_timer += 1
        if enemy.direction_change_timer >= enemy.direction_change_delay:
            enemy.direction *= -1
            enemy.direction_change_timer = 0
            enemy.direction_change_delay = random.randint(20, 40)
        
        # Keep within screen bounds
        if enemy.rect.top < 10:
            enemy.rect.top = 10
            enemy.direction = 1
        elif enemy.rect.bottom > SCREEN_HEIGHT - 10:
            enemy.rect.bottom = SCREEN_HEIGHT - 10
            enemy.direction = -1
        
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
            for bullet in list(enemy.bullets):
                # Update bullet position based on direction
                if 'direction' in bullet and bullet['direction'] == 'left':
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
