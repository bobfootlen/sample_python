import pygame

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.backgrounds = {}
        self.trees = {}
        self.load_assets()
    
    def load_assets(self):
        """Load all game assets"""
        # Load player sprites
        self.sprites['up'] = pygame.image.load('img/up.png').convert_alpha()
        self.sprites['down'] = pygame.image.load('img/down.png').convert_alpha()
        self.sprites['left'] = pygame.image.load('img/left.png').convert_alpha()
        self.sprites['right'] = pygame.image.load('img/right.png').convert_alpha()
        
        # Load remote player sprites
        self.sprites['remote_up'] = pygame.image.load('img/remote_up.png').convert_alpha()
        self.sprites['remote_down'] = pygame.image.load('img/remote_down.png').convert_alpha()
        self.sprites['remote_left'] = pygame.image.load('img/remote_left.png').convert_alpha()
        self.sprites['remote_right'] = pygame.image.load('img/remote_right.png').convert_alpha()

        # Load trees
        self.trees['tree_1'] = pygame.image.load('img/tree-1.png').convert_alpha()
        self.trees['tree_2'] = pygame.image.load('img/tree-2.png').convert_alpha()
        
        # Load background
        self.backgrounds['main'] = pygame.image.load('img/backround1.png').convert_alpha()
    
    def get_sprite(self, direction):
        """Get sprite for a given direction"""
        return self.sprites.get(direction, self.sprites['up'])
    
    def get_remote_sprite(self, direction):
        """Get remote player sprite for a given direction"""
        remote_key = f'remote_{direction}'
        return self.sprites.get(remote_key, self.sprites['remote_up'])
    
    def get_tree(self, tree_name):
        """Get tree sprite by name"""
        return self.trees.get(tree_name)
    
    def get_background(self, background_name='main'):
        """Get background by name"""
        return self.backgrounds.get(background_name)
