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
    def __init__(
        self,
        window_offset,
        space,
        spawner,
        timer,
        scoreboard,
        diffusion_handler,
        sprite_handler,
        collision_handler,
        batch,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.timer = timer
        self.spawner = spawner
        self.space = space
        self.batch = batch
        self.scoreboard = scoreboard
        self.diffusion_handler = diffusion_handler
        self.sprite_handler = sprite_handler
        self.options = pymunk.pyglet_util.DrawOptions()
        self.collision_handler = collision_handler
        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self.set_location(window_offset[0], window_offset[1])

        self.window_width, self.window_height = self.get_size()
        # self.options = DrawOptions(batch = my_batch)
        self.grana_radius = 200.0
        self.grana_origin = (200.0, 200.0)

        # openGL translation variables
        self.scale_factor = (1.0, 1.0, 0.0)
        self.delta_pos = (0.0, 0.0, 0.0)

        self.collision_list = (
            []
        )  # holds body objects that are currently colliding
        self.sum_overlap_dist = 0.0

        self.selected_objects = []  # holds the current selected objects
        self.selection_area = (
            1.0  # hodls the current selection area in square nm
        )

        self.cursor_xy = (
            100.0,
            100.0,
        )  # holds the current selected coordinates for our object sublist.
        self.sel_radius = 0.0  # holds the current radius selected for exporting a subset of objects

        # start the simulation by instantiating the objects
        self.obstacle_list, self.particle_list = self.spawner.setup_model()

    # window.get_size():
    def get_nm_coordinates(self, pyg_pos: tuple[float, float]):

        # pyg_pos is the pyglet coordinates in the window
        # x / get_window_size = a normalized number which you then multiply by the original window_height
        x1, y1 = pyg_pos
        cur_window_width, cur_window_height = self.get_size()

        x0 = (x1 / cur_window_width * self.window_width) - self.delta_pos[
            0
        ]  # gives coordinates in original window size, so it is nm
        y0 = (y1 / cur_window_height * self.window_height) - self.delta_pos[1]

        return (x0, y0)

        # for point in arbiter.contact_point_set.points:
        #     if point.distance < 0:
        #         for shape in arbiter.shapes:
        #             # add it to the collist list for scoring purposes
        #             if shape.body not in self.collision_list:
        #                 self.collision_list.append(shape.body
        #         self.sum_overlap_dist += point.distance
        #             # try a movement
        #             self.body_adjustment(shape.body)

    # def count_overlap_distance(self, col_list):

    #     def get_distance(arb):
    #         contact_points = []
    #         cp_set = arb.contact_point_set
    #         return cp_set

    #     body_list = [shape.body for shape in col_list]
    #     u_body_list = set(body_list)
    #     print(f"body_list: {len(body_list)} vs unique body_list: {len(u_body_list)}")

    #     # print(body_list)
    #     sum_dist = 0

    #     for body in u_body_list:
    #         temp = body.each_arbiter(get_distance)
    #         print(temp)

    #     return sum_dist

    # now take unique body list and get all arbiters dealing with them

    # if arbiter.contact_point_set.point.distance
    # contact_point_set = arbiter.contact_point_set
    # colliding_objects = arbiter.shapes

    # if contact_point_set.distance < 0:
    #     print(f"{colliding_objects} overlap: {contact_point_set.distance}")

    # for point in contact_point_set.points:
    #     print(point.distance)

    #     contact_point_set = arbiter.contact_point_set
    #     for point in contact_point_set.points:
    #         print(point.distance)
    # colliding_objects = arbiter.shapes
    # if contact_point_set.distance < 0:
    #     print(f"{colliding_objects} overlap: {contact_point_set.distance}")
    # print(f"contact_poinst_set is {contact_point_set}, shapes = {colliding_objects}")
    # for object in colliding_objects:
    #     if object not in self.collision_list:
    #         self.collision_list.append(object)

    def export_coordinates(self, ob_list):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M")
        filename = str(f"{dt_string}_object_data.csv")
        print(filename + " has been exported.")

        with open(filename, "w", newline="") as f:
            write = csv.writer(f)
            # write the headers
            write.writerow(["type", "x", "y", "angle", "area"])

            for obstacle in ob_list:
                write.writerow(
                    (
                        obstacle.type,
                        obstacle.body.position[0],
                        obstacle.body.position[1],
                        obstacle.body.angle,
                        obstacle.area,
                    )
                )

    def on_key_press(self, symbol, modifiers):
        if symbol == key.D:
            self.diffusion_handler.toggle_diffusion_state()
        if symbol == key.S:
            self.sprite_handler.toggle_debug_draw()
        if symbol == key.E:
            # export the coordinates for all objects in the obstacle list
            self.export_coordinates(ob_list=self.obstacle_list)
        if symbol == key.C:
            # center the grana in the screen and scale it up a bit
            self.set_size(self.window_width * 2, self.window_height * 2)
            glTranslatef(
                0.05 * self.window_width, 0.025 * self.window_height, 0
            )
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
            self.sprite_handler.change_scale_factor(value=-0.0005)
        if symbol == key.EQUAL:
            self.sprite_handler.change_scale_factor(value=0.0005)
        if symbol == key.BRACKETLEFT:
            self.sprite_handler.change_rotation_factor(value=-0.1)
        if symbol == key.BRACKETRIGHT:
            self.sprite_handler.change_rotation_factor(value=0.1)

    def window_move(self, axis: int, dist: int):
        if axis == 0:
            # move on x axis
            glTranslatef(dist, 0, 0)
            x, y, z = self.delta_pos
            self.delta_pos = (x + dist, y, z)
        else:
            # move on y axis
            glTranslatef(0, dist, 0)
            x, y, z = self.delta_pos
            self.delta_pos = (x, y + dist, z)
        print(self.delta_pos)

    def window_scale(self, factor: float):
        self.scale_factor = (
            self.scale_factor[0] + factor,
            self.scale_factor[1] + factor,
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
        for obstacle in self.obstacle_list:
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

        self.diffusion_handler.handle_diffusion(self.particle_list)

        self.timer.tick(
            print_ms_per_tick=True
        )  # update ticks since the world started
        self.collision_handler.reset_collision_count()  # collision handler reset of counts

        # reset overlap distance and collision list
        self.sum_overlap_dist = 0
        # self.collision_list = []

        # advance simulation one step
        self.space.step(dt)

        # scoreboard.update_score(self.collision_list)
        # scoreboard.update_overlap_score(self.sum_overlap_dist, self.selection_area)

        # for obstacle in self.obstacle_list:
        #     # obstacle.
        #     pass
        #    for shape in obstacle.body.shapes:
        #         print(shape.shapes_collide())

        # # # everything shifts a tiny tiny bit
        # for obstacle in self.obstacle_list:
        #     rand_int = random.randint(0, 3)

        #     if rand_int == 0:
        #         obstacle.move("up", step_distance=0.001)
        #     if rand_int == 1:
        #         obstacle.move("down", step_distance=0.001)
        #     if rand_int == 2:
        #         obstacle.move("left", step_distance=0.001)
        #     if rand_int == 3:
        #         obstacle.move("right", step_distance=0.001)

        # subdomain
        # go through all the objects in a list of selected objects one by one
        # while len(self.selected_objects) > 0:

        # for ob_num, obstacle in enumerate(self.selected_objects):
        #     # note the old normalized overlap score
        #     old_overlap = scoreboard.norm_overlap_score

        #     # perform an action
        #     obstacle.action(random.randint(0, 5))

        #     # advance the simulation one step to allow new collisions to occur
        #     self.space.step(dt)

        #     # calculate new overlap score after collisions solved
        #     scoreboard.update_overlap_score(self.sum_overlap_dist, self.selection_area)

        #     #if self.sum_overlap_dist is worse than old_overlap, we need to undo that action
        #     # first we have a bit of code here to give feedback to see if it is working.
        #     if scoreboard.norm_overlap_score < old_overlap:
        #         obstacle.undo()
        #         self.space.step(dt)

    def on_draw(self):
        self.clear()
        self.collision_handler.draw_collision_label(
            label_pos=(20, self.window_height - 35)
        )
        self.collision_handler.draw_area_label(
            label_pos=(20, self.window_height - 50)
        )
        self.fps_display.draw()
        # scoreboard.draw(label_pos=[20, window_height - 35])
        self.timer.draw_elapsed_time(label_pos=[20, self.window_height - 20])

        if self.sprite_handler.debug_draw == 0:
            self.space.debug_draw(self.options)
        else:
            self.sprite_handler.draw(self.obstacle_list, batch=self.batch)
