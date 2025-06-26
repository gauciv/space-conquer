"""
Phase Manager for the Space Impact game.
Handles game phases, difficulty progression, and enemy types.
"""
import pygame

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
        
        # Set the first phase as active
        if self.phases:
            self.phases[0].active = True
    
    def update(self, score):
        """Update phases based on current score."""
        # Find the current phase based on score
        old_phase_index = self.current_phase_index
        
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
                if not phase.active:
                    # Phase transition
                    phase.active = True
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
        
        # Handle boss spawning using the boss manager
        if phase.boss_type:
            self.game_manager.boss_manager.spawn_boss(phase.boss_type)
    
    def get_current_phase(self):
        """Get the current active phase."""
        if 0 <= self.current_phase_index < len(self.phases):
            return self.phases[self.current_phase_index]
        return None
    
    def skip_to_phase(self, phase_index):
        """Skip to a specific phase (for testing)."""
        if 0 <= phase_index < len(self.phases):
            target_phase = self.phases[phase_index]
            self.game_manager.score = target_phase.score_threshold
            self.update(self.game_manager.score)
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
    
    def draw_phase_markers(self, surface, testing_mode=False):
        """Draw phase markers for testing mode."""
        if not testing_mode:
            return
            
        # Draw title
        marker_title = pygame.font.SysFont('Arial', 18, bold=True)
        title_text = marker_title.render("Phase Markers:", True, (255, 255, 100))
        surface.blit(title_text, (surface.get_width() - 150, 120))
        
        # Draw markers
        marker_font = pygame.font.SysFont('Arial', 16)
        for i, phase in enumerate(self.phases):
            # Create marker rectangle
            marker_rect = pygame.Rect(surface.get_width() - 150, 150 + i * 30, 140, 25)
            
            # Highlight current phase
            if phase.active:
                pygame.draw.rect(surface, (100, 100, 50), marker_rect)
                pygame.draw.rect(surface, (255, 255, 100), marker_rect, 2)
            else:
                pygame.draw.rect(surface, (50, 50, 50), marker_rect)
                pygame.draw.rect(surface, (150, 150, 150), marker_rect, 1)
            
            # Draw marker text
            text = marker_font.render(f"{phase.name}", True, (255, 255, 255))
            surface.blit(text, (surface.get_width() - 145, 153 + i * 30))
            
            # Store rect for click detection (in the game manager)
            phase.rect = marker_rect
