from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import OpenSimplex
import random

app = Ursina()

# Constants
WORLD_SIZE = 30 # Reduced for better initial load performance
SEED = random.randint(0, 10000)
SCALE = 0.05
HEIGHT_MAX = 8

# Block textures
BLOCK_TEXTURES = {
    '1': 'grass.png',
    '2': 'dirt.png',
    '3': 'stone.png',
    '4': 'brick.png',
    '5': 'gold.png'
}

selected_block = '1'

# Initialize noise
simplex = OpenSimplex(seed=SEED)

# Dictionary to store voxels for O(1) lookup
voxels = {}

# HUD Elements
crosshair = Entity(model='quad', color=color.white, scale=0.02, parent=camera.ui)
block_indicator = Text(text='Current Block: Grass', position=(-0.85, 0.45), scale=1.5, color=color.white)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.light_gray,
        )
        voxels[position] = self

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                new_pos = self.position + mouse.normal
                if new_pos not in voxels:
                    Voxel(position=new_pos, texture=BLOCK_TEXTURES[selected_block])
            
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
            scale=500,
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
            elif y > height - 3:
                tex = 'dirt.png'
            else:
                tex = 'stone.png'
            
            # Randomly place gold
            if tex == 'stone.png' and random.random() < 0.05:
                tex = 'gold.png'
                
            Voxel(position=(x, y, z), texture=tex)

# Player and Environment
player = FirstPersonController()
player.gravity = 0.5
player.cursor.visible = False
sky = Sky()
hand = Hand()

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

def input(key):
    global selected_block
    if key in BLOCK_TEXTURES:
        selected_block = key
        block_name = {
            '1': 'Grass',
            '2': 'Dirt',
            '3': 'Stone',
            '4': 'Brick',
            '5': 'Gold'
        }[key]
        block_indicator.text = f'Current Block: {block_name}'
    
    if key == 'escape':
        quit()

app.run()