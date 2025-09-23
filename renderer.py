import pygame
from asset_manager import AssetManager

class Renderer:
    def __init__(self, screen, asset_manager:AssetManager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.bg_color = (50, 50, 50)
    
    def clear_screen(self):
        """Clear the screen with background color"""
        self.screen.fill(self.bg_color)
    
    def draw_background(self, camera_x, camera_y):
        """Draw the background at given coordinates, offset by camera"""
        background = self.asset_manager.get_background()
        # Adjust background position by camera offset
        self.screen.blit(background, (-camera_x, -camera_y))

    def draw_trees(self, camera_x, camera_y):
        """Draw trees at given coordinates, offset by camera"""
        tree_1 = self.asset_manager.get_tree('tree_1')
        tree_2 = self.asset_manager.get_tree('tree_2')

        # Adjust tree positions by camera offset
        self.screen.blit(tree_1, (300 - camera_x, 300 - camera_y))
        self.screen.blit(tree_2, (100 - camera_x, 100 - camera_y))

    def draw_player(self, player, camera_x, camera_y):
        """Draw a local player relative to the camera"""
        face = player.get_facing()
        sprite = self.asset_manager.get_sprite(face)
        # The local player being followed by camera is drawn at screen center
        screen_x = self.screen.get_width() // 2
        screen_y = self.screen.get_height() // 2

        self.screen.blit(sprite, (screen_x, screen_y))

    def draw_players(self, players, camera_x, camera_y):
        """Draw all local players"""
        # There's only one local player, so we draw it directly.
        # This method is kept for consistency with how it's called in game.py
        if players:
            self.draw_player(players[0], camera_x, camera_y)

    def draw_remote_players(self, remote_players, camera_x, camera_y):
        """Draw all remote players, adjusting for camera position"""
        for player_id, player_data in remote_players.items():
            # Exclude the local player (player_id 1)
            ##continue

            p_x = player_data['x']
            p_y = player_data['y']
            face = player_data['face']
            
            # Calculate screen coordinates relative to camera
            screen_x = p_x - camera_x
            screen_y = p_y - camera_y
            # Use the received face for remote players
            sprite = self.asset_manager.get_remote_sprite(face)
            self.screen.blit(sprite, (screen_x, screen_y))

    def update_display(self, x, y, fps, num_players):
        """Update the display caption with current info"""
        pygame.display.set_caption(f"python game: cam_x: {x} cam_y: {y} fps: {fps:.2f} players: {num_players}")
        pygame.display.update()
