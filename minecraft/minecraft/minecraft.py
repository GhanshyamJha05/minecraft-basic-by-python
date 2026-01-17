from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import OpenSimplex
import random
import math

app = Ursina()

# Constants
WORLD_SIZE = 30 
SEED = random.randint(0, 10000)
SCALE = 0.05
HEIGHT_MAX = 8

# Block textures
# Note: Using existing textures, but adding Wood and Leaves mapping
BLOCK_TEXTURES = {
    '1': 'grass.png',
    '2': 'dirt.png',
    '3': 'stone.png',
    '4': 'brick.png', # Using brick as 'Wood' for now
    '5': 'gold.png'
}

BLOCK_NAMES = {
    '1': 'Grass',
    '2': 'Dirt',
    '3': 'Stone',
    '4': 'Wood',
    '5': 'Gold'
}

selected_block = '1'

# Initialize noise
simplex = OpenSimplex(seed=SEED)

# Dictionary to store voxels for O(1) lookup
voxels = {}

# HUD Elements
crosshair = Entity(model='quad', color=color.white, scale=0.02, parent=camera.ui)
block_indicator = Text(text='Current Block: Grass', position=(-0.85, 0.45), scale=1.5, color=color.white)
coord_text = Text(text='', position=(0.65, 0.48), scale=1, color=color.white)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass.png', color=color.white):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color,
            highlight_color=color.light_gray,
        )
        voxels[position] = self

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                new_pos = self.position + mouse.normal
                if new_pos not in voxels:
                    # Logic for placing different blocks
                    tex = BLOCK_TEXTURES[selected_block]
                    col = color.white
                    if selected_block == '4': # Wood logic
                        col = color.brown
                    Voxel(position=new_pos, texture=tex, color=col)
            
            if key == 'right mouse down':
                if self.position in voxels:
                    del voxels[self.position]
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture='sky_default',
            scale=1000,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            texture='brick.png',
            scale=(0.2, 0.3, 0.4),
            rotation=(30, -40, 0),
            position=(0.6, -0.6)
        )

    def active(self):
        self.position = (0.5, -0.5)

    def passive(self):
        self.position = (0.6, -0.6)

class Cloud(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.white,
            scale=(random.randint(5,15), 1, random.randint(5,15)),
            position=(random.randint(-50, 50), 20, random.randint(-50, 50))
        )

    def update(self):
        self.x += time.dt * 0.5
        if self.x > 60:
            self.x = -60

# Add some clouds
clouds = [Cloud() for _ in range(10)]

def create_tree(pos):
    x, y, z = pos
    # Trunk (Brick used as Wood)
    for i in range(1, 5):
        Voxel(position=(x, y + i, z), texture='brick.png', color=color.brown)
    # Leaves (Grass used as Leaves)
    for i in range(-2, 3):
        for j in range(-2, 3):
            for k in range(4, 7):
                if abs(i) + abs(j) <= 2:
                    pos_leaf = (x + i, y + k, z + j)
                    if pos_leaf not in voxels:
                        Voxel(position=pos_leaf, texture='grass.png', color=color.green)

# Generate terrain
print("Generating terrain...")
for x in range(WORLD_SIZE):
    for z in range(WORLD_SIZE):
        noise_val = simplex.noise2(x * SCALE, z * SCALE)
        height = int((noise_val + 1) * HEIGHT_MAX / 2) + 2
        
        for y in range(height):
            # Select texture based on height
            if y == height - 1:
                tex = 'grass.png'
                col = color.white
            elif y > height - 3:
                tex = 'dirt.png'
                col = color.white
            else:
                tex = 'stone.png'
                col = color.white
            
            # Randomly place gold in stone
            if tex == 'stone.png' and random.random() < 0.05:
                tex = 'gold.png'
                
            Voxel(position=(x, y, z), texture=tex, color=col)

        # Randomly place trees on grass
        if height > 2 and random.random() < 0.02:
            create_tree((x, height - 1, z))

# Player and Environment
player = FirstPersonController()
player.gravity = 0.5
player.cursor.visible = False
sky = Sky()
hand = Hand()

# Flashlight
flashlight = SpotLight(parent=player, position=(0,2,1), enabled=False)
flashlight.look_at(player.position + player.forward * 10)

# Lighting
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,1))

day_time = 0

def update():
    global day_time
    # Hand animation
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    
    # Sprinting
    if held_keys['shift']:
        player.speed = 10
    else:
        player.speed = 5
    
    # Simple Day/Night Cycle
    day_time += time.dt * 0.02
    sky.rotation_x = day_time * 50
    sun.rotation_x = day_time * 50
    
    # Hand bobbing
    if player.walking:
        hand.position = Vec3(0.6, -0.6 + (math.sin(time.time() * 10) * 0.02), 0)
    
    # Update coordinates
    coord_text.text = f'({round(player.x, 1)}, {round(player.y, 1)}, {round(player.z, 1)})'
    
def input(key):
    global selected_block
    if key in BLOCK_TEXTURES:
        selected_block = key
        block_indicator.text = f'Current Block: {BLOCK_NAMES[key]}'
    
    if key == 'f': # Toggle flashlight
        flashlight.enabled = not flashlight.enabled
        print(f"Flashlight: {'ON' if flashlight.enabled else 'OFF'}")

    if key == 'escape':
        quit()

app.run()
