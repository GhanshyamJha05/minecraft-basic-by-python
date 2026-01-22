from ursina import *
from opensimplex import OpenSimplex
from config import WORLD_SIZE, SCALE, HEIGHT_MAX, SEED, BLOCK_TEXTURES

class MeshTerrain(Entity):
    def __init__(self):
        super().__init__()
        self.model = Mesh()
        self.texture = 'texture_atlas.png'
        
        # Block colors with vertex-based coloring
        self.block_colors = {
            '1': color.rgb(0, 150, 0),     # Grass (Green)
            '2': color.rgb(100, 50, 0),    # Dirt (Brown)
            '3': color.rgb(100, 100, 100), # Stone (Grey)
            '4': color.rgb(150, 75, 0),    # Wood
            '5': color.rgb(255, 200, 0)    # Gold
        }

        # Create one entity per block type
        self.subsets = {
            name: Entity(model=Mesh(), color=color.white, double_sided=True) 
            for name in BLOCK_TEXTURES
        }
        
        self.simplex = OpenSimplex(seed=SEED)
        self.voxels = {}  # Logical storage for collisions
        self.generate_terrain()
        
    def generate_terrain(self):
        """Generate initial terrain using OpenSimplex noise"""
        print("Generating Mesh Terrain...")
        
        for x in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                noise_val = self.simplex.noise2(x * SCALE, z * SCALE)
                height = int((noise_val + 1) * HEIGHT_MAX / 2) + 2
                
                for y in range(height):
                    # Determine block type by height
                    if y == height - 1:
                        block_type = '1'  # Grass
                    elif y > height - 3:
                        block_type = '2'  # Dirt
                    else:
                        block_type = '3'  # Stone
                    
                    self.voxels[(x, y, z)] = block_type
        
        self.update_mesh()
    
    def update_mesh(self):
        """Rebuild mesh after terrain changes"""
        # Clear existing mesh data
        mesh_data = {
            '1': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []},
            '2': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []},
            '3': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []},
            '4': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []},
            '5': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []},
        }

        # Build mesh with face culling
        for pos, block_type in self.voxels.items():
            x, y, z = pos
            
            # Check all 6 faces
            if (x, y + 1, z) not in self.voxels:
                self.add_face(mesh_data[block_type], (x, y, z), 'top', block_type)
            if (x, y - 1, z) not in self.voxels and y > 0:
                self.add_face(mesh_data[block_type], (x, y, z), 'bottom', block_type)
            if (x + 1, y, z) not in self.voxels:
                self.add_face(mesh_data[block_type], (x, y, z), 'right', block_type)
            if (x - 1, y, z) not in self.voxels:
                self.add_face(mesh_data[block_type], (x, y, z), 'left', block_type)
            if (x, y, z + 1) not in self.voxels:
                self.add_face(mesh_data[block_type], (x, y, z), 'forward', block_type)
            if (x, y, z - 1) not in self.voxels:
                self.add_face(mesh_data[block_type], (x, y, z), 'back', block_type)

        # Apply meshes
        for b_type, data in mesh_data.items():
            if not data['vertices']:
                continue
            
            mesh = self.subsets[b_type].model
            mesh.vertices = data['vertices']
            mesh.uvs = data['uvs']
            mesh.colors = data['colors']
            mesh.triangles = data['triangles']
            mesh.generate()

    def add_face(self, mesh_data, pos, face, block_type):
        """Add a cube face to the mesh"""
        x, y, z = pos
        vertex_offset = len(mesh_data['vertices'])
        color_val = self.block_colors[block_type]
        
        # Define cube vertices (8 corners)
        cube_verts = [
            (x, y, z), (x+1, y, z), (x+1, y+1, z), (x, y+1, z),  # Front
            (x, y, z+1), (x+1, y, z+1), (x+1, y+1, z+1), (x, y+1, z+1)  # Back
        ]
        
        # Define face indices
        faces_map = {
            'top': [(4, 7, 6), (6, 5, 4)],
            'bottom': [(0, 1, 2), (2, 3, 0)],
            'front': [(0, 4, 5), (5, 1, 0)],
            'back': [(2, 6, 7), (7, 3, 2)],
            'left': [(0, 3, 7), (7, 4, 0)],
            'right': [(1, 5, 6), (6, 2, 1)]
        }
        
        if face in faces_map:
            for tri_indices in faces_map[face]:
                for idx in tri_indices:
                    mesh_data['vertices'].append(cube_verts[idx])
                    mesh_data['colors'].append(color_val)
                    mesh_data['uvs'].append((0, 0))
                
                # Triangle indices
                mesh_data['triangles'].append(vertex_offset + len(mesh_data['triangles']) // 3 * 3)
                mesh_data['triangles'].append(vertex_offset + len(mesh_data['triangles']) // 3 * 3 + 1)
                mesh_data['triangles'].append(vertex_offset + len(mesh_data['triangles']) // 3 * 3 + 2)