# Pull Request: Add Procedural Terrain Generation

## Description
This PR implements procedural terrain generation using Perlin noise to create varied, natural-looking landscapes instead of the flat 20x20 grid. The world now features hills, valleys, and height variation, making gameplay more engaging and realistic.

## Changes
- **Terrain Generation**: Uses `noise.pnoise2` with configurable seed, scale, and max height.
- **World Expansion**: Increased world size to 50x50 blocks.
- **Bug Fixes**:
  - Fixed unsafe list modification during block removal.
  - Added collision check to prevent overlapping blocks.
- **Player Setup**: Positions player safely above terrain.
- **Dependencies**: Added `requirements.txt` for easy installation.

## Testing
- Code passes syntax checks.
- Generates deterministic worlds based on seed.
- Maintains existing block placement/removal mechanics.

## Screenshots/Demos
*(Add screenshots of the new terrain if possible)*

Closes #X *(link to the issue you created)*