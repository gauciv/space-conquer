"""
Super-type enemy for Space Impact game.
This is a specialized enemy type with shield, multi-phase attacks, and death explosion.
"""
import pygame
import random
import math
import time
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES
from src.sprites.enemy import Enemy

class SuperEnemy(Enemy):
    def __init__(self, images, behavior_manager=None):
        # Initialize with the base Enemy class but override key properties
        super().__init__('super', images, behavior_manager)
        
        # Override position to ensure it's always far to the right
        self.rect.x = SCREEN_WIDTH + 300
        self.rect.y = random.randint(80, SCREEN_HEIGHT - 80)
        
        # Shield system
        self.max_shield = 3  # Increased from 2 to 3 for more durability
        self.shield = self.max_shield
        self.has_shield = True
        self.shield_regen_cooldown = 0
        self.shield_pulse_cooldown = 0
        self.shield_pulse_active = False
        self.shield_pulse_radius = 0
        self.shield_opacity = 255
        self.shield_broken = False
        self.shield_break_time = 0
        
        # Health system (separate from shield)
        self.max_health = 4
        self.health = self.max_health
        
        # Attack system
        self.attack_cooldown = random.uniform(3.0, 5.0)
        self.attack_phase = 1  # Current attack phase (1-3)
        self.is_charging = False
        self.charge_cooldown = 0
        self.retreat_active = False
        self.berserk_mode = False
        
        # Laser attack system
        self.can_use_laser = True
        self.laser_active = False
        self.laser_charging = False
        self.laser_firing = False
        self.laser_cooldown = 0
        self.laser_charge_time = 0
        self.laser_fire_time = 0
        self.laser_target_y = 0
        self.laser_width = 15
        
        # Movement properties
        self.direction = -1  # Start moving left
        self.min_x = 100  # Don't go further left than this
        self.max_x = SCREEN_WIDTH - self.rect.width - 20  # Don't go off right edge
        self.preferred_distance = random.randint(180, 250)  # Distance from player
        self.min_distance = 120
        self.max_distance = 300
        self.position_update_timer = 0
        self.position_update_interval = random.uniform(0.8, 1.5)
        self.current_target_x = None
        
        # Death explosion properties
        self.is_exploding = False
        self.explosion_radius = 0
        self.explosion_max_radius = 100
        self.explosion_growth_rate = 150  # pixels per second
        self.explosion_damage_dealt = False
        self.explosion_damage_applied = False
        
        # Sound effect flags
        self.shield_break_sound_played = False
        
    def update(self):
        """Override the update method to handle shield and explosion logic."""
        # Get current time for time-based behaviors
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Handle death explosion if active
        if self.is_exploding:
            self.handle_explosion(delta_time)
            return
        
        # Apply speed multiplier
        self.speed = self.base_speed * self.speed_multiplier
        
        # Use behavior manager if available
        if self.behavior_manager:
            self.behavior_manager.update_behavior(self, delta_time)
            
            # Update attack behavior based on shield status
            if not self.has_shield and not self.laser_active:
                # When shield is down, use laser attacks instead of bullets
                self.try_laser_attack(delta_time)
            else:
                # When shield is up, use normal bullets
                self.behavior_manager.update_bullets(self)
        else:
            # Fallback to basic movement if no behavior manager
            self.rect.x -= self.speed
        
        # Update hitbox position
        self.hitbox.center = self.rect.center
        
        # Handle shield regeneration
        if not self.has_shield and self.shield_regen_cooldown > 0:
            self.shield_regen_cooldown -= delta_time
            if self.shield_regen_cooldown <= 0:
                self.has_shield = True
                self.shield = self.max_shield
                self.shield_broken = False
                self.shield_opacity = 255
        
        # Update shield break visual effect
        if self.shield_broken:
            if not self.shield_break_sound_played and current_time - self.shield_break_time < 0.1:
                # Play shield break sound (will be implemented in game manager)
                self.shield_break_sound_played = True
                
        # Update laser attack states
        self.update_laser(delta_time)
    
    def try_laser_attack(self, delta_time):
        """Try to use laser attack when shield is down."""
        if not self.can_use_laser or self.laser_active:
            return
            
        # 5% chance per second to start laser attack
        if random.random() < 0.05 * delta_time:
            self.start_laser_attack()
    
    def start_laser_attack(self):
        """Start the laser attack sequence."""
        self.laser_active = True
        self.laser_charging = True
        self.laser_firing = False
        self.laser_charge_time = time.time()
        
        # Target player if available
        if hasattr(self, 'game_manager') and self.game_manager and self.game_manager.player:
            self.laser_target_y = self.game_manager.player.rect.centery
        else:
            self.laser_target_y = self.rect.centery
    
    def update_laser(self, delta_time):
        """Update laser attack states."""
        if not self.laser_active:
            return
            
        current_time = time.time()
        
        if self.laser_charging:
            # Charging phase - 1.5 seconds
            if current_time - self.laser_charge_time > 1.5:
                self.laser_charging = False
                self.laser_firing = True
                self.laser_fire_time = current_time
                # Play laser sound if available
                if hasattr(self, 'game_manager') and self.game_manager and hasattr(self.game_manager, 'sound_manager'):
                    self.game_manager.sound_manager.play_sound('explosion')
        
        elif self.laser_firing:
            # Firing phase - 0.8 seconds
            if current_time - self.laser_fire_time > 0.8:
                self.laser_firing = False
                self.laser_active = False
                self.laser_cooldown = current_time
                # Set cooldown before next laser attack
                self.can_use_laser = False
                # Reset after 5 seconds
                self.laser_reset_timer = current_time + 5.0
        
        # Check if laser cooldown is over
        if not self.can_use_laser and hasattr(self, 'laser_reset_timer') and current_time > self.laser_reset_timer:
            self.can_use_laser = True
    
    def take_damage(self, damage=1):
        """Handle taking damage with shield logic."""
        # If exploding, can't take damage
        if self.is_exploding:
            return False
            
        damage_taken = False
        
        # If shield is active, damage the shield first
        if self.has_shield:
            self.shield -= damage
            if self.shield <= 0:
                self.has_shield = False
                self.shield = 0
                self.shield_broken = True
                self.shield_break_time = time.time()
                self.shield_break_sound_played = False
                self.shield_regen_cooldown = 5.0  # 5 seconds to regenerate shield
            damage_taken = True
            return damage_taken  # Shield absorbed all damage, don't damage health
        else:
            # No shield, damage health directly
            self.health -= damage
            damage_taken = True
            
            # Update attack phase based on health
            if self.health <= 1:
                self.attack_phase = 3  # Critical phase
                if not self.berserk_mode:
                    self.berserk_mode = True
                    self.base_speed *= 1.2  # 20% speed increase in berserk mode
            elif self.health <= 2:
                self.attack_phase = 2  # Damaged phase
            
            # Check if dead
            if self.health <= 0:
                self.start_death_explosion()
                
        return damage_taken
    
    def start_death_explosion(self):
        """Start the death explosion sequence."""
        self.is_exploding = True
        self.explosion_radius = 0
        self.explosion_damage_dealt = False
        # Death explosion sound will be played by game manager
    
    def handle_explosion(self, delta_time):
        """Handle the death explosion animation and damage."""
        # Grow the explosion
        self.explosion_radius += self.explosion_growth_rate * delta_time
        
        # Check if explosion should deal damage to player
        if not self.explosion_damage_dealt and self.explosion_radius >= 50:
            # The actual damage will be handled by the game manager
            self.explosion_damage_dealt = True
        
        # Check if explosion is complete
        if self.explosion_radius >= self.explosion_max_radius:
            self.kill()  # Remove the enemy
    
    def draw(self, surface):
        """Override draw method to handle shield and explosion effects."""
        # If exploding, draw explosion instead of ship
        if self.is_exploding:
            self.draw_explosion(surface)
            return
            
        # Draw laser effects if active
        if self.laser_active:
            if self.laser_charging:
                self.draw_laser_warning(surface)
            elif self.laser_firing:
                self.draw_laser_beam(surface)
            
        # Draw shield if active
        if self.has_shield:
            self.draw_shield(surface)
        
        # Draw the enemy ship
        surface.blit(self.image, self.rect)
        
        # Draw hitbox if debug mode is enabled
        if DEBUG_HITBOXES:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
        
        # Draw bullets
        for bullet in self.bullets:
            # Adjust bullet drawing based on direction (horizontal or vertical)
            if 'speed' in bullet and bullet['speed'] < 0:  # Horizontal bullet (moving left)
                bullet_rect = pygame.Rect(
                    bullet['x'],
                    bullet['y'] - bullet['height'] // 2,
                    bullet['width'],
                    bullet['height']
                )
                
                # Draw a more pronounced bullet
                pygame.draw.rect(surface, bullet['color'], bullet_rect)
                
                # Add a bright core to the bullet
                core_rect = pygame.Rect(
                    bullet['x'] + 1,
                    bullet['y'] - bullet['height'] // 4,
                    bullet['width'] // 2,
                    bullet['height'] // 2
                )
                pygame.draw.rect(surface, (255, 200, 200), core_rect)
            else:
                # Vertical bullet (moving down)
                bullet_rect = pygame.Rect(
                    bullet['x'] - bullet['width'] // 2,
                    bullet['y'],
                    bullet['width'],
                    bullet['height']
                )
                pygame.draw.rect(surface, bullet['color'], bullet_rect)
        
        # Draw health bar
        self.draw_health_bar(surface)
    
    def draw_shield(self, surface):
        """Draw the shield effect."""
        # Create shield surface with transparency
        shield_radius = max(self.rect.width, self.rect.height) // 2 + 5
        shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
        
        # Get shield opacity
        shield_opacity = self.shield_opacity
        
        # Calculate shield health percentage
        shield_health_percent = self.shield / self.max_shield
        
        # Draw shield with gradient effect and color based on health
        for i in range(3):
            thickness = 3 - i
            radius = shield_radius - i * 2
            alpha = min(255, shield_opacity - i*30)
            
            # Color changes based on shield health
            if shield_health_percent > 0.7:
                shield_color = (100, 150, 255, alpha)  # Blue shield (healthy)
            elif shield_health_percent > 0.3:
                shield_color = (150, 150, 255, alpha)  # Purple-blue shield (damaged)
            else:
                shield_color = (200, 100, 255, alpha)  # Purple shield (critical)
                
            pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), radius, thickness)
        
        # Add pulsing effect
        current_time = time.time()
        pulse = (math.sin(current_time * 5) + 1) / 2  # 0 to 1 pulsing
        
        # Draw inner glow with pulsing
        inner_radius = int(shield_radius * 0.7 * (0.9 + 0.1 * pulse))
        inner_color = (150, 200, 255, 50)  # Light blue, semi-transparent
        pygame.draw.circle(shield_surface, inner_color, (shield_radius, shield_radius), inner_radius, 1)
        
        # Draw shield on surface
        shield_rect = shield_surface.get_rect(center=self.rect.center)
        surface.blit(shield_surface, shield_rect)
        
        # Draw shield health percentage
        font = pygame.font.SysFont('Arial', 12)
        shield_text = font.render(f"{int(shield_health_percent * 100)}%", True, (150, 200, 255))
        text_pos = (self.rect.centerx - shield_text.get_width() // 2, 
                    self.rect.top - shield_text.get_height() - 5)
        surface.blit(shield_text, text_pos)
    
    def draw_laser_warning(self, surface):
        """Draw a warning for the laser attack."""
        # Calculate warning line properties
        current_time = time.time()
        charge_progress = (current_time - self.laser_charge_time) / 1.5  # 1.5 seconds charging
        
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
        warning_width = int(4 + charge_progress * 10)
        pygame.draw.line(surface, (r, g, b), start_pos, end_pos, warning_width)
        
        # Add pulsing glow effect around the line
        glow_width = warning_width + int(8 * pulse_factor)
        glow_color = (r, g, b, 100)  # Semi-transparent
        pygame.draw.line(surface, glow_color, start_pos, end_pos, glow_width)
        
        # Draw warning text that pulses
        font_size = int(16 + 6 * pulse_factor)  # Pulsing font size
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        warning_text = font.render("LASER CHARGING", True, (r, g, b))
        text_x = self.rect.left - warning_text.get_width() - 10
        text_y = self.laser_target_y - warning_text.get_height() // 2
        surface.blit(warning_text, (text_x, text_y))
    
    def draw_laser_beam(self, surface):
        """Draw the laser beam."""
        # Laser beam properties - start from the enemy's left side
        start_pos = (self.rect.left, self.laser_target_y)
        end_pos = (0, self.laser_target_y)
        
        # Draw main beam with pulsing effect
        current_time = time.time()
        pulse_factor = (math.sin(current_time * 20) + 1) / 2  # 0 to 1, faster pulse
        
        # Pulse the width slightly
        laser_width = 20  # Base laser width
        pulse_width = int(laser_width * (0.9 + 0.3 * pulse_factor))
        
        # Draw multiple layers for a more intense effect
        # Outer glow (semi-transparent)
        for i in range(4):
            glow_width = pulse_width + i * 5
            alpha = 150 - i * 30
            glow_color = (255, 100, 100, alpha)
            
            # Draw wider lines for glow effect
            pygame.draw.line(surface, glow_color, start_pos, end_pos, glow_width)
        
        # Main beam (solid)
        laser_color = (255, 50, 50)
        pygame.draw.line(surface, laser_color, start_pos, end_pos, pulse_width)
        
        # Bright core
        core_color = (255, 220, 220)
        pygame.draw.line(surface, core_color, start_pos, end_pos, pulse_width // 2)
        
        # Brightest center
        center_color = (255, 255, 255)
        pygame.draw.line(surface, center_color, start_pos, end_pos, pulse_width // 4)
        
        # Add impact effect at the left edge
        impact_x = 0
        impact_y = self.laser_target_y
        impact_radius = pulse_width + int(10 * pulse_factor)
        
        # Draw impact circles
        pygame.draw.circle(surface, (255, 200, 200), (impact_x, impact_y), impact_radius // 2)
        pygame.draw.circle(surface, (255, 100, 100, 200), (impact_x, impact_y), impact_radius)
        
        # Add bright center to impact
        pygame.draw.circle(surface, (255, 255, 255), (impact_x, impact_y), impact_radius // 4)
        
        # Add small particles around the impact point
        for _ in range(5):
            particle_x = impact_x + random.randint(-impact_radius, impact_radius//2)
            particle_y = impact_y + random.randint(-impact_radius, impact_radius)
            particle_size = random.randint(2, 4)
            pygame.draw.circle(surface, (255, 200, 200), (particle_x, particle_y), particle_size)
        
        # Check for collision with player
        self.check_laser_collision()
    
    def check_laser_collision(self):
        """Check if the laser beam is colliding with the player and apply damage."""
        if not hasattr(self, 'game_manager') or not self.game_manager or not self.game_manager.player:
            return
            
        # Create a collision rectangle for the laser beam
        laser_height = self.laser_width
        laser_rect = pygame.Rect(
            0,  # Left edge of screen
            self.laser_target_y - laser_height // 2,
            self.rect.left,  # Extends to the enemy's left edge
            laser_height
        )
        
        # Check for collision with player
        if laser_rect.colliderect(self.game_manager.player.hitbox):
            # Apply damage to player (once per frame)
            source_id = f"super_laser_{self.rect.x}_{self.rect.y}"
            self.game_manager.player.take_damage(
                self.game_manager.testing_mode and self.game_manager.ui_manager.god_mode,
                damage=2,  # Laser deals 2 damage
                source_id=source_id
            )
            
            # Play hit sound
            if hasattr(self.game_manager, 'sound_manager'):
                self.game_manager.sound_manager.play_sound('explosion')
    
    def draw_explosion(self, surface):
        """Draw the death explosion effect."""
        # Create explosion surface with transparency
        explosion_surface = pygame.Surface((self.explosion_max_radius * 2, self.explosion_max_radius * 2), pygame.SRCALPHA)
        
        # Calculate explosion colors based on radius
        outer_radius = self.explosion_radius
        mid_radius = self.explosion_radius * 0.7
        inner_radius = self.explosion_radius * 0.4
        
        # Draw outer explosion (orange)
        pygame.draw.circle(explosion_surface, (255, 100, 0, 150), 
                          (self.explosion_max_radius, self.explosion_max_radius), outer_radius)
        
        # Draw middle explosion (yellow)
        pygame.draw.circle(explosion_surface, (255, 200, 0, 200),
                          (self.explosion_max_radius, self.explosion_max_radius), mid_radius)
        
        # Draw inner explosion (white)
        pygame.draw.circle(explosion_surface, (255, 255, 255, 255),
                          (self.explosion_max_radius, self.explosion_max_radius), inner_radius)
        
        # Draw explosion on surface
        explosion_rect = explosion_surface.get_rect(center=self.rect.center)
        surface.blit(explosion_surface, explosion_rect)
    
    def draw_health_bar(self, surface):
        """Draw health and shield bars above the enemy."""
        # Health bar dimensions and position
        health_width = 40
        health_height = 4
        health_x = self.rect.centerx - health_width // 2
        health_y = self.rect.top - 12
        
        # Draw health background
        pygame.draw.rect(surface, (50, 50, 50), 
                        (health_x, health_y, health_width, health_height))
        
        # Draw health bar
        health_percent = self.health / self.max_health
        health_fill_width = int(health_width * health_percent)
        
        # Health color based on percentage
        if health_percent > 0.6:
            health_color = (0, 255, 0)  # Green
        elif health_percent > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red
            
        pygame.draw.rect(surface, health_color, 
                        (health_x, health_y, health_fill_width, health_height))
        
        # Draw shield bar if shield system is active
        if self.max_shield > 0:
            shield_y = self.rect.top - 8
            
            # Draw shield background
            pygame.draw.rect(surface, (50, 50, 50), 
                            (health_x, shield_y, health_width, health_height))
            
            # Draw shield bar
            if self.has_shield:
                shield_percent = self.shield / self.max_shield
                shield_fill_width = int(health_width * shield_percent)
                
                # Shield color based on percentage
                if shield_percent > 0.7:
                    shield_color = (100, 150, 255)  # Blue for healthy shield
                elif shield_percent > 0.3:
                    shield_color = (150, 150, 255)  # Purple-blue for damaged shield
                else:
                    shield_color = (200, 100, 255)  # Purple for critical shield
                    
                pygame.draw.rect(surface, shield_color, 
                                (health_x, shield_y, shield_fill_width, health_height))
