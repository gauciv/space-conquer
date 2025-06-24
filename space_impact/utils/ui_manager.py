"""
UI Manager for the Space Impact game.
Handles UI elements like settings panel, menus, etc.
"""
import pygame # type: ignore
import random
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY

class UIManager:
    def __init__(self, asset_loader, sound_manager):
        self.asset_loader = asset_loader
        self.sound_manager = sound_manager
        
        # Settings button
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 40, 10, 30, 30)
        
        # Main menu buttons
        self.start_button_rect = None
        self.test_button_rect = None
        
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
        """Display an enhanced game over screen."""
        # Create a dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Add some particle effects
        for i in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 4)
            color = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 50))
            pygame.draw.circle(surface, color, (x, y), size)
        
        # Create a semi-transparent panel for the game over message
        panel_width, panel_height = 500, 300
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - panel_width // 2, SCREEN_HEIGHT // 2 - panel_height // 2, 
                                panel_width, panel_height)
        
        # Draw panel background with gradient
        for i in range(panel_height):
            progress = i / panel_height
            color = (
                int(40 + 20 * progress),
                int(0 + 10 * progress),
                int(0 + 30 * progress),
                200
            )
            panel_surface = pygame.Surface((panel_width, 1), pygame.SRCALPHA)
            panel_surface.fill(color)
            surface.blit(panel_surface, (panel_rect.left, panel_rect.top + i))
        
        # Draw panel border
        pygame.draw.rect(surface, (150, 30, 30), panel_rect, 2)
        
        # Add some "tech" details to the panel
        pygame.draw.line(surface, (200, 50, 50, 150), 
                        (panel_rect.left + 20, panel_rect.top + 20), 
                        (panel_rect.left + panel_width - 20, panel_rect.top + 20), 2)
        pygame.draw.line(surface, (200, 50, 50, 150), 
                        (panel_rect.left + 20, panel_rect.bottom - 20), 
                        (panel_rect.left + panel_width - 20, panel_rect.bottom - 20), 2)
        
        # Draw game over text with glow effect
        game_over_font = pygame.font.SysFont('Arial', 48, bold=True)
        glow_text = game_over_font.render('GAME OVER', True, (100, 0, 0))
        surface.blit(glow_text, (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 + 2, panel_rect.top + 50 + 2))
        
        game_over_text = game_over_font.render('GAME OVER', True, (255, 50, 50))
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, panel_rect.top + 50))
        
        # Draw score
        score_font = pygame.font.SysFont('Arial', 32)
        score_text = score_font.render(f'Final Score: {score}', True, (220, 220, 255))
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, panel_rect.top + 120))
        
        # Create restart button
        restart_button_width, restart_button_height = 250, 50
        restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - restart_button_width // 2, 
                                        panel_rect.top + 180, 
                                        restart_button_width, restart_button_height)
        self._draw_stylized_button(surface, restart_button_rect, "RESTART", (60, 10, 10), (150, 30, 30))
        
        # Create test mode button
        test_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - restart_button_width // 2, 
                                    panel_rect.top + 240, 
                                    restart_button_width, restart_button_height)
        self._draw_stylized_button(surface, test_button_rect, "TEST MODE", (40, 10, 40), (100, 30, 100))
        
        # Store button rectangles for click detection
        self.start_button_rect = restart_button_rect
        self.test_button_rect = test_button_rect
    
    def show_start_screen(self, surface, testing_mode=False):
        """Display an enhanced start screen with mysterious vibe."""
        # Create a starry background effect
        for i in range(50):  # Add extra stars for the menu
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)
        
        # Add a mysterious nebula-like effect
        for i in range(5):
            nebula_surface = pygame.Surface((300, 200), pygame.SRCALPHA)
            color = (random.randint(20, 60), random.randint(0, 30), random.randint(40, 80), 15)
            pygame.draw.ellipse(nebula_surface, color, (0, 0, 300, 200))
            surface.blit(nebula_surface, (random.randint(0, SCREEN_WIDTH-300), random.randint(0, SCREEN_HEIGHT-200)))
        
        # Create a semi-transparent overlay for the title area
        title_overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
        title_overlay.fill((0, 0, 30, 180))
        surface.blit(title_overlay, (0, 130))
        
        # Draw a glowing effect for the title
        glow_font = pygame.font.SysFont('Arial', 60, bold=True)
        glow_text = glow_font.render('SPACE CONQUER', True, (60, 60, 120))
        surface.blit(glow_text, (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 + 2, 152))
        
        # Draw the main title
        title_font = pygame.font.SysFont('Arial', 60, bold=True)
        title_text = title_font.render('SPACE CONQUER', True, (150, 150, 255))
        surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        
        # Create stylized buttons
        button_width, button_height = 250, 50
        
        # Start Game Button
        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 280, button_width, button_height)
        self._draw_stylized_button(surface, start_button_rect, "START GAME", (30, 30, 80), (80, 80, 180))
        
        # Test Mode Button (smaller and less prominent)
        if testing_mode:
            test_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 350, button_width, button_height)
            self._draw_stylized_button(surface, test_button_rect, "TEST MODE", (40, 20, 60), (120, 80, 140))
        else:
            test_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 40)
            self._draw_stylized_button(surface, test_button_rect, "TEST MODE", (30, 15, 45), (90, 60, 105))
        
        # Controls section with a semi-transparent background
        controls_overlay = pygame.Surface((400, 80), pygame.SRCALPHA)
        controls_overlay.fill((0, 0, 30, 150))
        surface.blit(controls_overlay, (SCREEN_WIDTH // 2 - 200, 420))
        
        # Draw controls text
        controls_title = self.font_medium.render('CONTROLS:', True, (200, 200, 255))
        surface.blit(controls_title, (SCREEN_WIDTH // 2 - 180, 430))
        
        controls_text = self.font_small.render('Arrow keys: Move | SPACE: Shoot | ESC: Settings', True, (180, 180, 220))
        surface.blit(controls_text, (SCREEN_WIDTH // 2 - 180, 460))
        
        # Add a mysterious tagline
        tagline_font = pygame.font.SysFont('Arial', 18, italic=True)
        tagline_text = tagline_font.render('The void awaits...', True, (150, 150, 200))
        surface.blit(tagline_text, (SCREEN_WIDTH // 2 - tagline_text.get_width() // 2, 520))
        
        # Store button rectangles for click detection
        self.start_button_rect = start_button_rect
        self.test_button_rect = test_button_rect
        
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
                "0: Toggle Debug Info"
            ]
            
            # Create a semi-transparent background for test instructions
            test_overlay = pygame.Surface((300, len(test_instructions) * 20 + 20), pygame.SRCALPHA)
            test_overlay.fill((0, 0, 30, 150))
            surface.blit(test_overlay, (20, SCREEN_HEIGHT - len(test_instructions) * 20 - 30))
            
            for i, instruction in enumerate(test_instructions):
                text = self.font_small.render(instruction, True, (200, 200, 100))
                surface.blit(text, (30, SCREEN_HEIGHT - len(test_instructions) * 20 - 10 + i * 20))
    
    def _draw_stylized_button(self, surface, rect, text, color_dark, color_light):
        """Draw a stylized button with a space theme."""
        # Draw button background with gradient
        for i in range(rect.height):
            progress = i / rect.height
            color = (
                int(color_dark[0] + (color_light[0] - color_dark[0]) * progress),
                int(color_dark[1] + (color_light[1] - color_dark[1]) * progress),
                int(color_dark[2] + (color_light[2] - color_dark[2]) * progress)
            )
            pygame.draw.line(surface, color, (rect.left, rect.top + i), (rect.right, rect.top + i))
        
        # Draw button border with glow effect
        pygame.draw.rect(surface, color_light, rect, 2)
        
        # Add some "tech" details to the button
        pygame.draw.line(surface, (100, 100, 200, 150), 
                        (rect.left + 10, rect.top + 5), 
                        (rect.left + rect.width - 20, rect.top + 5), 1)
        pygame.draw.line(surface, (100, 100, 200, 150), 
                        (rect.left + 10, rect.bottom - 5), 
                        (rect.left + rect.width - 20, rect.bottom - 5), 1)
        
        # Draw text
        font = pygame.font.SysFont('Arial', 24, bold=True)
        text_surface = font.render(text, True, (220, 220, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
