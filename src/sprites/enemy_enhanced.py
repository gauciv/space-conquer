"""
Enhanced Enemy sprites for the Space Impact game with death animations and sound effects.
"""
import pygame
import random
import math
import time
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_HITBOXES
from src.sprites.enemy import Enemy

class EnhancedEnemy(Enemy):
    """Enhanced version of the Enemy class with death animations."""
    
    def __init__(self, enemy_type, images, behavior_manager=None):
        super().__init__(enemy_type, images, behavior_manager)
        
        # Death animation properties
        self.is_dying = False
        self.death_start_time = 0
        self.death_duration = 0.3  # 300ms for the animation
        self.explosion_particles = []
        self.explosion_radius = 0
        self.explosion_max_radius = 30
        self.explosion_color = (255, 100, 50)  # Default orange explosion
        
        # Set explosion color based on enemy type
        if enemy_type == 'low':
            self.explosion_color = (255, 100, 50)  # Orange-red
        elif enemy_type == 'elite':
            self.explosion_color = (255, 200, 50)  # Yellow-orange
        elif enemy_type == 'super':
            self.explosion_color = (150, 100, 255)  # Purple
    
    def update(self):
        """Update the enemy based on its behavior pattern."""
        # Handle death animation if active
        if self.is_dying:
            self.update_death_animation()
            return
            
        # Otherwise, use the normal update method
        super().update()
    
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed."""
        # Handle shield for super-type enemy
        if self.enemy_type == 'super' and hasattr(self, 'has_shield') and self.has_shield:
            # Use the parent class method for shield handling
            return super().take_damage(damage)
        
        # Normal damage handling
        self.health -= damage
        
        # Set damage flash effect for super-type
        if self.enemy_type == 'super' and hasattr(self, 'damage_flash'):
            self.damage_flash = 10.0
        
        if self.health <= 0:
            # Start death animation
            self.start_death_animation()
            return True
        return False
    
    def start_death_animation(self):
        """Start the death animation sequence."""
        if not self.is_dying:  # Only start if not already dying
            self.is_dying = True
            self.death_start_time = time.time()
            
            # Create initial explosion particles
            self.create_explosion_particles()
            
            # Play death sound if game manager is available
            if hasattr(self, 'game_manager') and self.game_manager and hasattr(self.game_manager, 'sound_manager'):
                if self.enemy_type == 'low':
                    # Use the dedicated enemy death sound for low-type enemies
                    if 'enemy_death' in self.game_manager.sound_manager.sounds:
                        self.game_manager.sound_manager.play_sound('enemy_death')
                    else:
                        self.game_manager.sound_manager.play_sound('explosion')
                elif self.enemy_type == 'elite':
                    # Play explosion sound for elite enemies
                    self.game_manager.sound_manager.play_sound('explosion')
                else:
                    # Default to explosion sound
                    self.game_manager.sound_manager.play_sound('explosion')
    
    def create_explosion_particles(self):
        """Create explosion particles based on enemy type."""
        self.explosion_particles = []
        
        # Number of particles based on enemy type
        if self.enemy_type == 'low':
            num_particles = 25  # Increased from 15 to 25
        elif self.enemy_type == 'elite':
            num_particles = 30  # Increased from 20 to 30
        elif self.enemy_type == 'super':
            num_particles = 40  # Increased from 30 to 40
        else:
            num_particles = 25
        
        # Create particles
        for _ in range(num_particles):
            # Random velocity
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)  # Increased max speed from 150 to 200
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random size and lifetime
            size = random.randint(2, 6)  # Increased max size from 5 to 6
            lifetime = random.uniform(0.1, 0.4)  # Increased max lifetime from 0.3 to 0.4
            
            # Random color variation
            r, g, b = self.explosion_color
            r_var = random.randint(-30, 30)
            g_var = random.randint(-30, 30)
            b_var = random.randint(-30, 30)
            color = (
                max(0, min(255, r + r_var)),
                max(0, min(255, g + g_var)),
                max(0, min(255, b + b_var))
            )
            
            # Add particle
            self.explosion_particles.append({
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'vx': vx,
                'vy': vy,
                'size': size,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color
            })
            
        # Add some bright white particles for extra flash effect
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 250)  # Faster white particles
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.randint(3, 7)  # Larger white particles
            lifetime = random.uniform(0.05, 0.2)  # Shorter lifetime for flash effect
            
            # Add white particle
            self.explosion_particles.append({
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'vx': vx,
                'vy': vy,
                'size': size,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': (255, 255, 255)  # Pure white
            })
    
    def update_death_animation(self):
        """Update the death animation."""
        current_time = time.time()
        elapsed = current_time - self.death_start_time
        
        # Update explosion radius
        progress = elapsed / self.death_duration
        self.explosion_radius = int(self.explosion_max_radius * min(progress, 1.0))
        
        # Update particles
        delta_time = 0.016  # Assuming ~60fps
        for particle in self.explosion_particles[:]:
            # Move particle
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            
            # Decrease lifetime
            particle['lifetime'] -= delta_time
            
            # Remove dead particles
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
        
        # Check if animation is complete
        if elapsed >= self.death_duration:
            self.kill()  # Remove the enemy
    
    def draw(self, surface):
        """Draw the enemy with visual effects."""
        # If dying, draw explosion instead of ship
        if self.is_dying:
            self.draw_explosion(surface)
            return
        
        # Otherwise, use the normal draw method
        super().draw(surface)
    
    def draw_explosion(self, surface):
        """Draw the death explosion effect."""
        # Draw explosion ring
        if self.explosion_radius > 0:
            # Create a surface for the explosion ring
            ring_surface = pygame.Surface((self.explosion_radius * 2, self.explosion_radius * 2), pygame.SRCALPHA)
            
            # Calculate alpha based on progress
            progress = min(1.0, (time.time() - self.death_start_time) / self.death_duration)
            alpha = int(255 * (1 - progress))
            
            # Draw outer ring
            r, g, b = self.explosion_color
            pygame.draw.circle(ring_surface, (r, g, b, alpha), 
                             (self.explosion_radius, self.explosion_radius), 
                             self.explosion_radius, 2)
            
            # Draw inner ring - ensure color values don't exceed 255
            inner_radius = int(self.explosion_radius * 0.7)
            inner_r = min(255, r + 50)
            inner_g = min(255, g + 50)
            inner_b = min(255, b)
            pygame.draw.circle(ring_surface, (inner_r, inner_g, inner_b, alpha), 
                             (self.explosion_radius, self.explosion_radius), 
                             inner_radius, 2)
            
            # Draw innermost ring (brightest)
            innermost_radius = int(self.explosion_radius * 0.4)
            pygame.draw.circle(ring_surface, (255, 255, 200, alpha), 
                             (self.explosion_radius, self.explosion_radius), 
                             innermost_radius, 1)
            
            # Position and draw the ring
            ring_rect = ring_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(ring_surface, ring_rect)
        
        # Draw particles
        for particle in self.explosion_particles:
            # Calculate alpha based on remaining lifetime
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            
            # Create a surface for the particle
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Get particle color with alpha
            r, g, b = particle['color']
            color_with_alpha = (r, g, b, alpha)
            
            # Draw particle
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (particle['size'], particle['size']), 
                             particle['size'])
            
            # Position and draw the particle
            particle_rect = particle_surface.get_rect(center=(particle['x'], particle['y']))
            surface.blit(particle_surface, particle_rect)
            
        # Draw bright flash at the center at the beginning of the explosion
        progress = (time.time() - self.death_start_time) / self.death_duration
        if progress < 0.3:  # Only during the first 30% of the animation
            flash_alpha = int(255 * (1 - progress / 0.3))
            flash_radius = int(self.rect.width * 0.7 * (1 - progress / 0.3))
            
            # Create a surface for the flash
            flash_surface = pygame.Surface((flash_radius * 2, flash_radius * 2), pygame.SRCALPHA)
            
            # Draw flash
            pygame.draw.circle(flash_surface, (255, 255, 255, flash_alpha), 
                             (flash_radius, flash_radius), 
                             flash_radius)
            
            # Position and draw the flash
            flash_rect = flash_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(flash_surface, flash_rect)
        
        # Draw particles
        for particle in self.explosion_particles:
            # Calculate alpha based on remaining lifetime
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            
            # Create a surface for the particle
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Get particle color with alpha
            r, g, b = particle['color']
            color_with_alpha = (r, g, b, alpha)
            
            # Draw particle
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (particle['size'], particle['size']), 
                             particle['size'])
            
            # Position and draw the particle
            particle_rect = particle_surface.get_rect(center=(particle['x'], particle['y']))
            surface.blit(particle_surface, particle_rect)
            
        # Draw bright flash at the center at the beginning of the explosion
        progress = (time.time() - self.death_start_time) / self.death_duration
        if progress < 0.3:  # Only during the first 30% of the animation
            flash_alpha = int(255 * (1 - progress / 0.3))
            flash_radius = int(self.rect.width * 0.7 * (1 - progress / 0.3))
            
            # Create a surface for the flash
            flash_surface = pygame.Surface((flash_radius * 2, flash_radius * 2), pygame.SRCALPHA)
            
            # Draw flash
            pygame.draw.circle(flash_surface, (255, 255, 255, flash_alpha), 
                             (flash_radius, flash_radius), 
                             flash_radius)
            
            # Position and draw the flash
            flash_rect = flash_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(flash_surface, flash_rect)
