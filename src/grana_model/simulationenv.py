# -*- coding: utf-8 -*-
"""simulation environment

This module implements an the grana_model simulation environment, with object instantiation,
overlap detection. It does not produce any graphical output on its own.

Parameters:
    pos_csv_filename (Path): path to the csv file containing object positions in format:
        type, position.x, position.y, angle, area

Example:
    $ 
    $ 

Todo:
    * everything. abstract strategies, coding the overlap agent, etc.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import pymunk
import time


class SimulationEnvironment:
    """represents a simulation environment, with pymunk.Space, PSIIStructures instantiated within it by a Spawner instance from a provided coord file."""

    def __init__(
        self,
        spawner,
        space,
        object_data,
        attraction_handler,
        densityhandler,
        dt: float = 0.01666667,
        damping: float = 0.1,
    ):
        # simulation components
        self.space = space
        self.attraction_handler = attraction_handler
        self.spawner = spawner
        self.collision_handler = self.create_sensor_collision_handler()
        self.densityhandler = densityhandler
        self.object_data = object_data
        self.obstacle_list, self.particle_list, _ = self.spawner.setup_model()
        self.sensor = self.densityhandler.create_ensemble_area_sensor()
        self.boundaries  = self.densityhandler.spawn_boundaries()

        # simulation variables
        self.active = True
        self.dt = dt
        self.space.damping = damping
        self.attraction_point_coords = []

    def check_for_active(self):
        """Search through all objects, and return FALSE if any have active==False"""

        object_status = [o.active for o in self.obstacle_list]

        if False in object_status:
            return False
        else:
            return True

    def initialze_simulation(self):
        for o in self.obstacle_list:
            for s in o.shape_list:
                s.color = self.out_color
        
        for b in self.boundaries:
            b.color = (0, 0, 0, 0)

    def run(self):
        """creates the obstacles and begins running the simulation"""
        self.obstacle_list, self.particle_list, _ = self.spawner.setup_model()

        while self.check_for_active():
            self.step()

    def step(self):

        if self.attraction_handler.active:
            # zero all vectors
            self.attraction_handler.reset_vectors_for_all_objects(self.obstacle_list)

            # tell all LHCII to update their attraction vectors for this next step
            self.attraction_handler.calculate_attraction_forces(self.obstacle_list)

            # apply all vectors to each LHCII particle
            self.attraction_handler.apply_all_vectors(self.obstacle_list)

        # update simulation one step
        self.space.step(self.dt)

        # # get a list of attraction point coordinates to draw during on_draw() call
        self.attraction_point_coords = self.attraction_handler.get_points_to_draw(
            self.obstacle_list
        )

    def fight(self):
        return "we fight now"

    def get_ensemble_area(self):
        # calculate the area within the ensemble boundaries
        internal_area, total_area = self.densityhandler.update_area_calculations(
            self.obstacle_list
        )
        ensemble_area = self.densityhandler.ensemble_area

        print(
            f"ensemble density = {round(internal_area / (ensemble_area), 2)}, interior_shape_area: {internal_area}, total_shape_area: {total_area}, ensemble_area: {ensemble_area}"
        )
    
    
    def create_sensor_collision_handler(self):
        h = self.space.add_collision_handler(1, 3)  # structure against boundary
        h.begin = self.bound_coll_begin
        h.separate = self.bound_coll_separate

        return h

    def bound_coll_begin(self, arbiter, space, data):
        arbiter.shapes[0].color = self.densityhandler.out_color
        return True

    def bound_coll_separate(self, arbiter, space, data):
        # if the shape separates from the boundary, and it is within the ensemble area,
        # add its area back to the internal_area calculation
        arbiter.shapes[0].color = self.densityhandler.in_color

        # s = arbiter.shapes[0]
        # x, y = s.center_of_gravity

        # if 200 < x < 300 and 200 < y < 300:
        return True

