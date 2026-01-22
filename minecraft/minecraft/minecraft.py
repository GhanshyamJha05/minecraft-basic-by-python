from ursina import *
from player import PlayerController
from mesh_terrain import MeshTerrain
from environment import Sky
from config import WORLD_SIZE, HEIGHT_MAX

# Initialize app and scene
app = Ursina()
Sky()

# Create optimized mesh-based terrain instead of individual entities
terrain = MeshTerrain()

# Create player with all features
player = PlayerController()
player.position = (WORLD_SIZE // 2, HEIGHT_MAX + 5, WORLD_SIZE // 2)

# Input handling for block placement/destruction
def input(key):
    """Handle player input for block interactions"""
    if key == 'f':
        player.toggle_flashlight()
    
    # Raycast to detect which block player is looking at
    hit_info = raycast(camera.world_position, camera.forward(), distance=10, ignore=[player])
    
    if hit_info.hit and key == 'left mouse down':
        # Place new block
        hit_pos = hit_info.entity.position
        normal = hit_info.normal
        new_pos = hit_pos + normal
        new_pos = (int(new_pos.x), int(new_pos.y), int(new_pos.z))
        
        # Check boundaries and if position is empty
        if (0 <= new_pos[0] < WORLD_SIZE and 
            0 <= new_pos[1] < HEIGHT_MAX * 2 and 
            0 <= new_pos[2] < WORLD_SIZE and 
            new_pos not in terrain.voxels):
            terrain.voxels[new_pos] = '1'  # Add grass block
            terrain.update_mesh()
    
    elif hit_info.hit and key == 'right mouse down':
        # Destroy block
        hit_pos = hit_info.entity.position
        hit_pos = (int(hit_pos.x), int(hit_pos.y), int(hit_pos.z))
        
        if hit_pos in terrain.voxels:
            del terrain.voxels[hit_pos]
            terrain.update_mesh()

# Run the app
app.run()