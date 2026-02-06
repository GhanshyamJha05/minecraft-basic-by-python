# Minecraft Basic by Python (Enhanced & Optimized)

A high-performance Minecraft-like voxel game built with Python and the Ursina game engine. This project features procedural terrain generation with OpenSimplex noise, a survival-style HUD, and an optimized mesh-based rendering system.

## 🚀 Recent Performance & Gameplay Updates

- **Optimized Mesh Rendering**: Implemented **Face Culling**—only rendering block faces exposed to air. This drastically reduces the polygon count and maximizes FPS.
- **Survival HUD**: Added a modern UI featuring real-time **Health** and **Stamina** bars.
- **Advanced Movement**: 
  - **Sprinting**: Pressing `Shift` increases speed but drains the Stamina bar.
  - **Recovery**: Stamina regenerates automatically when not sprinting.
  - **Smooth Transitions**: Implemented Linear Interpolation (Lerp) for natural speed changes.
- **Visual Polish**: 
  - **Procedural Clouds**: Dynamic clouds randomly generated in the sky.
  - **Atmospheric Fog**: Enhanced distance fog for depth and immersion.
- **Improved Interaction**: Refined block placement and destruction using hit normals for pixel-perfect accuracy.

## ✨ Features

- **Procedural Terrain**: OpenSimplex noise-driven landscape generation (hills, valleys, plains).
- **Survival Mechanics**: Health management and a dynamic stamina system for sprinting.
- **Optimized Subsets**: One mesh entity per block type for efficient rendering and texturing.
- **Interactive Environment**: Real-time world manipulation (Place/Destroy).
- **Visuals**: Day-time skybox, moving clouds, and vertex-colored terrain.
- **FPS Counter**: Built-in monitor to track performance.

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **W, A, S, D** | Move |
| **Left Shift** | Sprint (Drains Stamina) |
| **Space** | Jump |
| **Left Click** | Place Block |
| **Right Click** | Destroy Block |
| **F** | Toggle Flashlight |
| **ESC** | Quit Game |

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GhanshyamJha05/minecraft-basic-by-python.git
   cd minecraft-basic-by-python
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 How to Run

Navigate to the game directory and run the main entry point:
```bash
cd minecraft/minecraft
python minecraft.py
```

## 📂 Project Structure

```
minecraft-basic-by-python/
├── minecraft/
│   └── minecraft/
│       ├── minecraft.py      # Main Entry Point & HUD Logic
│       ├── mesh_terrain.py   # Face-Culling & Mesh Generation
│       ├── player.py         # Survival Logic, HUD & Movement
│       ├── environment.py    # Sky, Fog, Clouds
│       ├── config.py         # World Constants (Seed, Size, Heights)
│       └── assets/*.png      # Texture Assets
├── requirements.txt          # Python dependencies
└── README.md                # Documentation
```

## 🗺️ Roadmap

- [ ] Save/Load world functionality
- [ ] Basic Combat & Enemy AI
- [ ] Inventory Management (E)
- [ ] Diverse Biomes (Snowy, Desert)
- [ ] Multiplayer Support (Socket-based)
