# Minecraft Basic by Python (Enhanced)

A simple but powerful Minecraft-like voxel game built with Python and the Ursina game engine. This project features procedural terrain generation, multiple block types, and an optimized game engine logic.

## 🚀 New Features (Commendable Updates)

- **Optimized Performance**: Replaced O(N) block detection with O(1) dictionary-based lookup for smooth building and destroying.
- **Multiple Block Types**: Choose between Grass, Dirt, Stone, Brick, and Gold blocks.
- **Improved Procedural Terrain**: Complex height-based layering (Stone -> Dirt -> Grass) with rare mineral deposits (Gold).
- **Interactive HUD**: Added a crosshair and a real-time current block indicator.
- **Player Visuals**: Added a 3D hand that responds to building actions.
- **Dynamic Physics**: Improved gravity and player movement.

## Features

- **Procedural Terrain Generation**: Uses OpenSimplex noise to create natural-looking landscapes with hills and valleys.
- **Block Interaction**: Left-click to place blocks, right-click to remove them.
- **First-Person Controls**: Move around with WASD, look with mouse.
- **Configurable World**: Adjustable world size, seed, and terrain parameters.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GhanshyamJha05/minecraft-basic-by-python.git
   cd minecraft-basic-by-python
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Navigate to the game directory and run:
```bash
cd minecraft/minecraft
python minecraft.py
```

## Controls

- **Movement**: WASD keys
- **Look Around**: Mouse movement
- **Place Block**: Left mouse click
- **Remove Block**: Right mouse click
- **Select Block (1-5)**: 
    - `1`: Grass
    - `2`: Dirt
    - `3`: Stone
    - `4`: Brick
    - `5`: Gold
- **Exit**: Press `Esc` or close the window

## Configuration

You can modify the constants in `minecraft.py` to customize the game:

- `WORLD_SIZE`: Size of the world (default: 30)
- `SEED`: Random seed for terrain generation
- `SCALE`: Noise scale for terrain variation
- `HEIGHT_MAX`: Maximum terrain height

## Dependencies

- **Ursina**: Game engine for Python
- **OpenSimplex**: Pure Python noise library for terrain generation

## Project Structure

```
minecraft-basic-by-python/
├── minecraft/
│   └── minecraft/
│       ├── minecraft.py    # Main game file (Updated)
│       ├── grass.png       # Grass texture
│       ├── dirt.png        # Dirt texture (New)
│       ├── stone.png       # Stone texture (New)
│       ├── brick.png       # Brick texture (New)
│       └── gold.png        # Gold texture (New)
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Future Improvements

- Save/load world functionality
- Enemy AI and basic combat
- Inventory menu (press 'E')
- Multiplayer support (UDP/TCP)
- Biomes (Desert, Forest, Snowy)
