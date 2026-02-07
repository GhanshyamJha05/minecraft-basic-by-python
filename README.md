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
- **Inventory Management**: 
  - **Interactive Hotbar**: Switch between items using keys `1-5` or the **Scroll Wheel**.
  - **Storage Inventory (E)**: A full-screen menu to manage block assignments and view all available materials.
  - **Dynamic Hand Updates**: The player's held block updates visually based on the current selection.

## ✨ Features

- **Procedural Terrain**: OpenSimplex noise-driven landscape generation (hills, valleys, plains).
- **Survival Mechanics**: Health management and a dynamic stamina system for sprinting.
- **Optimized Subsets**: One mesh entity per block type for efficient rendering and texturing.
- **Interactive Environment**: Real-time world manipulation (Place/Destroy).
- **Visuals**: Day-time skybox, moving clouds, and vertex-colored terrain.
- **Inventory System**: Hotbar-based selection and a detailed management UI.
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
| **E** | Open Inventory / Storage |
| **1 - 5** | Select Hotbar Slot |
| **Scroll Wheel**| Cycle Hotbar Slots |
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
│       ├── inventory.py      # Hotbar & Inventory UI/Logic
│       ├── environment.py    # Sky, Fog, Clouds
│       ├── config.py         # World Constants (Seed, Size, Heights)
│       └── *.png             # Texture Assets
├── requirements.txt          # Python dependencies
└── README.md                # Documentation
```

## 🗺️ Roadmap

- [ ] Save/Load world functionality
- [ ] Basic Combat & Enemy AI
- [x] Inventory Management (E)
- [ ] Diverse Biomes (Snowy, Desert)
- [ ] Multiplayer Support (Socket-based)
