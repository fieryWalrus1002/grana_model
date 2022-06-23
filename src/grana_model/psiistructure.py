import pyglet
from math import degrees, sqrt
import random
from pymunk import Vec2d, Body, moment_for_circle, Poly, Space
import os
from pathlib import Path
from math import cos, sin, pi
from abc import ABC, abstractmethod

class DistanceMagnitude(ABC):
    def __init__(self, threshold: float = 10.0):
        self.threshold = threshold

    @abstractmethod
    def get_distance_scalar(self, distance):
        '''takes a distance and returns a vector scaled according to a particular algorithm''' 
        return 0

class WellMagnitude(DistanceMagnitude):
    def get_distance_scalar(self, distance):
        """ if distance is greater than a threshold, it returns 0. otherwise, 1."""
        if distance > self.threshold:
            return 0
        else:
            return 1

class AttractionPoint:
    ''' class to store values for attraction point variables.
    parent: the parent object. we reference it when we assign vectors.
    type = 'point', 'side'
    distance_scalar: the chosen method for scaling vectors by distance
    '''
    def __init__(self, parent, type: int, distance_scalar: DistanceMagnitude, offset_coords: tuple, batch):
        self.parent = parent
        self.distance_scalar = distance_scalar.get_distance_scalar
        self.type = type
        self.offset_coords = offset_coords
        self.batch = batch

    def get_world_coords(self):
        """ TODO: verify they are being rotated """
        x, y = self.offset_coords

        return self.parent.body.position + Vec2d(x, y).rotated(self.parent.body.angle)

    def calc_vector(self, other_point):
        """ TODO: write code to calculate attraction vector between these two points, and add it to the parent's vector list"""
        return 1

class PSIIStructure:
    def __init__(
        self,
        space: Space,
        obj_dict: dict,
        batch: pyglet.graphics.Batch,
        shape_type: str,
        pos: tuple[float, float],
        angle: float,
        mass=100,
        use_sprites: bool = True,
        move: float = 1
    ):
        self.vector_list = [] # holds vectors that will be used to calculate movement force
        self.mass = mass
        self.space = space
        self.shape_list = []
        self.move = move
        self.obj_dict = obj_dict
        self.type = obj_dict["obj_type"]
        self.origin_xy = pos
        self.current_xy = pos
        self.last_action = {
            "action": "rotate",
            "old_value": angle,
            "new_value": angle,
        }
        self.new_scale = 100

        self.body = self._create_body(mass=mass, angle=angle)

        shape_list, shape_str = self._create_shape_string(shape_type=shape_type)
        eval(shape_str)

        self.shape_list = shape_list

        if use_sprites:
            self._assign_sprite(batch=batch)

        
        self.attraction_points = {
                'p1': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='point', offset_coords=(3.92, 1.26), batch=batch),
                'p2': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='point', offset_coords=(-3.13, 3.06), batch=batch),
                'p3': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='point', offset_coords=(-0.97, -4.24), batch=batch),
                's1': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='side', offset_coords=(0.68, 3.02), batch=batch),
                's2': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='side', offset_coords=(-3.17, -1.08), batch=batch),
                's3': AttractionPoint(parent = self, distance_scalar = WellMagnitude(), type='side', offset_coords=(2.3, -1.98), batch=batch)
                }


    def get_attraction_points(self):
        """ return a list of the attraction points for this structure """
        return [p for p in self.attraction_points.values()]

    def exchange_simple_for_complex(self):
        """ remove the simple body and shapes from the space, and replace them with
        the complex shapes with the same position and rotation"""

        for s in self.body.shapes:
        # for s in self.shape_list:
            self.space.remove(s)
        
        # old body position and angle
        position = self.body.position
        angle = self.body.angle
        
        # remove old body
        self.space.remove(self.body)
        
        # create new body with old parameters
        self.body = self._create_body(mass=self.mass, angle=angle, position=position)

        # get coordinates for complex shapes
        coord_list = self.obj_dict["shapes_compound"]
        
        # create new shapes
        self.shape_list = [
            self._create_shape(shape_coord=shape_coord)
            for shape_coord in coord_list
        ]

        # add new shapes and body to the space
        self.space.add(self.body, *self.shape_list)
        
        # reindex shapes for collisions
        self.space.reindex_shapes_for_body(self.body)
       
        

    def _create_body(self, mass: float, angle: float, position=None):
        """create a pymunk.Body object with given mass, position, angle"""

        inertia = moment_for_circle(
            mass=mass, inner_radius=0, outer_radius=10, offset=(0, 0)
        )

        if self.type in ["C2S2M2", "C2S2M", "C2S2", "C2", "C1"]:
            body = Body(mass=mass, moment=inertia, body_type=Body.KINEMATIC)
        else:
            body = Body(mass=mass, moment=inertia, body_type=Body.DYNAMIC)

        if position is None:
            body.position = self.origin_xy  # given pos
            
            # random angle to start with
            body.angle = 2 * pi * random.random()

        else:
            body.position = position
            body.angle = angle

        body.velocity_func = self.limit_velocity  # limit velocity

        return body

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
        img_path = (
            Path.cwd()
            / "src"
            / "grana_model"
            / "res"
            / "sprites"
            / f"{self.obj_dict['sprite']}"
        )
        # src/grana_model/res/sprites/c2.png
        img = pyglet.image.load(img_path)
        color = self.obj_dict["color"]
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        self.sprite = pyglet.sprite.Sprite(
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
        add them to the space along with self.body"""

        if shape_type == "simple":
            coord_list = self.obj_dict["shapes_simple"]
        else:
            coord_list = self.obj_dict["shapes_compound"]
        shape_list = [
            self._create_shape(shape_coord=shape_coord)
            for shape_coord in coord_list
        ]

        return (
            shape_list,
            f"space.add(self.body, {','.join([str(f'shape_list[{i}]') for i, shape in enumerate(shape_list)])})",
        )

        # str_out = f"space.add({str_command})"

        # print(str_out)

        # return shape_list, str_out

    def _create_shape(self, shape_coord: tuple):
        """creates a shape"""
        my_shape = Poly(self.body, vertices=shape_coord)

        my_shape.color = self.obj_dict["color"]
        my_shape.friction = 0.04
        my_shape.elasticity = 0.0
        my_shape.collision_type = 1

        return my_shape

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

    # def action(self, action_num):
    #     if action_num == 0:
    #         # up
    #         self.move("up")
    #         pass
    #     if action_num == 1:
    #         # down
    #         self.move("down")
    #         pass
    #     if action_num == 2:
    #         # right
    #         self.move("right")
    #         pass
    #     if action_num == 3:
    #         # left
    #         self.move("left")
    #         pass
    #     if action_num == 4:
    #         # rotate left
    #         self.rotate(direction=0)
    #         pass
    #     if action_num == 5:
    #         # rotate right
    #         self.rotate(direction=1)
    #         pass

    def action(self, action_num):
        if action_num <= 4:
            self.move(random.randint(0, 3), step_dist=0.25)
        if action_num == 5:
            # rotate left
            self.rotate(direction=0)
            pass
        if action_num == 6:
            # rotate right
            self.rotate(direction=1)
            pass

    def rotate(self, direction):
        current_angle = self.body.angle
        # random_angle = random() * 2 * 0.0174533
        random_angle = random.random() * 15 * 0.0174533  # up to 15 degrees
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

    def move(self, direction, step_dist=1):
        step_distance = random.random() * step_dist

        # move in a direction but end within the tether distance
        # body.position.x and body.position.y can be modified, but the new position has to be within the distance of 1nm in any direction from the origin point.
        x0, y0 = self.origin_xy
        start_pos = self.body.position
        tether_radius = 1

        # the current dist from tether, starts too high because it is updated
        dist = 1000.0

        # is this a valid location?
        while dist > tether_radius and step_distance > 0:
            # will start as current pos
            x1, y1 = self.body.position

            # move in a direction the step distance
            if direction == 0:
                y1 += step_distance
            if direction == 1:
                y1 -= step_distance
            if direction == 2:
                x1 += step_distance
            if direction == 3:
                x1 -= step_distance

            # calculate the new distance from the tether point
            dist = sqrt(((x0 - x1) ** 2) + ((y0 - y1) ** 2))

            # each attempt will reduce the step distance a tiny amount
            step_distance -= 0.01

        # the new position is within the tether range, so lets assign it
        # if you didn't move at all, then you didn't move so keep your existing position
        if step_distance > 0:
            self.body.position = (x1, y1)

        # save the action so we can undo it later if needed
        self.last_action = {
            "action": "move",
            "old_value": start_pos,
            "new_value": self.body.position,
        }

    def get_thermal_movement(self):
        x = (random.random() * self.move) - self.move
        y = (random.random() * self.move) - self.move
        return (sin(x), cos(y))


    def brownian_motion(self):
        """ adjust position by brownian motion """

        x, y = self.body.position

        thermal_movement = self.get_thermal_movement()
        self.body.position = (
            x + thermal_movement[0],
            y + thermal_movement[1],
        )

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
