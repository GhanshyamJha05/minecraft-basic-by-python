from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from noise import pnoise2

app = Ursina()
player = FirstPersonController()
Sky()

# Constants for terrain generation
WORLD_SIZE = 50
SEED = 42
SCALE = 0.1
HEIGHT_MAX = 10

boxes = []
for x in range(WORLD_SIZE):
    for z in range(WORLD_SIZE):
        # Generate height using Perlin noise
        noise_val = pnoise2(x * SCALE, z * SCALE, base=SEED)
        height = int((noise_val + 1) * HEIGHT_MAX / 2)
        for y in range(height):
            box = Button(color=color.white, model='cube', position=(x, y, z),
                         texture='grass.png', parent=scene, origin_y=0.5)
            boxes.append(box)

# Position player above the terrain
player.position = (WORLD_SIZE // 2, HEIGHT_MAX + 5, WORLD_SIZE // 2)

def input(key):
    to_remove = []
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                new_pos = box.position + mouse.normal
                # Check if a block already exists at this position
                if not any(b.position == new_pos for b in boxes):
                    new = Button(color=color.white, model='cube', position=new_pos,
                                texture='grass.png', parent=scene, origin_y=0.5)
                    boxes.append(new)
            if key == 'right mouse down':
                to_remove.append(box)
    for box in to_remove:
        boxes.remove(box)
        destroy(box)

app.run()