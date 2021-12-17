""" This module handles the user interface for the grana model. 

Classes:
SimulationWindow -- the window that displays the grana model in progress, and handles
much of the user interface. 

"""

import csv
from datetime import datetime
import pyglet
from pyglet.gl import glTranslatef, glScalef
from pyglet.window import key
from math import sqrt
from math import pi
import pymunk
import pymunk.pyglet_util


class SimulationWindow(pyglet.window.Window):
    """Display window for the simulation."""

    def __init__(
        self, width, height, sim_env, window_offset, timer, scoreboard, sprite_handler
    ):
        super().__init__(width=width, height=height)
        self.sim_env = sim_env
        self.sprite_handler = sprite_handler
        self.scoreboard = scoreboard
        self.timer = timer
        self.options = pymunk.pyglet_util.DrawOptions()
        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.set_location(window_offset[0], window_offset[1])
        self.window_width, self.window_height = self.get_size()

        # openGL translation variables
        self.gl_scale_factor = (1.0, 1.0, 0.0)
        self.glTrans_offset = (0.0, 0.0, 0.0)

        self.selected_objects = []  # holds the current selected objects
        self.selection_area = 1.0  # hodls the current selection area in square nm

        self.cursor_xy = (
            100.0,
            100.0,
        )  # holds the current selected coordinates for our object sublist.
        self.sel_radius = (
            0.0  # holds the current radius selected for exporting a subset of objects
        )

    def get_nm_coordinates(self, pyg_pos: tuple[float, float]):
        """Takes pyglet coordinates and returns the corresponding coordinates in nm,
        adjusted for the GL shift"""

        x, y = pyg_pos
        cur_window_width, cur_window_height = self.get_size()

        x_nm = (x / cur_window_width * self.window_width) - self.glTrans_offset[0]
        y_nm = (y / cur_window_height * self.window_height) - self.glTrans_offset[1]

        return (x_nm, y_nm)

    def on_key_press(self, symbol, modifiers):
        """Handles key presses"""
        if symbol == key.D:
            self.diffusion_handler.toggle_diffusion_state()
        if symbol == key.S:
            self.sprite_handler.toggle_debug_draw()
        if symbol == key.E:
            # export the coordinates for all objects in the obstacle list
            self.sim_env.export_coordinates()
        if symbol == key.C:
            # center the grana in the screen and scale it up a bit
            self.set_size(self.window_width * 2, self.window_height * 2)
            glTranslatef(0.05 * self.window_width, 0.025 * self.window_height, 0)
            glScalef(2, 2, 0)
        if symbol == key.Q:
            self.export_subset()
        if symbol == key.K:
            self.window_move(axis=1, dist=20)
            # glTranslatef(0, 20, 0)
        if symbol == key.I:
            self.window_move(axis=1, dist=-20)
            # glTranslatef(0, -20, 0)
        if symbol == key.L:
            self.window_move(axis=0, dist=-20)
            # glTranslatef(-20, 0, 0)
        if symbol == key.J:
            self.window_move(axis=0, dist=20)
            # glTranslatef(20, 0, 0)
        if symbol == key.Z:
            glScalef(1.1, 1.1, 0)
        if symbol == key.X:
            glScalef(0.89, 0.89, 0)
        if symbol == key.MINUS:
            self.sprite_handler.change_gl_scale_factor(value=-0.0005)
        if symbol == key.EQUAL:
            self.sprite_handler.change_gl_scale_factor(value=0.0005)
        if symbol == key.BRACKETLEFT:
            self.sprite_handler.change_rotation_factor(value=-0.1)
        if symbol == key.BRACKETRIGHT:
            self.sprite_handler.change_rotation_factor(value=0.1)

    def window_move(self, axis: int, dist: int):
        """shifts the view of the window using glTranslatef, saves the offset of the
        window for accurate coordinate tracking"""
        if axis == 0:
            # move on x axis
            glTranslatef(dist, 0, 0)
            x, y, z = self.glTrans_offset
            self.glTrans_offset = (x + dist, y, z)
        else:
            # move on y axis
            glTranslatef(0, dist, 0)
            x, y, z = self.glTrans_offset
            self.glTrans_offset = (x, y + dist, z)
        print(self.glTrans_offset)

    def window_scale(self, factor: float):
        self.gl_scale_factor = (
            self.gl_scale_factor[0] + factor,
            self.gl_scale_factor[1] + factor,
            0.0,
        )
        glScalef(factor, factor, 0.0)

    def export_subset(self):
        obj_subset = self.find_objects_in_zone(
            origin=self.cursor_xy, radius=self.sel_radius
        )

        print(
            f"There are {len(obj_subset)} within {self.sel_radius} nm of the point {self.cursor_xy}."
        )

        if len(obj_subset) > 0:
            self.export_coordinates(obj_subset)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.cursor_xy = self.get_nm_coordinates((x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            x1, y1 = self.cursor_xy
            x2, y2 = self.get_nm_coordinates((x, y))
            self.sel_radius = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # calculate selection area
            self.selection_area = pi * self.sel_radius ** 2

            print(
                f"coordinates {self.cursor_xy} selected as origin, radius = {self.sel_radius}, area = {self.selection_area}"
            )

            self.selected_objects = self.find_objects_in_zone(
                origin=self.cursor_xy, radius=self.sel_radius
            )
            print(f"we selected {len(self.selected_objects)} objects.")

    def find_objects_in_zone(self, origin, radius):
        x, y = origin
        sel_obj = []
        for obstacle in self.sim_env.object_list:
            x1, y1 = obstacle.body.position

            # calculate distance from given point
            euc_dist = sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

            # if the distance is less than the radius
            # add it to the selected obj list
            if euc_dist <= radius:
                sel_obj.append(obstacle)

        return sel_obj

    def get_arb_shapes(self, arb):
        return arb.shapes

    def update(self, dt):
        self.timer.tick(print_ms_per_tick=True)
        self.sum_overlap_dist = 0
        # self.space.step(dt)
        self.sim_env.step(dt)

    def on_draw(self):
        self.clear()
        # self.collision_handler.draw_collision_label(
        #     label_pos=(20, self.window_height - 35)
        # )
        # self.collision_handler.draw_area_label(label_pos=(20, self.window_height - 50))
        self.fps_display.draw()
        # scoreboard.draw(label_pos=[20, window_height - 35])
        # self.timer.draw_elapsed_time(label_pos=[20, self.window_height - 20])

        if self.sprite_handler.debug_draw == 0:
            self.sim_env.space.debug_draw(self.options)
        else:
            self.sprite_handler.draw(self.sim_env.object_list, batch=self.sim_env.batch)
