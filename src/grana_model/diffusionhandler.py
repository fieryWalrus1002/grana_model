from particle import Particle
import itertools
import numpy as np
from sklearn.utils.extmath import cartesian
import pandas as pd
import time


class DiffusionHandler:
    def __init__(self):
        self.diffusion_state = False

    def toggle_diffusion_state(self):
        if self.diffusion_state is False:
            print("diffusion_state = true")
            self.diffusion_state = True
        else:
            print("diffusion_state = false")
            self.diffusion_state = False

    def handle_diffusion(self, object_list: list[Particle]):
        if self.diffusion_state is False or len(object_list) < 1:
            return

        for object in object_list:
            object.diffusion_move(object.diffusion_distance)


class LHCIIAttractionHandler:
    """ 
    handles the calculation of attraction vectors between objects and their 
    attraction points
    
    distance_threshold : determines the maximum distance between two objects before
                        their attraction vectors will no longer possibly affect each other. 
    """

    def __init__(self, distance_threshold: float = 10.0):
        self.distance_threshold = distance_threshold
        self.points_to_draw = []

    def handle_attraction_forces(self, object_list):
        """
        get a list of all combinations of objects, and calculate the forces between 
        each of them that are within a certain distance threshold
        """

        all_combinations = itertools.combinations(object_list, 2)
        self.points_to_draw = []

        for c in all_combinations:
            o1 = c[0]
            o2 = c[1]

            # dist = self.get_distance(o1.body.position, o2.body.position)
            dist = o1.body.position.get_distance(o2.body.position)

            if dist < self.distance_threshold:
                o1_points = o1.get_attraction_points()
                o2_points = o2.get_attraction_points()

                # get sklearn cartesian product of the two lists as a dataframe
                df = pd.DataFrame(cartesian((o1_points, o2_points)))

                for p in o1_points + o2_points:
                    self.points_to_draw.append(p.get_world_coords())
                               
    def get_dots(self):
        return self.points_to_draw

    # def get_distance(self, pos1, pos2):
    #     """ return the euclidean distance between two xy positions """
    #     x0, y0 = pos1
    #     x1, y1 = pos2

    #     return np.sqrt(np.power(x0 - x1) + np.power(y0 - y1))
