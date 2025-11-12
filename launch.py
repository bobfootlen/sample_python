import pygame
import pygame_gui
import subprocess
import sys
import os


pygame.init()

# Set up the display
window_surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Game Mode Selection')

# Set up Pygame GUI manager
manager = pygame_gui.UIManager((800, 600))

# Create title label
title_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((300, 50), (200, 40)),
    text='Select Game Mode',
    manager=manager
)

# Create radio buttons for mode selection
server_radio = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 120), (200, 40)),
    text='Server Mode',
    manager=manager
)

client_radio = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 170), (200, 40)),
    text='Client Mode',
    manager=manager
)

# Create a text entry box for server address (only visible in client mode)
server_address_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 230), (400, 30)),
    manager=manager,
    placeholder_text='Enter server address (e.g., localhost:5000)'
)

# Create username input (visible in both server and client mode)
username_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 280), (400, 30)),
    manager=manager,
    placeholder_text='Enter username'
)

# Create start game button
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 350), (100, 50)),
    text='Start Game',
    manager=manager
)

# Mode selection state
selected_mode = None
server_address_input.hide()
username_input.show()  # Show username input by default for server mode

running = True
clock = pygame.time.Clock()

def start_game():
    """Start the game with selected mode and parameters"""
    username = username_input.get_text()
    if not username:
        username = "Player"  # Default name if not provided
    
    if selected_mode == 'server':
        # Start server mode
        from game import Game
        game = Game()
        game.setup_networking(mode='server', username=username)
        game.run_game()
    elif selected_mode == 'client':
        # Start client mode
        server_address = server_address_input.get_text()
        if server_address and username:
            from game import Game
            game = Game()
            game.setup_networking(mode='client', server_address=server_address, username=username)
            game.run_game()
        else:
            print("Please enter both server address and username for client mode")

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == server_radio:
                selected_mode = 'server'
                server_address_input.hide()
                username_input.show()  # Show username input for server mode
                server_radio.set_text('✓ Server Mode')
                client_radio.set_text('Client Mode')
                
            elif event.ui_element == client_radio:
                selected_mode = 'client'
                server_address_input.show()
                username_input.show()
                server_radio.set_text('Server Mode')
                client_radio.set_text('✓ Client Mode')
                
            elif event.ui_element == start_button:
                if selected_mode:
                    start_game()
                    running = False
                else:
                    print("Please select a game mode first")
                        
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(pygame.Color('#222222')) # Fill background
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()