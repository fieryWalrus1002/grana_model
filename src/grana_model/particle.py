import pymunk
from pyglet import image
from pyglet import sprite
from math import degrees


class Particle(pymunk.Body):
    def __init__(self, space, pos, batch, particle_radius=1.5):
        self.max_movement = 1
        self.body = pymunk.Body(0, 0, body_type=pymunk.Body.DYNAMIC)
        c1 = pymunk.Circle(self.body, particle_radius)
        c1.color = (255, 0, 0, 255)
        self.shape = c1
        self.body.position = pos
        space.add(self.body, c1)
        self.diffusion_distance = 10

        self.img = image.load(
            "src/grana_model/res/sprites/lhcii_monomer.png"
        )  # TODO: get a better sprite
        # img.anchor_x = img.width // 2
        # img.anchor_y = img.height // 2

        # self.sprite = sprite.Sprite(
        #     img, x=self.body.position.x, y=self.body.position.y, batch=batch
        # )
        # self.sprite.scale = 0.003
        # self.sprite.color = (255, 255, 255)
        # self.sprite.rotation = degrees(-self.body.angle)

        # create the sprite
        self._assign_sprite(batch=batch)

    @property
    def area(self):
        """gets the total area of the object, by adding up the area of
        all of its indiviudal shapes. called as a property"""
        total_area = 0.0

        for shape in self.body.shapes:
            total_area += shape.area
        return total_area

    def _assign_sprite(self, batch):
        """loads the img and assigns it as a sprite to this obejct"""
        img = self.img
        color = (255, 0, 0)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        self.sprite = sprite.Sprite(
            img, x=self.body.position.x, y=self.body.position.y, batch=batch
        )
        self.sprite.scale = 0.003
        spr_color = (color[0], color[1], color[2])
        self.sprite.color = spr_color
        self.sprite.rotation = degrees(-self.body.angle)

    def __call__(self):
        return self.shape

    def update_sprite(self, sprite_scale_factor, rotation_factor):
        self.sprite.rotation = degrees(-self.body.angle) + rotation_factor
        self.sprite.position = self.body.position
        if self.sprite.scale == sprite_scale_factor:
            return
        self.sprite.scale = sprite_scale_factor

    def diffusion_move(self, diffusion_distance, **kwargs):
        pass
