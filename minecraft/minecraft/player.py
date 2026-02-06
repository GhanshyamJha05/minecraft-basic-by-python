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
        
        # Health and Stamina
        self.max_health = 100
        self.health = self.max_health
        self.max_stamina = 100
        self.stamina = self.max_stamina
        
        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        # UI Container
        self.hud = Entity(parent=camera.ui)
        
        # Health Bar Background
        self.health_bar_bg = Entity(
            parent=self.hud,
            model='quad',
            color=color.black66,
            scale=(0.4, 0.03),
            position=(-0.5, -0.4)
        )
        # Health Bar Fill
        self.health_bar = Entity(
            parent=self.health_bar_bg,
            model='quad',
            color=color.red,
            scale=(1, 1),
            position=(0, 0),
            origin=(-0.5, 0)
        )
        self.health_text = Text(
            parent=self.hud,
            text='HP',
            scale=1,
            position=(-0.72, -0.385),
            color=color.white
        )

        # Stamina Bar Background
        self.stamina_bar_bg = Entity(
            parent=self.hud,
            model='quad',
            color=color.black66,
            scale=(0.4, 0.03),
            position=(-0.5, -0.45)
        )
        # Stamina Bar Fill
        self.stamina_bar = Entity(
            parent=self.stamina_bar_bg,
            model='quad',
            color=color.cyan,
            scale=(1, 1),
            position=(0, 0),
            origin=(-0.5, 0)
        )
        self.stamina_text = Text(
            parent=self.hud,
            text='ST',
            scale=1,
            position=(-0.72, -0.435),
            color=color.white
        )

        # Crosshair
        self.crosshair = Entity(
            parent=camera.ui,
            model='quad',
            color=color.white,
            scale=(0.01, 0.01)
        )
        
    def update(self):
        super().update()
        
        # Hand animation
        if held_keys['left mouse'] or held_keys['right mouse']:
            self.hand.active()
        else:
            self.hand.passive()
        
        # Sprinting and Stamina logic
        is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
        target_speed = 5
        
        if held_keys['shift'] and is_moving and self.stamina > 0:
            target_speed = 10
            self.stamina -= 20 * time.dt  # Drain stamina
        else:
            if self.stamina < self.max_stamina:
                self.stamina += 10 * time.dt  # Regenerate stamina
        
        # Smoothly interpolate speed for better feel
        self.speed = lerp(self.speed, target_speed, time.dt * 10)
        
        # Update UI bars
        self.health_bar.scale_x = self.health / self.max_health
        self.stamina_bar.scale_x = self.stamina / self.max_stamina
        
        # Stamina bar color feedback
        if self.stamina < 20:
            self.stamina_bar.color = color.orange
        else:
            self.stamina_bar.color = color.cyan
            
        # Hand bobbing
        if is_moving:
            self.hand.position = Vec3(0.6, -0.6 + (math.sin(time.time() * 10) * 0.02), 0)

    def toggle_flashlight(self):
        self.flashlight.enabled = not self.flashlight.enabled
        print(f"Flashlight: {'ON' if self.flashlight.enabled else 'OFF'}")
