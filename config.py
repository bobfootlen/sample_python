# Game Configuration

# Screen settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

# Network settings
DEFAULT_PORT = 5000

# Player settings
PLAYER_START_X = 200
PLAYER_START_Y = 200
PLAYER_START_SPEED = 5
PLAYER_DEFAULT_SPEEDS = {
    'slow': 1,
    'normal': 5,
    'fast': 20
}

# World boundaries
WORLD_MAX_X = 200
WORLD_MIN_X = -9700
WORLD_MAX_Y = 200
WORLD_MIN_Y = -9700

# Camera settings
CAMERA_START_X = 40
CAMERA_START_Y = 0

# Asset paths
ASSET_PATHS = {
    'sprites': {
        'up': 'img/up.png',
        'down': 'img/down.png',
        'left': 'img/left.png',
        'right': 'img/right.png',
        'remote_up': 'img/remote_up.png',
        'remote_down': 'img/remote_down.png',
        'remote_left': 'img/rmote_left.png',
        'remote_right': 'img/remote_right.png'
    },
    'trees': {
        'tree_1': 'img/tree-1.png',
        'tree_2': 'img/tree-2.png'
    },
    'backgrounds': {
        'main': 'img/backround1.png'
    }
}

# Colors
BACKGROUND_COLOR = (50, 50, 50)
