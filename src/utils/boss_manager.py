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
        self.mini_boss_dying = False
        self.main_boss_dying = False
    
    def reset(self):
        """Reset boss state."""
        # Clean up any existing bosses
        if self.mini_boss:
            self.mini_boss.kill()
        if self.main_boss:
            self.main_boss.kill()
            
        # Reset all boss-related variables
        self.mini_boss = None
        self.main_boss = None
        self.mini_boss_spawned = False
        self.main_boss_spawned = False
        self.mini_boss_dying = False
        self.main_boss_dying = False
        
        print("Boss manager reset - all bosses cleared")
    
    def spawn_boss(self, boss_type):
        """Spawn a boss of the specified type."""
        # First, clear any existing bosses
        self.reset()
        
        if boss_type == 'mini':
            # Create mini boss
            self.mini_boss = Boss('mini', self.game_manager.asset_loader, self.game_manager.sound_manager)
            # Add to all sprites group
            self.game_manager.all_sprites.add(self.mini_boss)
            self.mini_boss_spawned = True
            print(f"Mini boss spawned!")
            return self.mini_boss
        elif boss_type == 'main':
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
        # Update mini boss
        if self.mini_boss:
            # Update boss and check if death animation is complete
            animation_complete = self.mini_boss.update()
            if animation_complete:
                # Death animation complete, remove boss from all sprite groups
                self.mini_boss.kill()  # Remove from all sprite groups
                self.mini_boss = None
                self.mini_boss_dying = False
                print("Mini boss destroyed and removed!")
                
                # Notify phase manager that mini boss is defeated
                if hasattr(self.game_manager.phase_manager, 'handle_boss_defeated'):
                    self.game_manager.phase_manager.handle_boss_defeated('mini')
        
        # Update main boss
        if self.main_boss:
            # Update boss and check if death animation is complete
            animation_complete = self.main_boss.update()
            if animation_complete:
                # Death animation complete, remove boss from all sprite groups
                self.main_boss.kill()  # Remove from all sprite groups
                self.main_boss = None
                self.main_boss_dying = False
                print("Main boss destroyed and removed!")
                
                # Notify phase manager that main boss is defeated
                if hasattr(self.game_manager.phase_manager, 'handle_boss_defeated'):
                    self.game_manager.phase_manager.handle_boss_defeated('main')
    
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
        if self.mini_boss and not self.mini_boss.dying:
            self._handle_boss_collision(self.mini_boss, player)
        
        # Process main-boss collisions
        if self.main_boss and not self.main_boss.dying:
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
                    
                    # Set dying flag
                    if boss == self.mini_boss:
                        self.mini_boss_dying = True
                    elif boss == self.main_boss:
                        self.main_boss_dying = True
                    
                    return  # Exit after boss is defeated
        
        # Check boss bullets against player
        if hasattr(boss, 'bullets'):
            for bullet in list(boss.bullets):
                if player.hitbox.colliderect(bullet.hitbox):
                    bullet.kill()
                    god_mode = self.game_manager.testing_mode and self.game_manager.ui_manager.god_mode
                    source_id = f"boss_bullet_{bullet.rect.x}_{bullet.rect.y}"
                    if player.take_damage(god_mode, source_id=source_id):
                        if player.health <= 0:
                            if self.game_manager.testing_mode and not self.game_manager.ui_manager.god_mode:
                                # In test mode without god mode, start respawn countdown instead of game over
                                self.game_manager.ui_manager.start_respawn_countdown()
                            else:
                                # Normal game over
                                self.game_manager.game_state = self.game_manager.GAME_STATE_GAME_OVER
                                self.game_manager.sound_manager.play_sound('game_over')
        
        # Check direct collision between player and boss
        if player.hitbox.colliderect(boss.hitbox):
            god_mode = self.game_manager.testing_mode and self.game_manager.ui_manager.god_mode
            source_id = f"boss_body_{boss.boss_type}"
            if player.take_damage(god_mode, source_id=source_id):
                if player.health <= 0:
                    if self.game_manager.testing_mode and not self.game_manager.ui_manager.god_mode:
                        # In test mode without god mode, start respawn countdown instead of game over
                        self.game_manager.ui_manager.start_respawn_countdown()
                    else:
                        # Normal game over
                        self.game_manager.game_state = self.game_manager.GAME_STATE_GAME_OVER
                        self.game_manager.sound_manager.play_sound('game_over')
            if player.take_damage(god_mode, source_id=source_id):
                if player.health <= 0:
                    self.game_manager.game_state = self.game_manager.GAME_STATE_GAME_OVER
                    self.game_manager.sound_manager.play_sound('game_over')
    
    def has_active_boss(self):
        """Check if there's an active boss (not including dying bosses)."""
        return (self.mini_boss is not None and not self.mini_boss.dying) or \
               (self.main_boss is not None and not self.main_boss.dying)
               
    def has_any_boss(self):
        """Check if there's any boss, including dying ones."""
        return self.mini_boss is not None or self.main_boss is not None
