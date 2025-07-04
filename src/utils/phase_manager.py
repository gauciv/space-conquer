"""
Phase Manager for the Space Impact game.
Handles game phases, difficulty progression, and enemy types based on time.
"""
import pygame
import time
import math

class Phase:
    """Represents a game phase with specific enemy types and difficulty settings."""
    def __init__(self, name, time_threshold, enemy_types, spawn_rate=None, boss_type=None, 
                 speed_multiplier=1.0, powerup_drop_chance_modifier=0.0):
        self.name = name
        self.time_threshold = time_threshold  # Time in seconds when this phase starts
        self.enemy_types = enemy_types
        self.spawn_rate = spawn_rate  # milliseconds between enemy spawns
        self.boss_type = boss_type    # 'mini', 'main', or None
        self.active = False
        self.completed = False
        self.transition_time = 0      # For phase transition effects
        self.rect = None              # For click detection
        self.speed_multiplier = speed_multiplier  # Multiplier for enemy speed
        self.powerup_drop_chance_modifier = powerup_drop_chance_modifier  # Modifier for powerup drop chance
        
    def __str__(self):
        return f"Phase: {self.name} (Time: {self.format_time(self.time_threshold)})"
        
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

class PhaseManager:
    """Manages game phases and progression based on time."""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.phases = []
        self.current_phase_index = 0
        self.showing_phase_transition = False
        self.transition_timer = 0
        self.transition_duration = 60  # frames (1 second at 60 FPS)
        
        # Game timer
        self.game_time = 0  # Time in seconds
        self.timer_paused = False
        self.timer_start_time = 0
        self.timer_paused_time = 0
        self.last_update_time_ms = time.time() * 1000  # Use milliseconds for more precision
        
        # Boss timer (separate from game timer)
        self.boss_timer = 0  # Time in seconds for boss fights
        self.boss_timer_active = False
        self.last_boss_update_time_ms = time.time() * 1000
        self.boss_asteroid_spawn_timer = 0  # Timer for spawning asteroids during boss fights
        
        # Frenzy mode
        self.frenzy_mode = False
        self.frenzy_start_time = 0
        self.frenzy_duration = 10  # seconds (changed from 8 to 10)
        self.frenzy_times = [35, 65, 115, 145]  # Specific times for frenzy mode in seconds
        
        # Phase selection cooldown
        self.phase_selection_cooldown = 3.0  # 3 seconds
        self.last_phase_selection_time = 0
        self.is_on_cooldown = False
        
        # Panel collapse state
        self.panel_collapsed = False
        self.collapse_button_rect = pygame.Rect(0, 0, 20, 20)  # Will be positioned later
        
        # Initialize phases
        self._init_phases()
    
    def _init_phases(self):
        """Initialize all game phases based on time thresholds."""
        self.phases = [
            Phase("Start", 0, ['low'], spawn_rate=1667),  # 2500/1.5 = ~1667 (1.5x faster)
            Phase("Low Enemies Speed Up", 15, ['low'], spawn_rate=1667, speed_multiplier=1.25),
            Phase("Asteroids & Elite Enemies", 30, ['low', 'elite'], spawn_rate=1667, powerup_drop_chance_modifier=-0.25),  # 3333/2 = ~1667 (2x faster for elite)
            Phase("Flying Debris", 45, ['low', 'elite'], spawn_rate=2667),  # 5333/2 = ~2667 (2x faster for elite)
            Phase("Super Monsters", 60, ['low', 'elite', 'super'], spawn_rate=2500, speed_multiplier=1.15, powerup_drop_chance_modifier=0.1),  # Reduced from 1667 to 2500 (50% decrease)
            Phase("Mini-Boss", 90, [], boss_type='mini'),  # 90 seconds = 1:30
            Phase("Post Mini-Boss", 91, ['low', 'elite', 'super'], spawn_rate=1500),  # Reduced from 1000 to 1500 (50% decrease)
            Phase("Final Boss", 180, [], boss_type='main')  # 180 seconds = 3:00
        ]
        
        # Set the first phase (Start) as active by default
        self._deselect_all_phases()
        self.phases[0].active = True
    
    def update(self):
        """Update phases based on current game time."""
        # Update cooldown state
        current_time = time.time()
        if self.is_on_cooldown and current_time - self.last_phase_selection_time >= self.phase_selection_cooldown:
            self.is_on_cooldown = False
        
        # Check if boss is active
        boss_active = self.game_manager.boss_manager.has_active_boss()
        
        # Update boss timer if a boss is active and settings not open
        if boss_active and not self.game_manager.ui_manager.settings_open:
            # Start boss timer if it just became active
            if not self.boss_timer_active:
                self.boss_timer = 0
                self.boss_timer_active = True
                self.last_boss_update_time_ms = time.time() * 1000
                self.boss_asteroid_spawn_timer = 0
            
            # Update boss timer
            current_time_ms = time.time() * 1000
            elapsed = (current_time_ms - self.last_boss_update_time_ms) / 1000
            self.boss_timer += elapsed
            self.last_boss_update_time_ms = current_time_ms
            
            # Update asteroid spawn timer during boss fights
            self.boss_asteroid_spawn_timer += elapsed
        else:
            # Reset boss timer when no boss is active
            if self.boss_timer_active:
                self.boss_timer_active = False
        
        # Update game timer if not paused, not showing map name, no active boss, and settings not open
        if (not self.timer_paused and 
            not self.game_manager.showing_map_name and 
            not boss_active and
            not self.game_manager.ui_manager.settings_open):
            
            # Use real time for accurate timing
            current_time_ms = time.time() * 1000  # Convert to milliseconds for more precision
            
            if hasattr(self, 'last_update_time_ms'):
                # Calculate elapsed time since last update in seconds
                elapsed = (current_time_ms - self.last_update_time_ms) / 1000
                self.game_time += elapsed
                
            self.last_update_time_ms = current_time_ms
        
        # Find the current phase based on time
        old_phase_index = self.current_phase_index
        
        # In testing mode, we don't automatically change phases based on time
        # The active phase is set manually through skip_to_phase
        if not self.game_manager.testing_mode:
            # First, deselect all phases
            self._deselect_all_phases()
            
            for i, phase in enumerate(self.phases):
                # Mark phases as completed if time is past their threshold
                if self.game_time >= phase.time_threshold:
                    phase.completed = True
                    
                    # Check if this is the highest completed phase
                    if i > self.current_phase_index:
                        self.current_phase_index = i
                
                # Determine which phase is currently active
                is_last_phase = (i == len(self.phases) - 1)
                next_threshold = float('inf') if is_last_phase else self.phases[i+1].time_threshold
                
                if self.game_time >= phase.time_threshold and self.game_time < next_threshold:
                    # This is the current active phase
                    phase.active = True
                    
                    if old_phase_index != i:
                        # Phase transition
                        self.showing_phase_transition = True
                        self.transition_timer = self.transition_duration
                        
                        # Update game settings for this phase
                        self._apply_phase_settings(phase)
            
            # If phase changed, trigger transition effects
            if old_phase_index != self.current_phase_index:
                self._handle_phase_transition()
                
            # Check for frenzy mode
            self._update_frenzy_mode()
    
    def _update_frenzy_mode(self):
        """Update frenzy mode status based on time."""
        # Skip frenzy mode if a boss is active
        if self.game_manager.boss_manager.has_active_boss():
            if self.frenzy_mode:
                self.frenzy_mode = False
                print(f"Frenzy mode ended due to boss at {self.format_time(self.game_time)}")
            return
            
        # Check if we should start a frenzy based on specific times
        if not self.frenzy_mode:
            # Check if current time matches any of our specific frenzy times
            for frenzy_time in self.frenzy_times:
                # Allow a small window of 0.1 seconds to catch the exact time
                if abs(self.game_time - frenzy_time) < 0.1:
                    self.frenzy_mode = True
                    self.frenzy_start_time = self.game_time
                    print(f"Frenzy mode activated at {self.format_time(self.game_time)}!")
                    break
        else:
            # Check if frenzy should end
            if self.game_time >= self.frenzy_start_time + self.frenzy_duration:
                self.frenzy_mode = False
                print(f"Frenzy mode ended at {self.format_time(self.game_time)}")
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def _handle_phase_transition(self):
        """Handle visual and gameplay effects when transitioning to a new phase."""
        current_phase = self.get_current_phase()
        if current_phase:
            # Play transition sound if available
            if 'phase_change' in self.game_manager.sound_manager.sounds:
                self.game_manager.sound_manager.play_sound('phase_change')
                
            # Only print phase changes in testing mode
            if self.game_manager.testing_mode:
                print(f"Entering new phase: {current_phase.name} (Time: {self.format_time(current_phase.time_threshold)})")
    
    def _apply_phase_settings(self, phase):
        """Apply the settings for the given phase to the game."""
        # Update enemy types - map old enemy types to new ones if needed
        enemy_types = []
        for enemy_type in phase.enemy_types:
            if enemy_type == 'normal':
                enemy_types.append('low')
            elif enemy_type == 'fast':
                enemy_types.append('elite')
            elif enemy_type == 'tank':
                enemy_types.append('super')
            else:
                enemy_types.append(enemy_type)
                
        self.game_manager.enemy_types_available = enemy_types
        
        # Update spawn rate if specified
        if phase.spawn_rate is not None:
            self.game_manager.enemy_spawn_delay = phase.spawn_rate
        
        # Apply speed multiplier to enemies
        if hasattr(phase, 'speed_multiplier'):
            self.game_manager.enemy_speed_multiplier = phase.speed_multiplier
        
        # Apply powerup drop chance modifier
        if hasattr(phase, 'powerup_drop_chance_modifier'):
            self.game_manager.powerup_drop_chance_modifier = phase.powerup_drop_chance_modifier
        
        # Clear existing bosses when changing phases
        self.game_manager.boss_manager.reset()
        
        # Handle boss spawning using the boss manager
        if phase.boss_type:
            # Show phase transition
            self.showing_phase_transition = True
            self.transition_timer = self.transition_duration
            
            # Pause the timer during boss fights
            self.pause_timer()
            
            # Spawn the appropriate boss
            boss = self.game_manager.boss_manager.spawn_boss(phase.boss_type)
            if boss:
                print(f"Boss spawned: {boss.name}")
                
                # For main boss, kill all remaining enemies with explosion effects
                if phase.boss_type == 'main':
                    self._clear_all_enemies_with_explosion()
                
                # Show warning effect for boss
                if hasattr(self.game_manager, 'show_boss_warning'):
                    self.game_manager.show_boss_warning(phase.boss_type)
            else:
                print(f"Failed to spawn boss for phase: {phase.name}")
        else:
            print(f"No boss for phase: {phase.name}")
            
        # Trigger phase transition effect
        self._handle_phase_transition()
    
    def get_current_phase(self):
        """Get the current active phase."""
        if 0 <= self.current_phase_index < len(self.phases):
            return self.phases[self.current_phase_index]
        return None
    
    def _deselect_all_phases(self):
        """Deselect all phases."""
        for phase in self.phases:
            phase.active = False
    
    def skip_to_phase(self, phase_index):
        """Skip to a specific phase (for testing)."""
        # Don't allow phase skipping during cooldown
        if self.is_on_cooldown:
            return False
            
        if 0 <= phase_index < len(self.phases):
            # Set cooldown
            self.last_phase_selection_time = time.time()
            self.is_on_cooldown = True
            
            # Deselect all phases first
            self._deselect_all_phases()
            
            # Skip to the selected phase
            target_phase = self.phases[phase_index]
            target_phase.active = True  # Mark only this phase as active
            self.current_phase_index = phase_index  # Update current phase index
            
            # Set game time to phase threshold
            self.game_time = target_phase.time_threshold
            
            # Apply phase settings directly
            self._apply_phase_settings(target_phase)
            
            print(f"Skipped to phase: {target_phase.name} (Time: {self.format_time(target_phase.time_threshold)})")
            return True
        return False
        
    def pause_timer(self):
        """Pause the game timer."""
        if not self.timer_paused:
            self.timer_paused = True
            self.timer_paused_time = self.game_time
            print(f"Timer paused at {self.format_time(self.game_time)}")
    
    def resume_timer(self):
        """Resume the game timer."""
        if self.timer_paused:
            self.timer_paused = False
            print(f"Timer resumed at {self.format_time(self.game_time)}")
            
    def handle_boss_defeated(self, boss_type):
        """Handle boss defeat events."""
        # Resume the timer after boss is defeated
        self.resume_timer()
        
        # Set a cooldown before enemies start spawning again
        if hasattr(self.game_manager, 'enemy_spawn_cooldown'):
            self.game_manager.enemy_spawn_cooldown = 2.5  # 2.5 seconds
        
        # If it was the mini-boss, move to the post-mini-boss phase
        if boss_type == 'mini':
            for i, phase in enumerate(self.phases):
                if phase.name == "Post Mini-Boss":
                    self.skip_to_phase(i)
                    break
    
    def draw_phase_transition(self, surface):
        """Draw phase transition effect."""
        # We're removing the phase transition headlines as requested
        # Only keep this method for compatibility
        if not self.showing_phase_transition:
            return
            
        # Decrease transition timer
        self.transition_timer -= 1
        if self.transition_timer <= 0:
            self.showing_phase_transition = False
            return
    
    def toggle_panel_collapse(self):
        """Toggle the collapsed state of the phase markers panel."""
        self.panel_collapsed = not self.panel_collapsed
    
    def handle_click(self, pos):
        """Handle mouse clicks on phase markers panel."""
        # Check if collapse button was clicked
        if self.collapse_button_rect.collidepoint(pos):
            self.toggle_panel_collapse()
            return True
            
        # If panel is collapsed, don't check phase markers
        if self.panel_collapsed:
            return False
            
        # Don't allow phase selection during cooldown
        if self.is_on_cooldown:
            return False
            
        # Check if any phase marker was clicked
        for i, phase in enumerate(self.phases):
            if phase.rect and phase.rect.collidepoint(pos):
                return self.skip_to_phase(i)
                
        return False
    
    def draw_phase_markers(self, surface, testing_mode=False):
        """Draw phase markers for testing mode."""
        if not testing_mode:
            return
            
        # Panel position and size
        panel_x = surface.get_width() - 150
        panel_y = 120
        panel_width = 140
        
        # Draw collapse button
        self.collapse_button_rect = pygame.Rect(panel_x + panel_width - 20, panel_y, 20, 20)
        pygame.draw.rect(surface, (80, 80, 80), self.collapse_button_rect)
        pygame.draw.rect(surface, (150, 150, 150), self.collapse_button_rect, 1)
        
        # Draw collapse/expand symbol
        if self.panel_collapsed:
            # Draw + symbol
            pygame.draw.line(surface, (200, 200, 200), 
                            (self.collapse_button_rect.centerx - 5, self.collapse_button_rect.centery),
                            (self.collapse_button_rect.centerx + 5, self.collapse_button_rect.centery), 2)
            pygame.draw.line(surface, (200, 200, 200), 
                            (self.collapse_button_rect.centerx, self.collapse_button_rect.centery - 5),
                            (self.collapse_button_rect.centerx, self.collapse_button_rect.centery + 5), 2)
        else:
            # Draw - symbol
            pygame.draw.line(surface, (200, 200, 200), 
                            (self.collapse_button_rect.centerx - 5, self.collapse_button_rect.centery),
                            (self.collapse_button_rect.centerx + 5, self.collapse_button_rect.centery), 2)
        
        # Draw title
        marker_title = pygame.font.SysFont('Arial', 18, bold=True)
        title_text = marker_title.render("Phase Markers:", True, (255, 255, 100))
        surface.blit(title_text, (panel_x, panel_y))
        
        # Draw current game time
        time_text = marker_title.render(f"Time: {self.format_time(self.game_time)}", True, (255, 255, 255))
        surface.blit(time_text, (panel_x, panel_y + 20))
        
        # If collapsed, don't draw the phase markers
        if self.panel_collapsed:
            return
            
        # Calculate cooldown progress
        cooldown_progress = 0
        if self.is_on_cooldown:
            elapsed = time.time() - self.last_phase_selection_time
            cooldown_progress = min(1.0, elapsed / self.phase_selection_cooldown)
        
        # Draw markers
        marker_font = pygame.font.SysFont('Arial', 16)
        for i, phase in enumerate(self.phases):
            # Create marker rectangle
            marker_rect = pygame.Rect(panel_x, panel_y + 50 + i * 30, panel_width, 25)
            phase.rect = marker_rect  # Store rect for click detection
            
            # Determine marker color based on state
            if self.is_on_cooldown and not phase.active:
                # Gray out during cooldown
                bg_color = (50, 50, 50)
                border_color = (100, 100, 100)
                text_color = (150, 150, 150)
            elif phase.active:
                # Highlight current phase
                bg_color = (100, 100, 50)
                border_color = (255, 255, 100)
                text_color = (255, 255, 255)
            else:
                # Normal state
                bg_color = (50, 50, 50)
                border_color = (150, 150, 150)
                text_color = (255, 255, 255)
            
            # Draw marker background
            pygame.draw.rect(surface, bg_color, marker_rect)
            pygame.draw.rect(surface, border_color, marker_rect, 1)
            
            # Draw marker text
            text = marker_font.render(f"{phase.name} ({self.format_time(phase.time_threshold)})", True, text_color)
            surface.blit(text, (panel_x + 5, panel_y + 53 + i * 30))
        
        # Draw cooldown indicator if on cooldown
        if self.is_on_cooldown:
            cooldown_rect = pygame.Rect(panel_x, panel_y + 50 + len(self.phases) * 30, panel_width, 5)
            pygame.draw.rect(surface, (50, 50, 50), cooldown_rect)
            progress_width = int(cooldown_progress * panel_width)
            if progress_width > 0:
                progress_rect = pygame.Rect(panel_x, panel_y + 50 + len(self.phases) * 30, progress_width, 5)
                pygame.draw.rect(surface, (100, 200, 100), progress_rect)
            
            # Draw cooldown text
            cooldown_font = pygame.font.SysFont('Arial', 12)
            cooldown_text = cooldown_font.render(f"Cooldown: {self.phase_selection_cooldown - (time.time() - self.last_phase_selection_time):.1f}s", 
                                               True, (200, 200, 200))
            surface.blit(cooldown_text, (panel_x, panel_y + 55 + len(self.phases) * 30))
    def draw_game_timer(self, surface):
        """Draw the game timer below the chapter title."""
        # Don't show game timer during boss fights
        if self.game_manager.show_chapter_header and not self.boss_timer_active:
            font = pygame.font.SysFont('Arial', 18)
            timer_text = font.render(f"Time: {self.format_time(self.game_time)}", True, (200, 200, 255))
            surface.blit(timer_text, (surface.get_width() // 2 - timer_text.get_width() // 2, 40))
    
    def draw_boss_timer(self, surface):
        """Draw the boss timer during boss fights."""
        if self.boss_timer_active:
            font = pygame.font.SysFont('Arial', 18)
            timer_text = font.render(f"Boss Time: {self.format_time(self.boss_timer)}", True, (255, 100, 100))
            surface.blit(timer_text, (surface.get_width() // 2 - timer_text.get_width() // 2, 40))
            
    def draw_boss_warning(self, surface, boss_type):
        """Draw warning effect for boss appearance."""
        # This is called when a boss is about to appear
        
        # Calculate pulsing effect
        pulse = (math.sin(pygame.time.get_ticks() / 100) + 1) * 0.5  # 0 to 1
        alpha = int(100 + pulse * 155)  # 100 to 255
        
        # Create overlay with pulsing red
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha // 4))  # Transparent red
        surface.blit(overlay, (0, 0))
        
        # Draw warning text
        font = pygame.font.SysFont('Arial', 48, bold=True)
        if boss_type == 'mini':
            warning_text = font.render("WARNING!", True, (255, 50, 50))
        else:
            warning_text = font.render("FINAL BOSS APPROACHING!", True, (255, 50, 50))
            
        # Add a pulsing effect to the text
        size_multiplier = 1.0 + pulse * 0.3  # 1.0 to 1.3
        scaled_text = pygame.transform.scale(warning_text, 
                                           (int(warning_text.get_width() * size_multiplier),
                                            int(warning_text.get_height() * size_multiplier)))
        
        # Position the text in the center of the screen
        text_rect = scaled_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        
        # Draw with a glow effect
        glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (255, 0, 0, 100), (0, 0, glow_surf.get_width(), glow_surf.get_height()), 
                       border_radius=15)
        surface.blit(glow_surf, glow_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
        surface.blit(scaled_text, text_rect)
    def draw_frenzy_mode(self, surface):
        """Draw an intense frenzy mode indicator."""
        if not self.frenzy_mode:
            return
            
        # Create a pulsing red overlay for the entire screen
        pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) * 0.5  # 0 to 1
        alpha = int(20 + pulse * 30)  # 20 to 50 alpha
        
        # Create semi-transparent red overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha))
        surface.blit(overlay, (0, 0))
        
        # Draw "FRENZY MODE" text with intense effects
        frenzy_font = pygame.font.SysFont('Arial', 32, bold=True)
        frenzy_text = frenzy_font.render("FRENZY MODE", True, (255, 50, 50))
        
        # Add a pulsing effect
        size_multiplier = 1.0 + pulse * 0.3  # 1.0 to 1.3
        
        # Scale the text
        scaled_text = pygame.transform.scale(frenzy_text, 
                                           (int(frenzy_text.get_width() * size_multiplier),
                                            int(frenzy_text.get_height() * size_multiplier)))
        
        # Position below the timer (y=100 instead of y=30)
        scaled_rect = scaled_text.get_rect(center=(surface.get_width() // 2, 100))
        
        # Create a glowing effect
        for i in range(3, 0, -1):
            glow_size = i * 4
            glow_alpha = 150 - i * 40
            glow_surf = pygame.Surface((scaled_rect.width + glow_size, scaled_rect.height + glow_size), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 50, 50, glow_alpha), 
                           (0, 0, glow_surf.get_width(), glow_surf.get_height()), 
                           border_radius=15)
            glow_rect = glow_surf.get_rect(center=(surface.get_width() // 2, 100))
            surface.blit(glow_surf, glow_rect)
        
        # Draw the text
        surface.blit(scaled_text, scaled_rect)
        
        # Draw warning triangles on the sides
        triangle_size = 20 + int(pulse * 10)  # 20-30 pixels
        triangle_y = 100  # Match the new y position
        triangle_margin = 50
        
        # Left triangle
        left_points = [
            (triangle_margin, triangle_y),
            (triangle_margin + triangle_size, triangle_y - triangle_size//2),
            (triangle_margin + triangle_size, triangle_y + triangle_size//2)
        ]
        pygame.draw.polygon(surface, (255, 50, 50), left_points)
        
        # Right triangle
        right_points = [
            (surface.get_width() - triangle_margin, triangle_y),
            (surface.get_width() - triangle_margin - triangle_size, triangle_y - triangle_size//2),
            (surface.get_width() - triangle_margin - triangle_size, triangle_y + triangle_size//2)
        ]
        pygame.draw.polygon(surface, (255, 50, 50), right_points)
        
        # Draw time remaining
        if self.frenzy_start_time > 0:
            time_remaining = max(0, self.frenzy_duration - (self.game_time - self.frenzy_start_time))
            time_font = pygame.font.SysFont('Arial', 16)
            time_text = time_font.render(f"{time_remaining:.1f}s", True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(surface.get_width() // 2, 130))  # Position below the frenzy text
            surface.blit(time_text, time_rect)
    def _clear_all_enemies_with_explosion(self):
        """Clear all enemies with explosion effects when main boss appears."""
        # Get all enemies, asteroids, and debris
        enemies = list(self.game_manager.enemies)
        asteroids = list(self.game_manager.asteroids)
        debris = list(self.game_manager.debris)
        
        # Create a delayed explosion effect for each enemy
        for i, enemy in enumerate(enemies):
            # Destroy the enemy
            enemy.health = 0
            
            # Play explosion sound with slight delay to avoid sound overload
            if i % 3 == 0 and 'explosion' in self.game_manager.sound_manager.sounds:
                self.game_manager.sound_manager.play_sound('explosion')
                
            # Remove from sprite groups
            enemy.kill()
        
        # Create a delayed explosion effect for each asteroid
        for i, asteroid in enumerate(asteroids):
            # Destroy the asteroid
            asteroid.health = 0
            
            # Play explosion sound with slight delay
            if i % 3 == 0 and 'explosion' in self.game_manager.sound_manager.sounds:
                self.game_manager.sound_manager.play_sound('explosion')
                
            # Remove from sprite groups
            asteroid.kill()
        
        # Create a delayed explosion effect for each debris
        for i, debris_obj in enumerate(debris):
            # Destroy the debris
            debris_obj.health = 0
            
            # Play explosion sound with slight delay
            if i % 3 == 0 and 'explosion' in self.game_manager.sound_manager.sounds:
                self.game_manager.sound_manager.play_sound('explosion')
                
            # Remove from sprite groups
            debris_obj.kill()
            
        print(f"Cleared {len(enemies)} enemies, {len(asteroids)} asteroids, and {len(debris)} debris for main boss entrance")
    def should_spawn_boss_asteroid(self):
        """Check if it's time to spawn an asteroid during boss fights."""
        if self.boss_timer_active and self.boss_asteroid_spawn_timer >= 6:  # Every 6 seconds
            self.boss_asteroid_spawn_timer = 0  # Reset the timer
            return True
        return False
