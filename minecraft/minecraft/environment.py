from ursina import *

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture='sky_default',
            scale=1000,
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

class Cloud(Entity):
    def __init__(self, pos, scale):
        super().__init__(
            model='cube',
            color=color.white,
            scale=scale,
            position=pos
        )

    def update(self):
        self.x += time.dt * 0.5
        if self.x > 60:
            self.x = -60
