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

                # save the points for drawing them in the simulation visualization space
                for p in o1_points + o2_points:
                    self.points_to_draw.append(p.get_world_coords())

                # print(f'o1.position: {o1.body.position}, o2.position: {o2.body.position}')
                for o1pt in o1_points:  
                  pt1 = o1pt.get_world_coords()
                  
                  for o2pt in o2_points:
                    pt2 = o2pt.get_world_coords()

                    
                  
                               
    def get_dots(self):
        return self.points_to_draw


    def calculate_attraction_between_objects(self, df):
        """ takes the combinations of points in a dataframe, and calculates the vectors
        of attraction between each of the points.  """
        print(df.head())



        out_df = {'1': {'p1': p1_vector, 'p2': p2_vector, 'p3': p3_vector, 's1': s1_vector, 's2': s2_vector, 's3': o1_s3_vector}}




    # def get_distance(self, pos1, pos2):
    #     """ return the euclidean distance between two xy positions """
    #     x0, y0 = pos1
    #     x1, y1 = pos2

    #     return np.sqrt(np.power(x0 - x1) + np.power(y0 - y1))
