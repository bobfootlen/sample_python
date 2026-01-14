import pygame

class Player:
    def __init__(self, x=200, y=200, speed=5, player_id="host", name="Player"):
        self.x = x
        self.y = y
        self.speed = speed
        self.face = "none"
        self.player_id = player_id
        self.name = name

    def handle_speed_input(self, keys):
        """Handle speed changes based on key input"""
        if keys[pygame.K_1]:
            self.speed = 1
        if keys[pygame.K_5]:
            self.speed = 5
        if keys[pygame.K_0]:
            self.speed = 20
        return self.speed
        
    def handle_movement(self, keys):
        """Handle movement based on key input"""
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.face = "left"
        if keys[pygame.K_d]:
            self.x += self.speed
            self.face = "right"
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.face = "up"
        if keys[pygame.K_s]:
            self.y += self.speed
            self.face = "down"

    def handle_walls(self):
        """Handle wall boundaries"""
        if self.x < 0:
            self.x = 0
        if self.x > 9900:
            self.x = 9900
        if self.y < 0:
            self.y = 0
        if self.y > 9900:
            self.y = 9900
        return self.x, self.y

    def get_facing_block_position(self, GRID_SIZE):
        face = self.face
        block_x = self.x
        block_y = self.y
        
        if face == "up":
            block_y -= GRID_SIZE // 2
            block_x += GRID_SIZE // 2
        elif face == "down":
            block_y += GRID_SIZE+GRID_SIZE // 2
            block_x += GRID_SIZE // 2
        elif face == "left":
            block_x -= GRID_SIZE // 2
            block_y += GRID_SIZE // 2
        elif face == "right":
            block_x += GRID_SIZE + GRID_SIZE // 2
            block_y += GRID_SIZE // 2
        else:
            # Default to down if no facing direction
            block_y += GRID_SIZE
        
        # Align to grid
        block_x = (block_x // GRID_SIZE) * GRID_SIZE
        block_y = (block_y // GRID_SIZE) * GRID_SIZE
        return block_x, block_y
    
    def get_position(self):
        """Get current position"""
        return self.x, self.y
    
    def get_facing(self):
        """Get current facing direction"""
        return self.face
    
    def get_speed(self):
        """Get current speed"""
        return self.speed
