from pyglet.graphics import Batch
from pymunk.space import Space
from grana_model.psiistructure import PSIIStructure
from grana_model.particle import Particle
from grana_model.objectdata import ObjectData
from random import random
from math import cos, sin, pi


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
        num_particles: int = 1000,
        num_psii: int = 1000,
    ):
        self.object_data = object_data
        self.num_psii = num_psii
        self.num_particles = num_particles
        self.ratio_free_LHC = 2  # Helmut says "Assuming that you have 212 PSII (dimer =C2) particles then LHCII should be 424 (2xPSII)"
        self.ratio_cytb6f = 0.3  # 083021: Helmut says cyt b6f 70 (1/3 x PSII)
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

    # def spawn_psii(self):
    #     """spawns only psii obstacles into the simulation space to be rendered
    #     as part of the provided batch, and appends them to the list provided
    #     for later usage in the simulation model"""

    #     object_list = [
    #         PSIIStructure(self.space, obj, self.batch, self.shape_type)
    #         for obj in self.object_data.object_list
    #     ]

    #     return object_list

    def spawn_psii(self):
        """spawns only psii obstacles into the simulation space to be rendered
        as part of the provided batch, and appends them to the list provided
        for later usage in the simulation model, up to a limit of self.num_psii"""

        object_list = []

        while len(object_list) < self.num_psii:
            try:
                obj = next(self.object_data.object_list)
            except StopIteration:
                return object_list
            # print(obj)
            # if obj.get("obj_type") == "C2S2M2":
            object_list.append(
                PSIIStructure(self.space, obj, self.batch, self.shape_type)
            )

        return object_list

    def spawn_particles(self):
        """Instantiates particles into the simulation space and returns a list
        of the particles for later usage in the simulation model
        """
        object_list = [
            Particle(
                space=self.space,
                batch=self.batch,
                pos=self.random_pos_in_circle(
                    max_radius=200, center=(200, 200)
                ),
            )
            for _ in range(0, self.num_particles)
        ]

        return object_list

    def spawn_particles_empty(self):
        """return an empty list for when you don't want to spawn particles"""
        return []

    def setup_model(self):
        """instantiates particles and obstacles according to spawner provided spawn_type"""

        if self.spawn_type == "psii_only":
            return self.spawn_psii(), self.spawn_particles_empty()

        else:
            return self.spawn_psii(), self.spawn_particles()

    # def spawn_secondary_obstacles(self, space, batch):
    #     """spawns only psii obstacles into the simulation space to be rendered
    #     as part of the provided batch, and appends them to the list provided
    #     for later usage in the simulation model"""
    #     object_list = [
    #         PSIIStructure(
    #             PSIIStructure(space, obj, batch, self.shape_type),
    #             space=space,
    #             batch=batch,
    #             pos=self.random_pos_in_circle(
    #                 max_radius=200, center=(200, 200)
    #             ),
    #         )
    #         for _ in range(0, self.particle_count)
    #     ]
    #     return object_list


#  for i in range(0, int(ratio_free_LHC * len(pos_dict["pos_xy"]))):
#                 obj_type = "LHCII"
#                 pos_xy = random_pos_in_circle(max_radius=200, center=(200,200))

#                 self.obstacle_list.append(PSII_structure(mass=10,
#                                                         space=self.space,
#                                                         filechunk=obj_point_filenames[obj_type],
#                                                         type=obj_type,
#                                                         pos=pos_xy,
#                                                         color=pos_dict['colors'][obj_type],
#                                                         img=pos_dict['sprites'][obj_type],
#                                                         batch=my_batch))

#             # instantiate cytb6f
#             for i in range(0, num_cytb6f):
#                 obj_type = "cytb6f"
#                 pos_xy = random_pos_in_circle(max_radius=200, center=(200,200))

#                 self.obstacle_list.append(PSII_structure(mass=10,
#                                                         space=self.space,
#                                                         filechunk=obj_point_filenames[obj_type],
#                                                         type=obj_type,
#                                                         pos=pos_xy,
#                                                         color=pos_dict['colors'][obj_type],
#                                                         img=pos_dict['sprites'][obj_type],
#                                                         batch=my_batch))
#         for i, pos_xy in enumerate(self.object_data.pos_xy):
#             obj_type = str(pos_dict["obj_type"][i])

#             # if obj_type == "C2S2M2":
#             self.obstacle_list.append(PSII_structure(mass=100,
#                                                     space=self.space,
#                                                     filechunk=obj_point_filenames[obj_type],
#                                                     type=obj_type,
#                                                     pos=pos_xy,
#                                                     color=pos_dict['colors'][obj_type],
#                                                     img=pos_dict['sprites'][obj_type],
#                                                     batch=my_batch))

# # instantiate particles
#         for i in range(particle_count):
#             self.particle_list.append(Particle(space=self.space,
#                                         position=random_pos_in_circle(self.grana_radius, self.grana_origin),
#                                         particle_list=self.particle_list,
#                                         particle_radius=1
#                                         ))


#         if spawn_psii_only == False:
#             # # instantiate free LHCII
#             for i in range(0, int(ratio_free_LHC * len(pos_dict["pos_xy"]))):
#                 obj_type = "LHCII"
#                 pos_xy = random_pos_in_circle(max_radius=200, center=(200,200))

#                 self.obstacle_list.append(PSII_structure(mass=10,
#                                                         space=self.space,
#                                                         filechunk=obj_point_filenames[obj_type],
#                                                         type=obj_type,
#                                                         pos=pos_xy,
#                                                         color=pos_dict['colors'][obj_type],
#                                                         img=pos_dict['sprites'][obj_type],
#                                                         batch=my_batch))

#             # instantiate cytb6f
#             for i in range(0, num_cytb6f):
#                 obj_type = "cytb6f"
#                 pos_xy = random_pos_in_circle(max_radius=200, center=(200,200))

#                 self.obstacle_list.append(PSII_structure(mass=10,
#                                                         space=self.space,
#                                                         filechunk=obj_point_filenames[obj_type],
#                                                         type=obj_type,
#                                                         pos=pos_xy,
#                                                         color=pos_dict['colors'][obj_type],
#                                                         img=pos_dict['sprites'][obj_type],
#                                                         batch=my_batch))
