from ursina import *
from config import BLOCK_TEXTURES

# Global voxel dictionary to allow other modules to check existence
# Key: position tuple (x,y,z), Value: Voxel instance
voxels = {}

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass.png', block_color=color.white):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=block_color,
            highlight_color=color.lime,
        )
        voxels[position] = self

    def input(self, key):
        from state import game_state

        if self.hovered:
            if key == 'left mouse down':
                new_pos = self.position + mouse.normal
                if new_pos not in voxels:
                    current_block_id = game_state.selected_block
                    tex = BLOCK_TEXTURES[current_block_id]
                    col = color.white
                    if current_block_id == '4': # Wood logic
                        col = color.brown
                    
                    Voxel(position=new_pos, texture=tex, block_color=col)
            
            if key == 'right mouse down':
                if self.position in voxels:
                    del voxels[self.position]
                destroy(self)
