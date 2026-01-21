from typing import List
import pygame
from network_manager import NetworkManager
from asset_manager import AssetManager
from player import Player
from renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        
        # Initialize Pygame mixer for music
        pygame.mixer.init()
        
        # Screen setup
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('sprite move')
        
        # Initialize components
        self.asset_manager = AssetManager()
        self.renderer = Renderer(self.screen, self.asset_manager)
        self.network_manager = NetworkManager()
        
        # Initialize single player
        player1_input_map = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'speed_1': pygame.K_1,
            'speed_5': pygame.K_5,
            'speed_0': pygame.K_0
        }

        self.player_name = "Player"  # Default name, will be set by setup_networking
        self.players = [
            Player(x=200, y=200, speed=5, name=self.player_name)
        ]
        self.network_manager.set_local_players_ref(self.players)
        
        # Game state
        self.run = True
        self.clock = pygame.time.Clock()
        self.frame = 0
        
        # Camera position (for scrolling background) - follows player 1
        self.screen_center_x = self.SCREEN_WIDTH // 2
        self.screen_center_y = self.SCREEN_HEIGHT // 2
        
        self.camera_x = 0
        self.camera_y = 0
        
        # Block storage - list of dictionaries with 'x' and 'y' positions
        self.placed_blocks: List[Block] = []
        
        # Grid size for block alignment
        self.GRID_SIZE = 100
        
        # Track key states to prevent continuous placement/destruction
        self.space_pressed = False
        self.q_pressed = False
        
        # Load and start background music
        self.setup_music()
        
        # Removed setup_networking from __init__
    
    def setup_music(self):
        """Setup background music"""
        try:
            pygame.mixer.music.load("Sample_Python/BeepBox.mp3")
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except pygame.error:
            print("Error loading music file - continuing without music")
    
    def setup_networking(self, mode='server', server_address=None, username=None):
        """Setup networking based on provided parameters"""
        if username:
            self.player_name = username
            # Update the player's name
            if self.players:
                self.players[0].name = username
        
        if mode == 'client' and server_address and username:
            self.network_manager.setup_client(server_address, username)
        else:
            self.network_manager.setup_server()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = True
                elif event.key == pygame.K_q:
                    self.q_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = False
                elif event.key == pygame.K_q:
                    self.q_pressed = False
    
    def update(self):
        """Update game state"""
        # Get key inputs
        keys = pygame.key.get_pressed()
        
        # Update all players
        for player in self.players:
            # Handle player movement
            player.handle_movement(keys)
            
            # Handle speed changes
            player.handle_speed_input(keys)
            
            # Handle wall boundaries
            player.handle_walls()
            
            # Handle block placement (space key)
            if self.space_pressed:
                self.place_block(player)
                self.space_pressed = False  # Reset to prevent continuous placement
            
            # Handle block destruction (q key)
            if self.q_pressed:
                self.destroy_block(player)
                self.q_pressed = False  # Reset to prevent continuous destruction
        
        # Camera follows player 1, keeping player 1 centered
        player1_x, player1_y = self.players[0].get_position()
        self.camera_x = player1_x - self.screen_center_x
        self.camera_y = player1_y - self.screen_center_y
    
    def place_block(self, player: Player):
        """Place a block in front of the player, aligned to grid"""
        
        # Get the position of the block the player is facing
        block_x, block_y = player.get_facing_block_position(self.GRID_SIZE)
        
        # Check if block already exists at this position
        block_pos = (block_x, block_y)
        if block_pos not in [(b.x, b.y) for b in self.placed_blocks]:
            self.placed_blocks.append(Block(block_x, block_y))
    
    def destroy_block(self, player: Player):
        """Destroy the block the player is facing"""
        # Get the position of the block the player is facing
        block_x, block_y = player.get_facing_block_position(self.GRID_SIZE)
        # Remove block at this position if it exists
        self.placed_blocks = [b for b in  self.placed_blocks if (b.x, b.y) != (block_x, block_y)]
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.renderer.clear_screen()
        
        # Draw background and trees
        self.renderer.draw_background(self.camera_x, self.camera_y)
        self.renderer.draw_trees(self.camera_x, self.camera_y)
        
        # Draw placed blocks
        self.renderer.draw_blocks(self.placed_blocks, self.camera_x, self.camera_y)
        
        # Draw remote players
        remote_players = self.network_manager.get_players()
        self.renderer.draw_remote_players(self.player_name,remote_players, self.camera_x, self.camera_y)
        
        # Draw all local players
        self.renderer.draw_players(self.players, self.camera_x, self.camera_y, self.GRID_SIZE)
        
        # Update display
        fps = self.clock.get_fps()
        self.renderer.update_display(self.camera_x, self.camera_y, fps, len(self.players))
    
    def network_update(self):
        """Handle networking updates"""
        if self.network_manager.is_client_mode():
            # Send position and facing of player 1 for networking
            player1 = self.players[0]
            x, y = player1.get_position()
            face = player1.get_facing()
            self.network_manager.send_position(1, x, y, face)
        else:
            # Server mode - broadcast player info periodically
            if self.frame % 1 == 0: # Broadcast every 10 frames
                self.network_manager.broadcast_player_states()
            # Also print client info periodically
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
        
        # Stop music before quitting
        pygame.mixer.music.stop()
        pygame.quit()

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 10
        self.max_hp = 10
        self.block_type = "stone"
        self.block_image = pygame.image.load("img/block1.png")
        #self.block_image_broken = pygame.image.load("img/block_1_broken.png")
        #self.block_image_destroyed = pygame.image.load("img/block_1_destroyed.png")
        #self.block_image_destroyed_broken = pygame.image.load("img/block_1_destroyed_broken.png")
        #self.block_image_destroyed_broken_destroyed = pygame.image.load("img/block_1_destroyed_broken_destroyed.png")

if __name__ == "__main__":
    game = Game()
    # setup_networking will be called from GUI or can be called manually
    game.setup_networking()
    game.run_game()
