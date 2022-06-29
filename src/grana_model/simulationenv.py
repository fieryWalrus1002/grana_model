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
        dt: float = 0.01666667,
        damping: float = 0.1,
    ):
        # simulation components
        self.space = space
        self.attraction_handler = attraction_handler
        self.spawner = spawner
        self.object_data = object_data

        # simulation variables
        self.active = True
        self.dt = dt
        self.space.damping = damping
        self.attraction_point_coords = []
        self.attraction_handler.enabled = (
            False  # false for only brownian motion, not attraction forces
        )

    def check_for_active(self):
        """ Search through all objects, and return FALSE if any have active==False"""

        object_status = [o.active for o in self.obstacle_list]
        
        if False in object_status:
            return False
        else:
            return True

    def run(self):
        """ creates the obstacles and begins running the simulation"""
        self.obstacle_list, self.particle_list, _ = self.spawner.setup_model()

        while self.check_for_active():
            self.step()


    def step(self):
        # zero all vectors
        self.attraction_handler.reset_vectors_for_all_objects(self.obstacle_list)

        # tell all LHCII to update their attraction vectors for this next step
        self.attraction_handler.calculate_attraction_forces(self.obstacle_list)

        # apply all vectors to each LHCII particle, if attraction_handler.enabled is True. Else, just do thermal movement and rotation.
        self.attraction_handler.apply_all_vectors(
            self.obstacle_list, attraction_enabled=self.attraction_handler.enabled
        )

        # update simulation one step
        self.space.step(self.dt)

        # get a list of attraction point coordinates to draw during on_draw() call
        self.attraction_point_coords = self.attraction_handler.get_points_to_draw(
            self.obstacle_list
        )

        

    
    def fight(self):
        return "we fight now"
