from ursina import *
from opensimplex import OpenSimplex
from config import WORLD_SIZE, SCALE, HEIGHT_MAX, SEED, BLOCK_TEXTURES

class MeshTerrain(Entity):
    def __init__(self):
        super().__init__()
        self.simplex = OpenSimplex(seed=SEED)
        self.voxels = {}  # Logical storage: (x,y,z) -> block_type
        
        # Block colors (fallback if texture fails)
        self.block_colors = {
            '1': color.rgb(0, 150, 0),     # Grass
            '2': color.rgb(100, 50, 0),    # Dirt
            '3': color.rgb(100, 100, 100), # Stone
            '4': color.rgb(150, 75, 0),    # Wood
            '5': color.rgb(255, 200, 0)    # Gold
        }

        # Create one entity per block type with its texture
        self.subsets = {}
        for b_type, texture_file in BLOCK_TEXTURES.items():
            self.subsets[b_type] = Entity(
                model=Mesh(), 
                texture=texture_file,
                parent=self,
                collider='mesh'
            )
        
        self.generate_terrain()
        
    def generate_terrain(self):
        """Generate initial terrain using OpenSimplex noise"""
        print("Generating Mesh Terrain...")
        
        for x in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                # Use multi-layered noise for more interesting terrain
                noise_val = self.simplex.noise2(x * SCALE, z * SCALE)
                height = int((noise_val + 1) * HEIGHT_MAX / 2) + 2
                
                for y in range(height):
                    if y == height - 1:
                        block_type = '1'  # Grass
                    elif y > height - 3:
                        block_type = '2'  # Dirt
                    else:
                        block_type = '3'  # Stone
                    self.voxels[(x, y, z)] = block_type
        
        self.update_mesh()
    
    def update_mesh(self):
        """Rebuild mesh with optimization for visible faces only"""
        mesh_data = {b_type: {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []} 
                    for b_type in BLOCK_TEXTURES}

        # Directions for face culling
        directions = {
            'top': (0, 1, 0),
            'bottom': (0, -1, 0),
            'front': (0, 0, -1),
            'back': (0, 0, 1),
            'left': (-1, 0, 0),
            'right': (1, 0, 0)
        }

        for pos, block_type in self.voxels.items():
            x, y, z = pos
            
            # Only add faces that are exposed to air
            for face, (dx, dy, dz) in directions.items():
                neighbor_pos = (x + dx, y + dy, z + dz)
                if neighbor_pos not in self.voxels:
                    # Special case: don't render bottom faces of the world's floor
                    if face == 'bottom' and y == 0:
                        continue
                    self.add_face(mesh_data[block_type], (x, y, z), face, block_type)

        # Apply meshes to subsets
        for b_type, data in mesh_data.items():
            subset = self.subsets[b_type]
            if not data['vertices']:
                subset.model = None
                continue
            
            mesh = subset.model
            mesh.vertices = data['vertices']
            mesh.uvs = data['uvs']
            mesh.colors = data['colors']
            mesh.triangles = data['triangles']
            mesh.generate()
            
            # Re-enable collider for the new mesh
            subset.collider = 'mesh'

    def add_face(self, mesh_data, pos, face, block_type):
        """Add a cube face to the mesh with correct UVs"""
        x, y, z = pos
        v_offset = len(mesh_data['vertices'])
        c = self.block_colors[block_type]
        
        # Local vertex positions
        v = [
            (0,0,0), (1,0,0), (1,1,0), (0,1,0), # 0,1,2,3 (Front)
            (0,0,1), (1,0,1), (1,1,1), (0,1,1)  # 4,5,6,7 (Back)
        ]

        # Map face to vertices
        f_map = {
            'front':  [v[0], v[1], v[2], v[3]],
            'back':   [v[5], v[4], v[7], v[6]],
            'left':   [v[4], v[0], v[3], v[7]],
            'right':  [v[1], v[5], v[6], v[2]],
            'top':    [v[3], v[2], v[6], v[7]],
            'bottom': [v[4], v[5], v[1], v[0]]
        }

        verts = f_map[face]
        for v_pos in verts:
            mesh_data['vertices'].append((x + v_pos[0], y + v_pos[1], z + v_pos[2]))
            mesh_data['colors'].append(c)

        # Standard UVs for a face
        mesh_data['uvs'].extend([(0,0), (1,0), (1,1), (0,1)])
        
        # Two triangles per face
        mesh_data['triangles'].extend([
            v_offset, v_offset + 1, v_offset + 2,
            v_offset, v_offset + 2, v_offset + 3
        ])
