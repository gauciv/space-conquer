"""
Game Manager for the Space Impact game.
Handles the main game loop and game state.
"""
import pygame
import sys
import random
import math
import time
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, ENEMY_SPAWN_DELAY, POWERUP_SPAWN_DELAY, DEBUG_HITBOXES, PLAYER_INITIAL_HEALTH
from .utils.sound_manager import SoundManager
from .utils.asset_loader import AssetLoader
from .utils.ui_manager import UIManager
from .utils.background_manager import BackgroundManager
from .utils.phase_manager import PhaseManager
from .utils.boss_manager import BossManager
from .utils.enemy_behavior_manager import EnemyBehaviorManager
from .sprites.player import Player
from .sprites.enemy import Enemy
from .sprites.enemy_enhanced import EnhancedEnemy
from .sprites.super_enemy import SuperEnemy
from .sprites.super_enemy_enhanced import SuperEnemyEnhanced
from .sprites.powerup import PowerUp
from .sprites.star import Star
from .sprites.asteroid import Asteroid
from .sprites.debris import Debris

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
        self.ui_manager.game_manager = self  # Add reference to game manager
        self.background_manager = BackgroundManager(self.asset_loader)
        self.enemy_behavior_manager = EnemyBehaviorManager()  # Initialize enemy behavior manager
        
        # Game state constants
        self.GAME_STATE_MENU = 0
        self.GAME_STATE_PLAYING = 1
        self.GAME_STATE_GAME_OVER = 2
        self.GAME_STATE_RESPAWNING = 3  # New state for respawning in test mode
        
        # Current game state
        self.game_state = self.GAME_STATE_MENU
        self.score = 0
        
        # Create stars
        self.stars = [Star() for _ in range(50)]
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.debris = pygame.sprite.Group()
        self.player = None
        
        # Game active property
        self.game_active = False
        
        # Boss manager
        self.boss_manager = BossManager(self)
        
        # Map system
        self.maps = [
            "Starlight's End"
        ]
        self.current_map = 0
        self.map_transition_timer = 0
        self.showing_map_name = False
        self.map_name_duration = 45  # 0.75 seconds at 60 FPS (further reduced from 1 second)
        self.show_chapter_header = False  # Flag to control when to show the chapter name at the top
        
        # Enemy progression
        self.enemy_types_available = ['normal']
        self.enemy_progression = [
            {'score': 0, 'types': ['low']},
            {'score': 200, 'types': ['low', 'elite']},
            {'score': 400, 'types': ['low', 'elite', 'super']}
        ]
        self.enemy_spawn_rates = [1500, 1200, 900, 700, 500]  # ms between spawns for each map
        self.enemy_points = {
            'low': 30,    # Low-type enemy
            'elite': 50,  # Elite-type enemy (increased from 45 to 50 due to enhanced burst capability)
            'super': 150  # Super-type enemy (doubled from 75 to 150 due to enhanced juggernaut capabilities)
        }
        
        # Testing mode
        self.testing_mode = False
        self.show_debug_info = False
        
        # Initialize phase manager
        self.phase_manager = PhaseManager(self)
        
        # Start menu music
        self.sound_manager.play_music('menu')
    
    def start_new_game(self, testing_mode=False):
        """Initialize a new game."""
        self.game_state = self.GAME_STATE_PLAYING
        self.game_active = True
        self.score = 0
        self.testing_mode = testing_mode
        
        # Stop menu music before switching to gameplay music
        self.sound_manager.stop_music()
        print(f"[DEBUG] After stop_music, current_music: {self.sound_manager.current_music}")
        
        # DEBUG: Print which music track is about to be played
        print(f"[DEBUG] Map: {self.maps[self.current_map] if hasattr(self, 'maps') and self.maps else 'Unknown'}, Music: starlight_end")
        
        # Switch to map-specific music (starlight_end) and play start sound
        if not testing_mode:
            self.sound_manager.play_music('starlight_end')
            
            if self.sound_manager.sound_enabled:
                # Temporarily lower music volume during start sound
                if self.sound_manager.music_enabled:
                    self.sound_manager.temporarily_lower_music()
                
                self.sound_manager.play_sound('game_start')
                
                # Schedule music volume restoration after start sound finishes
                pygame.time.set_timer(pygame.USEREVENT, 600)  # 0.6 second timer
        else:
            # In testing mode, just switch music without sound effects
            self.sound_manager.play_music('starlight_end')
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.debris = pygame.sprite.Group()
        
        # Create player
        self.player = Player(self.asset_loader.get_image('player'), self.sound_manager)
        self.all_sprites.add(self.player)
        
        # Store a reference to the asset loader for bullet images
        self.player.asset_loader = self.asset_loader
        
        # Reset boss manager
        self.boss_manager.reset()
        
        # If testing mode, open testing panel
        if testing_mode:
            # Keep default health (3)
            self.ui_manager.testing_panel_open = True
            self.ui_manager.testing_panel_collapsed = True
        
        # Reset map variables
        self.current_map = 0
        self.enemy_types_available = ['low']  # Start with low-type enemies
        self.showing_map_name = True
        self.map_transition_timer = self.map_name_duration
        self.show_chapter_header = False  # Don't show the chapter header until intro is done
        
        # Reset phase manager
        self.phase_manager = PhaseManager(self)
        
        # Enemy spawn timer
        self.enemy_spawn_delay = self.enemy_spawn_rates[0]
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        # Power-up spawn timer
        self.powerup_spawn_delay = POWERUP_SPAWN_DELAY
        self.last_powerup_spawn = pygame.time.get_ticks()
        
        # Asteroid spawn timer
        self.asteroid_spawn_delay = 3333  # ~3.3 seconds between asteroid spawns (5000/1.5)
        self.last_asteroid_spawn = pygame.time.get_ticks()
        
        # Debris spawn timer
        self.debris_spawn_delay = 5333  # ~5.3 seconds between debris spawns (8000/1.5)
        self.last_debris_spawn = pygame.time.get_ticks()
        
        # Enemy speed and powerup drop chance modifiers
        self.enemy_speed_multiplier = 1.0
        self.powerup_drop_chance_modifier = 0.0
        
        # Enemy spawn cooldown (after boss defeat)
        self.enemy_spawn_cooldown = 0
        
        # Boss warning effect
        self.showing_boss_warning = False
        self.boss_warning_timer = 0
        self.boss_warning_duration = 180  # 3 seconds at 60 FPS
        self.boss_warning_type = None
        
        # If testing mode, give player some advantages but not extra health by default
        if testing_mode:
            # Only give extra health if god mode is enabled
            if self.ui_manager.god_mode:
                self.player.health = 10
                self.player.max_health = 10
            
            # Always give extra speed for better testing experience
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
                # Check for Ctrl+D to toggle the robot button
                if event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.ui_manager.toggle_robot_button()
                    # Play a sound effect for feedback
                    if 'select' in self.sound_manager.sounds:
                        self.sound_manager.play_sound('select')
                
                elif event.key == pygame.K_SPACE:
                    if self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        # Start normal game with SPACE from menu
                        self.start_new_game(testing_mode=False)
                    elif self.game_state == self.GAME_STATE_GAME_OVER and not self.ui_manager.settings_open:
                        # Restart after game over
                        self.start_new_game(testing_mode=False)
                    # Note: We don't handle shooting here - it's handled in the Player.update() method
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
                        if not self.boss_manager.has_active_boss():
                            self.boss_manager.spawn_boss('mini')
                    elif event.key == pygame.K_2:
                        # Spawn main boss
                        if not self.boss_manager.has_active_boss():
                            self.boss_manager.spawn_boss('main')
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
                    # Handle testing panel clicks if in testing mode
                    if self.testing_mode and self.ui_manager.testing_panel_open:
                        if self.ui_manager.handle_testing_panel_click(event.pos, self.phase_manager):
                            # Apply god mode if enabled
                            if self.player and self.ui_manager.god_mode:
                                self.player.health = self.player.max_health
                            
                            # Play a sound effect for feedback
                            if 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                            continue
                    
                    # Handle phase marker clicks in testing mode
                    if self.testing_mode and self.game_active:
                        if self.phase_manager.handle_click(event.pos):
                            # Play a sound effect for feedback
                            if 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                            continue
                    
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
                            # Reset boss manager
                            self.boss_manager.reset()
                            # Switch back to menu music
                            self.sound_manager.switch_music('menu')
                            # Play a menu sound if available
                            if 'menu' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('menu')
                    
                    # Handle main menu button clicks
                    elif self.game_state == self.GAME_STATE_MENU and not self.ui_manager.settings_open:
                        if self.ui_manager.start_button_rect and self.ui_manager.start_button_rect.collidepoint(event.pos):
                            self.start_new_game(testing_mode=self.testing_mode)
                        # Handle robot button click
                        elif self.ui_manager.show_robot_button and self.ui_manager.robot_button_rect.collidepoint(event.pos):
                            self.start_new_game(testing_mode=True)
                            # Play a sound effect for feedback
                            if 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                    
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
                            # Reset boss manager
                            self.boss_manager.reset()
                            
                            # Reset testing mode when returning to main menu
                            if not pygame.key.get_mods() & pygame.KMOD_CTRL:  # Only reset if Ctrl is not held
                                self.testing_mode = False
                                self.ui_manager.testing_panel_open = False
                                self.ui_manager.show_robot_button = False
                            
                            # Switch back to menu music
                            self.sound_manager.switch_music('menu')
                            # Play a menu sound if available
                            if 'menu' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('menu')
                            elif 'select' in self.sound_manager.sounds:
                                self.sound_manager.play_sound('select')
                    # Handle phase marker clicks in testing mode
                    elif self.testing_mode and self.game_active:
                        for i, phase in enumerate(self.phase_manager.phases):
                            if hasattr(phase, 'rect') and phase.rect.collidepoint(event.pos):
                                self.phase_manager.skip_to_phase(i)
                                print(f"Skipped to phase: {phase.name} (Time: {phase.time_threshold})")
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
        elif self.game_state == self.GAME_STATE_RESPAWNING:
            # Keep the game state frozen during respawn
            self.game_active = False
            
        # Handle respawn in test mode
        if self.testing_mode and self.ui_manager.respawning:
            if self.ui_manager.update_respawn_countdown():
                # Respawn complete, reset player
                self.respawn_player()
            
        if not self.ui_manager.settings_open:
            if self.game_state == self.GAME_STATE_PLAYING and self.player:
                # Apply God Mode if enabled in testing mode (only restore health, don't make invulnerable)
                if self.testing_mode and self.ui_manager.god_mode and self.player:
                    self.player.health = self.player.max_health
                
                # Handle map name display
                if self.showing_map_name:
                    self.map_transition_timer -= 1
                    if self.map_transition_timer <= 0:
                        self.showing_map_name = False
                        self.show_chapter_header = True  # Now show the chapter header at the top
                        # Reset the game timer to 0:00 when chapter showcase ends
                        self.phase_manager.game_time = 0
                        self.phase_manager.last_update_time_ms = time.time() * 1000
                
                # Update player and sprites
                self.player.update()
                
                # Apply speed multiplier to enemies
                for enemy in self.enemies:
                    enemy.speed_multiplier = self.enemy_speed_multiplier
                
                # Update all sprites
                self.enemies.update()
                self.powerups.update()
                self.asteroids.update()
                self.debris.update()
                
                # Update bosses
                boss_spawned = self.boss_manager.update()
                
                # Handle boss music
                if self.boss_manager.has_active_boss():
                    # Switch to boss music if we're not already playing it
                    if self.sound_manager.get_current_track() != 'boss_battle':
                        print("[DEBUG] Switching to boss battle music")
                        self.sound_manager.switch_music('boss_battle')
                else:
                    # Only switch back to gameplay music if we were playing boss music and there's no active boss
                    if self.sound_manager.get_current_track() == 'boss_battle':
                        print("[DEBUG] Boss defeated, switching back to gameplay music")
                        self.sound_manager.switch_music('starlight_end')
                
                # Update phase manager based on time
                self.phase_manager.update()
                
                # Check if we should spawn an asteroid during boss fights
                if self.boss_manager.has_active_boss() and self.phase_manager.should_spawn_boss_asteroid():
                    # Spawn an asteroid during boss fight
                    asteroid = Asteroid(self.asset_loader.images, self.sound_manager)
                    self.asteroids.add(asteroid)
                    self.all_sprites.add(asteroid)
                
                # Update boss warning effect
                if self.showing_boss_warning:
                    self.boss_warning_timer -= 1
                    if self.boss_warning_timer <= 0:
                        self.showing_boss_warning = False
                
                # Only spawn entities if timer has started, no boss is active, and enemy spawn cooldown is over
                if (not self.showing_map_name and 
                    self.phase_manager.game_time > 0 and 
                    not self.boss_manager.has_active_boss() and 
                    self.enemy_spawn_cooldown <= 0):
                    
                    # Apply frenzy mode if active - 3x faster spawning during frenzy (0.33 multiplier)
                    spawn_rate_multiplier = 0.33 if self.phase_manager.frenzy_mode else 1.0
                    
                    # Spawn enemies if available in current phase
                    if self.enemy_types_available:
                        now = pygame.time.get_ticks()
                        if now - self.last_enemy_spawn > self.enemy_spawn_delay * spawn_rate_multiplier:
                            self.last_enemy_spawn = now
                            
                            # Enhanced enemy type selection with weighted probabilities
                            weighted_types = self.enemy_types_available.copy()
                            
                            # Check if we're in a phase with super enemies
                            if 'super' in self.enemy_types_available:
                                # Create a weighted list with 25% more super enemies (reduced from 50%)
                                base_count = len(weighted_types)
                                super_boost = max(1, int(base_count * 0.25))
                                
                                # Add extra super entries
                                for _ in range(super_boost):
                                    weighted_types.append('super')
                                    
                                print("Super enemy spawn chance boosted by 25%")
                            
                            # Also boost elite enemies if available
                            if 'elite' in self.enemy_types_available:
                                # Create a weighted list with 15% more elite enemies
                                base_count = len(weighted_types)
                                elite_boost = max(1, int(base_count * 0.15))
                                
                                # Add extra elite entries
                                for _ in range(elite_boost):
                                    weighted_types.append('elite')
                            
                            # Select from weighted list
                            enemy_type = random.choice(weighted_types)
                            
                            # Check if we're trying to spawn a super-type enemy
                            if enemy_type == 'super':
                                # Count current super enemies on screen
                                super_count = sum(1 for e in self.enemies if hasattr(e, 'enemy_type') and e.enemy_type == 'super')
                                
                                # Limit to maximum of 2 super enemies on screen at once
                                if super_count >= 2:
                                    # Spawn elite enemy instead if available, otherwise low
                                    if 'elite' in self.enemy_types_available:
                                        enemy_type = 'elite'
                                    else:
                                        enemy_type = 'low'
                            
                            # Create enemy with behavior manager
                            if enemy_type == 'super':
                                # Use the specialized SuperEnemyEnhanced class for super-type enemies
                                enemy = SuperEnemyEnhanced(self.asset_loader.images, self.enemy_behavior_manager)
                            else:
                                # Use the regular Enemy class for other enemy types
                                enemy = EnhancedEnemy(enemy_type, self.asset_loader.images, self.enemy_behavior_manager)
                                
                            enemy.points = self.enemy_points[enemy_type]  # Set points based on enemy type
                            enemy.speed_multiplier = self.enemy_speed_multiplier  # Apply speed multiplier
                            enemy.game_manager = self  # Give enemy a reference to the game manager
                            
                            self.enemies.add(enemy)
                            self.all_sprites.add(enemy)
                    
                    # Spawn asteroids after 30 seconds
                    current_phase = self.phase_manager.get_current_phase()
                    if current_phase and current_phase.time_threshold >= 30:
                        now = pygame.time.get_ticks()
                        if now - self.last_asteroid_spawn > self.asteroid_spawn_delay * spawn_rate_multiplier:
                            self.last_asteroid_spawn = now
                            asteroid = Asteroid(self.asset_loader.images, self.sound_manager)
                            
                            # Apply powerup drop chance modifier
                            base_drop_chance = asteroid.powerup_drop_chance
                            modified_chance = base_drop_chance + self.powerup_drop_chance_modifier
                            asteroid.powerup_drop_chance = max(0.0, min(1.0, modified_chance))  # Clamp between 0 and 1
                            
                            self.asteroids.add(asteroid)
                            self.all_sprites.add(asteroid)
                    
                    # Spawn debris after 45 seconds
                    if current_phase and current_phase.time_threshold >= 45:
                        now = pygame.time.get_ticks()
                        if now - self.last_debris_spawn > self.debris_spawn_delay * spawn_rate_multiplier:
                            self.last_debris_spawn = now
                            debris = Debris(self.asset_loader.images)
                            
                            # Apply speed multiplier if in super monsters phase or later
                            if current_phase and current_phase.time_threshold >= 60:
                                debris.speed_multiplier = 1.15
                                
                            self.debris.add(debris)
                            self.all_sprites.add(debris)
                else:
                    # Decrease enemy spawn cooldown if it's active
                    if self.enemy_spawn_cooldown > 0:
                        self.enemy_spawn_cooldown -= 1/60  # Decrease by 1 second per 60 frames
                
                # Check for bullet collisions with enemies
                for enemy in list(self.enemies):  # Use a copy of the list to avoid modification during iteration
                    for bullet in list(self.player.bullets):  # Use a copy of the list to avoid modification during iteration
                        if enemy.hitbox.colliderect(bullet.hitbox):
                            # Apply damage to enemy
                            bullet.kill()
                            
                            # Check if enemy is destroyed
                            if enemy.take_damage(1):
                                # Apply score multiplier if active
                                points = enemy.points * self.player.score_multiplier
                                self.score += points
                                
                                # The enemy's take_damage method will handle starting the death animation
                                # The enemy will be removed automatically when the animation completes
                
                # Check for bullet collisions with asteroids
                for asteroid in self.asteroids:
                    for bullet in self.player.bullets:
                        if asteroid.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if asteroid.take_damage(1):
                                # Asteroid destroyed, check if it should drop a powerup
                                if asteroid.should_drop_powerup():
                                    powerup = PowerUp(self.asset_loader.images, powerup_type=asteroid.powerup_type)
                                    powerup.rect.center = asteroid.rect.center
                                    self.powerups.add(powerup)
                                    self.all_sprites.add(powerup)
                                
                                # Apply score multiplier if active
                                points = asteroid.points * self.player.score_multiplier
                                self.score += points
                
                # Check for bullet collisions with debris
                for debris_obj in self.debris:
                    for bullet in self.player.bullets:
                        if debris_obj.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if debris_obj.take_damage(1):
                                # Apply score multiplier if active
                                points = debris_obj.points * self.player.score_multiplier
                                self.score += points
                                debris_obj.kill()
                
                # Handle all boss-related collisions
                self.boss_manager.handle_collisions(self.player)
                
                # Check for player collision with enemies
                for enemy in self.enemies:
                    # Check for collision with enemy bullets
                    if hasattr(enemy, 'bullets'):
                        for bullet in list(enemy.bullets):
                            # Create a bullet rect for collision detection based on direction
                            if 'direction' in bullet and bullet['direction'] == 'left':
                                # Horizontal bullet (moving left)
                                bullet_rect = pygame.Rect(
                                    bullet['x'] - bullet['width'] // 2,
                                    bullet['y'] - bullet['height'] // 2,
                                    bullet['width'],
                                    bullet['height']
                                )
                            elif 'vx' in bullet and 'vy' in bullet:
                                # Bullet with velocity components (for super enemies)
                                bullet_rect = pygame.Rect(
                                    bullet['x'] - bullet['width'] // 2,
                                    bullet['y'] - bullet['height'] // 2,
                                    bullet['width'],
                                    bullet['height']
                                )
                            else:
                                # Vertical bullet (moving down)
                                bullet_rect = pygame.Rect(
                                    bullet['x'] - bullet['width'] // 2,
                                    bullet['y'],
                                    bullet['width'],
                                    bullet['height']
                                )
                            
                            if self.player.hitbox.colliderect(bullet_rect):
                                # Remove the bullet
                                enemy.bullets.remove(bullet)
                                
                                # Apply damage to player
                                source_id = f"enemy_bullet_{enemy.rect.x}_{enemy.rect.y}"
                                damage_applied = self.player.take_damage(
                                    self.testing_mode and self.ui_manager.god_mode,
                                    source_id=source_id,
                                    damage=bullet['damage']
                                )
                                
                                if damage_applied and self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    self.game_active = False
                                    # Play game over sound
                                    self.sound_manager.play_sound('game_over')
                    
                    # Check for collision with enemy body
                    if self.player.hitbox.colliderect(enemy.hitbox):
                        # Use the new take_damage method with source ID for cooldown
                        source_id = f"enemy_{enemy.rect.x}_{enemy.rect.y}"
                        damage_applied = self.player.take_damage(
                            self.testing_mode and self.ui_manager.god_mode,  # Only god mode if both testing AND god mode enabled
                            source_id=source_id
                        )
                        
                        # Only kill the enemy if damage was applied and it's not a super enemy
                        # Super enemies have their own death sequence
                        if damage_applied:
                            if hasattr(enemy, 'is_exploding') and not enemy.is_exploding:
                                enemy.kill()  # Remove the enemy that collided with player
                        
                        if damage_applied and self.player.health <= 0:
                            self.game_state = self.GAME_STATE_GAME_OVER
                            self.game_active = False
                    
                    # Check for super enemy explosions
                    if isinstance(enemy, SuperEnemy) and enemy.is_exploding:
                        # Check if explosion should damage player
                        if enemy.explosion_damage_dealt and not enemy.explosion_damage_applied:
                            # Calculate distance from explosion center to player
                            dx = enemy.rect.centerx - self.player.rect.centerx
                            dy = enemy.rect.centery - self.player.rect.centery
                            distance = math.sqrt(dx*dx + dy*dy)
                            
                            # Check if player is within explosion radius
                            if distance < enemy.explosion_radius:
                                # Apply damage to player
                                source_id = f"explosion_{enemy.rect.x}_{enemy.rect.y}"
                                damage_applied = self.player.take_damage(
                                    self.testing_mode and self.ui_manager.god_mode,
                                    damage=2,  # Explosions deal 2 damage
                                    source_id=source_id
                                )
                                enemy.explosion_damage_applied = True
                                
                                # Play explosion sound
                                self.sound_manager.play_sound('explosion')
                                
                                # Check if player died
                                if damage_applied and self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    self.game_active = False
                        
                        # Play shield break sound if needed
                        if enemy.shield_broken and not enemy.shield_break_sound_played:
                            # Play shield break sound
                            self.sound_manager.play_sound('explosion')  # Use explosion sound for now
                            enemy.shield_break_sound_played = True
                            # Lower music volume for game over sound
                            if self.sound_manager.music_enabled:
                                self.sound_manager.temporarily_lower_music(duration=1500)
                            # Schedule music volume restoration
                            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 seconds
                
                # Check for player collision with debris
                for debris_obj in self.debris:
                    if self.player.hitbox.colliderect(debris_obj.hitbox):
                        # Use the take_damage method with source ID for cooldown
                        source_id = f"debris_{debris_obj.rect.x}_{debris_obj.rect.y}"
                        damage_applied = self.player.take_damage(
                            self.testing_mode and self.ui_manager.god_mode,  # Only god mode if both testing AND god mode enabled
                            source_id=source_id
                        )
                        
                        # Only kill the debris if damage was applied
                        if damage_applied:
                            debris_obj.kill()  # Remove the debris that collided with player
                        
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
                
                # Check for player collision with power-ups
                for powerup in self.powerups:
                    if self.player.hitbox.colliderect(powerup.hitbox):
                        self.player.apply_powerup(powerup.type)
                        # Play powerup sound
                        self.sound_manager.play_sound('powerup')
                        powerup.kill()
    
    def update_enemy_types(self):
        """Update available enemy types based on score."""
        # Use the phase manager to update phases based on score
        self.phase_manager.update(self.score)
    
    def handle_boss_collisions(self):
        """Handle all boss-related collisions."""
        # Delegate to the boss manager
        if self.player:
            self.boss_manager.handle_collisions(self.player)
            self.sound_manager.play_sound('game_over')
        
        # Process main-boss collisions
        if self.main_boss:
            # Check if main-boss is properly initialized
            if hasattr(self.main_boss, 'hitbox'):
                # Check player bullets against main-boss
                for bullet in list(self.player.bullets):
                    if bullet.hitbox.colliderect(self.main_boss.hitbox):
                        bullet.kill()
                        if self.main_boss.take_damage(1):
                            # Main-boss defeated
                            points = self.main_boss.score_value * self.player.score_multiplier
                            self.score += points
                            self.main_boss = None
                            self.sound_manager.play_sound('explosion')
                            break  # Exit loop since main_boss is now None
                
                # Check main-boss bullets against player
                if self.main_boss and hasattr(self.main_boss, 'bullets'):
                    for bullet in list(self.main_boss.bullets):
                        if self.player.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.player.take_damage(self.ui_manager.god_mode if self.testing_mode else False):
                                if self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    self.sound_manager.play_sound('game_over')
    
    def check_boss_spawning(self):
        """Check if it's time to spawn a boss based on score."""
        # This is now handled by the phase manager
        # We keep this method for compatibility
        pass
    
    def draw(self):
        """Draw the game screen."""
        # Fill with deep space color for Starlight's End
        deep_space = (5, 5, 15)  # Very dark blue-black
        self.screen.fill(deep_space)
        
        # Draw themed background elements
        if self.game_state == self.GAME_STATE_PLAYING or self.game_state == self.GAME_STATE_RESPAWNING:
            self.background_manager.draw(self.screen)
        
        # Draw stars
        for star in self.stars:
            star.draw(self.screen)
        
        if not self.ui_manager.settings_open:
            if (self.game_state == self.GAME_STATE_PLAYING or self.game_state == self.GAME_STATE_RESPAWNING) and self.player:
                # Draw game elements
                self.all_sprites.draw(self.screen)
                self.player.draw(self.screen)
                
                # Draw player bullets with enhanced effects
                for bullet in self.player.bullets:
                    bullet.draw(self.screen)
                
                # Draw enemies with enhanced effects
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    
                # Draw game timer below chapter title (or boss timer if boss is active)
                self.phase_manager.draw_game_timer(self.screen)
                
                # Draw boss timer if a boss is active
                if self.boss_manager.has_active_boss():
                    self.phase_manager.draw_boss_timer(self.screen)
                
                # Draw frenzy mode indicator if active
                if self.phase_manager.frenzy_mode:
                    self.phase_manager.draw_frenzy_mode(self.screen)
                
                # Draw boss warning effect if active
                if self.showing_boss_warning:
                    self.phase_manager.draw_boss_warning(self.screen, self.boss_warning_type)
                
                # Draw asteroids with enhanced effects
                for asteroid in self.asteroids:
                    asteroid.draw(self.screen)
                
                # Draw debris with enhanced effects
                for debris_obj in self.debris:
                    debris_obj.draw(self.screen)
                
                # Draw powerups with enhanced effects
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                
                # Draw bosses
                self.boss_manager.draw(self.screen)
                
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
                self.ui_manager.show_score(self.screen, self.score, self.player.health, self.player.max_health, 
                                          self.testing_mode, self.player, self.clock.get_fps())
                
                # Draw testing panel if in testing mode
                if self.testing_mode and self.ui_manager.testing_panel_open:
                    self.ui_manager.draw_testing_panel(self.screen, self.player, self.clock.get_fps(), self.phase_manager)
                
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
                        f"Super Enemies: {self.get_super_enemy_count()}/2 (Max)",
                        f"Player Speed: {self.player.speed}",
                        f"Rapid Fire: {'On' if self.player.rapid_fire else 'Off'}",
                        f"Enemy Spawn Rate: {self.enemy_spawn_delay}ms",
                        f"Mini-Boss: {'Active' if self.boss_manager.mini_boss else 'Inactive'}",
                        f"Main Boss: {'Active' if self.boss_manager.main_boss else 'Inactive'}",
                        f"Enemy Types: {', '.join(self.enemy_types_available)}",
                        f"Debug Hitboxes: {'ON' if DEBUG_HITBOXES else 'OFF'} (Press D to toggle)"
                    ]
                    
                    for i, info in enumerate(debug_info):
                        text = debug_font.render(info, True, (200, 200, 200))
                        self.screen.blit(text, (10, 80 + i * 20))
                
                # Draw phase markers in testing mode
                if self.testing_mode:
                    self.phase_manager.draw_phase_markers(self.screen, True)
                
                # Draw phase transition effect if active
                self.phase_manager.draw_phase_transition(self.screen)
            
            # Draw appropriate screen based on game state
            elif self.game_state == self.GAME_STATE_GAME_OVER:
                # Show game over screen
                self.ui_manager.show_game_over(self.screen, self.score)
            elif self.game_state == self.GAME_STATE_RESPAWNING:
                # In respawning state, we still draw the game elements but freeze them
                # This is handled by the respawn countdown overlay
                pass
            elif self.game_state == self.GAME_STATE_MENU:
                # Show start screen
                self.ui_manager.show_start_screen(self.screen, self.testing_mode)
        else:
            # Draw settings panel - pass the current game state
            self.ui_manager.draw_settings_panel(self.screen, self.game_state)
        
        # Draw respawn countdown if active (in test mode)
        if self.testing_mode and self.ui_manager.respawning:
            self.ui_manager.draw_respawn_countdown(self.screen)
        
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

    def initialize_boss(self, boss_type):
        """Initialize a boss of the specified type and add it to the game."""
        # Use the boss manager to spawn the boss
        return self.boss_manager.spawn_boss(boss_type)
        
    def handle_boss_collisions(self):
        """Handle all boss-related collisions."""
        # Delegate to the boss manager
        if self.player:
            self.boss_manager.handle_collisions(self.player)
            self.sound_manager.play_sound('game_over')
        
        # Process main-boss collisions
        if self.main_boss:
            # Check if main-boss is properly initialized
            if hasattr(self.main_boss, 'hitbox'):
                # Check player bullets against main-boss
                for bullet in list(self.player.bullets):
                    if bullet.hitbox.colliderect(self.main_boss.hitbox):
                        bullet.kill()
                        if self.main_boss.take_damage(1):
                            # Main-boss defeated
                            points = self.main_boss.score_value * self.player.score_multiplier
                            self.score += points
                            self.main_boss = None
                            self.sound_manager.play_sound('explosion')
                            break  # Exit loop since main_boss is now None
                
                # Check main-boss bullets against player
                if self.main_boss and hasattr(self.main_boss, 'bullets'):
                    for bullet in list(self.main_boss.bullets):
                        if self.player.hitbox.colliderect(bullet.hitbox):
                            bullet.kill()
                            if self.player.take_damage(self.ui_manager.god_mode if self.testing_mode else False):
                                if self.player.health <= 0:
                                    self.game_state = self.GAME_STATE_GAME_OVER
                                    self.sound_manager.play_sound('game_over')
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
        
        # Reset game state to playing
        self.game_state = self.GAME_STATE_PLAYING
        self.game_active = True
        
        # Reset UI respawn state
        self.ui_manager.respawning = False
            
        print("Player respawned in test mode")
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
    def should_use_respawn(self):
        """Check if we should use respawn instead of game over."""
        return self.testing_mode and not self.ui_manager.god_mode
    def show_boss_warning(self, boss_type):
        """Show warning effect for boss appearance."""
        self.showing_boss_warning = True
        self.boss_warning_timer = self.boss_warning_duration
        self.boss_warning_type = boss_type
        
        # Play warning sound if available
        if 'warning' in self.sound_manager.sounds:
            self.sound_manager.play_sound('warning')
        elif 'alert' in self.sound_manager.sounds:
            self.sound_manager.play_sound('alert')
        else:
            # Use explosion sound as fallback
            self.sound_manager.play_sound('explosion')
    def get_super_enemy_count(self):
        """Return the number of super-type enemies currently on screen."""
        return sum(1 for e in self.enemies if hasattr(e, 'enemy_type') and e.enemy_type == 'super')
