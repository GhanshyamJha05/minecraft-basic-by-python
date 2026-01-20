from ursina import color
import random

# World Settings
WORLD_SIZE = 30
SEED = random.randint(0, 10000)
SCALE = 0.05
HEIGHT_MAX = 8

# Block Configuration
BLOCK_TEXTURES = {
    '1': 'grass.png',
    '2': 'dirt.png',
    '3': 'stone.png',
    '4': 'brick.png',  # Using brick as 'Wood' for now
    '5': 'gold.png'
}

BLOCK_NAMES = {
    '1': 'Grass',
    '2': 'Dirt',
    '3': 'Stone',
    '4': 'Wood',
    '5': 'Gold'
}

# Defaults
DEFAULT_BLOCK = '1'
