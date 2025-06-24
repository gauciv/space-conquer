"""
Game Manager for the Space Impact game.
Handles the main game loop and game state.
"""
import pygame
import sys
import random
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, ENEMY_SPAWN_DELAY, POWERUP_SPAWN_DELAY
from .utils.sound_manager import SoundManager
from .utils.asset_loader import AssetLoader
from .utils.ui_manager import UIManager
from .sprites.player import Player
from .sprites.enemy import Enemy
from .sprites.powerup import PowerUp
from .sprites.star import Star

class GameManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Impact")
        self.clock = pygame.time.Clock()
        
        # Initialize managers
        self.asset_loader = AssetLoader()
        self.sound_manager = SoundManager()
        self.ui_manager = UIManager(self.asset_loader, self.sound_manager)
        
        # Game state
        self.game_active = False
        self.score = 0
        
        # Create stars
        self.stars = [Star() for _ in range(50)]
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = None
        
        # Start background music
        self.sound_manager.play_music()
    
    def start_new_game(self):
        """Initialize a new game."""
        self.game_active = True
        self.score = 0
        
        # Play the game start sound
        if self.sound_manager.sound_enabled:
            # Temporarily lower music volume during start sound
            if self.sound_manager.music_enabled:
                self.sound_manager.temporarily_lower_music()
            
            self.sound_manager.play_sound('game_start')
            
            # Schedule music volume restoration after start sound finishes
            pygame.time.set_timer(pygame.USEREVENT, 600)  # 0.6 second timer
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Create player
        self.player = Player(self.asset_loader.get_image('player'), self.sound_manager)
        self.all_sprites.add(self.player)
        
        # Enemy spawn timer
        self.enemy_spawn_delay = ENEMY_SPAWN_DELAY
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        # Power-up spawn timer
        self.powerup_spawn_delay = POWERUP_SPAWN_DELAY
        self.last_powerup_spawn = pygame.time.get_ticks()
        
        # Difficulty scaling
        self.difficulty_timer = 0
        self.enemy_types = ['normal']
    
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.USEREVENT:
                # Restore music volume after start sound finishes
                if self.sound_manager.music_enabled:
                    self.sound_manager.restore_music_volume()
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Disable the timer
            
            elif event.type == pygame.USEREVENT + 1:
                # Restore music volume after game over sound finishes
                if self.sound_manager.music_enabled:
                    self.sound_manager.restore_music_volume()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Disable the timer
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_active and not self.ui_manager.settings_open:
                    self.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    # Close settings if open
                    if self.ui_manager.settings_open:
                        self.ui_manager.settings_open = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.ui_manager.handle_settings_click(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.ui_manager.handle_mouse_up()
            
            elif event.type == pygame.MOUSEMOTION:
                self.ui_manager.handle_mouse_motion(event.pos)
        
        return True
    
    def update(self):
        """Update game state."""
        # Update stars
        for star in self.stars:
            star.update()
            
        if not self.ui_manager.settings_open:
            if self.game_active and self.player:
                # Update player and sprites
                self.player.update()
                self.enemies.update()
                self.powerups.update()
                
                # Increase difficulty over time
                self.difficulty_timer += 1
                if self.difficulty_timer == 1200:  # After 20 seconds
                    if 'fast' not in self.enemy_types:
                        self.enemy_types.append('fast')
                elif self.difficulty_timer == 3600:  # After 1 minute
                    if 'tank' not in self.enemy_types:
                        self.enemy_types.append('tank')
                
                # Spawn enemies
                now = pygame.time.get_ticks()
                if now - self.last_enemy_spawn > self.enemy_spawn_delay:
                    self.last_enemy_spawn = now
                    enemy_type = random.choice(self.enemy_types)
                    enemy = Enemy(enemy_type, self.asset_loader.images)
                    self.enemies.add(enemy)
                    self.all_sprites.add(enemy)
                
                # Spawn power-ups
                if now - self.last_powerup_spawn > self.powerup_spawn_delay:
                    self.last_powerup_spawn = now
                    powerup = PowerUp(self.asset_loader.images)
                    self.powerups.add(powerup)
                    self.all_sprites.add(powerup)
                
                # Check for bullet collisions with enemies
                hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
                for enemy, bullets in hits.items():
                    enemy.health -= len(bullets)
                    if enemy.health <= 0:
                        self.score += enemy.points
                        enemy.kill()
                        # Play explosion sound
                        self.sound_manager.play_sound('explosion')
                
                # Check for player collision with enemies
                if pygame.sprite.spritecollide(self.player, self.enemies, True):
                    self.player.health -= 1
                    # Play explosion sound
                    self.sound_manager.play_sound('explosion')
                    if self.player.health <= 0:
                        self.game_active = False
                        # Play game over sound
                        self.sound_manager.play_sound('game_over')
                        # Lower music volume for game over sound
                        if self.sound_manager.music_enabled:
                            self.sound_manager.temporarily_lower_music(duration=1500)
                        # Schedule music volume restoration
                        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
                
                # Check for player collision with power-ups
                powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                for powerup in powerup_hits:
                    self.player.apply_powerup(powerup.type)
                    # Play powerup sound
                    self.sound_manager.play_sound('powerup')
    
    def draw(self):
        """Draw the game screen."""
        # Fill the screen with black
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            star.draw(self.screen)
        
        if not self.ui_manager.settings_open:
            if self.game_active and self.player:
                # Draw game elements
                self.all_sprites.draw(self.screen)
                self.player.draw(self.screen)
                
                # Show score and health
                self.ui_manager.show_score(self.screen, self.score, self.player.health)
            else:
                if self.score > 0:
                    self.ui_manager.show_game_over(self.screen, self.score)
                else:
                    self.ui_manager.show_start_screen(self.screen)
        else:
            # Draw settings panel
            self.ui_manager.draw_settings_panel(self.screen)
        
        # Always draw the settings button
        self.ui_manager.draw_settings_button(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw the screen
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point when run as a module."""
    game = GameManager()
    game.run()
