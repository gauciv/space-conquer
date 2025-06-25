"""
Game Manager for the Space Conquer game.
Handles the main game loop and game state.
Uses the new AssetManager for asset loading.
"""
import pygame
import sys
import random
import math
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, ENEMY_SPAWN_DELAY, POWERUP_SPAWN_DELAY
from .utils.asset_manager import AssetManager
from .utils.enhanced_sound_manager import EnhancedSoundManager
from .utils.ui_manager import UIManager
from .utils.background_manager import BackgroundManager
from .sprites.player import Player
from .sprites.enemy import Enemy
from .sprites.powerup import PowerUp
from .sprites.star import Star
from .sprites.boss import Boss

class GameManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Conquer")
        self.clock = pygame.time.Clock()
        
        # Initialize asset manager
        self.asset_manager = AssetManager()
        self.asset_manager.load_all_assets()
        
        # Initialize sound manager with asset manager
        self.sound_manager = EnhancedSoundManager(self.asset_manager)
        
        # Initialize UI manager
        self.ui_manager = UIManager(self.asset_manager, self.sound_manager)
        
        # Initialize background manager
        self.background_manager = BackgroundManager()
        
        # Game state constants
        self.GAME_STATE_MENU = 0
        self.GAME_STATE_PLAYING = 1
        self.GAME_STATE_GAME_OVER = 2
        
        # Current game state
        self.game_state = self.GAME_STATE_MENU
        self.score = 0
        
        # Create stars
        self.stars = [Star() for _ in range(50)]
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = None
        
        # Boss variables
        self.mini_boss = None
        self.main_boss = None
        self.mini_boss_spawned = False
        self.main_boss_spawned = False
        self.mini_boss_score_threshold = 750
        self.main_boss_score_threshold = 1500
        
        # Map system
        self.maps = [
            "Starlight's End"
        ]
        self.current_map = 0
        self.map_transition_timer = 0
        self.showing_map_name = False
        self.map_name_duration = 180  # 3 seconds at 60 FPS
        self.show_chapter_header = False  # Flag to control when to show the chapter name at the top
        
        # Enemy progression
        self.enemy_types_available = ['normal']
        self.enemy_progression = [
            {'score': 0, 'types': ['normal']},
            {'score': 200, 'types': ['normal', 'fast']},
            {'score': 400, 'types': ['normal', 'fast', 'drone']},
            {'score': 600, 'types': ['normal', 'fast', 'drone', 'tank']},
            {'score': 800, 'types': ['normal', 'fast', 'drone', 'tank', 'bomber']}
        ]
        self.enemy_spawn_rates = [1500, 1200, 900, 700, 500]  # ms between spawns for each map
        self.enemy_points = {
            'normal': 10,
            'fast': 15,
            'tank': 25,
            'drone': 20,
            'bomber': 30
        }
        
        # Testing mode
        self.testing_mode = False
        self.show_debug_info = False
        self.phase_markers = [
            {'name': 'Start', 'score': 0},
            {'name': 'Fast Enemies', 'score': 200},
            {'name': 'Drone Enemies', 'score': 400},
            {'name': 'Tank Enemies', 'score': 600},
            {'name': 'Bomber Enemies', 'score': 800},
            {'name': 'Mini-Boss', 'score': 750},
            {'name': 'Main Boss', 'score': 1500}
        ]
        
        # Start background music - use menu music by default
        self.sound_manager.play_music('menu')
    
    def start_new_game(self, testing_mode=False):
        """Initialize a new game."""
        self.game_state = self.GAME_STATE_PLAYING
        self.score = 0
        self.testing_mode = testing_mode
        
        # Play the game start sound
        if not testing_mode:
            self.sound_manager.play_sound('game_start')
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Create player
        player_image = self.asset_manager.get_image('player')
        self.player = Player(player_image, self.sound_manager)
        self.all_sprites.add(self.player)
        
        # Reset boss variables
        self.mini_boss = None
        self.main_boss = None
        self.mini_boss_spawned = False
        self.main_boss_spawned = False
        
        # Reset map variables
        self.current_map = 0
        self.enemy_types_available = ['normal']
        self.showing_map_name = True
        self.map_transition_timer = self.map_name_duration
        self.show_chapter_header = False  # Don't show the chapter header until intro is done
        
        # Switch to the Starlight's End music when starting the game
        self.sound_manager.play_music('starlight_end', fade_ms=2000)  # 2-second crossfade
        
        # Enemy spawn timer
        self.enemy_spawn_delay = self.enemy_spawn_rates[0]
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        # Power-up spawn timer
        self.powerup_spawn_delay = POWERUP_SPAWN_DELAY
        self.last_powerup_spawn = pygame.time.get_ticks()
    
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Toggle settings panel
                    self.ui_manager.settings_open = not self.ui_manager.settings_open
                
                elif event.key == pygame.K_SPACE:
                    if self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        # Start normal game with SPACE from menu
                        self.start_new_game(testing_mode=False)
                    elif self.game_state == self.GAME_STATE_GAME_OVER and not self.ui_manager.settings_open:
                        # Restart after game over
                        self.start_new_game(testing_mode=False)
                
                elif event.key == pygame.K_t:
                    if self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        # Start test mode with T from menu
                        self.start_new_game(testing_mode=True)
                    elif self.game_state == self.GAME_STATE_GAME_OVER and not self.ui_manager.settings_open:
                        # Restart in test mode after game over
                        self.start_new_game(testing_mode=True)
                
                # Testing mode keys
                elif self.testing_mode and self.game_state == self.GAME_STATE_PLAYING:
                    if event.key == pygame.K_1:
                        # Spawn mini-boss
                        if not self.mini_boss:
                            mini_boss_image = self.asset_manager.get_image('mini_boss')
                            self.mini_boss = Boss(mini_boss_image, 'mini', SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
                            self.all_sprites.add(self.mini_boss)
                    
                    elif event.key == pygame.K_2:
                        # Spawn main boss
                        if not self.main_boss:
                            main_boss_image = self.asset_manager.get_image('main_boss')
                            self.main_boss = Boss(main_boss_image, 'main', SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2)
                            self.all_sprites.add(self.main_boss)
                    
                    elif event.key == pygame.K_3:
                        # Add 100 score
                        self.score += 100
                    
                    elif event.key == pygame.K_4:
                        # Add health
                        if self.player:
                            self.player.health = min(self.player.health + 1, self.player.max_health)
                    
                    elif event.key == pygame.K_5:
                        # Toggle rapid fire
                        if self.player:
                            self.player.rapid_fire = not self.player.rapid_fire
                            self.player.rapid_fire_timer = 600 if self.player.rapid_fire else 0
                    
                    elif event.key == pygame.K_6:
                        # Increase speed
                        if self.player:
                            self.player.speed += 1
                    
                    elif event.key == pygame.K_0:
                        # Toggle debug info
                        self.show_debug_info = not self.show_debug_info
            
            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Handle settings button click
                    settings_result = self.ui_manager.handle_settings_click(event.pos)
                    
                    if settings_result:
                        # Play click sound
                        self.sound_manager.play_sound('select')
                        
                        # Check if we need to return to main menu from settings
                        if settings_result == "main_menu":
                            # Return to main menu with proper reset
                            self.game_state = self.GAME_STATE_MENU
                            self.score = 0
                            self.player = None
                            self.enemies.empty()
                            self.powerups.empty()
                            self.all_sprites.empty()
                            self.mini_boss = None
                            self.main_boss = None
                            
                            # Switch back to menu music with fade
                            self.sound_manager.play_music('menu', fade_ms=1500)
                    
                    # Handle game over screen button clicks
                    elif self.game_state == self.GAME_STATE_GAME_OVER and not self.ui_manager.settings_open:
                        if self.ui_manager.start_button_rect and self.ui_manager.start_button_rect.collidepoint(event.pos):
                            # Restart game
                            self.start_new_game(testing_mode=False)
                        elif self.ui_manager.main_menu_button_rect and self.ui_manager.main_menu_button_rect.collidepoint(event.pos):
                            # Return to main menu with proper reset
                            self.game_state = self.GAME_STATE_MENU
                            self.score = 0
                            self.player = None
                            self.enemies.empty()
                            self.powerups.empty()
                            self.all_sprites.empty()
                            self.mini_boss = None
                            self.main_boss = None
                    
                    # Handle main menu button clicks
                    elif self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        if self.ui_manager.start_button_rect and self.ui_manager.start_button_rect.collidepoint(event.pos):
                            # Start game
                            self.start_new_game(testing_mode=False)
                        elif self.ui_manager.test_button_rect and self.ui_manager.test_button_rect.collidepoint(event.pos):
                            # Start test mode
                            self.start_new_game(testing_mode=True)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Handle slider drag end
                self.ui_manager.handle_mouse_up()
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle slider dragging
                self.ui_manager.handle_mouse_motion(event.pos)
            
            # Handle timer events
            elif event.type == pygame.USEREVENT:
                # Restore music volume after game start sound
                if self.sound_manager.music_enabled:
                    self.sound_manager.restore_music_volume()
            
            elif event.type == pygame.USEREVENT + 1:
                # Restore music volume after game over sound
                if self.sound_manager.music_enabled:
                    self.sound_manager.restore_music_volume()
        
        return True
    
    def update(self):
        """Update game state."""
        # Update based on game state
        if self.game_state == self.GAME_STATE_PLAYING:
            # Update all sprites
            self.all_sprites.update()
            
            # Update map transition timer
            if self.showing_map_name:
                self.map_transition_timer -= 1
                if self.map_transition_timer <= 0:
                    self.showing_map_name = False
                    self.show_chapter_header = True
            
            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time - self.last_enemy_spawn > self.enemy_spawn_delay:
                self.last_enemy_spawn = current_time
                
                # Don't spawn regular enemies if a boss is active
                if not self.mini_boss and not self.main_boss:
                    # Choose enemy type based on available types
                    enemy_type = random.choice(self.enemy_types_available)
                    
                    # Get enemy image
                    enemy_image = self.asset_manager.get_image(f"{enemy_type}_enemy")
                    
                    # Create enemy
                    enemy = Enemy(enemy_image, enemy_type)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
            
            # Spawn power-ups
            if current_time - self.last_powerup_spawn > self.powerup_spawn_delay:
                self.last_powerup_spawn = current_time
                
                # Choose power-up type
                powerup_type = random.choice(['health', 'speed', 'rapid_fire'])
                
                # Get power-up image
                powerup_image = self.asset_manager.get_image(f"{powerup_type}_powerup")
                
                # Create power-up
                powerup = PowerUp(powerup_image, powerup_type)
                self.all_sprites.add(powerup)
                self.powerups.add(powerup)
            
            # Update enemy types based on score
            for progression in self.enemy_progression:
                if self.score >= progression['score']:
                    self.enemy_types_available = progression['types']
            
            # Check for mini-boss spawn
            if self.score >= self.mini_boss_score_threshold and not self.mini_boss_spawned and not self.mini_boss:
                self.mini_boss_spawned = True
                mini_boss_image = self.asset_manager.get_image('mini_boss')
                self.mini_boss = Boss(mini_boss_image, 'mini', SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
                self.all_sprites.add(self.mini_boss)
            
            # Check for main boss spawn
            if self.score >= self.main_boss_score_threshold and not self.main_boss_spawned and not self.main_boss:
                self.main_boss_spawned = True
                main_boss_image = self.asset_manager.get_image('main_boss')
                self.main_boss = Boss(main_boss_image, 'main', SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2)
                self.all_sprites.add(self.main_boss)
            
            # Check for player bullet collisions with enemies
            if self.player:
                for bullet in self.player.bullets:
                    # Check for collisions with regular enemies
                    enemy_hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
                    if enemy_hits:
                        bullet.kill()
                        for enemy in enemy_hits:
                            # Play explosion sound
                            self.sound_manager.play_sound('explosion')
                            
                            # Add score based on enemy type
                            self.score += self.enemy_points.get(enemy.enemy_type, 10)
                    
                    # Check for collisions with mini-boss
                    if self.mini_boss and pygame.sprite.collide_rect(bullet, self.mini_boss):
                        bullet.kill()
                        if self.mini_boss.take_damage():
                            # Mini-boss defeated
                            self.mini_boss = None
                            
                            # Play explosion sound
                            self.sound_manager.play_sound('explosion')
                            
                            # Add score
                            self.score += 100
                    
                    # Check for collisions with main boss
                    if self.main_boss and pygame.sprite.collide_rect(bullet, self.main_boss):
                        bullet.kill()
                        if self.main_boss.take_damage():
                            # Main boss defeated
                            self.main_boss = None
                            
                            # Play explosion sound
                            self.sound_manager.play_sound('explosion')
                            
                            # Add score
                            self.score += 200
                
                # Check for player collision with enemies
                enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if enemy_hits:
                    # Use the new take_damage method which handles invulnerability and sound
                    damage_applied = self.player.take_damage()
                    
                    if damage_applied and self.player.health <= 0:
                        self.game_state = self.GAME_STATE_GAME_OVER
                        # Play game over sound
                        self.sound_manager.play_sound('game_over')
                        # Switch back to menu music with fade
                        self.sound_manager.play_music('menu', fade_ms=3000)  # 3-second crossfade
                
                # Check for player collision with boss bullets
                if self.mini_boss:
                    boss_bullet_hits = pygame.sprite.spritecollide(self.player, self.mini_boss.bullets, True)
                    if boss_bullet_hits and self.player.take_damage():
                        if self.player.health <= 0:
                            self.game_state = self.GAME_STATE_GAME_OVER
                            # Play game over sound
                            self.sound_manager.play_sound('game_over')
                            # Switch back to menu music with fade
                            self.sound_manager.play_music('menu', fade_ms=3000)  # 3-second crossfade
                
                if self.main_boss:
                    boss_bullet_hits = pygame.sprite.spritecollide(self.player, self.main_boss.bullets, True)
                    if boss_bullet_hits and self.player.take_damage():
                        if self.player.health <= 0:
                            self.game_state = self.GAME_STATE_GAME_OVER
                            # Play game over sound
                            self.sound_manager.play_sound('game_over')
                            # Switch back to menu music with fade
                            self.sound_manager.play_music('menu', fade_ms=3000)  # 3-second crossfade
                
                # Check for player collision with power-ups
                powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                for powerup in powerup_hits:
                    # Play power-up sound
                    self.sound_manager.play_sound('powerup')
                    
                    # Apply power-up effect
                    if powerup.powerup_type == 'health':
                        self.player.health = min(self.player.health + 1, self.player.max_health)
                    elif powerup.powerup_type == 'speed':
                        self.player.speed += 1
                    elif powerup.powerup_type == 'rapid_fire':
                        self.player.rapid_fire = True
                        self.player.rapid_fire_timer = 600  # 10 seconds at 60 FPS
    
    def draw(self):
        """Draw the game."""
        # Fill the screen with black
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            star.draw(self.screen)
        
        # Draw based on game state
        if self.game_state == self.GAME_STATE_PLAYING:
            # Draw all sprites
            self.all_sprites.draw(self.screen)
            
            # Draw UI
            self.ui_manager.show_score(self.screen, self.score, self.player.health if self.player else 0)
            
            # Draw boss health bars
            if self.mini_boss:
                self.mini_boss.draw_health_bar(self.screen)
            
            if self.main_boss:
                self.main_boss.draw_health_bar(self.screen)
            
            # Draw map name during transition
            if self.showing_map_name:
                # Create a semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 50))
                
                # Draw map name
                font = pygame.font.SysFont('Arial', 36, bold=True)
                text = font.render(self.maps[self.current_map], True, (255, 255, 255))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            
            # Draw chapter header
            if self.show_chapter_header:
                font = pygame.font.SysFont('Arial', 24, bold=True)
                text = font.render(f"Chapter {self.current_map + 1}: {self.maps[self.current_map]}", True, (200, 200, 255))
                self.screen.blit(text, (20, 20))
            
            # Draw debug info
            if self.testing_mode and self.show_debug_info:
                debug_font = pygame.font.SysFont('Arial', 16)
                debug_info = [
                    f"FPS: {int(self.clock.get_fps())}",
                    f"Score: {self.score}",
                    f"Health: {self.player.health if self.player else 0}",
                    f"Speed: {self.player.speed if self.player else 0}",
                    f"Rapid Fire: {'Yes' if self.player and self.player.rapid_fire else 'No'}",
                    f"Enemy Types: {', '.join(self.enemy_types_available)}",
                    f"Enemies: {len(self.enemies)}",
                    f"Power-ups: {len(self.powerups)}",
                    f"Mini-Boss: {'Active' if self.mini_boss else 'Inactive'}",
                    f"Main Boss: {'Active' if self.main_boss else 'Inactive'}"
                ]
                
                for i, info in enumerate(debug_info):
                    text = debug_font.render(info, True, (255, 255, 255))
                    self.screen.blit(text, (SCREEN_WIDTH - 200, 50 + i * 20))
                
                # Draw phase markers
                for i, marker in enumerate(self.phase_markers):
                    if self.score >= marker['score']:
                        color = (0, 255, 0)  # Green for passed phases
                    else:
                        color = (255, 0, 0)  # Red for upcoming phases
                    
                    text = debug_font.render(f"{marker['name']}: {marker['score']}", True, color)
                    self.screen.blit(text, (SCREEN_WIDTH - 200, 250 + i * 20))
            
            # Draw settings panel if open
            if self.ui_manager.settings_open:
                self.ui_manager.draw_settings_panel(self.screen, self.game_state)
        
        elif self.game_state == self.GAME_STATE_GAME_OVER:
            # Show game over screen
            self.ui_manager.show_game_over(self.screen, self.score)
        elif self.game_state == self.GAME_STATE_MENU:
            # Show start screen
            self.ui_manager.show_start_screen(self.screen, self.testing_mode)
        
        # Draw settings button (always visible)
        self.ui_manager.draw_settings_button(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the game loop."""
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw the game
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
