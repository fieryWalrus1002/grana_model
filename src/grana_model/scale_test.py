from pyglet.graphics import Batch
from pymunk.space import Space
from grana_model.psiistructure import PSIIStructure
from grana_model.particle import Particle
from grana_model.objectdata import ObjectData
from random import random
from math import cos, sin, pi
from pymunk import Vec2d, Body, moment_for_circle, Poly, Space


class TestObject:
    def __init__(
        self,
        space: Space,
        obj_dict: dict,
        batch: Batch,
        shape_type: str,
        mass=100,
    ):
        self.obj_dict = obj_dict
        self.type = obj_dict["obj_type"]
        self.origin_xy = obj_dict["pos"]
        self.current_xy = obj_dict["pos"]
        self.last_action = (
            {}
        )  # dict to save last action so we can undo it if necessary
        self.new_scale = 100

        # create the body
        inertia = moment_for_circle(
            mass=mass, inner_radius=0, outer_radius=10, offset=(0, 0)
        )

        if self.type in ["C2S2M2", "C2S2M", "C2S2", "C2", "C1"]:
            body = Body(mass=mass, moment=inertia, body_type=Body.KINEMATIC)
        else:
            body = Body(mass=mass, moment=inertia, body_type=Body.DYNAMIC)

        body.position = self.origin_xy  # given pos
        body.angle = obj_dict["angle"]  # in radians
        body.velocity_func = self.limit_velocity  # limit velocity
        self.body = (
            body  # save a reference to the body in the PSII_structure object
        )

        # create the shapes and add them to the space
        shape_list, shape_str = self._create_shape_string(shape_type=shape_type)
        eval(shape_str)

        # create the sprite
        self._assign_sprite(batch=batch)


class Spawner:
    """handles instantiation of objects into the simulation window, and for now
    has a random_pos_in_circle function because where else should it go"""

    def __init__(
        self,
        object_data: ObjectData,
        shape_type: str,
        space: Space,
        batch: Batch,
        spawn_type: str,
    ):
        self.object_data = object_data
        self.particle_count = 1000
        self.ratio_free_LHC = 2.00  # Helmut says "Assuming that you have 212 PSII (dimer =C2) particles then LHCII should be 424 (2xPSII)"
        self.num_cytb6f = 70  # 083021: Helmut says cyt b6f 70 (1/3 x PSII)
        self.shape_type = shape_type
        self.spawn_type = spawn_type
        self.space = space
        self.batch = batch

    def random_pos_in_circle(self, max_radius, center):
        rand_roll = random() + random()

        if rand_roll > 1:
            r = (2 - rand_roll) * max_radius
        else:
            r = rand_roll * max_radius

        t = 2 * pi * random()

        return [(r * cos(t)) + center[0], center[1] + (r * sin(t))]

   def setup_model(self, num_particles=0):
        #sets up the simulation with a certain test set of objects


    def spawn_scale_bar(self):
        pass


    def spawn_5nm_square(self):
        pass

    def spawn_super_simple_c2s2m2(self):
        pass
