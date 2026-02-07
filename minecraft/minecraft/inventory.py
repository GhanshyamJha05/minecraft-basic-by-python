from ursina import *
from config import BLOCK_TEXTURES, BLOCK_NAMES

class Inventory(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.is_open = False
        
        # Hotbar settings
        self.hotbar_size = 5
        self.selected_slot = 0
        self.items = ['1', '2', '3', '4', '5']  # Initial items (block IDs)
        
        # UI Elements
        self.hotbar_ui = Entity(parent=self, position=(0, -0.45))
        self.slots_ui = []
        self.setup_hotbar()
        
        # Full Inventory Panel
        self.inventory_panel = Entity(
            parent=self, 
            model='quad', 
            scale=(0.6, 0.4), 
            color=color.black66, 
            enabled=False,
            position=(0, 0)
        )
        self.panel_title = Text(
            parent=self.inventory_panel, 
            text='Storage Inventory', 
            origin=(0, 0), 
            y=0.4, 
            scale=1.5
        )
        self.panel_subtitle = Text(
            parent=self.inventory_panel, 
            text='Select a hotbar slot (1-5), then click a block to assign it', 
            origin=(0, 0), 
            y=0.3, 
            scale=0.8,
            color=color.light_gray
        )
        
        # Instructions
        self.instructions = Text(
            parent=self,
            text='Press [E] to Toggle Inventory | [1-5] to Select Block',
            position=(-0.85, -0.45),
            scale=0.8,
            color=color.light_gray
        )

    def setup_hotbar(self):
        spacing = 0.12
        start_x = -((self.hotbar_size - 1) * spacing) / 2
        
        for i in range(self.hotbar_size):
            # Slot Background
            slot = Button(
                parent=self.hotbar_ui,
                model='quad',
                scale=(0.1, 0.1),
                color=color.rgba(255, 255, 255, 100),
                position=(start_x + i * spacing, 0),
                pressed_color=color.white,
                highlight_color=color.rgba(255, 255, 255, 150)
            )
            
            # Item Icon
            block_id = self.items[i]
            item_icon = Entity(
                parent=slot,
                model='quad',
                texture=BLOCK_TEXTURES[block_id],
                scale=(0.8, 0.8),
                z=-0.1
            )
            
            # Key Hint
            Text(
                parent=slot,
                text=str(i+1),
                position=(-0.4, 0.4),
                scale=0.7,
                color=color.white
            )
            
            self.slots_ui.append({'bg': slot, 'icon': item_icon})
            
        # Selection Indicator
        self.indicator = Entity(
            parent=self.hotbar_ui,
            model='quad',
            scale=(0.11, 0.11),
            color=color.rgba(255, 255, 0, 150),
            position=self.slots_ui[0]['bg'].position,
            z=0.1
        )
        
        self.update_selection()

    def update_selection(self):
        # Update indicator position
        self.indicator.position = self.slots_ui[self.selected_slot]['bg'].position
        
        # Update game state
        from state import game_state
        game_state.selected_block = self.items[self.selected_slot]
        
        # Update player hand texture
        if hasattr(self.player, 'hand'):
            self.player.hand.texture = BLOCK_TEXTURES[game_state.selected_block]

    def input(self, key):
        if key == 'e':
            self.toggle_inventory()
            
        if not self.is_open:
            # Number keys 1-5
            if key in [str(i+1) for i in range(self.hotbar_size)]:
                self.selected_slot = int(key) - 1
                self.update_selection()
            
            # Scroll wheel
            if key == 'scroll up':
                self.selected_slot = (self.selected_slot + 1) % self.hotbar_size
                self.update_selection()
            if key == 'scroll down':
                self.selected_slot = (self.selected_slot - 1) % self.hotbar_size
                self.update_selection()

    def toggle_inventory(self):
        self.is_open = not self.is_open
        self.inventory_panel.enabled = self.is_open
        
        # Toggle mouse cursor and player movement
        mouse.visible = self.is_open
        mouse.locked = not self.is_open
        self.player.cursor.visible = not self.is_open
        
        # Disable player controller during inventory
        if self.is_open:
            self.player.enabled = False
        else:
            self.player.enabled = True
            
        if self.is_open:
            self.refresh_inventory_panel()

    def refresh_inventory_panel(self):
        # Clean up existing items in panel
        for child in self.inventory_panel.children:
            if isinstance(child, Button) and child != self.panel_title:
                destroy(child)
                
        # Fill with all available blocks
        x_start = -0.4
        y_start = 0.2
        spacing = 0.15
        
        for i, (block_id, texture) in enumerate(BLOCK_TEXTURES.items()):
            row = i // 4
            col = i % 4
            
            btn = Button(
                parent=self.inventory_panel,
                model='quad',
                texture=texture,
                scale=(0.12, 0.12),
                position=(x_start + col * spacing, y_start - row * spacing),
                tooltip=Tooltip(BLOCK_NAMES[block_id])
            )
            
            # When clicked, update selected slot with this item
            btn.on_click = Func(self.set_slot_item, self.selected_slot, block_id)

    def set_slot_item(self, slot_index, block_id):
        self.items[slot_index] = block_id
        self.slots_ui[slot_index]['icon'].texture = BLOCK_TEXTURES[block_id]
        self.update_selection()
        # self.toggle_inventory() # Optional: close inventory after selection
