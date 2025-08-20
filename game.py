import pygame
from network_manager import NetworkManager
from asset_manager import AssetManager
from player import Player
from renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('sprite move')
        
        # Initialize components
        self.asset_manager = AssetManager()
        self.renderer = Renderer(self.screen, self.asset_manager)
        self.network_manager = NetworkManager()
        
        # Initialize multiple players
        self.players = [
            Player(player_id=1, x=200, y=200, speed=5),  # Player 1
            Player(player_id=2, x=300, y=300, speed=5)   # Player 2
        ]
        
        # Game state
        self.run = True
        self.clock = pygame.time.Clock()
        self.frame = 0
        
        # Camera position (for scrolling background) - follows player 1
        self.camera_x = 40
        self.camera_y = 0
        
        self.setup_networking()
    
    def setup_networking(self):
        """Setup networking based on user input"""
        remote = input("server address (press Enter for server mode): ")
        if remote:
            username = input("username: ")
            self.network_manager.setup_client(remote, username)
        else:
            self.network_manager.setup_server()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
    
    def update(self):
        """Update game state"""
        # Get key inputs
        keys = pygame.key.get_pressed()
        
        # Update all players
        for player in self.players:
            # Handle player movement
            face, x, y = player.handle_movement(keys)
            
            # Handle speed changes
            player.handle_speed_input(keys)
            
            # Handle wall boundaries
            player.handle_walls()
        
        # Camera follows player 1
        player1_x, player1_y = self.players[0].get_position()
        self.camera_x = player1_x
        self.camera_y = player1_y
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.renderer.clear_screen()
        
        # Draw background and trees
        self.renderer.draw_background(self.camera_x, self.camera_y)
        self.renderer.draw_trees(self.camera_x, self.camera_y)
        
        # Draw all local players
        self.renderer.draw_players(self.players, self.camera_x, self.camera_y)
        
        # Draw remote players
        remote_players = self.network_manager.get_players()
        self.renderer.draw_remote_players(remote_players, self.camera_x, self.camera_y)
        
        # Update display
        fps = self.clock.get_fps()
        self.renderer.update_display(self.camera_x, self.camera_y, fps, len(self.players))
    
    def network_update(self):
        """Handle networking updates"""
        if self.network_manager.is_client_mode():
            # Send position of player 1 for networking
            x, y = self.players[0].get_position()
            self.network_manager.send_position(x, y)
        else:
            # Server mode - print client info periodically
            if self.frame % 600 == 0:
                print(f"Connected clients: {len(self.network_manager.get_clients())}")
    
    def run_game(self):
        """Main game loop"""
        while self.run:
            # Limit to 60 FPS
            self.clock.tick(60)
            
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render
            self.render()
            
            # Network updates
            self.network_update()
            
            self.frame += 1
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()
