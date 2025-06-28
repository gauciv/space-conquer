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
            self.bullet_patterns = ["spread", "focused", "barrage"]
            self.current_pattern_index = 0
            self.pattern_shots = 0  # Count shots in current pattern
            self.max_pattern_shots = 3  # Maximum shots before changing pattern
            
            # Movement parameters
            self.movement_timer = 0
            self.figure8_center_y = SCREEN_HEIGHT // 2
            self.figure8_amplitude = 120
            self.figure8_frequency = 0.015
            self.hover_position = None
            self.hover_timer = 0
            self.hover_duration = 0
            
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
            
        # Entry movement - move from right edge to battle position
        if not self.entry_complete:
            self.rect.x -= 3
            if self.rect.right < SCREEN_WIDTH - self.battle_distance:
                self.entry_complete = True
                self.last_shot = pygame.time.get_ticks()  # Reset shot timer when entry is complete
        else:
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
                    
                    # Chance to change position after pattern change
                    if random.random() < 0.7:
                        self.hover_position = (
                            SCREEN_WIDTH - self.battle_distance - self.rect.width - random.randint(0, 30),
                            random.randint(100, SCREEN_HEIGHT - 100)
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
                else:
                    # Different movement based on phase
                    if self.attack_phase == 1:
                        # Phase 1: Figure-8 pattern
                        self.movement_timer += 1
                        t = self.movement_timer * self.figure8_frequency
                        self.rect.centery = self.figure8_center_y + math.sin(t) * self.figure8_amplitude
                        
                        # Add slight horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width) + math.sin(t * 0.5) * 15
                    
                    elif self.attack_phase == 2:
                        # Phase 2: More aggressive vertical movement
                        self.movement_timer += 1
                        
                        # Change direction occasionally
                        if self.movement_timer % self.movement_change_delay == 0:
                            self.movement_direction = random.choice([-1, 1])
                            self.movement_change_delay = random.randint(30, 90)  # Faster direction changes
                        
                        # Move up/down faster
                        self.rect.y += self.speed * 1.5 * self.movement_direction
                        
                        # Add slight horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width) + math.sin(self.movement_timer * 0.02) * 25
                        
                        # Ensure boss stays on screen
                        if self.rect.top < 50:
                            self.rect.top = 50
                            self.movement_direction = 1
                        elif self.rect.bottom > SCREEN_HEIGHT - 50:
                            self.rect.bottom = SCREEN_HEIGHT - 50
                            self.movement_direction = -1
                    
                    elif self.attack_phase == 3:
                        # Phase 3: Erratic movement
                        self.movement_timer += 1
                        
                        # Combine sine wave and random movements
                        t = self.movement_timer * 0.04  # Faster frequency
                        self.rect.centery = self.figure8_center_y + math.sin(t) * self.figure8_amplitude * 1.2
                        
                        # More aggressive horizontal movement
                        self.rect.x = (SCREEN_WIDTH - self.battle_distance - self.rect.width - 10) + math.sin(t * 0.7) * 35
                        
                        # Add occasional jitter
                        if self.movement_timer % 10 == 0:
                            self.rect.x += random.randint(-5, 5)
                            self.rect.y += random.randint(-5, 5)
                
                # Handle special attack cooldown
                if self.special_attack_cooldown > 0:
                    self.special_attack_cooldown -= 16  # Approximately 16ms per frame at 60 FPS
            
            # Shoot bullets based on current attack pattern
            self.shoot()
        
        # Update hitbox position to follow the rect
        self.hitbox.center = self.rect.center
        
        # Update bullets
        self.bullets.update()
        
        return False  # Not finished dying
    
    def shoot(self):
        now = pygame.time.get_ticks()
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
                    spread_angle = 60  # Total spread angle in degrees
                    
                    for i in range(num_bullets):
                        # Calculate angle for this bullet
                        angle_rad = math.radians(-90 + spread_angle/2 - (spread_angle / (num_bullets-1)) * i)
                        
                        # Calculate velocity components
                        speed = abs(self.bullet_speed)
                        vx = math.cos(angle_rad) * speed
                        vy = math.sin(angle_rad) * speed
                        
                        # Create bullet
                        bullet = BossBullet(
                            self.rect.left, 
                            self.rect.centery, 
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
                    # Focused attack - straight line of bullets
                    num_bullets = 2 + self.attack_phase  # 3, 4, or 5 bullets
                    
                    for i in range(num_bullets):
                        # Create bullet with slight vertical offset
                        offset = 5 * (i - (num_bullets-1)/2)  # Centered around 0
                        
                        bullet = BossBullet(
                            self.rect.left - i*10,  # Staggered horizontally
                            self.rect.centery + offset,
                            self.bullet_speed * 1.2,  # Faster than normal
                            self.bullet_damage
                        )
                        
                        # Set color based on phase
                        if self.attack_phase == 2:
                            bullet.color_shift = (0, 255, 100)  # Green tint for phase 2
                        elif self.attack_phase == 3:
                            bullet.color_shift = (255, 100, 0)  # Orange tint for phase 3
                            
                        self.bullets.add(bullet)
                
                elif self.attack_pattern == "barrage":
                    # Barrage - random spread of bullets
                    num_bullets = 3 + (self.attack_phase * 2)  # 5, 7, or 9 bullets
                    
                    for i in range(num_bullets):
                        # Random position within a cone
                        offset_y = random.randint(-30, 30)
                        offset_x = random.randint(-10, 10)
                        
                        # Random speed variation
                        speed_var = random.uniform(0.85, 1.15)
                        
                        bullet = BossBullet(
                            self.rect.left + offset_x,
                            self.rect.centery + offset_y,
                            self.bullet_speed * speed_var,
                            self.bullet_damage
                        )
                        
                        # Add slight vertical drift
                        bullet.vy = random.uniform(-1.0, 1.0)
                        
                        # Set color based on phase
                        if self.attack_phase == 2:
                            bullet.color_shift = (255, 255, 0)  # Yellow tint for phase 2
                        elif self.attack_phase == 3:
                            bullet.color_shift = (255, 50, 50)  # Red tint for phase 3
                            
                        self.bullets.add(bullet)
                
                # Increment pattern shots counter
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
        else:
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
        
        # Draw health bar if not dying
        if not self.dying:
            self.draw_health_bar(surface)
            
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
        self.hitbox = self.rect.inflate(-2, -1)  # 2px smaller on width, 1px smaller on height
        
        # Add trail effect properties
        self.trail = []
        self.max_trail_length = 5
    
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
            pygame.draw.circle(surface, trail_color, (x, y), size)
        
        # Draw bullet
        surface.blit(self.image, self.rect)
