"""
Phase Manager for the Space Impact game.
Handles game phases, difficulty progression, and enemy types.
"""
import pygame
import time

class Phase:
    """Represents a game phase with specific enemy types and difficulty settings."""
    def __init__(self, name, score_threshold, enemy_types, spawn_rate=None, boss_type=None):
        self.name = name
        self.score_threshold = score_threshold
        self.enemy_types = enemy_types
        self.spawn_rate = spawn_rate  # milliseconds between enemy spawns
        self.boss_type = boss_type    # 'mini', 'main', or None
        self.active = False
        self.completed = False
        self.transition_time = 0      # For phase transition effects
        self.rect = None              # For click detection
        
    def __str__(self):
        return f"Phase: {self.name} (Score: {self.score_threshold})"

class PhaseManager:
    """Manages game phases and progression."""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.phases = []
        self.current_phase_index = 0
        self.showing_phase_transition = False
        self.transition_timer = 0
        self.transition_duration = 60  # frames (1 second at 60 FPS)
        
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
        """Initialize all game phases."""
        self.phases = [
            Phase("Start", 0, ['normal'], spawn_rate=1500),
            Phase("Fast Enemies", 200, ['normal', 'fast'], spawn_rate=1200),
            Phase("Tank Enemies", 400, ['normal', 'fast', 'tank'], spawn_rate=1000),
            Phase("Bomber Enemies", 600, ['normal', 'fast', 'tank', 'bomber'], spawn_rate=800),
            Phase("Mini-Boss", 750, ['normal', 'fast', 'tank'], spawn_rate=1000, boss_type='mini'),
            Phase("Main Boss", 1500, ['normal', 'fast', 'tank', 'bomber'], spawn_rate=800, boss_type='main')
        ]
        
        # Set the first phase (Start) as active by default
        self._deselect_all_phases()
        self.phases[0].active = True
    
    def update(self, score):
        """Update phases based on current score."""
        # Update cooldown state
        current_time = time.time()
        if self.is_on_cooldown and current_time - self.last_phase_selection_time >= self.phase_selection_cooldown:
            self.is_on_cooldown = False
        
        # Find the current phase based on score
        old_phase_index = self.current_phase_index
        
        # In testing mode, we don't automatically change phases based on score
        # The active phase is set manually through skip_to_phase
        if not self.game_manager.testing_mode:
            # First, deselect all phases
            self._deselect_all_phases()
            
            for i, phase in enumerate(self.phases):
                # Mark phases as completed if score is past their threshold
                if score >= phase.score_threshold:
                    phase.completed = True
                    
                    # Check if this is the highest completed phase
                    if i > self.current_phase_index:
                        self.current_phase_index = i
                
                # Determine which phase is currently active
                is_last_phase = (i == len(self.phases) - 1)
                next_threshold = float('inf') if is_last_phase else self.phases[i+1].score_threshold
                
                if score >= phase.score_threshold and score < next_threshold:
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
    
    def _handle_phase_transition(self):
        """Handle visual and gameplay effects when transitioning to a new phase."""
        current_phase = self.get_current_phase()
        if current_phase:
            # Play transition sound if available
            if 'phase_change' in self.game_manager.sound_manager.sounds:
                self.game_manager.sound_manager.play_sound('phase_change')
            
            # Log phase change
            print(f"Entering new phase: {current_phase.name} (Score: {current_phase.score_threshold})")
    
    def _apply_phase_settings(self, phase):
        """Apply the settings for the given phase to the game."""
        # Update enemy types
        self.game_manager.enemy_types_available = phase.enemy_types
        
        # Update spawn rate if specified
        if phase.spawn_rate is not None:
            self.game_manager.enemy_spawn_delay = phase.spawn_rate
        
        # Clear existing bosses when changing phases
        self.game_manager.boss_manager.reset()
        
        # Handle boss spawning using the boss manager
        if phase.boss_type:
            # Show phase transition
            self.showing_phase_transition = True
            self.transition_timer = self.transition_duration
            
            # Spawn the appropriate boss
            boss = self.game_manager.boss_manager.spawn_boss(phase.boss_type)
            if boss:
                print(f"Boss spawned: {boss.name}")
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
            
            # Set score to phase threshold
            self.game_manager.score = target_phase.score_threshold
            
            # Apply phase settings directly
            self._apply_phase_settings(target_phase)
            
            print(f"Skipped to phase: {target_phase.name} (Score: {target_phase.score_threshold})")
            return True
        return False
    
    def draw_phase_transition(self, surface):
        """Draw phase transition effect."""
        if not self.showing_phase_transition:
            return
            
        # Decrease transition timer
        self.transition_timer -= 1
        if self.transition_timer <= 0:
            self.showing_phase_transition = False
            return
        
        # Calculate alpha based on timer (fade in, then fade out)
        if self.transition_timer > self.transition_duration / 2:
            # Fade in
            alpha = 255 * (1 - (self.transition_timer - self.transition_duration/2) / (self.transition_duration/2))
        else:
            # Fade out
            alpha = 255 * (self.transition_timer / (self.transition_duration/2))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), 80), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(180, int(alpha * 0.7))))
        surface.blit(overlay, (0, surface.get_height() // 2 - 40))
        
        # Draw phase name
        current_phase = self.get_current_phase()
        if current_phase:
            font = pygame.font.SysFont('Arial', 32, bold=True)
            text = font.render(f"PHASE {self.current_phase_index + 1}: {current_phase.name}", True, (255, 255, 255))
            text.set_alpha(int(alpha))
            surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, 
                               surface.get_height() // 2 - text.get_height() // 2))
    
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
            marker_rect = pygame.Rect(panel_x, panel_y + 30 + i * 30, panel_width, 25)
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
            text = marker_font.render(f"{phase.name}", True, text_color)
            surface.blit(text, (panel_x + 5, panel_y + 33 + i * 30))
        
        # Draw cooldown indicator if on cooldown
        if self.is_on_cooldown:
            cooldown_rect = pygame.Rect(panel_x, panel_y + 30 + len(self.phases) * 30, panel_width, 5)
            pygame.draw.rect(surface, (50, 50, 50), cooldown_rect)
            progress_width = int(cooldown_progress * panel_width)
            if progress_width > 0:
                progress_rect = pygame.Rect(panel_x, panel_y + 30 + len(self.phases) * 30, progress_width, 5)
                pygame.draw.rect(surface, (100, 200, 100), progress_rect)
            
            # Draw cooldown text
            cooldown_font = pygame.font.SysFont('Arial', 12)
            cooldown_text = cooldown_font.render(f"Cooldown: {self.phase_selection_cooldown - (time.time() - self.last_phase_selection_time):.1f}s", 
                                               True, (200, 200, 200))
            surface.blit(cooldown_text, (panel_x, panel_y + 35 + len(self.phases) * 30))
