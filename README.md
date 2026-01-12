# Minecraft Basic by Python

A simple Minecraft-like voxel game built with Python and the Ursina game engine. Features procedural terrain generation, block placement, and removal in a 3D world.

## Features

- **Procedural Terrain Generation**: Uses OpenSimplex noise to create natural-looking landscapes with hills and valleys.
- **Block Interaction**: Left-click to place blocks, right-click to remove them.
- **First-Person Controls**: Move around with WASD, look with mouse.
- **Configurable World**: Adjustable world size, seed, and terrain parameters.
- **Collision Detection**: Prevents placing blocks where they already exist.

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

   Or manually:
   ```bash
   pip install ursina opensimplex
   ```

## How to Run

Navigate to the game directory and run:
```bash
cd minecraft/minecraft
python minecraft.py
```

A game window will open with the 3D world.

## Controls

- **Movement**: WASD keys
- **Look Around**: Mouse movement
- **Place Block**: Left mouse click (on a block face)
- **Remove Block**: Right mouse click (on a block)
- **Exit**: Close the window or press Alt+F4

## Configuration

You can modify the constants in `minecraft.py` to customize the game:

- `WORLD_SIZE`: Size of the world (default: 50)
- `SEED`: Random seed for terrain generation (default: 42)
- `SCALE`: Noise scale for terrain variation (default: 0.1)
- `HEIGHT_MAX`: Maximum terrain height (default: 10)

## Dependencies

- **Ursina**: Game engine for Python
- **OpenSimplex**: Pure Python noise library for terrain generation

## Project Structure

```
minecraft-basic-by-python/
├── minecraft/
│   └── minecraft/
│       ├── minecraft.py    # Main game file
│       └── grass.png       # Block texture
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── PR_DESCRIPTION.md      # Pull request description
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. Feel free to use and modify it.



## Future Improvements

- Multiple block types (stone, wood, etc.)
- Inventory system
- Day/night cycle
- Save/load world functionality
- Multiplayer support
