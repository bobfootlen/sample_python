import pygame

class Player:
    def __init__(self, x=200, y=200, speed=5, player_id="host"):
        self.x = x
        self.y = y
        self.speed = speed
        self.face = "none"
        self.player_id = player_id

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
            self.x += self.speed
            self.face = "left"
        if keys[pygame.K_d]:
            self.x -= self.speed
            self.face = "right"
        if keys[pygame.K_w]:
            self.y += self.speed
            self.face = "up"
        if keys[pygame.K_s]:
            self.y -= self.speed
            self.face = "down"
        
        return self.face, self.x, self.y
    
    def handle_walls(self):
        """Handle wall boundaries"""
        if self.x > 200:
            self.x = 200
        if self.x < -9700:
            self.x = -9700
        if self.y > 200:
            self.y = 200
        if self.y < -9700:
            self.y = -9700
        return self.x, self.y
    
    def get_position(self):
        """Get current position"""
        return self.x, self.y
    
    def get_facing(self):
        """Get current facing direction"""
        return self.face
    
    def get_speed(self):
        """Get current speed"""
        return self.speed
