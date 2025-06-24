"""
UI Manager for the Space Impact game.
Handles UI elements like settings panel, menus, etc.
"""
import pygame # type: ignore
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY

class UIManager:
    def __init__(self, asset_loader, sound_manager):
        self.asset_loader = asset_loader
        self.sound_manager = sound_manager
        
        # Settings button
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 40, 10, 30, 30)
        
        # Settings panel
        self.settings_open = False
        self.x_offset = 40
        self.panel_x = (SCREEN_WIDTH // 2 - 200) + self.x_offset
        self.panel_width = 400
        
        # Slider settings
        self.slider_width = 150
        
        # Volume sliders
        self.sfx_slider_rect = pygame.Rect(self.panel_x + 130, SCREEN_HEIGHT // 2 - 40, self.slider_width, 10)
        self.sfx_handle_rect = pygame.Rect(
            self.panel_x + 130 + int(sound_manager.sfx_volume * self.slider_width) - 10, 
            SCREEN_HEIGHT // 2 - 45, 
            20, 20
        )
        
        self.music_slider_rect = pygame.Rect(self.panel_x + 130, SCREEN_HEIGHT // 2 + 10, self.slider_width, 10)
        self.music_handle_rect = pygame.Rect(
            self.panel_x + 130 + int(sound_manager.music_volume * self.slider_width) - 10, 
            SCREEN_HEIGHT // 2 + 5, 
            20, 20
        )
        
        # Dragging state
        self.dragging_sfx_handle = False
        self.dragging_music_handle = False
        
        # Fonts
        self.font_large = pygame.font.SysFont('Arial', 32)
        self.font_medium = pygame.font.SysFont('Arial', 22)
        self.font_small = pygame.font.SysFont('Arial', 16)
        
        # Load heart images
        self.full_heart_img = self.asset_loader.get_image('full_heart')
        self.empty_heart_img = self.asset_loader.get_image('empty_heart')
        
        # Scale heart images if needed
        if self.full_heart_img.get_width() > 32 or self.full_heart_img.get_height() > 32:
            self.full_heart_img = pygame.transform.scale(self.full_heart_img, (32, 32))
        if self.empty_heart_img.get_width() > 32 or self.empty_heart_img.get_height() > 32:
            self.empty_heart_img = pygame.transform.scale(self.empty_heart_img, (32, 32))
    
    def draw_settings_button(self, surface):
        """Draw the settings button."""
        settings_cog_img = self.asset_loader.get_image('settings_cog')
        surface.blit(settings_cog_img, self.settings_button_rect)
    
    def draw_settings_panel(self, surface):
        """Draw the settings panel."""
        # Draw semi-transparent background
        settings_surface = pygame.Surface((self.panel_width, 250), pygame.SRCALPHA)
        settings_surface.fill((0, 0, 0, 200))
        surface.blit(settings_surface, (self.panel_x, SCREEN_HEIGHT // 2 - 125))
        
        # Draw panel border
        pygame.draw.rect(surface, WHITE, (self.panel_x, SCREEN_HEIGHT // 2 - 125, self.panel_width, 250), 2)
        
        # Draw title with proper padding
        title_text = self.font_large.render('Settings', True, WHITE)
        surface.blit(title_text, (self.panel_x + self.panel_width // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 105))
        
        # Draw horizontal separator line
        pygame.draw.line(surface, GRAY, 
                        (self.panel_x + 20, SCREEN_HEIGHT // 2 - 70),
                        (self.panel_x + self.panel_width - 20, SCREEN_HEIGHT // 2 - 70), 1)
        
        # Sound effects label
        sfx_text = self.font_medium.render('Sound Effects', True, WHITE)
        surface.blit(sfx_text, (self.panel_x + 20, SCREEN_HEIGHT // 2 - 45))
        
        # Sound effects slider
        sfx_slider_x = self.panel_x + 130
        sfx_slider_y = SCREEN_HEIGHT // 2 - 40
        
        # Create a local copy of the slider rect for drawing
        local_sfx_slider_rect = pygame.Rect(sfx_slider_x, sfx_slider_y, self.slider_width, 10)
        slider_bar_img = self.asset_loader.get_image('slider_bar')
        surface.blit(pygame.transform.scale(slider_bar_img, (self.slider_width, 10)), local_sfx_slider_rect)
        
        # Sound effects handle
        sfx_handle_x = sfx_slider_x + int(self.sound_manager.sfx_volume * self.slider_width) - 10
        sfx_handle_y = SCREEN_HEIGHT // 2 - 45
        local_sfx_handle_rect = pygame.Rect(sfx_handle_x, sfx_handle_y, 20, 20)
        slider_handle_img = self.asset_loader.get_image('slider_handle')
        surface.blit(slider_handle_img, local_sfx_handle_rect)
        
        # Update the handle rect position
        self.sfx_handle_rect.x = sfx_handle_x
        self.sfx_handle_rect.y = sfx_handle_y
        self.sfx_slider_rect.x = sfx_slider_x
        self.sfx_slider_rect.y = sfx_slider_y
        
        # Sound effects percentage
        sfx_value_text = self.font_medium.render(f'{int(self.sound_manager.sfx_volume * 100)}%', True, WHITE)
        surface.blit(sfx_value_text, (sfx_slider_x + self.slider_width + 15, SCREEN_HEIGHT // 2 - 45))
        
        # Music label
        music_text = self.font_medium.render('Music', True, WHITE)
        surface.blit(music_text, (self.panel_x + 20, SCREEN_HEIGHT // 2 + 5))
        
        # Music slider
        music_slider_x = self.panel_x + 130
        music_slider_y = SCREEN_HEIGHT // 2 + 10
        
        # Create a local copy of the slider rect for drawing
        local_music_slider_rect = pygame.Rect(music_slider_x, music_slider_y, self.slider_width, 10)
        surface.blit(pygame.transform.scale(slider_bar_img, (self.slider_width, 10)), local_music_slider_rect)
        
        # Music handle
        music_handle_x = music_slider_x + int(self.sound_manager.music_volume * self.slider_width) - 10
        music_handle_y = SCREEN_HEIGHT // 2 + 5
        local_music_handle_rect = pygame.Rect(music_handle_x, music_handle_y, 20, 20)
        surface.blit(slider_handle_img, local_music_handle_rect)
        
        # Update the handle rect position
        self.music_handle_rect.x = music_handle_x
        self.music_handle_rect.y = music_handle_y
        self.music_slider_rect.x = music_slider_x
        self.music_slider_rect.y = music_slider_y
        
        # Music percentage
        music_value_text = self.font_medium.render(f'{int(self.sound_manager.music_volume * 100)}%', True, WHITE)
        surface.blit(music_value_text, (music_slider_x + self.slider_width + 15, SCREEN_HEIGHT // 2 + 5))
        
        # Draw horizontal separator line
        pygame.draw.line(surface, GRAY, 
                        (self.panel_x + 20, SCREEN_HEIGHT // 2 + 50),
                        (self.panel_x + self.panel_width - 20, SCREEN_HEIGHT // 2 + 50), 1)
        
        # Draw close button
        close_button_x = self.panel_x + self.panel_width // 2 - 50
        close_button_y = SCREEN_HEIGHT // 2 + 80
        close_button_rect = pygame.Rect(close_button_x, close_button_y, 100, 35)
        pygame.draw.rect(surface, GRAY, close_button_rect)
        pygame.draw.rect(surface, WHITE, close_button_rect, 2)
        
        close_text = self.font_medium.render('Close', True, WHITE)
        surface.blit(close_text, (close_button_rect.centerx - close_text.get_width() // 2, 
                                close_button_rect.centery - close_text.get_height() // 2))
        
        return close_button_rect
    
    def handle_settings_click(self, pos):
        """Handle clicks in the settings panel."""
        if self.settings_button_rect.collidepoint(pos):
            self.settings_open = not self.settings_open
            return True
        
        if self.settings_open:
            # Check if SFX slider handle was clicked
            if self.sfx_handle_rect.collidepoint(pos):
                self.dragging_sfx_handle = True
                return True
            
            # Check if music slider handle was clicked
            elif self.music_handle_rect.collidepoint(pos):
                self.dragging_music_handle = True
                return True
            
            # Check if close button was clicked
            close_button_rect = pygame.Rect(
                self.panel_x + self.panel_width // 2 - 50, 
                SCREEN_HEIGHT // 2 + 80, 
                100, 35
            )
            if close_button_rect.collidepoint(pos):
                self.settings_open = False
                return True
        
        return False
    
    def handle_mouse_up(self):
        """Handle mouse button up events."""
        self.dragging_sfx_handle = False
        self.dragging_music_handle = False
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion events."""
        if self.dragging_sfx_handle:
            # Update SFX handle position
            mouse_x = pos[0]
            slider_left = self.sfx_slider_rect.left
            slider_right = self.sfx_slider_rect.right
            
            # Keep handle within slider bounds
            handle_x = max(slider_left, min(mouse_x, slider_right - self.sfx_handle_rect.width))
            self.sfx_handle_rect.x = handle_x
            
            # Update volume based on handle position
            volume_ratio = (handle_x - slider_left) / (slider_right - slider_left - self.sfx_handle_rect.width)
            self.sound_manager.set_sfx_volume(volume_ratio)
            return True
        
        elif self.dragging_music_handle:
            # Update music handle position
            mouse_x = pos[0]
            slider_left = self.music_slider_rect.left
            slider_right = self.music_slider_rect.right
            
            # Keep handle within slider bounds
            handle_x = max(slider_left, min(mouse_x, slider_right - self.music_handle_rect.width))
            self.music_handle_rect.x = handle_x
            
            # Update volume based on handle position
            volume_ratio = (handle_x - slider_left) / (slider_right - slider_left - self.music_handle_rect.width)
            self.sound_manager.set_music_volume(volume_ratio)
            return True
        
        return False
    
    def show_score(self, surface, score, health, max_health=3):
        """Display score and health on screen."""
        # Display score
        score_text = self.font_medium.render(f'Score: {score}', True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # Display health as hearts
        heart_spacing = 40  # Space between hearts
        for i in range(max_health):
            heart_x = 10 + (i * heart_spacing)
            heart_y = 40
            
            # Draw full or empty heart based on current health
            if i < health:
                surface.blit(self.full_heart_img, (heart_x, heart_y))
            else:
                surface.blit(self.empty_heart_img, (heart_x, heart_y))
    
    def show_game_over(self, surface, score):
        """Display game over screen."""
        game_over_text = self.font_large.render('GAME OVER', True, (255, 0, 0))
        score_text = self.font_medium.render(f'Final Score: {score}', True, WHITE)
        restart_text = self.font_medium.render('Press SPACE to restart', True, WHITE)
        test_text = self.font_medium.render('Press T for test mode', True, WHITE)
        
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))
        surface.blit(test_text, (SCREEN_WIDTH // 2 - test_text.get_width() // 2, 380))
    
    def show_start_screen(self, surface, testing_mode=False):
        """Display start screen."""
        title_text = self.font_large.render('SPACE CONQUER', True, WHITE)
        instruction_text = self.font_medium.render('Press SPACE to start', True, WHITE)
        test_text = self.font_medium.render('Press T for test mode', True, WHITE)
        controls_text = self.font_medium.render('Arrow keys to move, SPACE to shoot', True, WHITE)
        
        surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        surface.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 250))
        surface.blit(test_text, (SCREEN_WIDTH // 2 - test_text.get_width() // 2, 280))
        surface.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 320))
        
        # Show testing mode instructions
        if testing_mode:
            test_instructions = [
                "TESTING MODE CONTROLS:",
                "1: Spawn Mini-Boss",
                "2: Spawn Main Boss",
                "3: Add 100 Score",
                "4: Add Health",
                "5: Toggle Rapid Fire",
                "6: Increase Speed",
                "L: Cycle Through Levels",
                "0: Toggle Debug Info"
            ]
            
            for i, instruction in enumerate(test_instructions):
                text = self.font_small.render(instruction, True, (200, 200, 100))
                surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 360 + i * 20))
