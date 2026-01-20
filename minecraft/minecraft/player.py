from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
from environment import Hand

class PlayerController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0.5
        self.cursor.visible = False
        
        # Player attributes
        self.hand = Hand()
        self.flashlight = SpotLight(parent=self, position=(0,2,1), enabled=False)
        self.flashlight.look_at(self.position + self.forward * 10)
        
    def update(self):
        super().update()
        
        # Hand animation
        if held_keys['left mouse'] or held_keys['right mouse']:
            self.hand.active()
        else:
            self.hand.passive()
        
        # Sprinting
        if held_keys['shift']:
            self.speed = 10
        else:
            self.speed = 5
            
        # Hand bobbing
        walking = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
        if walking:
            self.hand.position = Vec3(0.6, -0.6 + (math.sin(time.time() * 10) * 0.02), 0)

    def toggle_flashlight(self):
        self.flashlight.enabled = not self.flashlight.enabled
        print(f"Flashlight: {'ON' if self.flashlight.enabled else 'OFF'}")
