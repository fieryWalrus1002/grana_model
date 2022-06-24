import pyglet
from math import degrees, sqrt
import random
from pymunk import Vec2d, Body, moment_for_circle, Poly, Space
import os
from pathlib import Path
from math import cos, sin, pi
from abc import ABC, abstractmethod
import numpy as np


class DistanceMagnitude(ABC):
    def __init__(self, threshold: float = 10.0):
        self.threshold = threshold

    @abstractmethod
    def get_distance_scalar(self, distance):
        """takes a distance and returns a vector scaled according to a particular algorithm"""
        return 0


class WellMagnitude(DistanceMagnitude):
    def get_distance_scalar(self, distance):
        """if distance is greater than a threshold, it returns 0. otherwise, 1."""
        if distance > self.threshold:
            return 0
        else:
            return 1


class AttractionPoint:
    """class to store values for attraction point variables.
    parent: the parent object. we reference it when we assign vectors.
    type = 'point', 'side'
    distance_scalar: the chosen method for scaling vectors by distance
    """

    def __init__(
        self,
        parent,
        type: int,
        distance_scalar: DistanceMagnitude,
        offset_coords: tuple,
        batch,
    ):
        self.parent = parent
        self.distance_scalar = distance_scalar.get_distance_scalar
        self.type = type
        self.offset_coords = offset_coords
        self.batch = batch

    def get_world_coords(self):
        """TODO: verify they are being rotated"""
        x, y = self.offset_coords

        return self.parent.body.position + Vec2d(x, y).rotated(self.parent.body.angle)

    def calc_vector(self, v2):
        """TODO: write code to calculate attraction vector between these two points, and return the vector"""
        v1 = self.get_world_coords()
        
        # vector between the two points
        vm = v2 - v1

        # magnitude of that vector
        v_mag =  np.sqrt(np.power(0.01 - vm[0], 2) + np.power(0.01 - vm[1], 2)).astype(
            np.float
        )

        v_inv = v1 - v2

        v3 = np.divide(v_inv, v_mag)

        return Vec2d(v3[0], v3[1])


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
        move: float = 1,
        move_factor: float = 25.0
    ):
        self.vector_list = (
            []
        )  # holds vectors that will be used to calculate movement force
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
        self.move_factor = move_factor

        self.body = self._create_body(mass=mass, angle=angle)

        shape_list, shape_str = self._create_shape_string(shape_type=shape_type)
        eval(shape_str)

        self.shape_list = shape_list

        if use_sprites:
            self._assign_sprite(batch=batch)

        self.attraction_points = {
            "p1": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="point",
                offset_coords=(3.92, 1.26),
                batch=batch,
            ),
            "p2": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="point",
                offset_coords=(-3.13, 3.06),
                batch=batch,
            ),
            "p3": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="point",
                offset_coords=(-0.97, -4.24),
                batch=batch,
            ),
            "s1": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="side",
                offset_coords=(0.68, 3.02),
                batch=batch,
            ),
            "s2": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="side",
                offset_coords=(-3.17, -1.08),
                batch=batch,
            ),
            "s3": AttractionPoint(
                parent=self,
                distance_scalar=WellMagnitude(),
                type="side",
                offset_coords=(2.3, -1.98),
                batch=batch,
            ),
        }




    def vec_mag(self, v1: Vec2d, v2: Vec2d):
        """ take two vectors and calculate the magnitude of the vector between them"""
        return np.sqrt(np.power(v1[0] - v2[0], 2) + np.power(v1[1] - v2[1], 2)).astype(
            np.float
        )

    def vec_norm(self, v1: Vec2d, v2: Vec2d):
        """ return unit vector between v1 and v2 and magnitude"""
        vm = v2 - v1
        mag = self.vec_mag(np.array([0.01, 0.01]), vm)
        v1 = v1 - v2
        v3 = np.divide(v1, mag)
        return v3, mag

    def get_thermal_movement(self) -> Vec2d:
        """generate random vector for thermal movement"""
        x = random.random() * self.move
        y = random.random() * self.move

        return Vec2d(np.sin(x), np.cos(y))

    def apply_vectors(self) -> None:
        
        # get sum of all vectors in vector_list
        vec_sum = Vec2d(0, 0)
        
        for v in self.vector_list:
            vec_sum += v

        # use vec_sum to create a unit vector scaled by a self.move_factor
        v_force, _ = self.vec_norm(vec_sum, Vec2d(0, 0))

        v_force = Vec2d(v_force[0] * self.move_factor, v_force[1] * self.move_factor)
        
        # calculate thermal movement
        thermal_movement = self.get_thermal_movement()

        v_force += thermal_movement

        print(v_force)
        # apply the vectors as an impulse    
        self.body.apply_impulse_at_local_point(v_force)
        
        # self.body.position = (
        #     x + self.v_force[0] + thermal_movement[0],
        #     y + self.v_force[1] + thermal_movement[1],
        # )

    def get_attraction_points(self):
        """return a list of the attraction points for this structure"""
        return [p for p in self.attraction_points.values()]

    def calculate_attraction_to_object(self, other_object):
        """this function calculates the attraction forces between each attraction point
        in this object toward each attraction point in other_object, and adds them to
        this objects vector list"""

        # get all attraction points for the other object
        o2_points = other_object.get_attraction_points()

        for o1pt in self.attraction_points.values():
            # for each point in obstacle 1, get the world coordinates
            pt1 = o1pt.get_world_coords()

            # now iterate through all the attraction points in obstacle 2
            for o2pt in o2_points:

                # calculate the attraction vector from pt1 toward the other point
                v = o1pt.calc_vector(o2pt.get_world_coords())

                # append the vector to this object's vector list
                self.vector_list.append(v)

    def exchange_simple_for_complex(self):
        """remove the simple body and shapes from the space, and replace them with
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
            self._create_shape(shape_coord=shape_coord) for shape_coord in coord_list
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
            self._create_shape(shape_coord=shape_coord) for shape_coord in coord_list
        ]

        return (
            shape_list,
            f"space.add(self.body, {','.join([str(f'shape_list[{i}]') for i, shape in enumerate(shape_list)])})",
        )

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

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 1
        Body.update_velocity(body, gravity, damping, dt)
        body_velocity_length = body.velocity.length
        if body_velocity_length > max_velocity:
            scale = max_velocity / body_velocity_length
            body.velocity = body.velocity * scale

