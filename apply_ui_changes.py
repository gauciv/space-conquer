#!/usr/bin/env python3
"""
Script to apply UI manager changes.
"""
import os
import re

def main():
    # Read the original file
    with open('space_impact/utils/ui_manager.py', 'r') as f:
        content = f.read()
    
    # Add to __init__ method
    init_addition = """        # For main menu button in settings
        self.settings_main_menu_rect = None
        
        # Confirmation dialog elements
        self.show_confirmation = False
        self.confirmation_rect = None
        self.confirm_yes_rect = None
        self.confirm_no_rect = None
"""
    content = content.replace('        # Button hover state', init_addition + '        # Button hover state')
    
    # Change draw_settings_panel method signature
    content = content.replace('    def draw_settings_panel(self, surface):', 
                             '    def draw_settings_panel(self, surface, game_state=None):')
    
    # Replace the end of draw_settings_panel method
    old_end = """        # Music percentage
        music_percent = percent_font.render(f"{int(self.sound_manager.music_volume * 100)}%", True, (180, 180, 255))
        surface.blit(music_percent, (music_slider_x + music_slider_width + 10, music_slider_y - 5))
        
        # Draw close button with the same style as other buttons
        close_button_width, close_button_height = 120, 40
        close_button_rect = pygame.Rect(panel_x + panel_width // 2 - close_button_width // 2, 
                                      panel_y + 240, # Moved up from 250 to add bottom margin
                                      close_button_width, close_button_height)
        
        # Store the close button rect for consistent click detection
        self.close_button_rect = close_button_rect
        
        is_close_hovered = close_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, close_button_rect, "CLOSE", (30, 30, 80), (80, 80, 180), is_close_hovered)
        
        return close_button_rect"""
    
    new_end = """        # Music percentage
        music_percent = percent_font.render(f"{int(self.sound_manager.music_volume * 100)}%", True, (180, 180, 255))
        surface.blit(music_percent, (music_slider_x + music_slider_width + 10, music_slider_y - 5))
        
        # Button dimensions
        button_width, button_height = 120, 40
        
        # If we're in the game (not in menu or game over), show the main menu button
        if game_state == 1:  # GAME_STATE_PLAYING
            # Draw main menu button first (above close button)
            main_menu_button_rect = pygame.Rect(panel_x + panel_width // 2 - button_width // 2, 
                                          panel_y + 190, # Position above close button
                                          button_width, button_height)
            
            # Store the main menu button rect for click detection
            self.settings_main_menu_rect = main_menu_button_rect
            
            is_menu_hovered = main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
            self._draw_stylized_button(surface, main_menu_button_rect, "MAIN MENU", (60, 20, 40), (180, 80, 100), is_menu_hovered)
            
            # Draw close button below main menu button
            close_button_rect = pygame.Rect(panel_x + panel_width // 2 - button_width // 2, 
                                          panel_y + 240, # Below main menu button
                                          button_width, button_height)
        else:
            # No main menu button needed, just the close button
            self.settings_main_menu_rect = None
            
            # Draw close button in the standard position
            close_button_rect = pygame.Rect(panel_x + panel_width // 2 - button_width // 2, 
                                          panel_y + 240,
                                          button_width, button_height)
        
        # Store the close button rect for consistent click detection
        self.close_button_rect = close_button_rect
        
        is_close_hovered = close_button_rect.collidepoint(pygame.mouse.get_pos())
        self._draw_stylized_button(surface, close_button_rect, "CLOSE", (30, 30, 80), (80, 80, 180), is_close_hovered)
        
        # Draw confirmation dialog if active
        if self.show_confirmation:
            self._draw_confirmation_dialog(surface)
        
        return close_button_rect"""
    
    content = content.replace(old_end, new_end)
    
    # Add _draw_confirmation_dialog method
    confirmation_dialog = """
    def _draw_confirmation_dialog(self, surface):
        \"\"\"Draw a confirmation dialog for returning to main menu.\"\"\"
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
        self.confirm_no_rect = no_button_rect"""
    
    # Find the handle_settings_click method
    handle_settings_click_pattern = r'def handle_settings_click\(self, pos\):(.*?)(?=def|$)'
    handle_settings_click_match = re.search(handle_settings_click_pattern, content, re.DOTALL)
    
    if handle_settings_click_match:
        old_method = handle_settings_click_match.group(0)
        
        new_method = """def handle_settings_click(self, pos):
        \"\"\"Handle clicks in the settings panel.\"\"\"
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
        
        return False"""
        
        content = content.replace(old_method, new_method)
    
    # Add the confirmation dialog method
    content += confirmation_dialog
    
    # Write the updated content back to the file
    with open('space_impact/utils/ui_manager.py', 'w') as f:
        f.write(content)
    
    print("UI manager changes applied successfully!")

if __name__ == "__main__":
    main()
