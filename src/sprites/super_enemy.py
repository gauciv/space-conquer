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
        self.max_shield = 2
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
        
        # Draw shield with gradient effect
        for i in range(3):
            thickness = 3 - i
            radius = shield_radius - i * 2
            alpha = min(255, shield_opacity - i*30)
            shield_color = (100, 150, 255, alpha)  # Blue shield
            pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), radius, thickness)
        
        # Draw shield on surface
        shield_rect = shield_surface.get_rect(center=self.rect.center)
        surface.blit(shield_surface, shield_rect)
    
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
                shield_color = (100, 150, 255)  # Blue for shield
                pygame.draw.rect(surface, shield_color, 
                                (health_x, shield_y, shield_fill_width, health_height))
