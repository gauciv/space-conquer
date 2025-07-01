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
        
        # Force initialization of critical attributes
        self.entry_complete = False
        self.movement_timer = 0
        self.dying = False
        self.attack_phase = 1
        self.pattern_shots = 0
        self.max_pattern_shots = 3
        
        # Set image based on boss type
        if boss_type == 'mini':
            original_image = asset_loader.get_image('mini_boss')
            self.name = "Vanguard"
            self.max_health = 50  # Doubled from 25 to 50
            self.health = self.max_health
            self.speed = 2.5  # Increased from 2 to 2.5
            self.shoot_delay = 800  # Increased to 800ms for burst pattern
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
            self.attack_pattern = "burst"  # Start with burst
            self.attack_timer = 0
            self.attack_change_delay = 5000  # Change attack pattern every 5 seconds
            self.sniper_cooldown = 0
            self.sniper_ready = True
            self.sniper_interval = 2200  # ms between sniper shots
            self.sniper_bullet_speed = -18  # Fast leftward
            self.sniper_bullet_color = (100, 255, 255)
            self.sniper_bullet_width = 6
            self.sniper_bullet_height = 2
            self.sniper_warning_time = 700  # ms telegraph before shot
            self.sniper_warning_timer = 0
            self.sniper_target_y = 0
            self.sniper_in_warning = False
            
            # Burst firing pattern
            self.burst_mode = True
            
            # Laser attack properties
            self.laser_charging = False
            self.laser_firing = False
            self.laser_cooldown = 5000  # 5 seconds between laser attacks
            self.laser_charge_time = 0
            self.laser_fire_time = 0
            self.laser_charge_duration = 1000  # 1 second to charge
            self.laser_fire_duration = 1500  # 1.5 seconds of firing
            self.laser_width = 20  # Thick laser
            self.laser_target_y = 0
            self.laser_damage = 1
            self.last_laser_time = 0
            self.burst_shots = 0
            self.max_burst_shots = 4  # Increased from 3 to 4
            self.burst_delay = 150  # Reduced from 200 to 150ms between shots
            self.burst_cooldown = 1500  # Reduced from 2000 to 1500ms
            self.in_burst = False
            self.last_burst_shot = 0
            self.burst_finished_time = 0
            self.player_ref = None  # Will be set by game manager
            

            
            # Weak point system
            self.has_weak_point = True
            self.weak_point_active = False
            self.weak_point_cooldown = 0
            self.weak_point_duration = 0
            self.weak_point_position = (0, 0)  # Will be updated during gameplay
            self.weak_point_radius = 15
            
        else:  # main boss
            original_image = asset_loader.get_image('main_boss')
            self.name = "Dreadnought"
            self.max_health = 150  # Increased from 100 to 150 for more durability
            self.health = self.max_health
            self.speed = 2.0  # Increased from 1.5 to 2.0 for faster movement
            self.shoot_delay = 1000  # Reduced from 1200 to 1000 for more frequent attacks
            self.bullet_speed = -10  # Increased from -8 to -10 for faster bullets
            self.bullet_damage = 2
            self.score_value = 2000  # Increased from 1500 to 2000
            self.movement_pattern = "multistage"  # Changed from "complex" to "multistage"
            self.battle_distance = 15  # Distance from right edge during battle (reduced to 15px)
            
            # Scale the main boss to 0.975x size (1.5 * 0.65 = 0.975, reducing by 35% from the 1.5x size)
            new_width = int(original_image.get_width() * 0.975)
            new_height = int(original_image.get_height() * 0.975)
            
            # Main boss specific attack patterns
            self.attack_phase = 1  # Current attack phase (1-3)
            self.attack_pattern = "spread"  # Initial attack pattern
            self.pattern_shots = 0  # Ensure pattern shots is initialized
            self.bullet_patterns = ["spread", "focused", "barrage"]  # Simplified patterns
            self.attack_timer = 0
            self.attack_change_delay = 6000  # Change attack pattern every 6 seconds
            self.special_attack_cooldown = 0
            self.special_attack_duration = 0
            self.is_charging = False
            self.charge_duration = 0
            self.charge_direction = 0
            # Bullet patterns already initialized in constructor
            self.current_pattern_index = 0
            
            # Charge attack properties
            self.is_charging = False
            self.charge_start_time = 0
            self.charge_duration = 800  # Reduced from 1000 to 800ms for faster charge
            self.charge_cooldown = 0
            self.charge_target_x = 0
            self.charge_target_y = 0
            self.charge_speed = 15  # Increased from 12 to 15 for faster charge
            self.charge_retreat = False
            self.charge_retreat_time = 0
            
            # Shield system
            self.has_shield = True
            self.shield_health = 50  # Additional 50 health in shield
            self.shield_active = True
            self.shield_regen_rate = 0.05  # Shield regenerates slowly
            self.shield_regen_delay = 5000  # 5 seconds delay before shield starts regenerating
            self.last_shield_hit = 0
            
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
            self.movement_timer = 0  # Initialize movement timer for main boss
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
        
        # Create a custom hitbox based on boss type
        if boss_type == 'mini':
            # Mini-boss has a smaller hitbox (75% of sprite size) for better gameplay
            hitbox_width = int(self.rect.width * 0.75)
            hitbox_height = int(self.rect.height * 0.75)
        else:
            # Main boss has a standard hitbox (85% of sprite size)
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
        self.last_shot = pygame.time.get_ticks()  # Time in milliseconds
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
        self.movement_timer = 0  # Timer for movement calculations
        
        # Death animation properties
        self.dying = False
        self.death_animation_start = 0
        self.death_animation_duration = 1500  # 1.5 seconds
        self.explosion_particles = []
        
        # Visual effect properties
        self.flash_effect = 0  # Used for visual feedback
        self.hit_flash = 0  # Flash when taking damage
        
        self.dash_trail = []  # Store previous positions for dash trail
        self.dash_trail_length = 6  # Number of trail segments
    
    def update(self):
        """Update the boss state."""
        # Boss update called
        
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
            print(f"Boss entry: x={self.rect.x}, right={self.rect.right}, target={SCREEN_WIDTH - self.battle_distance}")
            if self.rect.right < SCREEN_WIDTH - self.battle_distance:
                self.entry_complete = True
                self.last_shot = now  # Reset shot timer when entry is complete
                print(f"Boss entry complete: type={self.boss_type}, pattern={self.movement_pattern}, entry_complete={self.entry_complete}")
                # Force initial position
                if self.boss_type == 'main':
                    self.rect.x = SCREEN_WIDTH - self.battle_distance - self.rect.width
                    # Initialize movement timer to ensure it starts moving
                    self.movement_timer = 0
                    self.pattern_shots = 0
                    print(f"Main boss initialized: pos=({self.rect.x}, {self.rect.y}), timer={self.movement_timer}")
        else:
        # Debug entry_complete status
            if self.boss_type == 'main' and self.movement_timer % 60 == 0:
                print(f"Main boss status: entry_complete={self.entry_complete}, pos=({self.rect.x}, {self.rect.y}), shoot_delay={self.shoot_delay}")
            # Ensure movement_timer is initialized for main boss
            if self.boss_type == 'main' and not hasattr(self, 'movement_timer'):
                self.movement_timer = 0
                print(f"Initialized movement_timer for main boss")
                
            # Debug: Print current state
            if self.boss_type == 'main' and self.movement_timer % 60 == 0:
                print(f"Main boss state: pattern={self.movement_pattern}, timer={self.movement_timer}")
                
            # Ensure bullets are properly managed
            # Remove bullets that have gone off-screen
            for bullet in list(self.bullets):
                if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH or \
                   bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT:
                    bullet.kill()
            
            # Force shooting if no bullets are active and not in special attack
            # Force shooting if no bullets and entry is complete
            if len(self.bullets) == 0 and self.entry_complete:
                self.last_shot = now - self.shoot_delay  # Force immediate shot
            
            # Different movement patterns based on boss type
            print(f"Checking movement pattern: {self.movement_pattern}")
            if self.movement_pattern == "advanced":
                print(f"Using advanced movement pattern")
                # Advanced movement for mini-boss
                self.movement_timer += 1
                
                # Only apply sine wave movement if not dashing (for mini-boss)
                if self.boss_type == 'mini' and hasattr(self, 'is_dashing') and self.is_dashing:
                    # Skip sine wave movement during dash
                    pass
                else:
                    # Vertical sine wave movement
                    base_y = self.center_y + math.sin(self.movement_timer * 0.03) * self.amplitude
                    self.rect.centery = base_y
                    # Add horizontal movement
                    base_x = SCREEN_WIDTH - self.battle_distance - self.rect.width
                    horizontal_offset = math.sin(self.movement_timer * 0.02) * 40
                    self.rect.x = base_x + horizontal_offset
                
                # Add phase-specific movement modifications
                if self.attack_phase >= 2 and hasattr(self, 'is_dashing') and not self.is_dashing:
                    # Phase 2+: Add occasional quick movements
                    if self.movement_timer % 90 == 0:  # Every 1.5 seconds
                        self.rect.y += random.randint(-40, 40)
                        self.rect.x += random.randint(-20, 20)
                
                # For mini-boss, handle attack pattern transitions
                if self.boss_type == 'mini':
                    now = pygame.time.get_ticks()
                    self.attack_timer += 16
                    # Alternate between burst and sniper
                    if self.attack_pattern == "burst":
                        # After a burst, switch to sniper
                        if not self.in_burst and now - self.burst_finished_time > self.burst_cooldown:
                            self.attack_pattern = "sniper"
                            self.sniper_in_warning = True
                            self.sniper_warning_timer = self.sniper_warning_time
                            # Target player y for sniper shot
                            if self.player_ref and hasattr(self.player_ref, 'rect'):
                                self.sniper_target_y = self.player_ref.rect.centery
                            else:
                                self.sniper_target_y = self.rect.centery
                    elif self.attack_pattern == "sniper":
                        if self.sniper_in_warning:
                            self.sniper_warning_timer -= 16
                            if self.sniper_warning_timer <= 0:
                                # Fire sniper shot
                                bullet = BossBullet(
                                    0, 0, 0, 0)  # placeholder, see below
                                bullet = BossBullet(
                                    self.rect.left, self.sniper_target_y, self.sniper_bullet_speed, self.bullet_damage * 2)
                                bullet.image = pygame.Surface((self.sniper_bullet_width, self.sniper_bullet_height), pygame.SRCALPHA)
                                bullet.image.fill(self.sniper_bullet_color)
                                bullet.rect = bullet.image.get_rect()
                                bullet.rect.left = self.rect.left
                                bullet.rect.centery = self.sniper_target_y
                                bullet.hitbox = pygame.Rect(0, 0, self.sniper_bullet_width, self.sniper_bullet_height)
                                bullet.hitbox.center = bullet.rect.center
                                bullet.is_sniper = True
                                self.bullets.add(bullet)
                                self.sound_manager.play_sound('shoot')
                                self.sniper_in_warning = False
                                self.sniper_cooldown = self.sniper_interval
                        else:
                            self.sniper_cooldown -= 16
                            if self.sniper_cooldown <= 0:
                                self.attack_pattern = "burst"
                    # Burst logic is handled in shoot()
                
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
                print(f"Using multistage movement pattern")
                # Multistage movement pattern for main boss
                now = pygame.time.get_ticks()
                
                # Force initialization of critical attributes
                if not hasattr(self, 'pattern_shots'):
                    self.pattern_shots = 0
                if not hasattr(self, 'attack_pattern'):
                    self.attack_pattern = "spread"
                
                # Ensure we're actually moving and attacking
                self.movement_timer += 1
                print(f"Movement timer incremented to: {self.movement_timer}")
                
                # SIMPLIFIED MOVEMENT - Always move regardless of other conditions
                t = self.movement_timer * 0.015  # Slower movement
                
                # Calculate base position
                base_x = SCREEN_WIDTH - self.battle_distance - self.rect.width
                base_y = SCREEN_HEIGHT // 2
                
                # Apply movement pattern
                new_x = base_x + math.sin(t) * 40
                new_y = base_y + math.sin(t * 1.5) * 80
                
                # Debug movement calculation
                if self.movement_timer % 60 == 0:  # Print every second
                    print(f"Boss movement: timer={self.movement_timer}, t={t:.2f}, pos=({new_x:.1f}, {new_y:.1f})")
                
                # Apply new position
                self.rect.x = int(new_x)
                self.rect.y = int(new_y)
                print(f"Applied new position: ({self.rect.x}, {self.rect.y})")
                
                # Simplified attack pattern management - just shoot regularly
                # No complex pattern switching for now
                print(f"About to call shoot method")
                
                # Debug bullets
                print(f"Boss has {len(self.bullets)} bullets")
                
                # Shoot bullets based on current attack pattern
                # Ready to shoot
                try:
                    print(f"Calling shoot method for {self.boss_type} boss")
                    self.shoot()
                    print(f"After shoot, boss has {len(self.bullets)} bullets")
                except Exception as e:
                    print(f"Error in shoot method: {e}")
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Update bullets
        if len(self.bullets) > 0:
            print(f"Updating {len(self.bullets)} bullets")
        self.bullets.update()
        
        return False  # Not finished dying
    
    def shoot(self):
        """Shoot bullets."""
        # SUPER SIMPLIFIED SHOOTING - Just create a bullet
        bullet = BossBullet(
            self.rect.left, 
            self.rect.centery, 
            -8,  # Fixed leftward velocity
            2    # Fixed damage
        )
        self.bullets.add(bullet)
        print(f"Created bullet at ({bullet.rect.x}, {bullet.rect.y})")
        
        # Play sound
        self.sound_manager.play_sound('shoot')
    
    def take_damage(self, damage=1, hit_position=None):
        """Handle boss taking damage."""
        print(f"{self.boss_type} boss taking damage: {damage}")
        # Prevent damage during entrance
        if not self.entry_complete:
            return False
            
        # Handle shield for main boss
        if self.boss_type == 'main' and hasattr(self, 'has_shield') and self.has_shield and self.shield_active:
            self.last_shield_hit = pygame.time.get_ticks()
            self.shield_health -= damage
            
            # Visual feedback
            self.hit_flash = 5  # Shorter flash for shield hit
            
            # Shield break
            if self.shield_health <= 0:
                self.shield_active = False
                self.sound_manager.play_sound('explosion')  # Shield break sound
                self.hit_flash = 15  # Longer flash for shield break
                return False  # Shield absorbed all damage
                
            # Shield absorbed damage
            self.sound_manager.play_sound('shoot')  # Lighter sound for shield hit
            return False
            
        # Check for weak point hit for mini-boss
        if self.boss_type == 'mini' and self.has_weak_point and self.weak_point_active and hit_position:
            # Calculate distance to weak point
            weak_point_x = self.rect.centerx + (self.weak_point_position[0] - self.rect.centerx)
            weak_point_y = self.rect.centery + (self.weak_point_position[1] - self.rect.centery)
            
            dx = hit_position[0] - weak_point_x
            dy = hit_position[1] - weak_point_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= self.weak_point_radius:
                # Hit the weak point - triple damage!
                damage *= 3
                # Deactivate weak point
                self.weak_point_active = False
                self.weak_point_cooldown = 5000  # Longer cooldown after being hit
                # Special effect for weak point hit
                self.flash_effect = 20
                # Play critical hit sound
                self.sound_manager.play_sound('explosion')
            
        # Store previous health for phase transition check
        previous_health = self.health
        previous_phase = self.attack_phase
            
        self.health -= damage
        self.sound_manager.play_sound('explosion')
        
        # Set hit flash effect
        self.hit_flash = 10
        
        # Update attack phase based on health percentage
        health_percent = self.health / self.max_health
        
        if self.boss_type == 'mini':
            if health_percent <= 0.33 and self.attack_phase < 3:
                # Phase 3: Most aggressive
                self.attack_phase = 3
                self.shoot_delay = 700  # Faster shooting
                self.attack_change_delay = 3000  # Faster pattern changes
                self.max_pattern_shots = 2  # Change patterns more frequently
                self.amplitude = 150  # Wider movement
                self.frequency = 0.03  # Faster movement
                self.dash_speed = 12  # Faster dashes
                
                # Clear bullets on phase change for cleaner transition
                self.bullets.empty()
                
                # Play phase transition sound
                self.sound_manager.play_sound('explosion')
                
            elif health_percent <= 0.66 and self.attack_phase < 2:
                # Phase 2: More aggressive
                self.attack_phase = 2
                self.shoot_delay = 850  # Faster shooting
                self.attack_change_delay = 4000  # Faster pattern changes
                self.max_pattern_shots = 3  # Change patterns more frequently
                self.dash_speed = 10  # Enable dashing
                
                # Clear bullets on phase change for cleaner transition
                self.bullets.empty()
                
                # Play phase transition sound
                self.sound_manager.play_sound('explosion')
        
        elif self.boss_type == 'main':
            # Check if we're skipping a phase (e.g., from 1 to 3)
            new_phase = 1
            if health_percent <= 0.33:
                new_phase = 3
            elif health_percent <= 0.66:
                new_phase = 2
                
            # If phase changed, apply phase-specific changes
            if new_phase != previous_phase:
                self.attack_phase = new_phase
                
                # Apply phase-specific changes
                if new_phase == 3:
                    # Phase 3: Most aggressive
                    self.shoot_delay = 1000  # Faster shooting but still nerfed from original
                    self.figure8_amplitude = 150  # Wider movement
                    self.figure8_frequency = 0.025  # Faster movement
                    self.max_pattern_shots = 2  # Change patterns more frequently
                    
                    # Play phase transition sound
                    self.sound_manager.play_sound('explosion')
                    
                    # Clear bullets on phase change for cleaner transition
                    self.bullets.empty()
                    
                    # If we skipped phase 2, ensure we get all phase 2 benefits as well
                    if previous_phase == 1:
                        self.figure8_amplitude = 130  # From phase 2
                        self.max_pattern_shots = 3  # From phase 2
                        
                elif new_phase == 2:
                    # Phase 2: More aggressive
                    self.shoot_delay = 1100  # Faster shooting but still nerfed from original
                    self.figure8_amplitude = 130  # Wider movement
                    self.max_pattern_shots = 3  # Change patterns more frequently
                    
                    # Play phase transition sound
                    self.sound_manager.play_sound('explosion')
                    
                    # Clear bullets on phase change for cleaner transition
                    self.bullets.empty()
        
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
        
        # Clear all active bullets immediately
        for bullet in list(self.bullets):
            bullet.kill()
        self.bullets.empty()
        
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
    
    def check_laser_collision(self):
        """Check if the laser beam is colliding with the player and apply damage."""
        if not self.player_ref:
            return
            
        # Create a collision rectangle for the laser beam
        laser_height = self.laser_width  # Use laser width as height for the collision rect
        laser_rect = pygame.Rect(
            0,  # Left edge of screen
            self.laser_target_y - laser_height // 2,
            self.rect.left,  # Extends to the boss's left edge
            laser_height
        )
        
        # Check for collision with player
        if laser_rect.colliderect(self.player_ref.hitbox):
            # Apply damage to player (once per frame)
            self.player_ref.take_damage(self.laser_damage)
            
            # Visual effect for player hit
            if hasattr(self.player_ref, 'hit_flash'):
                self.player_ref.hit_flash = 10
                
            # Play hit sound
            self.sound_manager.play_sound('hit')
            
            # Add knockback effect
            if hasattr(self.player_ref, 'knockback'):
                # Knockback to the left
                self.player_ref.knockback = -5
                
    def get_player_position(self):
        """Safely get player position with fallback values."""
        if self.player_ref and hasattr(self.player_ref, 'rect'):
            return self.player_ref.rect.centerx, self.player_ref.rect.centery
        else:
            # Default to middle of left side of screen if no player reference
            return SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2
            
    def update_player_reference(self, player):
        """Update the player reference safely."""
        self.player_ref = player
        
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
        
        # Draw sniper warning and bullet for mini-boss
        if self.boss_type == 'mini':
            if self.attack_pattern == "sniper" and self.sniper_in_warning:
                # Draw a warning line where the sniper shot will go
                warning_color = (100, 255, 255)
                pulse = 0.5 + 0.5 * abs(math.sin(pygame.time.get_ticks() * 0.01))
                warning_width = int(2 + 2 * pulse)
                start_pos = (self.rect.left, self.sniper_target_y)
                end_pos = (0, self.sniper_target_y)
                pygame.draw.line(surface, warning_color, start_pos, end_pos, warning_width)
                # Draw warning text
                font = pygame.font.SysFont('Arial', 16)
                warn_text = font.render("SNIPER!", True, warning_color)
                surface.blit(warn_text, (self.rect.left - warn_text.get_width() - 10, self.sniper_target_y - 20))
        
        # Create a copy of the image for effects
        display_image = self.image.copy()
        
        # Apply hit flash effect
        if self.hit_flash > 0:
            # Create white flash overlay
            flash_overlay = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            flash_intensity = min(255, self.hit_flash * 25)
            flash_overlay.fill((flash_intensity, flash_intensity, flash_intensity, 0))
            display_image.blit(flash_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Decrease hit flash
            self.hit_flash -= 1
        
        # Apply pattern change flash effect
        if hasattr(self, 'flash_effect') and self.flash_effect > 0:
            # Create colored flash overlay based on attack pattern
            flash_overlay = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            
            if self.attack_pattern == "spread":
                # Red for spread
                flash_color = (255, 100, 100, 0)
            elif self.attack_pattern == "aimed":
                # Blue for aimed
                flash_color = (100, 100, 255, 0)
            else:  # barrage
                # Yellow for barrage
                flash_color = (255, 255, 100, 0)
                
            flash_intensity = min(100, self.flash_effect * 10)
            flash_overlay.fill((flash_color[0], flash_color[1], flash_color[2], flash_intensity))
            display_image.blit(flash_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Decrease flash effect
            self.flash_effect -= 1
        
        # Draw the boss with effects applied
        surface.blit(display_image, self.rect)
        
        # Draw shield for main boss
        if self.boss_type == 'main' and hasattr(self, 'has_shield') and self.has_shield and self.shield_active:
            # Calculate shield size based on health percentage
            shield_health_percent = self.shield_health / 50  # 50 is max shield health
            shield_size = int(max(self.rect.width, self.rect.height) * (1.0 + 0.1 * shield_health_percent))
            
            # Pulsing effect
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
            shield_alpha = int(100 + 50 * pulse)  # 100-150 alpha
            
            # Create shield surface
            shield_surface = pygame.Surface((shield_size, shield_size), pygame.SRCALPHA)
            
            # Draw shield circle
            shield_color = (100, 150, 255, shield_alpha)  # Blue shield
            pygame.draw.circle(shield_surface, shield_color, (shield_size//2, shield_size//2), shield_size//2, 3)
            
            # Draw inner glow
            inner_color = (150, 200, 255, shield_alpha // 2)
            pygame.draw.circle(shield_surface, inner_color, (shield_size//2, shield_size//2), shield_size//2 - 5, 2)
            
            # Position and draw shield
            shield_rect = shield_surface.get_rect(center=self.rect.center)
            surface.blit(shield_surface, shield_rect)
        
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
        
        # Draw mini-boss laser effects
        if self.boss_type == 'mini':
            if self.laser_charging:
                self.draw_mini_laser_warning(surface)
            elif self.laser_firing:
                self.draw_mini_laser_beam(surface)
        
        # Draw weak point for mini-boss
        if self.boss_type == 'mini' and self.has_weak_point and self.weak_point_active:
            # Update weak point position to follow the boss
            weak_point_x = self.rect.centerx + (self.weak_point_position[0] - self.rect.centerx)
            weak_point_y = self.rect.centery + (self.weak_point_position[1] - self.rect.centery)
            
            # Pulsing effect
            now = pygame.time.get_ticks()
            pulse = (math.sin(now * 0.01) + 1) / 2
            
            # Draw outer glow
            glow_radius = int(self.weak_point_radius * (1.2 + 0.3 * pulse))
            pygame.draw.circle(surface, (255, 50, 50, 100), (weak_point_x, weak_point_y), glow_radius)
            
            # Draw weak point
            pygame.draw.circle(surface, (255, 50, 50), (weak_point_x, weak_point_y), self.weak_point_radius)
            
            # Draw inner highlight
            highlight_radius = int(self.weak_point_radius * 0.5)
            pygame.draw.circle(surface, (255, 200, 200), (weak_point_x, weak_point_y), highlight_radius)
            
            # Draw "WEAK POINT" text
            font = pygame.font.SysFont('Arial', 12)
            weak_text = font.render("WEAK POINT", True, (255, 50, 50))
            surface.blit(weak_text, (weak_point_x - weak_text.get_width()//2, weak_point_y - 30))
    
    def draw_mini_laser_warning(self, surface):
        """Draw laser warning for mini-boss."""
        # Draw warning line
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Pulsing red warning line
        pulse = (math.sin(pygame.time.get_ticks() * 0.02) + 1) / 2
        r = 255
        g = int(100 * (1 - pulse))
        b = int(100 * (1 - pulse))
        
        # Draw dashed warning line
        dash_length = 20
        gap_length = 10
        x = start_pos[0]
        warning_width = max(5, int(self.laser_width * 0.5))
        
        while x > end_pos[0]:
            dash_start = (x, start_pos[1])
            dash_end = (max(x - dash_length, end_pos[0]), start_pos[1])
            pygame.draw.line(surface, (r, g, b), dash_start, dash_end, warning_width)
            x -= (dash_length + gap_length)
        
        # Warning text
        font = pygame.font.SysFont('Arial', 18)
        warning_text = font.render("LASER CHARGING", True, (255, 50, 50))
        surface.blit(warning_text, (50, self.laser_target_y - 30))
    
    def draw_mini_laser_beam(self, surface):
        """Draw laser beam for mini-boss."""
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Pulsing effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
        pulse_width = int(self.laser_width * (0.9 + 0.2 * pulse))
        
        # Draw outer glow
        for i in range(3):
            glow_width = pulse_width + i * 4
            pygame.draw.line(surface, (255, 50, 50, 150 - i * 40), start_pos, end_pos, glow_width)
        
        # Draw main beam
        pygame.draw.line(surface, (255, 50, 50), start_pos, end_pos, pulse_width)
        
        # Draw bright core
        pygame.draw.line(surface, (255, 200, 200), start_pos, end_pos, pulse_width // 3)
        
        # Draw impact effect at left edge
        impact_x = 0
        impact_y = self.laser_target_y
        impact_radius = pulse_width // 2
        pygame.draw.circle(surface, (255, 200, 200), (impact_x, impact_y), impact_radius)
        pygame.draw.circle(surface, (255, 50, 50, 150), (impact_x, impact_y), impact_radius * 2)
    
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
        self.is_aimed = False  # Whether this is an aimed shot
        self.is_special = False  # Whether this is a special attack bullet
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
        
        # Draw special effects for aimed or special bullets
        if self.is_aimed:
            # Draw targeting line
            pygame.draw.line(surface, (100, 200, 255, 100), 
                           (self.rect.centerx, self.rect.centery), 
                           (self.rect.centerx + self.vx * 10, self.rect.centery + self.vy * 10), 
                           2)
        
        if self.is_special:
            # Draw pulsing glow for special bullets
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
            glow_size = int(self.width * (1.2 + 0.4 * pulse))
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            # Golden glow
            glow_color = (255, 200, 0, 100)
            pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
            
            # Position and draw glow
            glow_rect = glow_surface.get_rect(center=self.rect.center)
            surface.blit(glow_surface, glow_rect)
        
        # Draw bullet
        surface.blit(self.image, self.rect)
