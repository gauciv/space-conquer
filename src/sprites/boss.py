"""
Boss class for Space Impact game.
"""
import pygame
import math
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES

class Boss(pygame.sprite.Sprite):
    """Boss enemy class."""
    
    def __init__(self, x, y, boss_type, asset_loader, sound_manager):
        """Initialize the boss."""
        super().__init__()
        self.asset_loader = asset_loader
        self.sound_manager = sound_manager
        self.boss_type = boss_type
        
        # Set boss-specific properties based on type
        if boss_type == 'mini':
            original_image = asset_loader.get_image('mini_boss')
            self.name = "Sentinel"
            self.max_health = 100
            self.health = self.max_health
            self.speed = 3.0
            self.shoot_delay = 1000
            self.bullet_speed = -8
            self.bullet_damage = 1
            self.score_value = 1000
            self.movement_pattern = "sine"
            self.battle_distance = 100  # Distance from right edge during battle
            
            # Scale the mini boss to 0.75x size
            new_width = int(original_image.get_width() * 0.75)
            new_height = int(original_image.get_height() * 0.75)
            
            # Mini boss specific attack patterns
            self.attack_phase = 1  # Current attack phase (1-3)
            self.attack_pattern = "normal"  # Initial attack pattern
            self.pattern_shots = 0  # Number of shots fired in current pattern
            self.max_pattern_shots = 5  # Number of shots before changing pattern
            self.attack_timer = 0
            self.attack_change_delay = 5000  # Change attack pattern every 5 seconds
            
            # Sine wave movement parameters
            self.amplitude = 100  # Amplitude of sine wave
            self.frequency = 0.02  # Frequency of sine wave
            self.phase = 0  # Phase of sine wave
            
            # Dash attack parameters
            self.dash_cooldown = 0
            self.dash_duration = 0
            self.dash_speed = 0  # Will be set in phase 2
            self.is_dashing = False
            self.dash_target_y = 0
            
            # Weak point parameters
            self.has_weak_point = True
            self.weak_point_active = False
            self.weak_point_cooldown = 0
            self.weak_point_duration = 5000  # 5 seconds
            self.weak_point_position = (0, 0)  # Will be updated in update()
            self.weak_point_radius = 15
            
            # Laser attack parameters
            self.laser_charging = False
            self.laser_firing = False
            self.laser_cooldown = 0
            self.laser_charge_time = 0
            self.laser_fire_time = 0
            self.laser_target_y = 0
            
            # Sniper attack parameters
            self.sniper_charging = False
            self.sniper_firing = False
            self.sniper_cooldown = 0
            self.sniper_charge_time = 0
            self.sniper_fire_time = 0
            self.sniper_target_y = 0
            self.sniper_in_warning = False
            
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
            
            # Shield system - ENHANCED
            self.has_shield = True
            self.max_shield_health = self.max_health // 2  # Shield is half of max health
            self.shield_health = self.max_shield_health
            self.shield_active = True
            self.last_shield_hit = 0
            # Shield will fully regenerate after 30 seconds
            
            # Player tracking
            self.player_ref = None  # Will be set by game manager
            self.tracking_player = True  # Whether to follow player's y position
            self.tracking_speed = 2.0  # Speed to follow player
            self.target_y = SCREEN_HEIGHT // 2  # Target y position (will be updated to player's position)
            
            # Laser attack parameters
            self.laser_active = False
            self.laser_phase = None
            self.laser_charge_time = 0
            self.laser_fire_time = 0
            self.laser_cooldown = 0
            self.laser_target_y = SCREEN_HEIGHT // 2
            
        # Scale the image
        self.original_image = pygame.transform.scale(original_image, (new_width, new_height))
        self.image = self.original_image.copy()
        
        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        
        # Create a smaller hitbox for more precise collision detection
        hitbox_width = int(self.rect.width * 0.8)
        hitbox_height = int(self.rect.height * 0.8)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
        
        # Movement variables
        self.vx = 0
        self.vy = 0
        self.entry_complete = False
        self.entry_speed = -5  # Speed during entry animation
        self.entry_target_x = SCREEN_WIDTH - self.battle_distance - self.rect.width
        
        # Combat variables
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.hit_flash = 0
        self.flash_effect = 0
        
        # Death animation variables
        self.dying = False
        self.death_start_time = 0
        self.death_duration = 2000  # 2 seconds
        self.explosion_particles = []
        
        # Load health bar images
        self.health_bar_bg = asset_loader.get_image('health_bar_bg')
        self.health_bar_fill = asset_loader.get_image('health_bar_fill')
        
        # Movement timer for animations
        self.movement_timer = 0
        
        # Player tracking
        self.player_y_position = SCREEN_HEIGHT // 2  # Default player position
        
        # Laser attack
        self.shot_pattern = 'cone'  # Start with cone pattern
        self.shot_counter = 0
        self.last_shot_time = 0
    def update(self):
        """Update the boss."""
        # Increment movement timer
        self.movement_timer += 1
        
        # Track player position if available
        if self.player_ref and hasattr(self.player_ref, 'rect'):
            # Smoothly track player's y position
            target_y = self.player_ref.rect.centery
            if not hasattr(self, 'player_y_position'):
                self.player_y_position = target_y
            else:
                # Smooth tracking - move 10% of the way to the target each frame
                self.player_y_position += (target_y - self.player_y_position) * 0.1
        
        # Handle death animation
        if self.dying:
            return self.update_death_animation()
            
        # Handle entry animation
        if not self.entry_complete:
            return self.update_entry_animation()
            
        # Update position based on movement pattern
        self.update_movement()
        
        # Update shooting
        self.update_shooting()
        
        # Update hitbox position
        self.hitbox.center = self.rect.center
        
        # Update bullets
        self.bullets.update()
        
        # Handle shield regeneration for main boss
        if self.boss_type == 'main' and hasattr(self, 'has_shield') and self.has_shield and not self.shield_active:
            # Check if enough time has passed since last hit (30 seconds)
            shield_regen_delay = 30000  # 30 seconds
            now = pygame.time.get_ticks()
            
            if now - self.last_shield_hit > shield_regen_delay:
                # Fully restore shield
                self.shield_health = self.max_shield_health
                self.shield_active = True
                self.flash_effect = 20  # Visual feedback (increased from 15)
                print(f"Shield fully restored after 30 seconds! Shield health: {self.shield_health}/{self.max_shield_health}")
                self.sound_manager.play_sound('powerup')  # Play shield reactivation sound
                
                # Reset last hit time to prevent immediate regeneration
                self.last_shield_hit = now
                
                # Visual warning to player
                if self.player_ref:
                    # Flash screen briefly
                    if hasattr(self.player_ref, 'screen_flash'):
                        self.player_ref.screen_flash = 10
        
        return False  # Not finished dying
    def update_movement(self):
        """Update boss movement based on pattern."""
        # Different movement patterns based on boss type
        if self.boss_type == 'mini':
            if self.movement_pattern == "sine":
                # Sine wave movement
                self.phase += self.frequency
                self.rect.centery = SCREEN_HEIGHT // 2 + int(self.amplitude * math.sin(self.phase))
                
                # Handle dash attack in phase 2+
                if self.attack_phase >= 2 and not self.is_dashing:
                    # Check if it's time to dash
                    now = pygame.time.get_ticks()
                    if now > self.dash_cooldown:
                        # Start dash
                        self.is_dashing = True
                        self.dash_duration = now + 500  # Dash for 500ms
                        
                        # Target player's position
                        if self.player_ref:
                            self.dash_target_y = self.player_ref.rect.centery
                        else:
                            self.dash_target_y = SCREEN_HEIGHT // 2
                            
                if self.is_dashing:
                    # Execute dash
                    now = pygame.time.get_ticks()
                    if now < self.dash_duration:
                        # Move towards target y
                        dy = self.dash_target_y - self.rect.centery
                        if abs(dy) > self.dash_speed:
                            self.rect.centery += self.dash_speed if dy > 0 else -self.dash_speed
                        else:
                            self.rect.centery = self.dash_target_y
                    else:
                        # End dash
                        self.is_dashing = False
                        self.dash_cooldown = now + 3000  # Cooldown for 3 seconds
                        
        elif self.boss_type == 'main':
            if self.movement_pattern == "multistage":
                # Initialize movement mode if not set
                if not hasattr(self, 'movement_mode'):
                    self.movement_mode = "track_player"
                    self.movement_mode_timer = 0
                    self.movement_mode_duration = 300  # 5 seconds at 60 FPS
                    self.figure8_center_y = SCREEN_HEIGHT // 2
                    self.circle_radius = 100
                    self.circle_angle = 0
                    self.circle_direction = 1  # 1 for clockwise, -1 for counterclockwise
                    
                # Update movement mode timer
                self.movement_mode_timer += 1
                
                # Change movement mode periodically
                if self.movement_mode_timer >= self.movement_mode_duration:
                    # Reset timer
                    self.movement_mode_timer = 0
                    
                    # Choose next movement mode
                    modes = ["track_player", "figure8", "circle", "zigzag"]
                    
                    # Don't repeat the same mode
                    current_mode_index = modes.index(self.movement_mode) if self.movement_mode in modes else 0
                    next_mode_index = (current_mode_index + 1) % len(modes)
                    self.movement_mode = modes[next_mode_index]
                    
                    # Set up parameters for the new mode
                    if self.movement_mode == "figure8":
                        self.figure8_center_y = SCREEN_HEIGHT // 2
                        self.figure8_phase = 0
                        self.figure8_amplitude = 150
                        self.figure8_frequency = 0.02
                        self.movement_mode_duration = 360  # 6 seconds
                        print(f"Boss switching to figure8 movement pattern")
                        
                    elif self.movement_mode == "circle":
                        self.circle_center_y = SCREEN_HEIGHT // 2
                        self.circle_radius = 120
                        self.circle_angle = 0
                        self.circle_speed = 0.05
                        self.circle_direction = random.choice([-1, 1])  # Random direction
                        self.movement_mode_duration = 240  # 4 seconds
                        print(f"Boss switching to circle movement pattern (direction: {self.circle_direction})")
                        
                    elif self.movement_mode == "zigzag":
                        self.zigzag_points = []
                        # Create random zigzag points
                        num_points = 5
                        for i in range(num_points):
                            x = self.entry_target_x + random.randint(-50, 50)
                            y = random.randint(100, SCREEN_HEIGHT - 100)
                            self.zigzag_points.append((x, y))
                        self.zigzag_current_point = 0
                        self.zigzag_speed = 5
                        self.movement_mode_duration = 300  # 5 seconds
                        print(f"Boss switching to zigzag movement pattern with {num_points} points")
                        
                    elif self.movement_mode == "track_player":
                        self.tracking_speed = 3.0  # Faster tracking
                        self.movement_mode_duration = 180  # 3 seconds
                        print(f"Boss switching to player tracking movement")
                
                # Execute current movement mode
                if self.movement_mode == "track_player":
                    # Track player's y position with smooth movement
                    if self.tracking_player and self.player_ref:
                        # Get player's y position
                        self.target_y = self.player_y_position
                        
                        # Move towards target y with smooth movement
                        dy = self.target_y - self.rect.centery
                        if abs(dy) > 1:
                            # Move at tracking_speed, but don't overshoot
                            move_amount = min(abs(dy), self.tracking_speed)
                            self.rect.centery += move_amount if dy > 0 else -move_amount
                    
                elif self.movement_mode == "figure8":
                    # Figure-8 movement with improved dynamics
                    self.figure8_phase += self.figure8_frequency
                    
                    # Calculate x and y offsets using parametric equations for a figure-8
                    # Using Lissajous curve with frequency ratio 2:1
                    x_offset = int(self.figure8_amplitude * 0.5 * math.sin(self.figure8_phase))
                    y_offset = int(self.figure8_amplitude * 0.5 * math.sin(2 * self.figure8_phase))
                    
                    # Apply offset with smoother transitions
                    target_x = self.entry_target_x + x_offset
                    target_y = self.figure8_center_y + y_offset
                    
                    # Move towards target with smooth interpolation
                    self.rect.x += (target_x - self.rect.x) * 0.1
                    self.rect.centery += (target_y - self.rect.centery) * 0.1
                    
                elif self.movement_mode == "circle":
                    # Circular movement with improved dynamics
                    self.circle_angle += self.circle_speed * self.circle_direction
                    
                    # Calculate position using parametric circle equations
                    x_offset = int(self.circle_radius * 0.5 * math.cos(self.circle_angle))
                    y_offset = int(self.circle_radius * math.sin(self.circle_angle))
                    
                    # Apply offset with smoother transitions
                    target_x = self.entry_target_x + x_offset
                    target_y = self.circle_center_y + y_offset
                    
                    # Move towards target with smooth interpolation
                    self.rect.x += (target_x - self.rect.x) * 0.1
                    self.rect.centery += (target_y - self.rect.centery) * 0.1
                    
                elif self.movement_mode == "zigzag":
                    # Zigzag movement between points with improved dynamics
                    if self.zigzag_current_point < len(self.zigzag_points):
                        target_x, target_y = self.zigzag_points[self.zigzag_current_point]
                        
                        # Calculate distance to target
                        dx = target_x - self.rect.centerx
                        dy = target_y - self.rect.centery
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        if distance > self.zigzag_speed:
                            # Move towards target with easing
                            angle = math.atan2(dy, dx)
                            move_x = math.cos(angle) * self.zigzag_speed
                            move_y = math.sin(angle) * self.zigzag_speed
                            
                            # Apply easing for smoother movement
                            self.rect.centerx += int(move_x)
                            self.rect.centery += int(move_y)
                        else:
                            # Reached target, move to next point
                            self.rect.centerx = target_x
                            self.rect.centery = target_y
                            self.zigzag_current_point += 1
                            
                            # Add a small pause at each point
                            if random.random() < 0.5:  # 50% chance to pause
                                self.zigzag_pause = 10  # Pause for 10 frames
                    else:
                        # Reset to first point
                        self.zigzag_current_point = 0
                        
        # Keep boss within screen boundaries
        screen_margin = 20  # Margin to keep boss visible
        
        # Constrain X position
        right_boundary = SCREEN_WIDTH - screen_margin
        left_boundary = SCREEN_WIDTH // 2  # Don't let boss go past middle of screen
        
        if self.rect.right > right_boundary:
            self.rect.right = right_boundary
        elif self.rect.left < left_boundary:
            self.rect.left = left_boundary
            
        # Constrain Y position
        if self.rect.bottom > SCREEN_HEIGHT - screen_margin:
            self.rect.bottom = SCREEN_HEIGHT - screen_margin
        elif self.rect.top < screen_margin:
            self.rect.top = screen_margin
    def update_shooting(self):
        """Update boss shooting."""
        now = pygame.time.get_ticks()
        
        # Check if it's time to shoot
        if now - self.last_shot > self.shoot_delay:
            print(f"Time to shoot! Last shot: {self.last_shot}, now: {now}, delay: {self.shoot_delay}")
            self.last_shot = now
            self.shoot()
        else:
            if self.movement_timer % 60 == 0:  # Print every second (assuming 60 FPS)
                print(f"Waiting to shoot... {(now - self.last_shot) / 1000:.1f}s / {self.shoot_delay / 1000:.1f}s")
            
    def update_entry_animation(self):
        """Update boss entry animation."""
        print(f"Entry animation: x={self.rect.x}, target={self.entry_target_x}, speed={self.entry_speed}")
        # Move boss from right edge to battle position
        if self.rect.right > self.entry_target_x:
            self.rect.x += self.entry_speed
        else:
            # Entry complete
            self.entry_complete = True
            self.rect.right = self.entry_target_x
            print(f"Entry animation complete! Boss ready to battle.")
            
            # Play boss arrival sound
            self.sound_manager.play_sound('explosion')
            
            # Set initial attack pattern
            if self.boss_type == 'mini':
                self.attack_pattern = "normal"
            else:
                self.attack_pattern = "spread"
                
        return False
        
    def update_death_animation(self):
        """Update boss death animation."""
        now = pygame.time.get_ticks()
        progress = (now - self.death_start_time) / self.death_duration
        
        if progress >= 1.0:
            # Death animation complete
            return True
            
        # Create explosion particles
        if len(self.explosion_particles) < 50:
            # Add new particles
            for _ in range(5):
                # Random position within boss
                x = self.rect.centerx + random.randint(-self.rect.width//2, self.rect.width//2)
                y = self.rect.centery + random.randint(-self.rect.height//2, self.rect.height//2)
                
                # Random velocity
                vx = random.uniform(-3, 3)
                vy = random.uniform(-3, 3)
                
                # Random size and lifetime
                size = random.randint(3, 10)
                lifetime = random.randint(20, 40)
                
                # Random color (red/orange/yellow)
                r = random.randint(200, 255)
                g = random.randint(100, 200)
                b = random.randint(0, 100)
                
                # Add particle
                self.explosion_particles.append({
                    'x': x,
                    'y': y,
                    'vx': vx,
                    'vy': vy,
                    'size': size,
                    'lifetime': lifetime,
                    'color': (r, g, b)
                })
                
        # Update existing particles
        for particle in self.explosion_particles[:]:
            # Move particle
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Decrease lifetime
            particle['lifetime'] -= 1
            
            # Remove dead particles
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
                
        return False
    def shoot(self):
        """Shoot bullets with alternating patterns and reasonable fire rate."""
        now = pygame.time.get_ticks()
        
        # Only shoot if boss is on screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            return  # Don't shoot if off screen
        
        # Only shoot if enough time has passed since last shot (fire rate control)
        if not hasattr(self, 'last_shot_time'):
            self.last_shot_time = 0
            self.shot_pattern = 'cone'  # Start with cone pattern
            self.shot_counter = 0
            self.laser_active = False
            self.laser_charge_time = 0
            self.laser_fire_time = 0
            self.laser_cooldown = 0
            self.player_y_position = SCREEN_HEIGHT // 2  # Default player position
        
        # Track player position for targeting
        if self.player_ref and hasattr(self.player_ref, 'rect'):
            # Smoothly track player's y position
            target_y = self.player_ref.rect.centery
            if not hasattr(self, 'player_y_position'):
                self.player_y_position = target_y
            else:
                # Smooth tracking - move 10% of the way to the target each frame
                self.player_y_position += (target_y - self.player_y_position) * 0.1
        
        # Handle laser attack
        if hasattr(self, 'laser_active') and self.laser_active:
            # Laser has three phases: charging, firing, cooldown
            if hasattr(self, 'laser_phase'):
                if self.laser_phase == 'charging':
                    # Charging phase - show warning
                    charge_time = 1500  # 1.5 seconds charging
                    if now - self.laser_charge_time > charge_time:
                        # Start firing
                        self.laser_phase = 'firing'
                        self.laser_fire_time = now
                        self.sound_manager.play_sound('explosion')  # Laser fire sound
                        print(f"Laser firing started!")
                    return
                    
                elif self.laser_phase == 'firing':
                    # Firing phase - damage player if in path
                    fire_time = 1000  # 1 second firing
                    if now - self.laser_fire_time > fire_time:
                        # End firing, start cooldown
                        self.laser_phase = 'cooldown'
                        self.laser_cooldown = now
                        self.laser_active = False
                        print(f"Laser firing ended, entering cooldown")
                    return
                    
                elif self.laser_phase == 'cooldown':
                    # Cooldown phase - wait before next attack
                    cooldown_time = 3000  # 3 seconds cooldown
                    if now - self.laser_cooldown > cooldown_time:
                        # End cooldown
                        self.laser_active = False
                        self.shot_pattern = 'cone'  # Reset to cone pattern
                        print(f"Laser cooldown ended")
                    return
            else:
                # Initialize laser phases if not set
                self.laser_phase = 'charging'
                self.laser_charge_time = now
                # Store the current position for the laser
                self.laser_target_y = self.rect.centery
                if hasattr(self, 'player_y_position'):
                    self.laser_target_y = self.player_y_position
                print(f"Laser charging started at y={self.laser_target_y}!")
                return
        
        # Set a slower fire rate (2000ms = 2 seconds between shots)
        fire_rate = 2000  # milliseconds between shots
        
        if now - self.last_shot_time < fire_rate:
            return  # Don't shoot yet
            
        self.last_shot_time = now
        self.shot_counter += 1
        
        # Check if shield is down to determine laser attack probability
        shield_down = False
        if self.boss_type == 'main' and hasattr(self, 'has_shield') and self.has_shield:
            shield_down = not self.shield_active
        
        # Switch patterns every 3 shots, with a higher chance for laser attack when shield is down
        if self.shot_counter % 3 == 0:
            # 70% chance to use laser attack when shield is down (increased from 40%), 40% otherwise
            laser_chance = 0.7 if shield_down else 0.4
            
            if random.random() < laser_chance:
                self.shot_pattern = 'laser'
                print(f"Switching to laser pattern (Shield down: {shield_down})")
                self.laser_active = True
                self.laser_phase = 'charging'
                self.laser_charge_time = now
                # Target current player position for laser
                self.laser_target_y = self.rect.centery
                if hasattr(self, 'player_y_position'):
                    self.laser_target_y = self.player_y_position
                # Set laser width for collision detection
                self.laser_width = 25  # Increased from 20
                return
            else:
                # Alternate between cone and line patterns
                self.shot_pattern = 'line' if self.shot_pattern == 'cone' else 'cone'
                print(f"Switching to {self.shot_pattern} pattern")
        
        # Play sound
        self.sound_manager.play_sound('shoot')
        
        if self.shot_pattern == 'cone':
            # V-shaped cone pattern (shotgun spread)
            num_bullets = 5
            spread_angle = 30  # Total spread angle in degrees
            
            # Target player position
            target_y = self.player_y_position
            
            for i in range(num_bullets):
                # Calculate angle for this bullet in the spread
                angle_offset = spread_angle / (num_bullets - 1)
                base_angle = 180  # Base angle (left)
                
                # Adjust angle to aim at player
                if self.rect.centery != target_y:
                    # Calculate angle to player
                    dy = target_y - self.rect.centery
                    dx = -400  # Approximate distance to player
                    aim_angle = math.degrees(math.atan2(dy, dx))
                    base_angle = aim_angle
                
                angle = base_angle + (i - (num_bullets-1)/2) * angle_offset
                angle_rad = math.radians(angle)
                
                # Calculate velocity components
                speed = 5  # Slower bullet speed
                vx = math.cos(angle_rad) * speed
                vy = math.sin(angle_rad) * speed
                
                # Create bullet
                bullet = BossBullet(
                    self.rect.left, 
                    self.rect.centery, 
                    vx,
                    1  # Lower damage per bullet since there are multiple
                )
                bullet.vy = vy
                self.bullets.add(bullet)
                print(f"Created cone bullet at angle {angle:.1f}° targeting y={target_y}")
        else:
            # Horizontal line pattern
            num_bullets = 3
            vertical_spacing = 40  # pixels between bullets
            
            # Target player position
            target_y = self.player_y_position
            
            # Center the pattern on the player's position
            for i in range(num_bullets):
                # Calculate vertical position relative to target
                y_offset = (i - (num_bullets-1)/2) * vertical_spacing
                
                # Create bullet
                bullet = BossBullet(
                    self.rect.left,
                    self.rect.centery + y_offset,  # Center on boss position with offset
                    -6,  # Straight left, slower
                    2    # Higher damage for line shots
                )
                self.bullets.add(bullet)
                print(f"Created line bullet at y={self.rect.centery + y_offset}")
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
            print(f"Boss shield damaged! Shield health: {self.shield_health}/{self.max_shield_health}")
            
            # Visual feedback
            self.hit_flash = 5  # Shorter flash for shield hit
            
            # Shield break
            if self.shield_health <= 0:
                self.shield_active = False
                self.sound_manager.play_sound('explosion')  # Shield break sound
                self.hit_flash = 15  # Longer flash for shield break
                print(f"Boss shield BROKEN! Will regenerate in 30 seconds.")
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
        print(f"Boss health reduced to {self.health}/{self.max_health}")
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
                print(f"Boss entering phase {new_phase}!")
                
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
            print(f"Boss defeated!")
            self.destroy()
            return True
        return False
    def destroy(self):
        """Start the boss death animation."""
        if not self.dying:
            self.dying = True
            self.death_start_time = pygame.time.get_ticks()
            self.explosion_particles = []
            self.sound_manager.play_sound('explosion')
            
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
        
        # Draw shield bar for main boss
        if self.boss_type == 'main' and hasattr(self, 'has_shield') and self.has_shield:
            # Position shield bar below health bar
            shield_bar_y = bar_y + 30
            
            # Draw shield bar background (slightly smaller than health bar)
            shield_bg_rect = pygame.Rect(bar_x, shield_bar_y, self.health_bar_bg.get_width(), 10)
            pygame.draw.rect(surface, (50, 50, 100), shield_bg_rect)
            pygame.draw.rect(surface, (100, 100, 150), shield_bg_rect, 1)  # Border
            
            if self.shield_active:
                # Calculate shield fill width
                shield_fill_width = int((self.shield_health / self.max_shield_health) * (self.health_bar_bg.get_width() - 2))
                
                # Draw shield fill
                if shield_fill_width > 0:
                    shield_fill_rect = pygame.Rect(bar_x + 1, shield_bar_y + 1, shield_fill_width, 8)
                    shield_color = (100, 150, 255)  # Blue shield
                    pygame.draw.rect(surface, shield_color, shield_fill_rect)
                
                # Draw shield text
                shield_text = font.render(f"Shield: {int(self.shield_health)}/{self.max_shield_health}", True, (200, 200, 255))
                surface.blit(shield_text, (bar_x + (self.health_bar_bg.get_width() - shield_text.get_width()) // 2, shield_bar_y + 12))
            else:
                # Shield is down, show regeneration countdown
                now = pygame.time.get_ticks()
                time_since_hit = now - self.last_shield_hit
                regen_time = 30000  # 30 seconds
                time_left = max(0, (regen_time - time_since_hit) / 1000)  # Convert to seconds
                
                # Draw regeneration progress bar
                if time_left > 0:
                    regen_progress = 1 - (time_left / 30)  # 0 to 1
                    regen_width = int(regen_progress * (self.health_bar_bg.get_width() - 2))
                    
                    if regen_width > 0:
                        regen_rect = pygame.Rect(bar_x + 1, shield_bar_y + 1, regen_width, 8)
                        # Color changes from red to green as it gets closer to regenerating
                        r = int(255 * (1 - regen_progress))
                        g = int(255 * regen_progress)
                        regen_color = (r, g, 50)
                        pygame.draw.rect(surface, regen_color, regen_rect)
                
                # Draw countdown text
                countdown_text = font.render(f"Shield Regenerating: {int(time_left)}s", True, (255, 200, 100))
                surface.blit(countdown_text, (bar_x + (self.health_bar_bg.get_width() - countdown_text.get_width()) // 2, shield_bar_y + 12))
    
    def draw(self, surface):
        """Draw the boss and its bullets."""
        if self.dying:
            self.draw_death_animation(surface)
            return
            
        # Draw laser if active
        if hasattr(self, 'laser_active') and self.laser_active:
            if hasattr(self, 'laser_phase'):
                if self.laser_phase == 'charging':
                    self.draw_laser_warning(surface)
                elif self.laser_phase == 'firing':
                    self.draw_laser_beam(surface)
            
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
            shield_health_percent = self.shield_health / self.max_shield_health
            shield_size = int(max(self.rect.width, self.rect.height) * (1.0 + 0.15 * shield_health_percent))
            
            # Pulsing effect
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
            shield_alpha = int(100 + 50 * pulse)  # 100-150 alpha
            
            # Create shield surface
            shield_surface = pygame.Surface((shield_size, shield_size), pygame.SRCALPHA)
            
            # Draw shield circle with color based on health percentage
            if shield_health_percent > 0.7:
                # Strong shield - blue
                shield_color = (100, 150, 255, shield_alpha)
            elif shield_health_percent > 0.3:
                # Medium shield - purple
                shield_color = (150, 100, 255, shield_alpha)
            else:
                # Weak shield - red
                shield_color = (255, 100, 100, shield_alpha)
                
            pygame.draw.circle(shield_surface, shield_color, (shield_size//2, shield_size//2), shield_size//2, 3)
            
            # Draw inner glow
            inner_color = (150, 200, 255, shield_alpha // 2)
            pygame.draw.circle(shield_surface, inner_color, (shield_size//2, shield_size//2), shield_size//2 - 5, 2)
            
            # Position and draw shield
            shield_rect = shield_surface.get_rect(center=self.rect.center)
            surface.blit(shield_surface, shield_rect)
            
            # Draw shield percentage near the boss
            font = pygame.font.SysFont('Arial', 14)
            shield_text = font.render(f"{int(shield_health_percent * 100)}%", True, shield_color[:3])
            text_pos = (self.rect.centerx - shield_text.get_width() // 2, 
                        self.rect.top - shield_text.get_height() - 5)
            surface.blit(shield_text, text_pos)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Draw bullets with custom draw method
        for bullet in self.bullets:
            if hasattr(bullet, 'draw'):
                bullet.draw(surface)
            else:
                surface.blit(bullet.image, bullet.rect)
        
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
            
        # Draw explosion text
        progress = (pygame.time.get_ticks() - self.death_start_time) / self.death_duration
        if progress < 0.5:
            # First half of animation - show "BOSS DEFEATED"
            font_size = int(20 + 20 * progress)  # Grow from 20 to 40
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = font.render("BOSS DEFEATED!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            surface.blit(text, text_rect)
        else:
            # Second half - show score
            font_size = 40
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = font.render(f"+{self.score_value} POINTS", True, (255, 255, 100))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            surface.blit(text, text_rect)
            
    def draw_laser_warning(self, surface):
        """Draw a warning for the laser attack."""
        if not hasattr(self, 'laser_target_y'):
            self.laser_target_y = self.player_y_position if hasattr(self, 'player_y_position') else self.rect.centery
            
        # Calculate warning line properties
        now = pygame.time.get_ticks()
        charge_progress = (now - self.laser_charge_time) / 1500  # 1.5 seconds charging
        
        # Warning line color pulses from white to red
        pulse_rate = 10  # Higher value = faster pulse
        pulse_factor = (math.sin(charge_progress * pulse_rate) + 1) / 2  # 0 to 1
        
        r = 255
        g = int(255 * (1 - pulse_factor))
        b = int(100 * (1 - pulse_factor))
        
        # Draw warning line
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Draw solid line with increasing width as charging progresses
        warning_width = int(6 + charge_progress * 15)  # Increased base width and max width
        pygame.draw.line(surface, (r, g, b), start_pos, end_pos, warning_width)
        
        # Add pulsing glow effect around the line
        glow_width = warning_width + int(10 * pulse_factor)
        glow_color = (r, g, b, 100)  # Semi-transparent
        pygame.draw.line(surface, glow_color, start_pos, end_pos, glow_width)
        
        # Draw warning text that pulses
        font_size = int(22 + 8 * pulse_factor)  # Pulsing font size between 22 and 30
        font = pygame.font.SysFont('Arial', font_size, bold=True)  # Added bold
        warning_text = font.render("!!! LASER CHARGING !!!", True, (r, g, b))
        text_x = SCREEN_WIDTH // 2 - warning_text.get_width() // 2
        text_y = self.laser_target_y - 50  # Moved up slightly
        surface.blit(warning_text, (text_x, text_y))
        
        # Draw second warning text below
        font2 = pygame.font.SysFont('Arial', 18)
        warning_text2 = font2.render("MOVE OUT OF THE WAY!", True, (r, g, b))
        text_x2 = SCREEN_WIDTH // 2 - warning_text2.get_width() // 2
        text_y2 = self.laser_target_y + 30  # Below the laser line
        surface.blit(warning_text2, (text_x2, text_y2))
        
        # Draw warning indicators at both ends of the laser path
        indicator_radius = 15 + int(10 * pulse_factor)  # Increased size
        pygame.draw.circle(surface, (r, g, b), (0, self.laser_target_y), indicator_radius, 4)  # Increased line width
        pygame.draw.circle(surface, (r, g, b), (self.rect.left, self.laser_target_y), indicator_radius, 4)
        
        # Add flashing effect at both ends
        if pulse_factor > 0.7:  # Only draw during high pulse
            pygame.draw.circle(surface, (255, 255, 255), (0, self.laser_target_y), indicator_radius // 2)
            pygame.draw.circle(surface, (255, 255, 255), (self.rect.left, self.laser_target_y), indicator_radius // 2)
        
    def draw_laser_beam(self, surface):
        """Draw the laser beam."""
        if not hasattr(self, 'laser_target_y'):
            self.laser_target_y = self.player_y_position if hasattr(self, 'player_y_position') else self.rect.centery
            
        # Laser beam properties - start from the boss's left side
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Draw main beam with pulsing effect
        now = pygame.time.get_ticks()
        pulse_factor = (math.sin(now * 0.02) + 1) / 2  # 0 to 1, faster pulse
        
        # Pulse the width slightly
        laser_width = 35  # Increased base laser width even more for better visibility
        pulse_width = int(laser_width * (0.9 + 0.3 * pulse_factor))
        
        # Draw multiple layers for a more intense effect
        # Outer glow (semi-transparent)
        for i in range(6):  # Increased from 5 to 6 layers for more pronounced effect
            glow_width = pulse_width + i * 10  # Increased from i*8 to i*10
            alpha = 180 - i * 25  # Increased alpha from 150 to 180
            glow_color = (255, 100, 100, alpha)
            
            # Draw wider lines for glow effect
            pygame.draw.line(surface, glow_color, start_pos, end_pos, glow_width)
        
        # Main beam (solid)
        laser_color = (255, 50, 50)
        pygame.draw.line(surface, laser_color, start_pos, end_pos, pulse_width)
        
        # Bright core
        core_color = (255, 220, 220)  # Brighter core
        pygame.draw.line(surface, core_color, start_pos, end_pos, pulse_width // 2)
        
        # Brightest center
        center_color = (255, 255, 255)  # Pure white
        pygame.draw.line(surface, center_color, start_pos, end_pos, pulse_width // 4)
        
        # Add impact effect at the left edge
        impact_x = 0
        impact_y = self.laser_target_y
        impact_radius = pulse_width + int(20 * pulse_factor)  # Increased from 15 to 20
        
        # Draw impact circles with pulsing effect
        pulse_intensity = abs(math.sin(now * 0.01)) * 0.5 + 0.5  # 0.5 to 1.0
        impact_color1 = (255, int(150 + 50 * pulse_intensity), int(150 * pulse_intensity))
        impact_color2 = (255, int(50 + 50 * pulse_intensity), int(50 * pulse_intensity))
        
        # Draw impact circles
        pygame.draw.circle(surface, impact_color1, (impact_x, impact_y), impact_radius // 2)
        pygame.draw.circle(surface, (impact_color2[0], impact_color2[1], impact_color2[2], 200), (impact_x, impact_y), impact_radius)
        
        # Add bright center to impact
        pygame.draw.circle(surface, (255, 255, 255), (impact_x, impact_y), impact_radius // 4)
        
        # Add small particles around the impact point
        for _ in range(15):  # Increased from 10 to 15 particles
            particle_x = impact_x + random.randint(-impact_radius, impact_radius//2)
            particle_y = impact_y + random.randint(-impact_radius, impact_radius)
            particle_size = random.randint(2, 8)  # Increased from 2-6 to 2-8
            
            # Randomize particle color for more visual interest
            r = random.randint(200, 255)
            g = random.randint(100, 200)
            b = random.randint(50, 150)
            pygame.draw.circle(surface, (r, g, b), (particle_x, particle_y), particle_size)
            
        # Add streaking effect along the beam
        for _ in range(8):  # Increased from 5 to 8 streaks
            streak_x = random.randint(0, self.rect.left)
            streak_y = self.laser_target_y + random.randint(-5, 5)  # Wider variation
            streak_length = random.randint(20, 60)  # Longer potential streaks
            streak_width = random.randint(1, 4)  # Thicker potential streaks
            
            # Randomize streak brightness
            brightness = random.randint(200, 255)
            pygame.draw.line(surface, (brightness, brightness, brightness), 
                            (streak_x, streak_y), 
                            (streak_x + streak_length, streak_y), 
                            streak_width)
            
        # Add secondary impact particles that fly outward from the impact point
        for _ in range(5):  # Add 5 flying particles
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(impact_radius//2, impact_radius*2)
            particle_x = impact_x + int(math.cos(angle) * distance)
            particle_y = impact_y + int(math.sin(angle) * distance)
            size = random.randint(2, 5)
            pygame.draw.circle(surface, (255, 200, 100), (particle_x, particle_y), size)
            
        # Check for collision with player
        self.check_laser_collision()
        
    def check_laser_collision(self):
        """Check if the laser beam is colliding with the player and apply damage."""
        if not self.player_ref:
            return
            
        # Create a collision rectangle for the laser beam
        laser_height = 30  # Increased from 20 to 30 to match the visual width
        laser_rect = pygame.Rect(
            0,  # Left edge of screen
            self.laser_target_y - laser_height // 2,
            self.rect.left,  # Extends to the boss's left edge
            laser_height
        )
        
        # Check for collision with player
        if laser_rect.colliderect(self.player_ref.hitbox):
            # Apply damage to player (once per frame)
            self.player_ref.take_damage(3)  # Increased from 2 to 3 damage
            
            # Visual effect for player hit
            if hasattr(self.player_ref, 'hit_flash'):
                self.player_ref.hit_flash = 15  # Increased from 10 to 15
                
            # Play hit sound
            self.sound_manager.play_sound('explosion')  # Use explosion sound for laser hit
            
            # Add knockback effect
            if hasattr(self.player_ref, 'knockback'):
                # Knockback to the left
                self.player_ref.knockback = -8  # Increased from -5 to -8
                
        # Debug visualization - draw the laser collision rect if debug mode is on
        if DEBUG_HITBOXES:
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), laser_rect, 1)
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
        
        # Set color based on damage
        if damage >= 2:
            self.color_shift = (255, 100, 0)  # Orange for higher damage
        else:
            self.color_shift = (0, 150, 255)  # Blue for lower damage
            
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
        
        # Rotate the bullet based on its velocity
        if hasattr(self, 'vy') and self.vy != 0:
            angle = math.degrees(math.atan2(self.vy, self.vx))
            self.image = pygame.transform.rotate(self.image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            
    def update(self):
        """Update the bullet position."""
        # Move the bullet
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Update hitbox position
        self.hitbox.center = self.rect.center
        
        # Add trail effect
        if hasattr(self, 'trail'):
            # Add current position to trail
            self.trail.append((self.rect.centerx, self.rect.centery))
            
            # Limit trail length
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
        
        # Check if bullet is off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
    def draw(self, surface):
        """Draw the bullet with trail effect."""
        # Draw trail
        if hasattr(self, 'trail') and len(self.trail) > 1:
            # Calculate trail alpha based on position in trail
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                
                # Get trail segment
                start_pos = self.trail[i]
                end_pos = self.trail[i + 1]
                
                # Draw trail segment
                if self.color_shift:
                    trail_color = (
                        min(255, self.color_shift[0] // 2),
                        min(255, self.color_shift[1] // 2),
                        min(255, self.color_shift[2] // 2),
                        alpha
                    )
                else:
                    trail_color = (255, 100, 100, alpha)
                    
                # Draw trail segment as a line
                pygame.draw.line(surface, trail_color, start_pos, end_pos, 2)
        
        # Draw bullet
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
