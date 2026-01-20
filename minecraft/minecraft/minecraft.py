from ursina import *
from config import BLOCK_TEXTURES, BLOCK_NAMES, DEFAULT_BLOCK
from player import PlayerController
from terrain import generate_terrain
from environment import Sky, Cloud
import random

from state import game_state

# IMPORTANT: Inject game_state into module namespace for voxel.py to use
import sys
import builtins
# This is a bit of a hack to make game_state available to Voxel without circular imports in a simple script structure
# Ideally we would pass it, but Voxel is instantiated deep in logic.
# For now, we will hotfix Voxel's access in the input method or use a Better pattern.
# Actually, let's just make sure Voxel imports this module or we pass it.
# The Voxel class in voxel.py tries to import 'main_game'

app = Ursina()

# HUD Elements
crosshair = Entity(model='quad', color=color.white, scale=0.02, parent=camera.ui)
block_indicator = Text(text=f'Current Block: {BLOCK_NAMES[DEFAULT_BLOCK]}', position=(-0.85, 0.45), scale=1.5, color=color.white)
coord_text = Text(text='', position=(0.65, 0.48), scale=1, color=color.white)

# Initialize
generate_terrain()
player = PlayerController()
sky = Sky()

# Clouds
clouds = [Cloud(pos=(random.randint(-50, 50), 20, random.randint(-50, 50)), scale=(random.randint(5,15), 1, random.randint(5,15))) for _ in range(10)]

# Lighting
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,1))
day_time = 0

def update():
    global day_time
    # Day/Night Cycle
    day_time += time.dt * 0.02
    sky.rotation_x = day_time * 50
    sun.rotation_x = day_time * 50
    
    # Coordinates
    coord_text.text = f'({round(player.x, 1)}, {round(player.y, 1)}, {round(player.z, 1)})'

def input(key):
    if key in BLOCK_TEXTURES:
        game_state.selected_block = key
        block_indicator.text = f'Current Block: {BLOCK_NAMES[key]}'
    
    if key == 'f':
        player.toggle_flashlight()

    if key == 'escape':
        quit()

if __name__ == '__main__':
    app.run()
