"""
UI Manager for the Space Impact game.
Handles UI elements like settings panel, menus, etc.
"""
import pygame # type: ignore
import random
import math
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
        self.main_menu_button_rect = None
        self.close_button_rect = None  # Added to store close button rect
        
        # For main menu button in settings
        self.settings_main_menu_rect = None
        
        # Confirmation dialog elements
        self.show_confirmation = False
        self.confirmation_rect = None
        self.confirm_yes_rect = None
        self.confirm_no_rect = None
        # Button hover state
        self.hovered_button = None
        
        # Slider drag offsets for smooth dragging
        self.sfx_drag_offset = 0
        self.music_drag_offset = 0
        
        # Settings panel
        self.settings_open = False
        self.x_offset = 0  # Removed the offset to center the panel
        self.panel_x = SCREEN_WIDTH // 2 - 200  # Centered panel
        self.panel_width = 400
        
        # Slider settings
        self.slider_width = 150
        
        # Volume sliders
        self.sfx_slider_rect = pygame.Rect(self.panel_x + 130, SCREEN_HEIGHT // 2 - 40, self.slider_width, 10)
        self.sfx_handle_rect = pygame.Rect(0, 0, 24, 24)  # Larger clickable area
        
        # Music slider
        self.music_slider_rect = pygame.Rect(self.panel_x + 130, SCREEN_HEIGHT // 2 + 10, self.slider_width, 10)
        self.music_handle_rect = pygame.Rect(0, 0, 24, 24)  # Larger clickable area
        
        # Expand the clickable area for the sliders
        self.sfx_slider_clickable_rect = pygame.Rect(
            self.sfx_slider_rect.left - 10,
            self.sfx_slider_rect.top - 10,
            self.sfx_slider_rect.width + 20,
            self.sfx_slider_rect.height + 20
        )
        
        self.music_slider_clickable_rect = pygame.Rect(
            self.music_slider_rect.left - 10,
            self.music_slider_rect.top - 10,
            self.music_slider_rect.width + 20,
            self.music_slider_rect.height + 20
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
        """Draw an enhanced settings button with the space theme."""
        # Create a semi-transparent panel for the button
        button_size = 40
        button_rect = pygame.Rect(SCREEN_WIDTH - button_size - 10, 10, button_size, button_size)
        
        # Check if mouse is hovering over the button
        is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        
        # Draw button background with gradient
        for i in range(button_size):
            progress = i / button_size
            if is_hovered:
                color = (
                    int(30 + 40 * progress),
                    int(30 + 40 * progress),
                    int(60 + 60 * progress),
                    200
                )
            else:
                color = (
                    int(20 + 30 * progress),
                    int(20 + 30 * progress),
                    int(40 + 50 * progress),
                    180
                )
            panel_surface = pygame.Surface((button_size, 1), pygame.SRCALPHA)
            panel_surface.fill(color)
            surface.blit(panel_surface, (button_rect.left, button_rect.top + i))
        
        # Draw button border with glow effect
        border_color = (150, 150, 255) if is_hovered else (100, 100, 180)
        pygame.draw.rect(surface, border_color, button_rect, 2)
        
        # Draw gear icon with glow effect
        center_x = button_rect.centerx
        center_y = button_rect.centery
        radius = 12
        inner_radius = 6
        num_teeth = 8
        
        # Draw outer gear with glow
        if is_hovered:
            # Glow effect
            pygame.draw.circle(surface, (100, 100, 200, 100), (center_x, center_y), radius + 4)
        
        # Draw gear teeth
        for i in range(num_teeth):
            angle = 2 * math.pi * i / num_teeth
            outer_x = center_x + radius * math.cos(angle)
            outer_y = center_y + radius * math.sin(angle)
            inner_x = center_x + inner_radius * math.cos(angle + math.pi / num_teeth)
            inner_y = center_y + inner_radius * math.sin(angle + math.pi / num_teeth)
            
            # Draw tooth
            pygame.draw.line(surface, (180, 180, 255), (outer_x, outer_y), (inner_x, inner_y), 2)
        
        # Draw gear center circle
        pygame.draw.circle(surface, (180, 180, 255), (center_x, center_y), inner_radius)
        pygame.draw.circle(surface, (100, 100, 180), (center_x, center_y), inner_radius, 1)
        
        # Store the button rect for click detection
        self.settings_button_rect = button_rect
    
    def draw_settings_panel(self, surface, game_state=None):
        """Draw an enhanced settings panel with the same mysterious space theme."""
        # Create a semi-transparent overlay for the entire screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 200))
        surface.blit(overlay, (0, 0))
        
        # Add some particle effects (stars) in the background
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)
        
        # Create a semi-transparent panel
        panel_width = self.panel_width
        panel_height = 300
        panel_x = self.panel_x
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
        
        # Draw panel background with gradient
        for i in range(panel_height):
            progress = i / panel_height
            color = (
                int(20 + 30 * progress),
                int(20 + 30 * progress),
                int(50 + 30 * progress),
                220
            )
            panel_surface = pygame.Surface((panel_width, 1), pygame.SRCALPHA)
            panel_surface.fill(color)
            surface.blit(panel_surface, (panel_x, panel_y + i))
        
        # Draw panel border with glow effect
        pygame.draw.rect(surface, (100, 100, 180), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Draw settings title with glow effect
        settings_font = pygame.font.SysFont('Arial', 36, bold=True)
        glow_text = settings_font.render('SETTINGS', True, (40, 40, 100))
        surface.blit(glow_text, (panel_x + panel_width // 2 - glow_text.get_width() // 2 + 2, panel_y + 30 + 2))
        
        settings_text = settings_font.render('SETTINGS', True, (150, 150, 255))
        surface.blit(settings_text, (panel_x + panel_width // 2 - settings_text.get_width() // 2, panel_y + 30))
        
        
        # Sound effects label with enhanced styling
        sfx_font = pygame.font.SysFont('Arial', 22, bold=True)
        sfx_text = sfx_font.render('SOUND EFFECTS', True, (180, 180, 255))
        surface.blit(sfx_text, (panel_x + 20, panel_y + 100))
        
        # Sound effects slider
        sfx_slider_x = panel_x + 20
        sfx_slider_y = panel_y + 130
        sfx_slider_width = panel_width - 90
        
        # Draw slider background with gradient
        slider_height = 10
        # Draw slider background with hover effect
        slider_bg_color = (30, 30, 60, 220)
        if self.sfx_slider_clickable_rect.collidepoint(pygame.mouse.get_pos()):
            slider_bg_color = (40, 40, 80, 220)  # Brighter when hovered
        
        slider_bg_rect = pygame.Rect(sfx_slider_x, sfx_slider_y, sfx_slider_width, slider_height)
        for i in range(slider_height):
            progress = i / slider_height
            color = (
                int(20 + 20 * progress),
                int(20 + 20 * progress),
                int(40 + 20 * progress),
                220
            )
            slider_bg = pygame.Surface((sfx_slider_width, 1), pygame.SRCALPHA)
            slider_bg.fill(color)
            surface.blit(slider_bg, (slider_bg_rect.left, slider_bg_rect.top + i))
        
        # Draw slider border
        pygame.draw.rect(surface, (100, 100, 180), slider_bg_rect, 1)
        
        # Draw slider fill with gradient
        fill_width = int(sfx_slider_width * self.sound_manager.sfx_volume)
        fill_rect = pygame.Rect(sfx_slider_x, sfx_slider_y, fill_width, slider_height)
        for i in range(fill_rect.height):
            progress = i / fill_rect.height
            color = (
                int(40 + 60 * progress),
                int(40 + 60 * progress),
                int(120 + 80 * progress),
                220
            )
            fill_bg = pygame.Surface((fill_width, 1), pygame.SRCALPHA)
            fill_bg.fill(color)
            surface.blit(fill_bg, (fill_rect.left, fill_rect.top + i))
        
        # Draw slider handle with glow effect
        handle_x = sfx_slider_x + int(sfx_slider_width * self.sound_manager.sfx_volume)
        handle_y = sfx_slider_y + slider_height // 2
        handle_radius = 10
        
        # Ensure handle stays within slider bounds
        handle_x = max(sfx_slider_x, min(handle_x, sfx_slider_x + sfx_slider_width))
        
        # Update handle rect for click detection - make it slightly larger for easier clicking
        self.sfx_handle_rect = pygame.Rect(0, 0, 24, 24)  # Larger clickable area
        self.sfx_handle_rect.center = (handle_x, handle_y)
        
        # Draw handle with hover/drag effect
        is_hovered = self.sfx_handle_rect.collidepoint(pygame.mouse.get_pos())
        handle_color = (150, 150, 255)
        glow_color = (100, 100, 200, 150)
        
        if self.dragging_sfx_handle:
            handle_color = (180, 180, 255)  # Brighter when dragging
            glow_color = (120, 120, 220, 180)
        elif is_hovered:
            handle_color = (170, 170, 255)  # Slightly brighter when hovered
            glow_color = (110, 110, 210, 170)
        
        # Glow effect
        pygame.draw.circle(surface, glow_color, (handle_x, handle_y), handle_radius + 2)
        # Main handle
        pygame.draw.circle(surface, handle_color, (handle_x, handle_y), handle_radius)
        # Inner highlight
        pygame.draw.circle(surface, (200, 200, 255), (handle_x - 2, handle_y - 2), handle_radius // 2)
        
        # Draw a small indicator line to show the handle is draggable
        indicator_color = (180, 180, 255)
        pygame.draw.line(surface, indicator_color, 
                       (handle_x - 4, handle_y), 
                       (handle_x + 4, handle_y), 2)
        pygame.draw.line(surface, indicator_color, 
                       (handle_x, handle_y - 4), 
                       (handle_x, handle_y + 4), 2)
        
        # Update the handle rect position
        self.sfx_handle_rect = pygame.Rect(handle_x - handle_radius, handle_y - handle_radius, handle_radius * 2, handle_radius * 2)
        self.sfx_slider_rect = slider_bg_rect
        
        # Sound effects percentage
        percent_font = pygame.font.SysFont('Arial', 18)
        sfx_percent = percent_font.render(f"{int(self.sound_manager.sfx_volume * 100)}%", True, (180, 180, 255))
        surface.blit(sfx_percent, (sfx_slider_x + sfx_slider_width + 10, sfx_slider_y - 5))
        
        # Music label with enhanced styling
        music_font = pygame.font.SysFont('Arial', 22, bold=True)
        music_text = music_font.render('MUSIC', True, (180, 180, 255))
        surface.blit(music_text, (panel_x + 20, panel_y + 160))
        
        # Music slider
        music_slider_x = panel_x + 20
        music_slider_y = panel_y + 190
        music_slider_width = panel_width - 90
        
        # Draw slider background with gradient
        # Draw slider background with hover effect
        music_slider_bg_color = (30, 30, 60, 220)
        if self.music_slider_clickable_rect.collidepoint(pygame.mouse.get_pos()):
            music_slider_bg_color = (40, 40, 80, 220)  # Brighter when hovered
        
        music_slider_bg_rect = pygame.Rect(music_slider_x, music_slider_y, music_slider_width, slider_height)
        for i in range(slider_height):
            progress = i / slider_height
            color = (
                int(20 + 20 * progress),
                int(20 + 20 * progress),
                int(40 + 20 * progress),
                220
            )
            slider_bg = pygame.Surface((music_slider_width, 1), pygame.SRCALPHA)
            slider_bg.fill(color)
            surface.blit(slider_bg, (music_slider_bg_rect.left, music_slider_bg_rect.top + i))
        
        # Draw slider border
        pygame.draw.rect(surface, (100, 100, 180), music_slider_bg_rect, 1)
        
        # Draw slider fill with gradient
        music_fill_width = int(music_slider_width * self.sound_manager.music_volume)
        music_fill_rect = pygame.Rect(music_slider_x, music_slider_y, music_fill_width, slider_height)
        for i in range(music_fill_rect.height):
            progress = i / music_fill_rect.height
            color = (
                int(40 + 60 * progress),
                int(40 + 60 * progress),
                int(120 + 80 * progress),
                220
            )
            fill_bg = pygame.Surface((music_fill_width, 1), pygame.SRCALPHA)
            fill_bg.fill(color)
            surface.blit(fill_bg, (music_fill_rect.left, music_fill_rect.top + i))
        
        # Draw slider handle with glow effect
        music_handle_x = music_slider_x + int(music_slider_width * self.sound_manager.music_volume)
        music_handle_y = music_slider_y + slider_height // 2
        
        # Ensure handle stays within slider bounds
        music_handle_x = max(music_slider_x, min(music_handle_x, music_slider_x + music_slider_width))
        
        # Update handle rect for click detection - make it slightly larger for easier clicking
        self.music_handle_rect = pygame.Rect(0, 0, 24, 24)  # Larger clickable area
        self.music_handle_rect.center = (music_handle_x, music_handle_y)
        
        # Draw handle with hover/drag effect
        is_hovered = self.music_handle_rect.collidepoint(pygame.mouse.get_pos())
        handle_color = (150, 150, 255)
        glow_color = (100, 100, 200, 150)
        
        if self.dragging_music_handle:
            handle_color = (180, 180, 255)  # Brighter when dragging
            glow_color = (120, 120, 220, 180)
        elif is_hovered:
            handle_color = (170, 170, 255)  # Slightly brighter when hovered
            glow_color = (110, 110, 210, 170)
        
        # Glow effect
        pygame.draw.circle(surface, glow_color, (music_handle_x, music_handle_y), handle_radius + 2)
        # Main handle
        pygame.draw.circle(surface, handle_color, (music_handle_x, music_handle_y), handle_radius)
        # Inner highlight
        pygame.draw.circle(surface, (200, 200, 255), (music_handle_x - 2, music_handle_y - 2), handle_radius // 2)
        
        # Draw a small indicator line to show the handle is draggable
        indicator_color = (180, 180, 255)
        pygame.draw.line(surface, indicator_color, 
                       (music_handle_x - 4, music_handle_y), 
                       (music_handle_x + 4, music_handle_y), 2)
        pygame.draw.line(surface, indicator_color, 
                       (music_handle_x, music_handle_y - 4), 
                       (music_handle_x, music_handle_y + 4), 2)
        
        # Update the handle rect position
        self.music_handle_rect = pygame.Rect(music_handle_x - handle_radius, music_handle_y - handle_radius, handle_radius * 2, handle_radius * 2)
        self.music_slider_rect = music_slider_bg_rect
        
        # Music percentage
        music_percent = percent_font.render(f"{int(self.sound_manager.music_volume * 100)}%", True, (180, 180, 255))
        surface.blit(music_percent, (music_slider_x + music_slider_width + 10, music_slider_y - 5))
        
        # Button dimensions - make main menu button wider to fit text
        main_menu_button_width = 150  # Increased width for main menu button
        close_button_width = 120      # Original width for close button
        button_height = 40
        button_gap = 20  # Gap between buttons
        
        # If we're in the game (not in menu or game over), show the main menu button
        if game_state == 1:  # GAME_STATE_PLAYING
            # Calculate positions for a row layout with two buttons
            total_width = (main_menu_button_width + close_button_width) + button_gap
            row_start_x = panel_x + (panel_width - total_width) // 2
            
            # Draw main menu button (left button)
            main_menu_button_rect = pygame.Rect(
                row_start_x,
                panel_y + 240,  # Both buttons at the same y position
                main_menu_button_width, 
                button_height
            )
            
            # Store the main menu button rect for click detection
            self.settings_main_menu_rect = main_menu_button_rect
            
            is_menu_hovered = main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
            self._draw_stylized_button(surface, main_menu_button_rect, "MAIN MENU", (60, 20, 40), (180, 80, 100), is_menu_hovered)
            
            # Draw close button (right button)
            close_button_rect = pygame.Rect(
                row_start_x + main_menu_button_width + button_gap,  # Position after main menu button + gap
                panel_y + 240,  # Same y position
                close_button_width, 
                button_height
            )
        else:
            # No main menu button needed, just the close button centered
            self.settings_main_menu_rect = None
            
            # Draw close button in the standard position (centered)
            close_button_rect = pygame.Rect(
                panel_x + panel_width // 2 - close_button_width // 2, 
                panel_y + 240,
                close_button_width, 
                button_height
            )
        
        # Store the close button rect for consistent click detection
        self.close_button_rect = close_button_rect
        
        is_close_hovered = close_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, close_button_rect, "CLOSE", (30, 30, 80), (80, 80, 180), is_close_hovered)
        
        # Draw confirmation dialog if active
        if self.show_confirmation:
            self._draw_confirmation_dialog(surface)
        
        return close_button_rect
    
    def handle_settings_click(self, pos):
        """Handle clicks in the settings panel."""
        # If confirmation dialog is active, handle its clicks first
        if self.show_confirmation:
            if self.confirm_yes_rect and self.confirm_yes_rect.collidepoint(pos):
                # User confirmed going to main menu
                self.show_confirmation = False
                self.settings_open = False
                return "main_menu"  # Return special value to indicate main menu transition
            elif self.confirm_no_rect and self.confirm_no_rect.collidepoint(pos):
                # User cancelled
                self.show_confirmation = False
                return True
            elif not self.confirmation_rect.collidepoint(pos):
                # Clicked outside the dialog, treat as cancel
                self.show_confirmation = False
                return True
            return True  # Consumed the click
            
        # Normal settings panel clicks
        if self.settings_button_rect.collidepoint(pos):
            self.settings_open = not self.settings_open
            return True
        
        if self.settings_open:
            # Check if main menu button was clicked
            if self.settings_main_menu_rect and self.settings_main_menu_rect.collidepoint(pos):
                # Show confirmation dialog instead of immediately going to main menu
                self.show_confirmation = True
                return True
                
            # Check if SFX slider handle was clicked (only the handle)
            if self.sfx_handle_rect.collidepoint(pos):
                self.dragging_sfx_handle = True
                # Store offset between mouse and handle center for smooth dragging
                self.sfx_drag_offset = pos[0] - self.sfx_handle_rect.centerx
                return True
            
            # Check if music slider handle was clicked (only the handle)
            elif self.music_handle_rect.collidepoint(pos):
                self.dragging_music_handle = True
                # Store offset between mouse and handle center for smooth dragging
                self.music_drag_offset = pos[0] - self.music_handle_rect.centerx
                return True
            
            # Check if SFX slider bar was clicked (not the handle)
            elif self.sfx_slider_rect.collidepoint(pos):
                # Calculate new volume based on click position
                slider_left = self.sfx_slider_rect.left
                slider_width = self.sfx_slider_rect.width
                volume_ratio = (pos[0] - slider_left) / slider_width
                volume_ratio = max(0, min(1, volume_ratio))
                
                # Update volume
                self.sound_manager.set_sfx_volume(volume_ratio)
                return True
            
            # Check if music slider bar was clicked (not the handle)
            elif self.music_slider_rect.collidepoint(pos):
                # Calculate new volume based on click position
                slider_left = self.music_slider_rect.left
                slider_width = self.music_slider_rect.width
                volume_ratio = (pos[0] - slider_left) / slider_width
                volume_ratio = max(0, min(1, volume_ratio))
                
                # Update volume
                self.sound_manager.set_music_volume(volume_ratio)
                return True
            
            # Check if close button was clicked
            if self.close_button_rect and self.close_button_rect.collidepoint(pos):
                self.settings_open = False
                return True
        
        return False
        
    def handle_mouse_up(self):
        """Handle mouse button up events."""
        self.dragging_sfx_handle = False
        self.dragging_music_handle = False
        self.sfx_drag_offset = 0
        self.music_drag_offset = 0
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion events."""
        if self.dragging_sfx_handle:
            # Update SFX handle position, accounting for drag offset
            mouse_x = pos[0] - self.sfx_drag_offset
            slider_left = self.sfx_slider_rect.left
            slider_right = self.sfx_slider_rect.right
            slider_width = self.sfx_slider_rect.width
            
            # Keep handle within slider bounds
            new_x = max(slider_left, min(mouse_x, slider_right))
            
            # Only update if position changed
            if new_x != self.sfx_handle_rect.centerx:
                self.sfx_handle_rect.centerx = new_x
                
                # Update volume based on handle position
                volume_ratio = (new_x - slider_left) / slider_width
                volume_ratio = max(0, min(1, volume_ratio))  # Clamp between 0 and 1
                self.sound_manager.set_sfx_volume(volume_ratio)
            
            return True
        
        elif self.dragging_music_handle:
            # Update music handle position, accounting for drag offset
            mouse_x = pos[0] - self.music_drag_offset
            slider_left = self.music_slider_rect.left
            slider_right = self.music_slider_rect.right
            slider_width = self.music_slider_rect.width
            
            # Keep handle within slider bounds
            new_x = max(slider_left, min(mouse_x, slider_right))
            
            # Only update if position changed
            if new_x != self.music_handle_rect.centerx:
                self.music_handle_rect.centerx = new_x
                
                # Update volume based on handle position
                volume_ratio = (new_x - slider_left) / slider_width
                volume_ratio = max(0, min(1, volume_ratio))  # Clamp between 0 and 1
                self.sound_manager.set_music_volume(volume_ratio)
            
            return True
        
        return False
    
    def show_score(self, surface, score, health, max_health=3):
        """Display score and health with enhanced visual styling."""
        # Create a semi-transparent panel for the score
        score_panel_width = 150
        score_panel_height = 40
        score_panel_rect = pygame.Rect(10, 10, score_panel_width, score_panel_height)
        
        # Draw panel background with gradient
        for i in range(score_panel_height):
            progress = i / score_panel_height
            color = (
                int(20 + 20 * progress),
                int(20 + 20 * progress),
                int(40 + 20 * progress),
                180
            )
            panel_surface = pygame.Surface((score_panel_width, 1), pygame.SRCALPHA)
            panel_surface.fill(color)
            surface.blit(panel_surface, (score_panel_rect.left, score_panel_rect.top + i))
        
        # Draw panel border with glow effect
        pygame.draw.rect(surface, (100, 100, 180), score_panel_rect, 1)
        
        # Draw score with glow effect
        score_font = pygame.font.SysFont('Arial', 24, bold=True)
        score_text = f"SCORE: {score}"
        
        # Glow effect
        glow_text = score_font.render(score_text, True, (40, 40, 100))
        surface.blit(glow_text, (20 + 1, 18 + 1))
        
        # Main text
        main_text = score_font.render(score_text, True, (150, 150, 255))
        surface.blit(main_text, (20, 18))
        
        # Create a semi-transparent panel for health
        health_panel_width = max_health * 45 + 20
        health_panel_height = 40
        health_panel_rect = pygame.Rect(10, 60, health_panel_width, health_panel_height)
        
        # Draw panel background with gradient
        for i in range(health_panel_height):
            progress = i / health_panel_height
            color = (
                int(40 + 10 * progress),
                int(10 + 10 * progress),
                int(10 + 10 * progress),
                180
            )
            panel_surface = pygame.Surface((health_panel_width, 1), pygame.SRCALPHA)
            panel_surface.fill(color)
            surface.blit(panel_surface, (health_panel_rect.left, health_panel_rect.top + i))
        
        # Draw panel border with glow effect
        pygame.draw.rect(surface, (180, 100, 100), health_panel_rect, 1)
        
        # Draw health hearts with animation effect
        heart_spacing = 45
        for i in range(max_health):
            heart_x = 20 + i * heart_spacing
            heart_y = 70
            
            # Use the existing heart images with added effects
            if i < health:
                # Add pulsing glow effect to full hearts
                pulse_factor = 0.8 + 0.2 * abs(math.sin(pygame.time.get_ticks() * 0.003 + i * 0.5))
                glow_size = int(40 * pulse_factor)
                
                # Create a glow surface
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 100, 100, 50), (glow_size//2, glow_size//2), glow_size//2)
                
                # Blit the glow and then the heart
                surface.blit(glow_surface, (heart_x - 5, heart_y - 5))
                surface.blit(self.full_heart_img, (heart_x, heart_y))
            else:
                # Just draw the empty heart
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
        panel_width, panel_height = 500, 340  # Increased height for better padding
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
                        (panel_rect.left + 20, panel_rect.bottom - 30),  # Moved up to 30px from bottom
                        (panel_rect.left + panel_width - 20, panel_rect.bottom - 30), 2)
        
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
        is_restart_hovered = restart_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, restart_button_rect, "RESTART", (60, 10, 10), (150, 30, 30), is_restart_hovered)
        
        # Create main menu button with proper padding and gap
        main_menu_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - restart_button_width // 2, 
                                    panel_rect.top + 250,  # Increased gap from first button (from 180 to 250 = 70px gap)
                                    restart_button_width, restart_button_height)
        is_menu_hovered = main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, main_menu_button_rect, "MAIN MENU", (30, 30, 60), (70, 70, 140), is_menu_hovered)
        
        # Store button rectangles for click detection - make sure these are class variables
        self.start_button_rect = restart_button_rect
        self.main_menu_button_rect = main_menu_button_rect  # Store the main menu button rect
        self.test_button_rect = None  # No test button on game over screen
        
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
                        (panel_rect.left + 20, panel_rect.bottom - 30),  # Moved up to 30px from bottom
                        (panel_rect.left + panel_width - 20, panel_rect.bottom - 30), 2)
        
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
        is_restart_hovered = restart_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, restart_button_rect, "RESTART", (60, 10, 10), (150, 30, 30), is_restart_hovered)
        
        # Create main menu button with proper padding and gap
        main_menu_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - restart_button_width // 2, 
                                    panel_rect.top + 250,  # Increased gap from first button (from 180 to 250 = 70px gap)
                                    restart_button_width, restart_button_height)
        is_menu_hovered = main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, main_menu_button_rect, "MAIN MENU", (30, 30, 60), (70, 70, 140), is_menu_hovered)
        
        # Store button rectangles for click detection - make sure these are class variables
        self.start_button_rect = restart_button_rect
        self.main_menu_button_rect = main_menu_button_rect  # Store the main menu button rect
        self.test_button_rect = None  # No test button on game over screen
    
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
        is_start_hovered = start_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, start_button_rect, "START GAME", (30, 30, 80), (80, 80, 180), is_start_hovered)
        
        # Test Mode Button (only shown during development if testing_mode is True)
        if testing_mode:
            test_button_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40, 100, 30)
            is_test_hovered = test_button_rect.collidepoint(pygame.mouse.get_pos())
            self._draw_stylized_button(surface, test_button_rect, "TEST MODE", (40, 20, 60), (120, 80, 140), is_test_hovered)
            self.test_button_rect = test_button_rect
        else:
            self.test_button_rect = None
        
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
        # Make sure we clear the main menu button rect when showing the start screen
        # to avoid confusion with the game over screen
        self.main_menu_button_rect = None
        
        # Show testing mode instructions (only during development)
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
    
    def _draw_stylized_button(self, surface, rect, text, color_dark, color_light, is_hovered=False):
        """Draw a stylized button with a space theme."""
        # Draw button background with gradient
        for i in range(rect.height):
            progress = i / rect.height
            
            # Brighten colors if hovered
            if is_hovered:
                color = (
                    min(255, int(color_dark[0] + (color_light[0] - color_dark[0]) * progress + 30)),
                    min(255, int(color_dark[1] + (color_light[1] - color_dark[1]) * progress + 30)),
                    min(255, int(color_dark[2] + (color_light[2] - color_dark[2]) * progress + 30))
                )
            else:
                color = (
                    int(color_dark[0] + (color_light[0] - color_dark[0]) * progress),
                    int(color_dark[1] + (color_light[1] - color_dark[1]) * progress),
                    int(color_dark[2] + (color_light[2] - color_dark[2]) * progress)
                )
            pygame.draw.line(surface, color, (rect.left, rect.top + i), (rect.right, rect.top + i))
        
        # Draw button border with glow effect
        border_color = (min(255, color_light[0] + 30 if is_hovered else color_light[0]),
                        min(255, color_light[1] + 30 if is_hovered else color_light[1]),
                        min(255, color_light[2] + 30 if is_hovered else color_light[2]))
        pygame.draw.rect(surface, border_color, rect, 2)
        
        # Add some "tech" details to the button
        pygame.draw.line(surface, (100, 100, 200, 150), 
                        (rect.left + 10, rect.top + 5), 
                        (rect.left + rect.width - 20, rect.top + 5), 1)
        pygame.draw.line(surface, (100, 100, 200, 150), 
                        (rect.left + 10, rect.bottom - 5), 
                        (rect.left + rect.width - 20, rect.bottom - 5), 1)
        
        # Draw text
        font = pygame.font.SysFont('Arial', 24, bold=True)
        text_color = (240, 240, 255) if is_hovered else (220, 220, 255)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def _draw_confirmation_dialog(self, surface):
        """Draw a confirmation dialog for returning to main menu."""
        # Create a dark overlay for the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Darker overlay for the confirmation dialog
        surface.blit(overlay, (0, 0))
        
        # Create dialog box
        dialog_width, dialog_height = 400, 200
        dialog_x = SCREEN_WIDTH // 2 - dialog_width // 2
        dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        
        # Draw dialog background with gradient
        for i in range(dialog_height):
            progress = i / dialog_height
            color = (
                int(40 + 20 * progress),
                int(20 + 10 * progress),
                int(30 + 20 * progress),
                240
            )
            dialog_surface = pygame.Surface((dialog_width, 1), pygame.SRCALPHA)
            dialog_surface.fill(color)
            surface.blit(dialog_surface, (dialog_x, dialog_y + i))
        
        # Draw dialog border with glow effect
        pygame.draw.rect(surface, (180, 80, 100), dialog_rect, 2)
        
        # Add tech details to the dialog
        pygame.draw.line(surface, (200, 100, 80, 150), 
                       (dialog_x + 20, dialog_y + 20), 
                       (dialog_x + dialog_width - 20, dialog_y + 20), 2)
        pygame.draw.line(surface, (200, 100, 80, 150), 
                       (dialog_x + 20, dialog_y + dialog_height - 20), 
                       (dialog_x + dialog_width - 20, dialog_y + dialog_height - 20), 2)
        
        # Draw warning text
        warning_font = pygame.font.SysFont('Arial', 24, bold=True)
        warning_text = warning_font.render("Return to Main Menu?", True, (255, 200, 180))
        surface.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, dialog_y + 40))
        
        # Draw confirmation message
        confirm_font = pygame.font.SysFont('Arial', 18)
        confirm_text = confirm_font.render("Are you sure? Your current progress will be lost.", True, (220, 220, 255))
        surface.blit(confirm_text, (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, dialog_y + 80))
        
        # Draw Yes button
        yes_button_width, yes_button_height = 100, 40
        yes_button_rect = pygame.Rect(dialog_x + dialog_width // 4 - yes_button_width // 2, 
                                    dialog_y + 130, 
                                    yes_button_width, yes_button_height)
        is_yes_hovered = yes_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, yes_button_rect, "YES", (60, 20, 20), (200, 80, 80), is_yes_hovered)
        
        # Draw No button
        no_button_width, no_button_height = 100, 40
        no_button_rect = pygame.Rect(dialog_x + dialog_width * 3 // 4 - no_button_width // 2, 
                                   dialog_y + 130, 
                                   no_button_width, no_button_height)
        is_no_hovered = no_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, no_button_rect, "NO", (30, 30, 60), (80, 80, 180), is_no_hovered)
        
        # Store button rectangles for click detection
        self.confirmation_rect = dialog_rect
        self.confirm_yes_rect = yes_button_rect
        self.confirm_no_rect = no_button_rect