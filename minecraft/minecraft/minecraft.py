from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import OpenSimplex

app = Ursina()
player = FirstPersonController()
Sky()

# Constants for terrain generation
WORLD_SIZE = 50
SEED = 42
SCALE = 0.1
HEIGHT_MAX = 10

# Initialize noise generator
simplex = OpenSimplex(seed=SEED)

boxes = []
for x in range(WORLD_SIZE):
    for z in range(WORLD_SIZE):
        # Generate height using OpenSimplex noise
        noise_val = simplex.noise2(x * SCALE, z * SCALE)
        height = int((noise_val + 1) * HEIGHT_MAX / 2)
        for y in range(height):
            box = Button(color=color.white, model='cube', position=(x, y, z),
                         texture='grass.png', parent=scene, origin_y=0.5)
            boxes.append(box)

# Position player above the terrain
player.position = (WORLD_SIZE // 2, HEIGHT_MAX + 5, WORLD_SIZE // 2)

block_pick = 1

def input(key):
    global block_pick
    if key == '1': block_pick = 1
    if key == '2': block_pick = 2
    if key == '3': block_pick = 3
    if key == '4': block_pick = 4
    to_remove = []
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                new_pos = box.position + mouse.normal
                # Check if a block already exists at this position
                if not any(b.position == new_pos for b in boxes):
                    if block_pick == 1: block_color = color.white
                    if block_pick == 2: block_color = color.gray
                    if block_pick == 3: block_color = color.red
                    if block_pick == 4: block_color = color.orange

                    new = Button(color=block_color, model='cube', position=new_pos,
                                texture='grass.png', parent=scene, origin_y=0.5)
                    boxes.append(new)
            if key == 'right mouse down':
                to_remove.append(box)
    for box in to_remove:
        boxes.remove(box)
        destroy(box)

app.run()