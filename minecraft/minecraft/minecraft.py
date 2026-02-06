from ursina import *
from player import PlayerController
from mesh_terrain import MeshTerrain
from environment import Sky, Cloud
from config import WORLD_SIZE, HEIGHT_MAX
import math # Added for math.floor

# Initialize app and scene
app = Ursina()
Sky()

# Add random clouds
for i in range(20):
    Cloud(
        pos=(random.randint(0, WORLD_SIZE), random.randint(HEIGHT_MAX + 10, HEIGHT_MAX + 20), random.randint(0, WORLD_SIZE)),
        scale=(random.randint(5, 15), 1, random.randint(5, 10))
    )

# Improved visuals
Scene.fog_density = 0.05
Scene.fog_color = color.rgb(200, 200, 255)

# Create optimized mesh-based terrain
terrain = MeshTerrain()

# Create player with HUD and attributes
player = PlayerController()
player.position = (WORLD_SIZE // 2, HEIGHT_MAX + 5, WORLD_SIZE // 2)

# FPS Counter for monitoring smoothness
fps = Text(text='FPS: ', position=(0.7, 0.45), scale=1)

def update():
    fps.text = f'FPS: {int(1/time.dt)}'

# Input handling for block placement/destruction
def input(key):
    """Handle player input for block interactions"""
    if key == 'f':
        player.toggle_flashlight()
    
    # Raycast to detect which block player is looking at
    hit_info = raycast(camera.world_position, camera.forward(), distance=10, ignore=[player])
    
    if hit_info.hit:
        if key == 'left mouse down':
            # Place new block - use hit_point + half normal to find the center of the next voxel
            new_pos = hit_info.world_point + hit_info.normal * 0.5
            new_pos = (math.floor(new_pos.x), math.floor(new_pos.y), math.floor(new_pos.z))
            
            # Check boundaries and if position is empty
            if (0 <= new_pos[0] < WORLD_SIZE and 
                0 <= new_pos[1] < HEIGHT_MAX * 2 and 
                0 <= new_pos[2] < WORLD_SIZE and 
                new_pos not in terrain.voxels):
                terrain.voxels[new_pos] = '1'  # Add grass block
                terrain.update_mesh()
        
        elif key == 'right mouse down':
            # Destroy block - use hit_point - half normal to find the center of the hit voxel
            hit_pos = hit_info.world_point - hit_info.normal * 0.5
            voxel_pos = (math.floor(hit_pos.x), math.floor(hit_pos.y), math.floor(hit_pos.z))
            
            if voxel_pos in terrain.voxels:
                del terrain.voxels[voxel_pos]
                terrain.update_mesh()

# Run the app
app.run()