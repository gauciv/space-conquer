"""
Boss sprites for the Space Impact game.
"""
import pygame
import random
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES
from .bullet import Bullet

class Boss(pygame.sprite.Sprite):
    """Base class for boss enemies."""
    def __init__(self, boss_type, asset_loader, sound_manager):
        super().__init__()
        self.boss_type = boss_type
        self.sound_manager = sound_manager
        
        # Set image based on boss type
        if boss_type == 'mini':
            original_image = asset_loader.get_image('mini_boss')
            self.name = "Vanguard"
            self.max_health = 50  # Doubled from 25 to 50
            self.health = self.max_health
            self.speed = 2.5  # Increased from 2 to 2.5
            self.shoot_delay = 1000  # milliseconds
            self.bullet_speed = -8  # Negative because bullets move left
            self.bullet_damage = 1
            self.score_value = 750  # Increased from 250 to 750 (3x)
            self.movement_pattern = "advanced"  # Changed from "sine" to "advanced"
            self.battle_distance = 15  # Distance from right edge during battle (reduced to 15px)
            
            # Scale the mini boss to 1.5x size
            new_width = int(original_image.get_width() * 1.5)
            new_height = int(original_image.get_height() * 1.5)
            
            # Mini boss specific attack patterns
            self.attack_phase = 1  # Current attack phase (1-3)
            self.attack_pattern = "spread"  # Initial attack pattern
            self.attack_timer = 0
            self.attack_change_delay = 5000  # Change attack pattern every 5 seconds
            self.dash_cooldown = 0
            self.dash_duration = 0
            self.is_dashing = False
            self.dash_target_y = 0
            self.dash_speed = 8
            self.bullet_patterns = ["spread", "aimed", "barrage"]
            self.current_pattern_index = 0
            
        else:  # main boss
            original_image = asset_loader.get_image('main_boss')
            self.name = "Dreadnought"
            self.max_health = 100  # Doubled from 50 to 100
            self.health = self.max_health
            self.speed = 1.5
            self.shoot_delay = 1200  # Nerfed from 800 to 1200 milliseconds
            self.bullet_speed = -8  # Slightly nerfed from -10 to -8
            self.bullet_damage = 2
            self.score_value = 1500  # Increased from 500 to 1500 (3x)
            self.movement_pattern = "multistage"  # Changed from "complex" to "multistage"
            self.battle_distance = 15  # Distance from right edge during battle (reduced to 15px)
            
            # Scale the main boss to 0.975x size (1.5 * 0.65 = 0.975, reducing by 35% from the 1.5x size)
            new_width = int(original_image.get_width() * 0.975)
            new_height = int(original_image.get_height() * 0.975)
            
            # Main boss specific attack patterns
            self.attack_phase = 1  # Current attack phase (1-3)
            self.attack_pattern = "spread"  # Initial attack pattern
            self.attack_timer = 0
            self.attack_change_delay = 6000  # Change attack pattern every 6 seconds
            self.special_attack_cooldown = 0
            self.special_attack_duration = 0
            self.is_charging = False
            self.charge_duration = 0
            self.charge_direction = 0
            self.bullet_patterns = ["spread", "laser", "focused", "charge", "laser"]  # Added laser twice for higher frequency
            self.current_pattern_index = 0
            self.pattern_shots = 0  # Count shots in current pattern
            self.max_pattern_shots = 3  # Maximum shots before changing pattern
            
            # Charge attack properties
            self.is_charging = False
            self.charge_start_time = 0
            self.charge_duration = 1000  # 1 second charge
            self.charge_cooldown = 0
            self.charge_target_x = 0
            self.charge_target_y = 0
            self.charge_speed = 12
            self.charge_retreat = False
            self.charge_retreat_time = 0
            
            # Player tracking
            self.player_ref = None  # Will be set by game manager
            self.tracking_player = True  # Whether to follow player's y position
            self.tracking_speed = 2.0  # Speed to follow player
            self.target_y = SCREEN_HEIGHT // 2  # Target y position (will be updated to player's position)
            
            # Laser attack properties
            self.laser_charging = False
            self.laser_charge_time = 0
            self.laser_charge_duration = 1200  # Reduced from 1500 to 1200ms for faster charging
            self.laser_firing = False
            self.laser_fire_time = 0
            self.laser_fire_duration = 1500  # Increased from 1000 to 1500ms for longer firing
            self.laser_width = 0  # Grows during charging
            self.laser_target_y = 0  # Y position to aim laser
            self.laser_damage = 2  # Damage per frame when in contact
            self.laser_color = (255, 50, 50)  # Red laser
            self.is_aiming = False  # Whether the boss is currently aiming
            self.aiming_time = 0  # Time when aiming started
            self.aiming_duration = 400  # Reduced from 500 to 400ms for faster aiming
            
            # Target position for shooting
            self.target_y_for_shooting = SCREEN_HEIGHT // 2  # Default to middle
            self.moving_to_position = False
            
            # Movement parameters
            self.movement_timer = 0
            self.figure8_center_y = SCREEN_HEIGHT // 2
            self.figure8_amplitude = 120
            self.figure8_frequency = 0.015
            self.hover_position = None
            self.hover_timer = 0
            self.hover_duration = 0
            self.movement_paused = False  # Whether movement is paused for aiming/firing
            
        # Scale the image to the calculated size
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        
        # Common properties
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 50  # Start off-screen
        self.rect.centery = SCREEN_HEIGHT // 2
        
        # Create a custom hitbox based on boss type (85% of sprite size for better gameplay)
        hitbox_width = int(self.rect.width * 0.85)
        hitbox_height = int(self.rect.height * 0.85)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # Now that rect is initialized, set tactical positioning
        if boss_type == 'main':
            # Tactical positioning
            self.preferred_distance = SCREEN_WIDTH - self.battle_distance - self.rect.width - 30  # Default distance
            self.close_combat_distance = SCREEN_WIDTH // 2  # Distance for close combat
            self.current_tactic = "ranged"  # Current tactical approach
        
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.entry_complete = False
        self.movement_direction = 1  # 1 for down, -1 for up
        self.movement_change_delay = 120  # frames before changing direction
        
        # Health bar images
        self.health_bar_bg = asset_loader.get_image('health_bar_bg')
        self.health_bar_fill = asset_loader.get_image('health_bar_fill')
        
        # For complex movement pattern
        self.angle = 0
        self.center_y = SCREEN_HEIGHT // 2
        self.amplitude = 100  # How far up/down the boss moves
        self.frequency = 0.02  # How fast the boss moves up/down
        
        # Death animation properties
        self.dying = False
        self.death_animation_start = 0
        self.death_animation_duration = 1500  # 1.5 seconds
        self.explosion_particles = []
    
    def update(self):
        """Update the boss state."""
        # If dying, update death animation
        if self.dying:
            # Update death animation and check if it's complete
            animation_complete = self.update_death_animation()
            return animation_complete
            
        # Get current time for timing-based actions
        now = pygame.time.get_ticks()
        
        # Entry movement - move from right edge to battle position
        if not self.entry_complete:
            self.rect.x -= 3
            if self.rect.right < SCREEN_WIDTH - self.battle_distance:
                self.entry_complete = True
                self.last_shot = now  # Reset shot timer when entry is complete
        else:
            # Ensure bullets are properly managed
            # Remove bullets that have gone off-screen
            for bullet in list(self.bullets):
                if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH or \
                   bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT:
                    bullet.kill()
            
            # Force shooting if no bullets are active and not in special attack
            if len(self.bullets) == 0 and not (self.is_charging or self.laser_charging or self.laser_firing or self.is_aiming):
                # If no bullets are active, force a shot soon
                if now - self.last_shot > 500:  # At least 500ms since last shot
                    self.last_shot = now - self.shoot_delay + 100  # Force a shot soon
            
            # Different movement patterns based on boss type
            if self.movement_pattern == "sine":
                # Sine wave movement
                self.movement_timer += 1
                self.rect.centery = self.center_y + math.sin(self.movement_timer * 0.05) * self.amplitude
            
            elif self.movement_pattern == "complex":
                # More complex movement with occasional direction changes
                self.movement_timer += 1
                
                # Change direction occasionally
                if self.movement_timer % self.movement_change_delay == 0:
                    self.movement_direction = random.choice([-1, 1])
                    self.movement_change_delay = random.randint(60, 180)  # Random delay before next change
                
                # Move up/down with some randomness
                self.rect.y += self.speed * self.movement_direction
                
                # Ensure boss stays on screen
                if self.rect.top < 50:
                    self.rect.top = 50
                    self.movement_direction = 1
                elif self.rect.bottom > SCREEN_HEIGHT - 50:
                    self.rect.bottom = SCREEN_HEIGHT - 50
                    self.movement_direction = -1
            
            elif self.movement_pattern == "multistage":
                # Multistage movement pattern for main boss
                now = pygame.time.get_ticks()
                
                # Update attack pattern based on shots fired
                if self.pattern_shots >= self.max_pattern_shots:
                    self.current_pattern_index = (self.current_pattern_index + 1) % len(self.bullet_patterns)
                    self.attack_pattern = self.bullet_patterns[self.current_pattern_index]
                    self.pattern_shots = 0
                    
                    # Set target position based on new attack pattern
                    if self.attack_pattern == "charge":
                        # For charge attack, prepare to charge
                        if self.player_ref:
                            # Store original position
                            self.original_x = self.rect.x
                            self.original_y = self.rect.y
                            
                            # Target directly at player with slight lead
                            self.charge_target_x = max(50, self.player_ref.rect.x - 20)  # Don't go too far left
                            self.charge_target_y = self.player_ref.rect.y
                            self.is_charging = True
                            self.charge_start_time = now
                            self.movement_paused = True  # Pause normal movement during charge
                            self.current_tactic = "aggressive"
                            self.charge_speed = 18  # Even faster charge speed
                            self.charge_duration = 1200  # Longer charge duration (1.2 seconds)
                            # Play warning sound
                            self.sound_manager.play_sound('explosion')  # Use explosion sound for more impact
                    elif self.attack_pattern == "laser":
                        # For laser attack, move closer to player first
                        if self.player_ref:
                            # Set position closer to player for laser attack
                            self.hover_position = (
                                SCREEN_WIDTH // 2,  # Move to middle of screen
                                self.player_ref.rect.centery  # Match player's y position
                            )
                            self.hover_timer = 0
                            self.hover_duration = 30  # frames - shorter duration
                            # Will start aiming after reaching position
                            self.current_tactic = "close_combat"
                        else:
                            # Skip laser if no player reference
                            self.current_pattern_index = (self.current_pattern_index + 1) % len(self.bullet_patterns)
                            self.attack_pattern = self.bullet_patterns[self.current_pattern_index]
                    else:
                        # For other attacks, use standard positioning
                        self.target_y_for_shooting = SCREEN_HEIGHT // 2
                        self.current_tactic = "ranged"
                        
                        # Set hover position to move to target position
                        self.hover_position = (
                            self.preferred_distance,
                            self.target_y_for_shooting
                        )
                        self.hover_timer = 0
                        self.hover_duration = random.randint(60, 120)  # frames
                
                # Handle hovering to a position
                if self.hover_position:
                    # Move toward hover position
                    dx = self.hover_position[0] - self.rect.x
                    dy = self.hover_position[1] - self.rect.centery
                    
                    # Calculate distance
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance > 5:
                        # Move toward position
                        speed = min(distance * 0.1, 5)  # Speed based on distance, max 5
                        self.rect.x += dx * speed / distance
                        self.rect.y += dy * speed / distance
                    else:
                        # Reached position, increment timer
                        self.hover_timer += 1
                        if self.hover_timer >= self.hover_duration:
                            self.hover_position = None
                elif not self.movement_paused:  # Only move if not paused for aiming/firing
                    # ALWAYS track player if available - this is the key change
                    if self.player_ref:
                        # Calculate target y position (player's y position)
                        self.target_y = self.player_ref.rect.centery
                        
                        # Move toward target y position with increased tracking speed
                        dy = self.target_y - self.rect.centery
                        if abs(dy) > 3:  # Reduced threshold for more responsive tracking
                            # Move toward player with tracking speed
                            tracking_speed = self.tracking_speed
                            if self.attack_phase > 1:
                                tracking_speed *= 1.2  # Faster tracking in later phases
                            self.rect.y += math.copysign(min(abs(dy) * 0.15, tracking_speed), dy)
                    
                    # Different movement based on phase - only horizontal movement
                    if self.attack_phase == 1:
                        # Phase 1: Gentle horizontal movement
                        self.movement_timer += 1
                        t = self.movement_timer * self.figure8_frequency
                        
                        # Add slight horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width) + math.sin(t * 0.5) * 15
                    
                    elif self.attack_phase == 2:
                        # Phase 2: More aggressive horizontal movement
                        self.movement_timer += 1
                        
                        # Add horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width) + math.sin(self.movement_timer * 0.02) * 25
                    
                    elif self.attack_phase == 3:
                        # Phase 3: Erratic horizontal movement
                        self.movement_timer += 1
                        
                        # More aggressive horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width - 10) + math.sin(self.movement_timer * 0.03) * 35
                        
                        # Add occasional jitter
                        if self.movement_timer % 10 == 0:
                            self.rect.x += random.randint(-5, 5)
                
                # Handle special attack cooldown
                if self.special_attack_cooldown > 0:
                    self.special_attack_cooldown -= 16  # Approximately 16ms per frame
                
                # Handle charge attack
                if self.is_charging:
                    charge_progress = (now - self.charge_start_time) / self.charge_duration
                    
                    if not self.charge_retreat:
                        # Pre-charge warning
                        if charge_progress < 0.3:  # 30% of time is warning
                            # Just show warning effect, don't move yet
                            pass
                        # Charging toward player
                        elif charge_progress < 1.0:
                            # Calculate direction to target
                            dx = self.charge_target_x - self.rect.x
                            dy = self.charge_target_y - self.rect.y
                            distance = math.sqrt(dx*dx + dy*dy)
                            
                            # Accelerating charge speed
                            actual_charge_speed = self.charge_speed * min(2.0, (charge_progress - 0.3) * 3)
                            
                            if distance > 10:
                                # Move toward target at charge speed
                                self.rect.x += dx * actual_charge_speed / distance
                                self.rect.y += dy * actual_charge_speed / distance
                        else:
                            # Charge complete, start retreat
                            self.charge_retreat = True
                            self.charge_retreat_time = now
                            
                            # Store original position to return to
                            self.original_x = SCREEN_WIDTH - self.battle_distance - self.rect.width
                            self.original_y = self.rect.centery
                    else:
                        # Retreating after charge
                        retreat_progress = (now - self.charge_retreat_time) / (self.charge_duration * 0.7)
                        
                        if retreat_progress < 1.0:
                            # Move back to original position
                            dx = self.original_x - self.rect.x
                            dy = self.original_y - self.rect.y
                            distance = math.sqrt(dx*dx + dy*dy)
                            
                            if distance > 10:
                                # Move toward original position with smooth deceleration
                                retreat_speed = self.charge_speed * 0.7 * (1 - retreat_progress)
                                self.rect.x += dx * retreat_speed / distance
                                self.rect.y += dy * retreat_speed / distance
                        else:
                            # Retreat complete
                            self.is_charging = False
                            self.charge_retreat = False
                            self.movement_paused = False
                            self.charge_cooldown = 3000  # 3 seconds cooldown
                            
                            # Reset bullet management to ensure bullets continue to appear
                            self.last_shot = now - self.shoot_delay + 100  # Force a shot soon after charge
                            
                            # Move to next attack pattern
                            self.current_pattern_index = (self.current_pattern_index + 1) % len(self.bullet_patterns)
                            self.attack_pattern = self.bullet_patterns[self.current_pattern_index]
                
                # Handle hover position reached for laser attack
                if self.attack_pattern == "laser" and self.hover_position is None and not self.is_aiming and not self.laser_charging and not self.laser_firing:
                    # Start aiming sequence when in position
                    self.is_aiming = True
                    self.aiming_time = now
                    self.movement_paused = True  # Pause movement during aiming
                
                # Handle aiming for laser
                if self.is_aiming:
                    # Update aiming
                    aim_progress = (now - self.aiming_time) / self.aiming_duration
                    
                    # Update target position continuously during aiming
                    if self.player_ref:
                        self.laser_target_y = self.player_ref.rect.centery
                    
                    # Check if aiming is complete
                    if aim_progress >= 1.0:
                        self.is_aiming = False
                        # Start laser charging sequence
                        self.laser_charging = True
                        self.laser_charge_time = now
                        self.laser_width = 2  # Initial width
                        
                        # Lock in the final target position
                        if self.player_ref:
                            self.laser_target_y = self.player_ref.rect.centery
                        else:
                            # Fallback to random position if no player reference
                            self.laser_target_y = random.randint(100, SCREEN_HEIGHT - 100)
                
                # Handle laser attack
                if self.laser_charging:
                    # Update laser charging
                    charge_progress = (now - self.laser_charge_time) / self.laser_charge_duration
                    
                    # Grow laser width during charging
                    self.laser_width = int(2 + charge_progress * 10)  # Grows from 2 to 12
                    
                    # Play charging sound occasionally
                    if random.random() < 0.05:  # 5% chance per frame
                        self.sound_manager.play_sound('shoot')
                    
                    # Check if charging is complete
                    if charge_progress >= 1.0:
                        self.laser_charging = False
                        self.laser_firing = True
                        self.laser_fire_time = now
                        self.laser_width = 15  # Full width when firing
                        # Play laser fire sound
                        self.sound_manager.play_sound('explosion')
                
                elif self.laser_firing:
                    # Update laser firing
                    fire_progress = (now - self.laser_fire_time) / self.laser_fire_duration
                    
                    # Check if firing is complete
                    if fire_progress >= 1.0:
                        self.laser_firing = False
                        self.movement_paused = False  # Resume movement after firing
                        
                        # Return to preferred distance
                        self.hover_position = (
                            self.preferred_distance,
                            self.figure8_center_y
                        )
                        self.hover_timer = 0
                        self.hover_duration = 60
                        self.current_tactic = "ranged"
                        
                        # Move to next attack pattern
                        self.current_pattern_index = (self.current_pattern_index + 1) % len(self.bullet_patterns)
                        self.attack_pattern = self.bullet_patterns[self.current_pattern_index]
                        self.pattern_shots = 0
            
            # Shoot bullets based on current attack pattern
            self.shoot()
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Update bullets
        self.bullets.update()
        
        return False  # Not finished dying
    
    def shoot(self):
        now = pygame.time.get_ticks()
        
        # Skip shooting if laser is active or charging
        if self.boss_type == 'main' and (self.laser_charging or self.laser_firing or self.is_aiming):
            return
            
        # Skip shooting if charging
        if self.boss_type == 'main' and self.is_charging:
            return
            
        # Force shooting if no bullets are active for too long
        if self.boss_type == 'main' and len(self.bullets) == 0 and now - self.last_shot > 1500:
            self.last_shot = now - self.shoot_delay  # Force immediate shot
            
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            if self.boss_type == 'mini':
                # Mini boss has different attack patterns
                if self.attack_pattern == "spread":
                    # Spread shot - 3 bullets in a fan pattern
                    bullet1 = BossBullet(self.rect.left, self.rect.centery, self.bullet_speed, self.bullet_damage)
                    bullet2 = BossBullet(self.rect.left, self.rect.centery - 10, self.bullet_speed, self.bullet_damage)
                    bullet3 = BossBullet(self.rect.left, self.rect.centery + 10, self.bullet_speed, self.bullet_damage)
                    
                    # Add vertical velocity to create a spread pattern
                    bullet2.vy = -1.5
                    bullet3.vy = 1.5
                    
                    self.bullets.add(bullet1, bullet2, bullet3)
                
                elif self.attack_pattern == "aimed":
                    # Aimed shot - try to predict player position
                    # This would normally use the player's position, but we'll simulate it
                    target_y = random.randint(100, SCREEN_HEIGHT - 100)
                    
                    # Calculate angle to target
                    dx = -200  # Assume player is 200 pixels to the left
                    dy = target_y - self.rect.centery
                    angle = math.atan2(dy, dx)
                    
                    # Create bullet with calculated velocity
                    speed = abs(self.bullet_speed)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    
                    bullet = BossBullet(self.rect.left, self.rect.centery, vx, self.bullet_damage)
                    bullet.vy = vy
                    self.bullets.add(bullet)
                
                elif self.attack_pattern == "barrage":
                    # Barrage - multiple bullets in quick succession
                    # We'll create 5 bullets with slight variations
                    for i in range(5):
                        offset_y = random.randint(-20, 20)
                        bullet = BossBullet(
                            self.rect.left, 
                            self.rect.centery + offset_y, 
                            self.bullet_speed * random.uniform(0.9, 1.1),  # Slight speed variation
                            self.bullet_damage
                        )
                        bullet.vy = random.uniform(-0.5, 0.5)  # Slight vertical drift
                        self.bullets.add(bullet)
            
            else:  # Main boss
                # Main boss has different attack patterns based on phase
                if self.attack_pattern == "spread":
                    # Spread shot - number of bullets depends on phase
                    num_bullets = 3 + (self.attack_phase - 1)  # 3, 4, or 5 bullets
                    
                    # Calculate angles for a forward-facing spread
                    for i in range(num_bullets):
                        # Calculate angle for this bullet (all horizontal or slightly angled)
                        angle_offset = 10  # Maximum angle offset in degrees
                        angle_rad = math.radians(180 + (angle_offset * (i - (num_bullets-1)/2)))
                        
                        # Calculate velocity components
                        speed = abs(self.bullet_speed)
                        vx = math.cos(angle_rad) * speed
                        vy = math.sin(angle_rad) * speed * 0.2  # Reduce vertical component
                        
                        # Create bullet
                        bullet = BossBullet(
                            self.rect.left, 
                            self.rect.centery + random.randint(-5, 5), 
                            vx, 
                            self.bullet_damage
                        )
                        bullet.vy = vy
                        
                        # Set color based on phase
                        if self.attack_phase == 2:
                            bullet.color_shift = (0, 100, 255)  # Blue tint for phase 2
                        elif self.attack_phase == 3:
                            bullet.color_shift = (255, 0, 100)  # Purple tint for phase 3
                            
                        self.bullets.add(bullet)
                
                elif self.attack_pattern == "focused":
                    # Focused attack - straight line of bullets aimed at player
                    num_bullets = 2 + self.attack_phase  # 3, 4, or 5 bullets
                    
                    # Calculate aim direction if player reference exists
                    target_y = self.rect.centery
                    if self.player_ref:
                        target_y = self.player_ref.rect.centery
                    
                    # Calculate angle to target
                    dx = -200  # Aim ahead of the player
                    dy = target_y - self.rect.centery
                    angle = math.atan2(dy, dx)
                    
                    for i in range(num_bullets):
                        # Create bullet with slight offset
                        offset_x = -i*10  # Staggered horizontally
                        offset_y = 0
                        
                        # Calculate velocity components
                        speed = abs(self.bullet_speed) * 1.2  # Faster than normal
                        vx = math.cos(angle) * speed
                        vy = math.sin(angle) * speed
                        
                        bullet = BossBullet(
                            self.rect.left + offset_x,
                            self.rect.centery + offset_y,
                            vx,
                            self.bullet_damage
                        )
                        
                        # Set color based on phase
                        if self.attack_phase == 2:
                            bullet.color_shift = (0, 255, 100)  # Green tint for phase 2
                        elif self.attack_phase == 3:
                            bullet.color_shift = (255, 100, 0)  # Orange tint for phase 3
                            
                        self.bullets.add(bullet)
                
                # Increment pattern shots counter (except for laser and charge patterns)
                if self.attack_pattern not in ["laser", "charge"]:
                    self.pattern_shots += 1
            
            # Play sound
            self.sound_manager.play_sound('shoot')
    
    def take_damage(self, damage=1):
        """Handle boss taking damage."""
        # Prevent damage during entrance
        if not self.entry_complete:
            return False
            
        self.health -= damage
        self.sound_manager.play_sound('explosion')
        
        # Update attack phase based on health percentage
        health_percent = self.health / self.max_health
        
        if self.boss_type == 'mini':
            if health_percent <= 0.33 and self.attack_phase < 3:
                # Phase 3: Most aggressive
                self.attack_phase = 3
                self.shoot_delay = 700  # Faster shooting
                self.attack_change_delay = 3000  # Faster pattern changes
                self.amplitude = 150  # Wider movement
                self.frequency = 0.03  # Faster movement
                
            elif health_percent <= 0.66 and self.attack_phase < 2:
                # Phase 2: More aggressive
                self.attack_phase = 2
                self.shoot_delay = 850  # Faster shooting
                self.attack_change_delay = 4000  # Faster pattern changes
        
        elif self.boss_type == 'main':
            if health_percent <= 0.33 and self.attack_phase < 3:
                # Phase 3: Most aggressive
                self.attack_phase = 3
                self.shoot_delay = 1000  # Faster shooting but still nerfed from original
                self.figure8_amplitude = 150  # Wider movement
                self.figure8_frequency = 0.025  # Faster movement
                self.max_pattern_shots = 2  # Change patterns more frequently
                
                # Play phase transition sound
                self.sound_manager.play_sound('explosion')
                
            elif health_percent <= 0.66 and self.attack_phase < 2:
                # Phase 2: More aggressive
                self.attack_phase = 2
                self.shoot_delay = 1100  # Faster shooting but still nerfed from original
                self.figure8_amplitude = 130  # Wider movement
                self.max_pattern_shots = 3  # Change patterns more frequently
                
                # Play phase transition sound
                self.sound_manager.play_sound('explosion')
        
        # Check if boss is defeated
        if self.health <= 0 and not self.dying:
            self.destroy()
            return True
        return False
    
    def destroy(self):
        """Handle boss destruction with animation."""
        # Set dying state
        self.dying = True
        self.death_animation_start = pygame.time.get_ticks()
        self.explosion_particles = []
        
        # Create explosion particles
        for _ in range(20):
            particle = {
                'x': self.rect.centerx + random.randint(-self.rect.width//2, self.rect.width//2),
                'y': self.rect.centery + random.randint(-self.rect.height//2, self.rect.height//2),
                'size': random.randint(5, 15),
                'speed_x': random.uniform(-3, 3),
                'speed_y': random.uniform(-3, 3),
                'color': random.choice([(255, 100, 0), (255, 200, 0), (255, 50, 0), (200, 0, 0)]),
                'lifetime': random.randint(30, 60)  # frames
            }
            self.explosion_particles.append(particle)
        
        # Play explosion sound
        self.sound_manager.play_sound('explosion')
        
    def update_death_animation(self):
        """Update the death animation."""
        # Update explosion particles
        for particle in self.explosion_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
        
        # Check if animation is complete
        current_time = pygame.time.get_ticks()
        if current_time - self.death_animation_start > self.death_animation_duration:
            # Clear any remaining bullets
            for bullet in list(self.bullets):
                bullet.kill()
            self.bullets.empty()
            return True  # Animation complete, boss can be removed
        return False
    
    def draw_health_bar(self, surface):
        """Draw the boss health bar at the top of the screen."""
        # Don't draw health bar if dying
        if self.dying:
            return
            
        # Position the health bar lower to avoid overlap with chapter header and time
        bar_x = (SCREEN_WIDTH - self.health_bar_bg.get_width()) // 2
        bar_y = 70  # Moved down from 10 to 70
        
        # Draw the background
        surface.blit(self.health_bar_bg, (bar_x, bar_y))
        
        # Calculate the width of the fill based on current health
        fill_width = int((self.health / self.max_health) * (self.health_bar_bg.get_width() - 2))
        
        # Create a subsurface of the fill image with the correct width
        if fill_width > 0:
            fill_rect = pygame.Rect(0, 0, fill_width, self.health_bar_fill.get_height())
            fill_surface = self.health_bar_fill.subsurface(fill_rect)
            surface.blit(fill_surface, (bar_x + 1, bar_y + 1))
        
        # Draw the boss name and health
        font = pygame.font.SysFont('Arial', 16)
        text = font.render(f"{self.name}: {self.health}/{self.max_health}", True, (255, 255, 255))
        surface.blit(text, (bar_x + (self.health_bar_bg.get_width() - text.get_width()) // 2, bar_y + 16))
    
    def draw(self, surface):
        """Draw the boss and its bullets."""
        if self.dying:
            self.draw_death_animation(surface)
            return
            
        # Draw charge effect if charging
        if self.boss_type == 'main' and self.is_charging and not self.charge_retreat:
            # Draw charge trail with improved visuals
            for i in range(8):  # More trail segments
                alpha = 180 - i * 20
                
                # Pulse the trail color
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
                r = 255
                g = int(100 + 50 * pulse)
                b = int(50 * pulse)
                
                trail_color = (r, g, b, alpha)
                trail_rect = self.rect.copy()
                trail_rect.x += i * 8  # Trail behind the boss
                
                # Create a surface for the trail
                trail_surface = pygame.Surface((trail_rect.width, trail_rect.height), pygame.SRCALPHA)
                trail_surface.fill(trail_color)
                
                # Draw trail
                surface.blit(trail_surface, trail_rect)
                
            # Draw charge warning
            font = pygame.font.SysFont('Arial', 16)
            warning_text = font.render("CHARGING!", True, (255, 50, 50))
            surface.blit(warning_text, (self.rect.centerx - warning_text.get_width()//2, self.rect.top - 25))
        
        # Draw the boss
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Draw bullets with custom draw method
        for bullet in self.bullets:
            if hasattr(bullet, 'draw'):
                bullet.draw(surface)
            else:
                surface.blit(bullet.image, bullet.rect)
        
        # Draw laser if active (draw last to ensure it's on top)
        if self.boss_type == 'main':
            if self.is_aiming:
                self.draw_laser_warning(surface)
            elif self.laser_charging:
                self.draw_laser_warning(surface)
            elif self.laser_firing:
                self.draw_laser_beam(surface)
        
        # Draw health bar if not dying
        if not self.dying:
            self.draw_health_bar(surface)
    
    def draw_laser_warning(self, surface):
        """Draw the laser warning indicator."""
        # Calculate warning line properties
        now = pygame.time.get_ticks()
        
        # If in aiming mode, draw a targeting reticle
        if self.is_aiming:
            aim_progress = (now - self.aiming_time) / self.aiming_duration
            
            # Target position (player's position if available)
            target_y = self.rect.centery
            if self.player_ref:
                target_y = self.player_ref.rect.centery
            
            # Draw targeting reticle
            reticle_radius = 20 + int(10 * math.sin(aim_progress * 10))
            reticle_color = (255, 0, 0, 150)
            
            # Draw outer circle
            pygame.draw.circle(surface, reticle_color, (self.rect.left - 20, target_y), reticle_radius, 2)
            
            # Draw crosshairs
            pygame.draw.line(surface, reticle_color, 
                            (self.rect.left - 20 - reticle_radius, target_y), 
                            (self.rect.left - 20 + reticle_radius, target_y), 2)
            pygame.draw.line(surface, reticle_color, 
                            (self.rect.left - 20, target_y - reticle_radius), 
                            (self.rect.left - 20, target_y + reticle_radius), 2)
            
            # Draw text warning
            font = pygame.font.SysFont('Arial', 16)
            warning_text = font.render("LASER CHARGING", True, (255, 0, 0))
            surface.blit(warning_text, (self.rect.left - 100, target_y - 40))
            
            return
        
        # For charging laser, draw warning line
        charge_progress = (now - self.laser_charge_time) / self.laser_charge_duration
        
        # Warning line color pulses from white to red
        pulse_rate = 10  # Higher value = faster pulse
        pulse_factor = (math.sin(charge_progress * pulse_rate) + 1) / 2  # 0 to 1
        
        r = 255
        g = int(255 * (1 - pulse_factor))
        b = int(100 * (1 - pulse_factor))
        
        # Draw warning line
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Draw dashed line with increasing width as charging progresses
        dash_length = 10
        gap_length = 5
        x = start_pos[0]
        
        # Width increases with charge progress
        warning_width = int(2 + charge_progress * 10)
        
        while x > end_pos[0]:
            # Calculate dash start and end
            dash_start = (x, start_pos[1])
            dash_end = (max(x - dash_length, end_pos[0]), start_pos[1])
            
            # Draw dash
            pygame.draw.line(surface, (r, g, b), dash_start, dash_end, warning_width)
            
            # Move to next dash position
            x -= (dash_length + gap_length)
        
        # Draw warning text that pulses
        font = pygame.font.SysFont('Arial', 18)
        warning_text = font.render("!!! LASER IMMINENT !!!", True, (r, g, b))
        text_x = SCREEN_WIDTH // 2 - warning_text.get_width() // 2
        text_y = self.laser_target_y - 40
        surface.blit(warning_text, (text_x, text_y))
        
        # Draw warning indicators at both ends of the laser path
        indicator_radius = 10 + int(5 * pulse_factor)
        pygame.draw.circle(surface, (r, g, b), (0, self.laser_target_y), indicator_radius, 2)
        pygame.draw.circle(surface, (r, g, b), (self.rect.left, self.laser_target_y), indicator_radius, 2)
    
    def draw_laser_beam(self, surface):
        """Draw the laser beam."""
        # Laser beam properties - start from the boss's left side
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Draw main beam with pulsing effect
        now = pygame.time.get_ticks()
        pulse_factor = (math.sin(now * 0.01) + 1) / 2  # 0 to 1
        
        # Pulse the width slightly
        pulse_width = int(self.laser_width * (0.9 + 0.2 * pulse_factor))
        
        # Draw multiple layers for a more intense effect
        # Outer glow (semi-transparent)
        for i in range(3):
            glow_width = pulse_width + i * 4
            alpha = 100 - i * 30
            glow_color = (255, 100, 100, alpha)
            
            # Draw wider lines for glow effect
            pygame.draw.line(surface, glow_color, start_pos, end_pos, glow_width)
        
        # Main beam (solid)
        pygame.draw.line(surface, self.laser_color, start_pos, end_pos, pulse_width)
        
        # Bright core
        core_color = (255, 200, 200)
        pygame.draw.line(surface, core_color, start_pos, end_pos, pulse_width // 3)
        
        # Add impact effect at the left edge
        impact_x = 0
        impact_y = self.laser_target_y
        impact_radius = pulse_width + int(5 * pulse_factor)
        
        # Draw impact circles
        pygame.draw.circle(surface, (255, 200, 200), (impact_x, impact_y), impact_radius // 2)
        pygame.draw.circle(surface, (255, 100, 100, 150), (impact_x, impact_y), impact_radius)
        
        # Add small particles around the impact point
        for _ in range(3):
            particle_x = impact_x + random.randint(-impact_radius, impact_radius//2)
            particle_y = impact_y + random.randint(-impact_radius, impact_radius)
            particle_size = random.randint(1, 3)
            pygame.draw.circle(surface, (255, 200, 200), (particle_x, particle_y), particle_size)
            
    def draw_death_animation(self, surface):
        """Draw the death animation."""
        # Draw explosion particles
        for particle in self.explosion_particles:
            pygame.draw.circle(
                surface, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
            
        # Draw fading boss sprite
        alpha = 255 * (1 - (pygame.time.get_ticks() - self.death_animation_start) / self.death_animation_duration)
        if alpha > 0:
            # Create a copy of the image with transparency
            temp_image = self.image.copy()
            temp_image.set_alpha(int(alpha))
            surface.blit(temp_image, self.rect)


class BossBullet(pygame.sprite.Sprite):
    """Bullets fired by bosses."""
    def __init__(self, x, y, speed, damage):
        super().__init__()
        
        # Create a more interesting bullet shape
        self.width = 12
        self.height = 6
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Color properties
        self.color_shift = None  # Can be set to tint the bullet
        self.create_bullet_image()
        
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        
        # Store speed as vx for horizontal movement
        if isinstance(speed, (int, float)):
            self.vx = speed
            self.vy = 0
        else:
            self.vx = speed  # Already calculated as a vector
            self.vy = 0
            
        self.damage = damage
        
        # Create a smaller hitbox for more precise collision detection
        self.hitbox = pygame.Rect(0, 0, self.width-2, self.height-1)  # 2px smaller on width, 1px smaller on height
        self.hitbox.center = self.rect.center
        
        # Add trail effect properties
        self.trail = []
        self.max_trail_length = 5
        
        # Time tracking for visual effects
        self.creation_time = pygame.time.get_ticks()
    
    def create_bullet_image(self):
        """Create the bullet image with optional color shift."""
        # Clear the image
        self.image.fill((0, 0, 0, 0))
        
        # Draw a gradient bullet with a bright core
        for i in range(self.width):
            # Calculate color intensity based on position
            intensity = 255 - int(200 * (i / self.width))
            
            # Apply color shift if specified
            if self.color_shift:
                r = min(255, intensity + self.color_shift[0] // 3)
                g = min(255, intensity + self.color_shift[1] // 3)
                b = min(255, intensity + self.color_shift[2] // 3)
                color = (r, g, b)
            else:
                color = (255, intensity, intensity)  # Red to bright red gradient
            
            # Draw a vertical line at position i
            pygame.draw.line(self.image, color, (i, 0), (i, self.height-1), 1)
        
        # Add a bright core
        core_color = (255, 255, 200)
        if self.color_shift:
            # Mix the core color with the color shift
            core_color = (
                min(255, 200 + self.color_shift[0] // 4),
                min(255, 200 + self.color_shift[1] // 4),
                min(255, 200 + self.color_shift[2] // 4)
            )
            
        pygame.draw.rect(self.image, core_color, (0, self.height//4, self.width//2, self.height//2))
    
    def update(self):
        # Store current position for trail
        self.trail.append((self.rect.centerx, self.rect.centery))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Update position
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Remove if off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
    
    def draw(self, surface):
        # Draw trail
        for i, (x, y) in enumerate(self.trail):
            # Calculate alpha based on position in trail
            alpha = int(150 * (i / len(self.trail)))
            size = int(self.height * 0.8 * (i / len(self.trail)))
            
            # Get trail color based on bullet color
            if self.color_shift:
                trail_color = (
                    min(255, self.color_shift[0]),
                    min(255, self.color_shift[1]),
                    min(255, self.color_shift[2]),
                    alpha
                )
            else:
                trail_color = (255, 100, 100, alpha)
            
            # Draw trail segment
            pygame.draw.circle(surface, trail_color, (int(x), int(y)), max(1, size))
        
        # Draw bullet
        surface.blit(self.image, self.rect)
