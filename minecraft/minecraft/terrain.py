import random
from ursina import color
from opensimplex import OpenSimplex
from config import WORLD_SIZE, SCALE, HEIGHT_MAX, SEED
from voxel import Voxel, voxels

simplex = OpenSimplex(seed=SEED)

def create_tree(pos):
    x, y, z = pos
    # Trunk (Brick used as Wood)
    for i in range(1, 5):
        Voxel(position=(x, y + i, z), texture='brick.png', block_color=color.brown)
    # Leaves (Grass used as Leaves)
    for i in range(-2, 3):
        for j in range(-2, 3):
            for k in range(4, 7):
                if abs(i) + abs(j) <= 2:
                    pos_leaf = (x + i, y + k, z + j)
                    if pos_leaf not in voxels:
                        Voxel(position=pos_leaf, texture='grass.png', block_color=color.green)

def generate_terrain():
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
                    
                Voxel(position=(x, y, z), texture=tex, block_color=col)

            # Randomly place trees on grass
            if height > 2 and random.random() < 0.02:
                create_tree((x, height - 1, z))
