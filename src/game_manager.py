"""
Game Manager for the Space Impact game.
Handles the main game loop and game state.
"""
import pygame
import sys
import random
import math
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, ENEMY_SPAWN_DELAY, POWERUP_SPAWN_DELAY, DEBUG_HITBOXES
from .utils.sound_manager import SoundManager
from .utils.asset_loader import AssetLoader
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
        
        # Initialize managers
        self.asset_loader = AssetLoader()
        self.sound_manager = SoundManager()
        self.ui_manager = UIManager(self.asset_loader, self.sound_manager)
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
        
        # Game active property
        self.game_active = False
        
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
        
        # Start background music
        self.sound_manager.play_music()
    
    def start_new_game(self, testing_mode=False):
        """Initialize a new game."""
        self.game_state = self.GAME_STATE_PLAYING
        self.game_active = True
        self.score = 0
        self.testing_mode = testing_mode
        
        # Play the game start sound
        if self.sound_manager.sound_enabled and not testing_mode:
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
        
        # Enemy spawn timer
        self.enemy_spawn_delay = self.enemy_spawn_rates[0]
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        # Power-up spawn timer
        self.powerup_spawn_delay = POWERUP_SPAWN_DELAY
        self.last_powerup_spawn = pygame.time.get_ticks()
        
        # If testing mode, give player some advantages
        if testing_mode:
            self.player.health = 10  # Extra health for testing
            self.player.max_health = 10
            self.player.speed = 8    # Extra speed for testing
    
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
                if event.key == pygame.K_SPACE:
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
                elif event.key == pygame.K_ESCAPE:
                    # Close settings if open
                    if self.ui_manager.settings_open:
                        self.ui_manager.settings_open = False
                        # Play a sound effect for feedback
                        if 'menu' in self.sound_manager.sounds:
                            self.sound_manager.play_sound('menu')
                        elif 'select' in self.sound_manager.sounds:
                            self.sound_manager.play_sound('select')
                
                # Testing mode hotkeys (only active in testing mode)
                if self.testing_mode and self.game_active:
                    if event.key == pygame.K_1:
                        # Spawn mini-boss
                        if not self.mini_boss and not self.main_boss:
                            self.mini_boss = Boss('mini', self.asset_loader, self.sound_manager)
                    elif event.key == pygame.K_2:
                        # Spawn main boss
                        if not self.mini_boss and not self.main_boss:
                            self.main_boss = Boss('main', self.asset_loader, self.sound_manager)
                    elif event.key == pygame.K_3:
                        # Add 100 score
                        self.score += 100
                        self.update_enemy_types()
                    elif event.key == pygame.K_4:
                        # Add health
                        if self.player:
                            self.player.health = min(self.player.health + 1, self.player.max_health)
                    elif event.key == pygame.K_5:
                        # Toggle rapid fire
                        if self.player:
                            self.player.rapid_fire = not self.player.rapid_fire
                            if self.player.rapid_fire:
                                self.player.shoot_delay = 100
                                self.player.rapid_fire_timer = 600  # 10 seconds at 60 FPS
                    elif event.key == pygame.K_6:
                        # Increase speed
                        if self.player:
                            self.player.speed += 1
                    elif event.key == pygame.K_0:
                        # Toggle debug info
                        self.show_debug_info = not self.show_debug_info
                    elif event.key == pygame.K_d:
                        # Toggle debug hitboxes
                        from src.config import DEBUG_HITBOXES
                        import src.config as config
                        config.DEBUG_HITBOXES = not config.DEBUG_HITBOXES
                        print(f"Debug hitboxes: {'ON' if config.DEBUG_HITBOXES else 'OFF'}")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Handle settings button click
                    settings_result = self.ui_manager.handle_settings_click(event.pos)
                    if settings_result:
                        # Play a sound effect for feedback when clicking UI elements
                        if 'select' in self.sound_manager.sounds:
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
                            self.mini_boss_spawned = False
                            self.main_boss_spawned = False
                            # Play a menu sound if available
                            if 'menu' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('menu')
                    
                    # Handle main menu button clicks
                    elif self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        if self.ui_manager.start_button_rect and self.ui_manager.start_button_rect.collidepoint(event.pos):
                            self.start_new_game(testing_mode=False)
                        elif self.ui_manager.test_button_rect and self.ui_manager.test_button_rect.collidepoint(event.pos):
                            self.start_new_game(testing_mode=True)
                    
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
                            self.mini_boss_spawned = False
                            self.main_boss_spawned = False
                            # Play a menu sound if available
                            if 'menu' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('menu')
                            elif 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                            self.main_boss = None
                            self.mini_boss_spawned = False
                            self.main_boss_spawned = False
                            # Play a menu sound if available
                            if 'menu' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('menu')
                            elif 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                    # Handle phase marker clicks in testing mode
                    elif self.testing_mode and self.game_active:
                        for marker in self.phase_markers:
                            marker_rect = pygame.Rect(SCREEN_WIDTH - 150, 150 + self.phase_markers.index(marker) * 30, 140, 25)
                            if marker_rect.collidepoint(event.pos):
                                self.score = marker['score']
                                self.update_enemy_types()
                                print(f"Skipped to phase: {marker['name']} (Score: {marker['score']})")
                                break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.ui_manager.handle_mouse_up()
            
            elif event.type == pygame.MOUSEMOTION:
                self.ui_manager.handle_mouse_motion(event.pos)
        
        return True
    
    def update(self):
        """Update game state."""
        # Update stars and background
        for star in self.stars:
            star.update()
        
        if self.game_state == self.GAME_STATE_PLAYING:
            self.background_manager.update()
            self.game_active = True
        elif self.game_state == self.GAME_STATE_GAME_OVER:
            self.game_active = False
            
        if not self.ui_manager.settings_open:
            if self.game_state == self.GAME_STATE_PLAYING and self.player:
                # Handle map name display
                if self.showing_map_name:
                    self.map_transition_timer -= 1
                    if self.map_transition_timer <= 0:
                        self.showing_map_name = False
                        self.show_chapter_header = True  # Now show the chapter header at the top
                
                # Update player and sprites
                self.player.update()
                self.enemies.update()
                self.powerups.update()
                
                # Update bosses if they exist
                if self.mini_boss:
                    self.mini_boss.update()
                if self.main_boss:
                    self.main_boss.update()
                
                # Check for enemy type progression based on score
                self.update_enemy_types()
                
                # Check for boss spawning based on score
                if not self.testing_mode:  # Only auto-spawn bosses in normal mode
                    self.check_boss_spawning()
                
                # Spawn enemies (only if no boss is active)
                if not self.mini_boss and not self.main_boss:
                    now = pygame.time.get_ticks()
                    if now - self.last_enemy_spawn > self.enemy_spawn_delay:
                        self.last_enemy_spawn = now
                        enemy_type = random.choice(self.enemy_types_available)
                        enemy = Enemy(enemy_type, self.asset_loader.images)
                        enemy.points = self.enemy_points[enemy_type]  # Set points based on enemy type
                        self.enemies.add(enemy)
                        self.all_sprites.add(enemy)
                
                # Spawn power-ups
                now = pygame.time.get_ticks()
                if now - self.last_powerup_spawn > self.powerup_spawn_delay:
                    self.last_powerup_spawn = now
                    powerup = PowerUp(self.asset_loader.images)
                    self.powerups.add(powerup)
                    self.all_sprites.add(powerup)
                
                # Check for bullet collisions with enemies
                for enemy in self.enemies:
                    for bullet in self.player.bullets:
                        if enemy.hitbox.colliderect(bullet.hitbox):
                            enemy.health -= 1
                            bullet.kill()
                            if enemy.health <= 0:
                                # Apply score multiplier if active
                                points = enemy.points * self.player.score_multiplier
                                self.score += points
                                enemy.kill()
                                # Play explosion sound
                                self.sound_manager.play_sound('explosion')
                
                # Check for bullet collisions with mini-boss
                if self.mini_boss:
                    for bullet in self.player.bullets:
                        if self.mini_boss.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.mini_boss.take_damage(1):
                                # Mini-boss defeated
                                # Apply score multiplier if active
                                points = self.mini_boss.score_value * self.player.score_multiplier
                                self.score += points
                                self.mini_boss = None
                                # Play explosion sound (could be a special boss explosion)
                                self.sound_manager.play_sound('explosion')
                
                # Check for bullet collisions with main boss
                if self.main_boss:
                    for bullet in self.player.bullets:
                        if self.main_boss.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.main_boss.take_damage(1):
                                # Main boss defeated
                                # Apply score multiplier if active
                                points = self.main_boss.score_value * self.player.score_multiplier
                                self.score += points
                                self.main_boss = None
                                # Play explosion sound (could be a special boss explosion)
                                self.sound_manager.play_sound('explosion')
                
                # Check for player collision with enemies
                for enemy in self.enemies:
                    if self.player.hitbox.colliderect(enemy.hitbox):
                        # Use the new take_damage method which handles invulnerability and sound
                        damage_applied = self.player.take_damage()
                        enemy.kill()  # Remove the enemy that collided with player
                        
                        if damage_applied and self.player.health <= 0:
                            self.game_state = self.GAME_STATE_GAME_OVER
                            self.game_active = False
                            # Play game over sound
                            self.sound_manager.play_sound('game_over')
                            # Lower music volume for game over sound
                            if self.sound_manager.music_enabled:
                                self.sound_manager.temporarily_lower_music(duration=1500)
                            # Schedule music volume restoration
                            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
                
                # Check for player collision with boss bullets
                if self.mini_boss:
                    for bullet in self.mini_boss.bullets:
                        if self.player.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.player.take_damage():
                                if self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    # Play game over sound
                                    self.sound_manager.play_sound('game_over')
                                    # Lower music volume for game over sound
                                    if self.sound_manager.music_enabled:
                                        self.sound_manager.temporarily_lower_music(duration=1500)
                                    # Schedule music volume restoration
                                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
                
                if self.main_boss:
                    for bullet in self.main_boss.bullets:
                        if self.player.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.player.take_damage():
                                if self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    # Play game over sound
                                    self.sound_manager.play_sound('game_over')
                                    # Lower music volume for game over sound
                                    if self.sound_manager.music_enabled:
                                        self.sound_manager.temporarily_lower_music(duration=1500)
                                    # Schedule music volume restoration
                                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
                
                # Check for player collision with power-ups
                for powerup in self.powerups:
                    if self.player.hitbox.colliderect(powerup.hitbox):
                        self.player.apply_powerup(powerup.type)
                        # Play powerup sound
                        self.sound_manager.play_sound('powerup')
                        powerup.kill()
    
    def update_enemy_types(self):
        """Update available enemy types based on score."""
        for progression in self.enemy_progression:
            if self.score >= progression['score']:
                self.enemy_types_available = progression['types']
    
    def check_boss_spawning(self):
        """Check if it's time to spawn a boss based on score."""
        # Spawn mini-boss at score threshold
        if self.score >= self.mini_boss_score_threshold and not self.mini_boss_spawned and not self.mini_boss and not self.main_boss:
            self.mini_boss = Boss('mini', self.asset_loader, self.sound_manager)
            self.mini_boss_spawned = True
        
        # Spawn main boss at score threshold
        if self.score >= self.main_boss_score_threshold and not self.main_boss_spawned and not self.main_boss and not self.mini_boss:
            self.main_boss = Boss('main', self.asset_loader, self.sound_manager)
            self.main_boss_spawned = True
    
    def draw(self):
        """Draw the game screen."""
        # Fill with deep space color for Starlight's End
        deep_space = (5, 5, 15)  # Very dark blue-black
        self.screen.fill(deep_space)
        
        # Draw themed background elements
        if self.game_state == self.GAME_STATE_PLAYING:
            self.background_manager.draw(self.screen)
        
        # Draw stars
        for star in self.stars:
            star.draw(self.screen)
        
        if not self.ui_manager.settings_open:
            if self.game_state == self.GAME_STATE_PLAYING and self.player:
                # Draw game elements
                self.all_sprites.draw(self.screen)
                self.player.draw(self.screen)
                
                # Draw enemies with enhanced effects
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                
                # Draw powerups with enhanced effects
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                
                # Draw bosses if they exist
                if self.mini_boss:
                    self.mini_boss.draw(self.screen)
                if self.main_boss:
                    self.main_boss.draw(self.screen)
                
                # Show current map name at the top only after intro
                if self.show_chapter_header:
                    map_font = pygame.font.SysFont('Arial', 22)
                    map_text = map_font.render(f"Chapter {self.current_map + 1}: {self.maps[self.current_map]}", True, (255, 255, 255))
                    self.screen.blit(map_text, (SCREEN_WIDTH // 2 - map_text.get_width() // 2, 10))
                
                # Show map name during transition
                if self.showing_map_name:
                    # Create semi-transparent overlay
                    overlay = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))
                    self.screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 60))
                    
                    # Draw chapter and map name
                    chapter_font = pygame.font.SysFont('Arial', 28)
                    map_font = pygame.font.SysFont('Arial', 36)
                    
                    chapter_text = chapter_font.render(f"Chapter {self.current_map + 1}:", True, (200, 200, 255))
                    map_name = map_font.render(self.maps[self.current_map], True, (255, 255, 255))
                    
                    self.screen.blit(chapter_text, (SCREEN_WIDTH // 2 - chapter_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
                    self.screen.blit(map_name, (SCREEN_WIDTH // 2 - map_name.get_width() // 2, SCREEN_HEIGHT // 2))
                
                # Show score and health
                self.ui_manager.show_score(self.screen, self.score, self.player.health, self.player.max_health)
                
                # Show score multiplier if active
                if self.player.score_multiplier > 1:
                    multiplier_font = pygame.font.SysFont('Arial', 22)
                    multiplier_text = multiplier_font.render(f"Score x{self.player.score_multiplier}", True, (255, 215, 0))  # Gold color
                    self.screen.blit(multiplier_text, (SCREEN_WIDTH - multiplier_text.get_width() - 10, 40))
                    
                    # Show remaining time
                    time_left = self.player.score_multiplier_timer // 60  # Convert frames to seconds
                    time_text = multiplier_font.render(f"Time: {time_left}s", True, (255, 215, 0))
                    self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 70))
                
                # Show debug info if enabled
                if self.show_debug_info and self.testing_mode:
                    debug_font = pygame.font.SysFont('Arial', 16)
                    debug_info = [
                        f"Testing Mode: Active",
                        f"FPS: {int(self.clock.get_fps())}",
                        f"Enemies: {len(self.enemies)}",
                        f"Player Speed: {self.player.speed}",
                        f"Rapid Fire: {'On' if self.player.rapid_fire else 'Off'}",
                        f"Enemy Spawn Rate: {self.enemy_spawn_delay}ms",
                        f"Mini-Boss: {'Active' if self.mini_boss else 'Inactive'}",
                        f"Main Boss: {'Active' if self.main_boss else 'Inactive'}",
                        f"Enemy Types: {', '.join(self.enemy_types_available)}",
                        f"Debug Hitboxes: {'ON' if DEBUG_HITBOXES else 'OFF'} (Press D to toggle)"
                    ]
                    
                    for i, info in enumerate(debug_info):
                        text = debug_font.render(info, True, (200, 200, 200))
                        self.screen.blit(text, (10, 80 + i * 20))
                
                # Draw phase markers in testing mode
                if self.testing_mode:
                    marker_font = pygame.font.SysFont('Arial', 16)
                    marker_title = pygame.font.SysFont('Arial', 18, bold=True)
                    
                    # Draw title
                    title_text = marker_title.render("Phase Markers:", True, (255, 255, 100))
                    self.screen.blit(title_text, (SCREEN_WIDTH - 150, 120))
                    
                    # Draw markers
                    for i, marker in enumerate(self.phase_markers):
                        # Create marker rectangle
                        marker_rect = pygame.Rect(SCREEN_WIDTH - 150, 150 + i * 30, 140, 25)
                        
                        # Highlight current phase
                        if self.score >= marker['score'] and (i == len(self.phase_markers) - 1 or self.score < self.phase_markers[i + 1]['score']):
                            pygame.draw.rect(self.screen, (100, 100, 50), marker_rect)
                            pygame.draw.rect(self.screen, (255, 255, 100), marker_rect, 2)
                        else:
                            pygame.draw.rect(self.screen, (50, 50, 50), marker_rect)
                            pygame.draw.rect(self.screen, (150, 150, 150), marker_rect, 1)
                        
                        # Draw marker text
                        text = marker_font.render(f"{marker['name']}", True, (255, 255, 255))
                        self.screen.blit(text, (SCREEN_WIDTH - 145, 153 + i * 30))
            
            # Draw appropriate screen based on game state
            elif self.game_state == self.GAME_STATE_GAME_OVER:
                # Show game over screen
                self.ui_manager.show_game_over(self.screen, self.score)
            elif self.game_state == self.GAME_STATE_MENU:
                # Show start screen
                self.ui_manager.show_start_screen(self.screen, self.testing_mode)
        else:
            # Draw settings panel - pass the current game state
            self.ui_manager.draw_settings_panel(self.screen, self.game_state)
        
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
