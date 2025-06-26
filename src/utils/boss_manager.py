"""
Boss Manager for the Space Impact game.
Handles boss creation, updates, and collisions.
"""
import pygame
from ..sprites.boss import Boss

class BossManager:
    """Manages boss entities and their interactions."""
    
    def __init__(self, game_manager):
        """Initialize the boss manager."""
        self.game_manager = game_manager
        self.mini_boss = None
        self.main_boss = None
        self.mini_boss_spawned = False
        self.main_boss_spawned = False
    
    def reset(self):
        """Reset boss state."""
        self.mini_boss = None
        self.main_boss = None
        self.mini_boss_spawned = False
        self.main_boss_spawned = False
    
    def spawn_boss(self, boss_type):
        """Spawn a boss of the specified type."""
        if boss_type == 'mini' and not self.mini_boss_spawned:
            # Create mini boss
            self.mini_boss = Boss('mini', self.game_manager.asset_loader, self.game_manager.sound_manager)
            # Add to all sprites group
            self.game_manager.all_sprites.add(self.mini_boss)
            self.mini_boss_spawned = True
            print(f"Mini boss spawned!")
            return self.mini_boss
        elif boss_type == 'main' and not self.main_boss_spawned:
            # Create main boss
            self.main_boss = Boss('main', self.game_manager.asset_loader, self.game_manager.sound_manager)
            # Add to all sprites group
            self.game_manager.all_sprites.add(self.main_boss)
            self.main_boss_spawned = True
            print(f"Main boss spawned!")
            return self.main_boss
        return None
    
    def update(self):
        """Update all active bosses."""
        if self.mini_boss:
            self.mini_boss.update()
        
        if self.main_boss:
            self.main_boss.update()
    
    def draw(self, surface):
        """Draw all active bosses."""
        if self.mini_boss:
            self.mini_boss.draw(surface)
        
        if self.main_boss:
            self.main_boss.draw(surface)
    
    def handle_collisions(self, player):
        """Handle all boss-related collisions."""
        if not player or not hasattr(player, 'bullets'):
            return
        
        # Process mini-boss collisions
        if self.mini_boss:
            self._handle_boss_collision(self.mini_boss, player)
        
        # Process main-boss collisions
        if self.main_boss:
            self._handle_boss_collision(self.main_boss, player)
    
    def _handle_boss_collision(self, boss, player):
        """Handle collisions for a specific boss."""
        # Only process if boss is properly initialized
        if not hasattr(boss, 'hitbox'):
            return
            
        # Check player bullets against boss
        for bullet in list(player.bullets):
            if bullet.hitbox.colliderect(boss.hitbox):
                bullet.kill()
                if boss.take_damage(1):
                    # Boss defeated
                    points = boss.score_value * player.score_multiplier
                    self.game_manager.score += points
                    
                    # Clear the appropriate boss reference
                    if boss == self.mini_boss:
                        self.mini_boss = None
                    elif boss == self.main_boss:
                        self.main_boss = None
                    
                    # Play explosion sound
                    self.game_manager.sound_manager.play_sound('explosion')
                    return  # Exit after boss is defeated
        
        # Check boss bullets against player
        if hasattr(boss, 'bullets'):
            for bullet in list(boss.bullets):
                if player.hitbox.colliderect(bullet.hitbox):
                    bullet.kill()
                    god_mode = self.game_manager.testing_mode and self.game_manager.ui_manager.god_mode
                    if player.take_damage(god_mode):
                        if player.health <= 0:
                            self.game_manager.game_state = self.game_manager.GAME_STATE_GAME_OVER
                            self.game_manager.sound_manager.play_sound('game_over')
    
    def has_active_boss(self):
        """Check if there's an active boss."""
        return self.mini_boss is not None or self.main_boss is not None
