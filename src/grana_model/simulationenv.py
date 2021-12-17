# -*- coding: utf-8 -*-
"""simulation environment

This module implements an the grana_model simulation environment, with object
instantiation, overlap detection. It does not produce any graphical output on
its own.

Parameters:
    pos_csv_filename (Path): path to the csv file containing object positions
    in format:
        type, position.x, position.y, angle, area

Example:
    $
    $

Todo:
    * everything. abstract strategies, coding the overlap agent, etc.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import csv
from datetime import datetime
from pathlib import Path
import pyglet
import pymunk

from grana_model.collisionhandler import CollisionHandler
from grana_model.objectdata import ObjectData, ObjectDataExistingData
from grana_model.spawner import Spawner


class SimulationEnvironment:
    """represents a simulation environment, with pymunk.Space, PSIIStructures
    instantiated within it by a Spawner instance from a provided coord file."""

    def __init__(self, pos_csv_filename: str, object_data_exists: bool):
        self.space = pymunk.Space()
        self.batch = pyglet.graphics.Batch()
        self.spawn_type: str = "full"

        if object_data_exists:
            object_data = ObjectDataExistingData(pos_csv_filename=pos_csv_filename)
        else:
            object_data = ObjectData(pos_csv_filename=pos_csv_filename)

        self.spawner = Spawner(
            object_data=object_data,
            spawn_type=self.spawn_type,
            shape_type="complex",
            space=self.space,
            batch=self.batch,
            num_particles=0,
            num_psii=211,
        )

        self.collision_handler = CollisionHandler(self.space)

        self.object_list, self.particle_list = self.spawner.setup_model()

    def export_coordinates(self):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")
        filename = Path.cwd() / "output" / f"{dt_string}_data.csv"

        with open(filename, "w", newline="") as f:
            write = csv.writer(f)
            # write the headers
            write.writerow(["type", "x", "y", "angle", "area"])
            for object in self.object_list:
                write.writerow(
                    (
                        object.type,
                        round(object.body.position[0], 2),
                        round(object.body.position[1], 2),
                        round(object.body.angle, 2),
                        round(object.area, 2),
                    )
                )

    def step(self, dt):
        self.space.step(dt)
