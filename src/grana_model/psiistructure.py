from pyglet.sprite import Sprite
from math import degrees, sqrt
from random import random
from pymunk import Vec2d, Body, moment_for_circle, Poly, Space
from pyglet.graphics import Batch


class PSIIStructure:
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

    def _assign_sprite(self, batch):
        """loads the img and assigns it as a sprite to this obejct"""
        img = self.obj_dict["sprite"]
        color = self.obj_dict["color"]
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        self.sprite = Sprite(
            img, x=self.body.position.x, y=self.body.position.y, batch=batch
        )
        self.sprite.scale = 0.009
        spr_color = (color[0], color[1], color[2])
        self.sprite.color = spr_color
        self.sprite.rotation = degrees(-self.body.angle)
        # obstacle_dict["sprite_list"].append(self.sprite)

    def _create_shape_string(self, shape_type: str):
        """create a shape_string that when provided as
        an argument to eval(), will create all the compound or simple
        shapes needed to define complex structures and
        add them to the space along with the object body"""

        # now create all the shapes from the shape coordinate files
        shape_list = []
        str_command = "self.body, "

        if shape_type == "simple":
            coord_list = self.obj_dict["shapes_simple"]
        else:
            coord_list = self.obj_dict["shapes_compound"]

        # find all the matching coordinate files
        for i, shape_coordinates in enumerate(coord_list):

            # shape_coordinates = read_csv(file).values.tolist()

            # create the shape
            my_shape = Poly(self.body, vertices=shape_coordinates)

            my_shape.color = self.obj_dict["color"]

            my_shape.collision_type = 1

            # append the shape to our shape list
            shape_list.append(my_shape)

            # add the shape to the string
            str_command += str(f"shape_list[{i}], ")

        return shape_list, (f"space.add({str_command})")

    def update_sprite(self, sprite_scale_factor, rotation_factor):
        self.sprite.rotation = degrees(-self.body.angle) + rotation_factor
        self.sprite.position = self.body.position
        if self.sprite.scale == sprite_scale_factor:
            return
        self.sprite.scale = sprite_scale_factor

    def get_current_pos(self):
        self.current_xy = (self.body.x, self.body.y)

    def go_home(self):
        direction = Vec2d(
            x=self.origin_xy[0] / 10000, y=self.origin_xy[1] / 10000
        )
        self.body.apply_force_at_local_point(force=direction, point=(0, 0))

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 1
        Body.update_velocity(body, gravity, damping, dt)
        body_velocity_length = body.velocity.length
        if body_velocity_length > max_velocity:
            scale = max_velocity / body_velocity_length
            body.velocity = body.velocity * scale

    def undo(self):
        if self.last_action["action"] == "rotate":
            self.body.angle = self.last_action["old_value"]
        if self.last_action["action"] == "move":
            self.body.position = self.last_action["old_value"]

    def action(self, action_num):
        if action_num == 0:
            # up
            self.move("up")
            pass
        if action_num == 1:
            # down
            self.move("down")
            pass
        if action_num == 2:
            # right
            self.move("right")
            pass
        if action_num == 3:
            # left
            self.move("left")
            pass
        if action_num == 4:
            # rotate left
            self.rotate(direction=0)
            pass
        if action_num == 5:
            # rotate right
            self.rotate(direction=1)
            pass

    def rotate(self, direction):
        current_angle = self.body.angle
        random_angle = random() * 2 * 0.0174533

        if direction == 0:
            # rotate left
            new_angle = current_angle + random_angle

            self.last_action = {
                "action": "rotate",
                "old_value": current_angle,
                "new_value": new_angle,
            }
        else:
            # rotate right
            new_angle = current_angle - random_angle

            self.last_action = {
                "action": "rotate",
                "old_value": current_angle,
                "new_value": new_angle,
            }
        # set the new angle
        self.body.angle = new_angle

    def move(self, direction, **kwargs):
        # what distance should the model move in one action? use a provided value or use this one
        step_distance = kwargs.get("step_distance", 0.26)

        # move in a direction but end within the tether distance
        # body.position.x and body.position.y can be modified, but the new position has to be within the distance of 1nm in any direction from the origin point.
        # a new point must be within tether_radius of tether_pointFcircle
        x0, y0 = self.origin_xy
        start_pos = self.body.position
        tether_radius = 1

        # the current dist from tether, starts too high because it is updated
        dist = 1000.0

        # is this a valid location?
        while dist > tether_radius:
            # will start as current pos
            x1, y1 = self.body.position

            # each attempt will reduce the step distance a tiny amount
            step_distance = step_distance - 0.01

            # move in a direction the step distance
            if direction == "up":
                y1 += step_distance
            if direction == "down":
                y1 -= step_distance
            if direction == "right":
                x1 += step_distance
            if direction == "left":
                x1 -= step_distance

            # calculate the new distance from the tether point
            dist = sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

        # the new position is within the tether range, so lets assign it
        self.body.position = (x1, y1)

        # save the action so we can undo it later if needed
        self.last_action = {
            "action": "move",
            "old_value": start_pos,
            "new_value": self.body.position,
        }

    # ### random position
    #     # generate a new position within range of the origin, and move the object to that location
    #     # new position
    #     # random angle
    #     alpha = 2 * pi * random()

    #     # random radius, random float between 0 to 1 * tether_radius
    #     r = random() * tether_radius

    #     t = 2 * pi * random()

    #     # new (x, y) tuple
    #     random_pos = ((r*cos(t)) + x0, y0 + (r*sin(t)))
    #     # x1, y1 = obstacle.body.position

    #     #     # calculate distance from given point
    #     #     euc_dist = sqrt((x1-x)**2 + (y1-y)**2)

    #     #     # if the distance is less than the radius
    #     #     # add it to the selected obj list
    #     #     if euc_dist <= radius:
    #     #         sel_obj.append(obstacle)
