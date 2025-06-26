import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_INITIAL_HEALTH

class GameManagerPatch:
    def handle_player_death(self):
        """Handle player death based on game mode."""
        if self.testing_mode and not self.ui_manager.god_mode:
            # In test mode without god mode, start respawn countdown instead of game over
            self.ui_manager.start_respawn_countdown()
            print("Player died in test mode - starting respawn countdown")
            return True
        else:
            # Normal game over
            self.game_state = self.GAME_STATE_GAME_OVER
            self.game_active = False
            # Play game over sound
            self.sound_manager.play_sound('game_over')
            # Lower music volume for game over sound
            if self.sound_manager.music_enabled:
                self.sound_manager.temporarily_lower_music(duration=1500)
            # Schedule music volume restoration
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
            return False
            
    def respawn_player(self):
        """Respawn the player in test mode."""
        # Reset player health
        self.player.health = PLAYER_INITIAL_HEALTH
        
        # Reset player position
        self.player.rect.centerx = 100
        self.player.rect.centery = SCREEN_HEIGHT // 2
        
        # Make player temporarily invulnerable
        self.player.invulnerable = True
        self.player.invulnerable_timer = pygame.time.get_ticks()
        self.player.invulnerable_duration = 3000  # 3 seconds of invulnerability after respawn
        
        # Clear nearby enemies for safety
        for enemy in self.enemies:
            if enemy.rect.x < SCREEN_WIDTH // 2:
                enemy.kill()
                
        # Play respawn sound if available
        if 'powerup' in self.sound_manager.sounds:
            self.sound_manager.play_sound('powerup')
            
        print("Player respawned in test mode")
