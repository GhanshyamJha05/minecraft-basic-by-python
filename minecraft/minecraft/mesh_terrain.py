from ursina import *
from opensimplex import OpenSimplex
from config import WORLD_SIZE, SCALE, HEIGHT_MAX, SEED, BLOCK_TEXTURES

class MeshTerrain(Entity):
    def __init__(self):
        super().__init__()
        self.model = Mesh()
        self.texture = 'texture_atlas.png'  # We need a texture atlas for this to work well, or we map UVs manually
        # Ideally, we create a texture atlas. For now, we will try to stick to single texture or coloring.
        # Actually, for a quick win without complex UV mapping, we can use vertex colors or separate meshes for separate textures.
        # Separate meshes is easier: one mesh for Grass, one for Stone, etc.
        
        self.subsets = {name: Entity(model=Mesh(), texture=tex, double_sided=True) for name, tex in BLOCK_TEXTURES.items()}
        
        self.simplex = OpenSimplex(seed=SEED)
        self.voxels = {} # Logical storage for collisions
        self.generate_terrain()
        
    def generate_terrain(self):
        print("Generating Mesh Terrain...")
        
        # Temporary storage for vertices and triangles for each block type
        mesh_data = {
            '1': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []}, # Grass
            '2': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []}, # Dirt
            '3': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []}, # Stone
            '4': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []}, # Wood
            '5': {'vertices': [], 'uvs': [], 'triangles': [], 'colors': []}, # Gold
        }

        # Vertices for a 1x1x1 cube centered at 0,0,0 (relative)
        # However, we will push absolute positions directly.
        
        # Directions: Up, Down, Right, Left, Forward, Back
        # We only draw faces that are exposed.
        
        for x in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                noise_val = self.simplex.noise2(x * SCALE, z * SCALE)
                height = int((noise_val + 1) * HEIGHT_MAX / 2) + 2
                
                for y in range(height):
                    # Determine Block Type
                    block_type = '3' # Stone
                    if y == height - 1: block_type = '1' # Grass
                    elif y > height - 3: block_type = '2' # Dirt
                    
                    self.voxels[(x,y,z)] = block_type
                    
                    # Back-face culling logic (simple)
                    # Only add faces if they are visible (air next to them)
                    # Since we are generating the world, we can't easily check neighbors yet unless we generate data first.
                    # Two pass approach: 
                    # 1. Fill `self.voxels`
                    # 2. Iterate `self.voxels` and build meshes.

        # Re-iterate to build mesh with occlusion culling
        import random
        for pos, block_type in self.voxels.items():
            x, y, z = pos
            
            # 6 Faces checks
            # Up
            if (x, y+1, z) not in self.voxels:
                self.add_face(mesh_data[block_type], (x,y,z), 'top')
            # Down
            if (x, y-1, z) not in self.voxels and y > 0:
                 self.add_face(mesh_data[block_type], (x,y,z), 'bottom')
            # Right
            if (x+1, y, z) not in self.voxels:
                 self.add_face(mesh_data[block_type], (x,y,z), 'right')
            # Left
            if (x-1, y, z) not in self.voxels:
                 self.add_face(mesh_data[block_type], (x,y,z), 'left')
            # Forward
            if (x, y, z+1) not in self.voxels:
                 self.add_face(mesh_data[block_type], (x,y,z), 'forward')
            # Back
            if (x, y, z-1) not in self.voxels:
                 self.add_face(mesh_data[block_type], (x,y,z), 'back')

        # Apply to meshes
        for b_type, data in mesh_data.items():
            if not data['vertices']: continue
            print(f"Generating mesh for {b_type}: {len(data['vertices'])} vertices")
            mesh = self.subsets[b_type].model
            mesh.vertices = data['vertices']
            mesh.uvs = data['uvs']
            mesh.colors = data['colors']
            mesh.generate() # Generate normals etc
            self.subsets[b_type].collider = 'mesh' # Mesh collider is accurate but can be slow. Box collider is better if approximated.
            # OPTIMIZATION: Do not add collider to the visual mesh. 
            # We should handle collisions separately or use a simplified mesh for collision.
            # For now, let's try 'mesh' collider. If slow, we switch to math-based collision.
            self.subsets[b_type].collider = 'mesh'

    def add_face(self, data, pos, face):
        x, y, z = pos
        # Define vertices for each face relative to x,y,z
        # Standard unit cube vertices
        
        # UVS: (0,0), (1,0), (1,1), (0,1) for standard mapping
        uvs = [(0,0), (1,0), (1,1), (0,1)]
        
        if face == 'top':
            verts = [(x, y+1, z), (x+1, y+1, z), (x+1, y+1, z+1), (x, y+1, z+1)] # Top Face
        elif face == 'bottom':
            verts = [(x, y, z+1), (x+1, y, z+1), (x+1, y, z), (x, y, z)] # Bottom Face
        elif face == 'right':
            verts = [(x+1, y, z+1), (x+1, y+1, z+1), (x+1, y+1, z), (x+1, y, z)]
        elif face == 'left':
            verts = [(x, y, z), (x, y+1, z), (x, y+1, z+1), (x, y, z+1)]
        elif face == 'forward':
            verts = [(x+1, y, z+1), (x, y, z+1), (x, y+1, z+1), (x+1, y+1, z+1)] # z+1
        elif face == 'back':
            verts = [(x, y, z), (x+1, y, z), (x+1, y+1, z), (x, y+1, z)] # z
           
        # Fix winding order if faces are invisible or inside out.
        # Ursina/Panda3D winding is CCW usually.
        # Let's use a standard lookup for simplicity if debugging is needed.
        
        # Easier manual definition to ensure correct normal direction:
        # Top: y+1
        v = []
        if face == 'top':    v = [Vec3(0,1,0)+pos, Vec3(1,1,0)+pos, Vec3(1,1,1)+pos, Vec3(0,1,1)+pos]
        if face == 'bottom': v = [Vec3(0,0,1)+pos, Vec3(1,0,1)+pos, Vec3(1,0,0)+pos, Vec3(0,0,0)+pos]
        if face == 'right':  v = [Vec3(1,0,0)+pos, Vec3(1,1,0)+pos, Vec3(1,1,1)+pos, Vec3(1,0,1)+pos] # Error here likely in winding
        if face == 'left':   v = [Vec3(0,0,1)+pos, Vec3(0,1,1)+pos, Vec3(0,1,0)+pos, Vec3(0,0,0)+pos]
        if face == 'forward':v = [Vec3(1,0,1)+pos, Vec3(1,1,1)+pos, Vec3(0,1,1)+pos, Vec3(0,0,1)+pos]
        if face == 'back':   v = [Vec3(0,0,0)+pos, Vec3(0,1,0)+pos, Vec3(1,1,0)+pos, Vec3(1,0,0)+pos]
            
        # Quad format: 0,1,2, 2,3,0 (Two triangles)
        # Vertices in list are just points. We need to add them 
        
        # However, Ursina Mesh(vertices=[...], triangles=[...])
        # If we provide list of Vec3s divisible by 3 (triangles) or 4 (quads is deprecated?), simple list of vertices is auto-triangulated if mode='triangle'
        
        # We will add 6 vertices for 2 triangles per face to be explicit and safe.
        # 0, 1, 2, 2, 3, 0
        
        data['vertices'].extend([v[0], v[1], v[2], v[2], v[3], v[0]])
        data['uvs'].extend([(0,0), (1,0), (1,1), (1,1), (0,1), (0,0)])
        
        # Fake lighting
        c = color.white
        if face == 'top': c = color.color(0,0,1) # White
        elif face == 'bottom': c = color.color(0,0,0.5) # Dark
        else: c = color.color(0,0,0.8) # Sides
        
        data['colors'].extend([c] * 6)

    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity in self.subsets.values():
                # Placing block on mesh is harder because we don't have individual voxel objects.
                # We need to calculate position relative to the hit normal.
                hit_info = mouse.raycast(camera.world_position, camera.forward, distance=10)
                if hit_info.hit:
                    pos = hit_info.entity.world_position + hit_info.point + hit_info.normal * 0.5
                    pos = (int(pos.x), int(pos.y), int(pos.z))
                    # Add to logical voxels and Re-build specific mesh? 
                    # For a truly scalable system, we'd update the chunk mesh locally. 
                    # For now, let's just spawn a Voxel object for newly placed blocks (hybrid approach)
                    # or Re-generate entire terrain (SLOW).
                    
                    # fast hybrid:
                    from voxel import Voxel # dynamic import
                    Voxel(position=pos, texture='grass.png')
                    self.voxels[pos] = '1'

        if key == 'right mouse down':
             if mouse.hovered_entity in self.subsets.values():
                hit_info = mouse.raycast(camera.world_position, camera.forward, distance=10)
                if hit_info.hit:
                    # Remove block
                    # Getting exact block from mesh is Tricky without storage
                    point = hit_info.point - hit_info.normal * 0.5
                    pos = (int(point.x), int(point.y), int(point.z))
                    
                    if pos in self.voxels:
                        del self.voxels[pos]
                        # We need to rebuild mesh to make a hole.
                        # For prototype: Rebuild ALL. (Will lag on click, but FPS is high otherwise)
                        self.generate_terrain()
