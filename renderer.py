import pygame

class Renderer:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.bg_color = (50, 50, 50)
    
    def clear_screen(self):
        """Clear the screen with background color"""
        self.screen.fill(self.bg_color)
    
    def draw_background(self, x, y):
        """Draw the background at given coordinates"""
        background = self.asset_manager.get_background()
        self.screen.blit(background, (x, y))
    
    def draw_trees(self, x, y):
        """Draw trees at given coordinates"""
        tree_1 = self.asset_manager.get_tree('tree_1')
        tree_2 = self.asset_manager.get_tree('tree_2')
        
        self.screen.blit(tree_1, (x + 300, y + 300))
        self.screen.blit(tree_2, (x + 100, y + 100))
    
    def draw_player(self, player, player_x, player_y):
        """Draw the main player"""
        face = player.get_facing()
        sprite = self.asset_manager.get_sprite(face)
        self.screen.blit(sprite, (player_x, player_y))
    
    def draw_remote_players(self, players, camera_x, camera_y):
        """Draw all remote players"""
        for player_addr, (p_x, p_y) in players.items():
            # Draw remote players relative to camera position
            screen_x = p_x - camera_x
            screen_y = p_y - camera_y
            # Use a default sprite for remote players
            sprite = self.asset_manager.get_sprite('up')
            self.screen.blit(sprite, (screen_x, screen_y))
    
    def update_display(self, x, y, fps):
        """Update the display caption with current info"""
        pygame.display.set_caption(f"python game: {x} {y} fps: {fps:.2f}")
        pygame.display.update()
