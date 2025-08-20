# Modular Python Game

This is a refactored version of the original `base_game.py` that has been broken down into logical, maintainable components.

## File Structure

- **`game.py`** - Main game file that orchestrates everything
- **`network_manager.py`** - Handles all networking (client/server, player synchronization)
- **`asset_manager.py`** - Manages loading and access to all game assets (sprites, backgrounds, etc.)
- **`player.py`** - Handles player state, movement, and input
- **`renderer.py`** - Manages all rendering and drawing operations
- **`config.py`** - Centralized configuration and constants
- **`base_game.py`** - Original monolithic file (kept for reference)

## Benefits of This Structure

1. **Separation of Concerns** - Each file has a single responsibility
2. **Maintainability** - Easier to find and fix bugs
3. **Reusability** - Components can be reused in other projects
4. **Testability** - Each component can be tested independently
5. **Readability** - Code is easier to understand and navigate

## How to Run

Simply run the main game file:
```bash
python game.py
```

## Key Components

### NetworkManager
- Handles client/server setup
- Manages player connections
- Synchronizes player positions

### AssetManager
- Loads all game assets on startup
- Provides easy access to sprites, backgrounds, and trees
- Centralizes asset loading logic

### Player
- Manages player state (position, speed, facing direction)
- Handles input processing
- Manages movement and collision detection

### Renderer
- Handles all drawing operations
- Separates rendering logic from game logic
- Makes it easy to modify visual appearance

### Game
- Main orchestrator class
- Manages the game loop
- Coordinates between all components

## Configuration

Edit `config.py` to modify:
- Screen dimensions
- Player starting positions
- World boundaries
- Asset paths
- Colors and other constants

## Adding New Features

To add new features:
1. **New sprites/assets** - Add to `AssetManager`
2. **New player abilities** - Extend the `Player` class
3. **New rendering effects** - Add methods to `Renderer`
4. **New networking features** - Extend `NetworkManager`
5. **New game mechanics** - Add to the main `Game` class

This modular structure makes it much easier to maintain and extend the game!
