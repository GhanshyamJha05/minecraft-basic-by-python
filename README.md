# Minecraft Basic by Python (Enhanced)

A simple but powerful Minecraft-like voxel game built with Python and the Ursina game engine. This project features procedural terrain generation, multiple block types, and an optimized game engine logic.

## 🚀 Major Updates (Performance & Visuals)

- **Mesh Terrain System**: Moved from individual entities to a single mesh-based rendering system, boosting FPS essentially to infinity for this scale.
- **Modular Architecture**: Refactored the monolithic code into a clean, maintainable structure (`minecraft.py`, `mesh_terrain.py`, `player.py`, etc.).
- **Visual Polish**: Added distance fog, seamless skybox, and vertex-based ambient occlusion (AO) for depth.
- **Robustness**: Fixed critical crashes and implemented a solid-color fallback for reliable rendering on all systems.

## Features

- **Procedural Terrain Generation**: Uses OpenSimplex noise to create natural-looking landscapes with hills and valleys.
- **Optimized Rendering**: Uses chunk-like mesh generation with face culling.
- **Interactive World**: Place and destroy blocks in real-time.
- **First-Person Controls**: Smooth movement, sprinting (Shift), and flashlight (F).
- **Environment**: Day/Night cycle with moving sun and clouds.
- **Block Types**: Grass, Dirt, Stone, Wood, and Gold.

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

Navigate to the game directory and run the main entry point:
```bash
cd minecraft/minecraft
python minecraft.py
```

## Project Structure

```
minecraft-basic-by-python/
├── minecraft/
│   └── minecraft/
│       ├── minecraft.py      # Main Entry Point
│       ├── mesh_terrain.py   # Optimized Mesh Generation Logic
│       ├── player.py         # Player Movement & Input
│       ├── environment.py    # Sky, Fog, Clouds
│       ├── voxel.py          # Individual Voxel Logic (Fallback/Hybrid)
│       ├── config.py         # Global Constants (Seed, World Size)
│       ├── state.py          # Shared Game State
│       └── assets/           # Textures (grass.png, etc.)
├── requirements.txt          # Python dependencies
├── .gitignore               # System file exclusions
└── README.md                # Documentation
```

## Future Improvements

- Save/load world functionality
- Enemy AI and basic combat
- Inventory menu (press 'E')
- Multiplayer support (UDP/TCP)
- Biomes (Desert, Forest, Snowy)
