from typing import Any, Iterator
import pandas as pd
from random import random
from pyglet import image
import os
from math import pi
import glob
import numpy as np


class ObjectData:
    '''This data structure represents the object coordinates, object types, object color attributes, and object angles that are used in psii_structure
    instatiation.'''
    def __init__(self,
                 pos_csv_filename: str,
                 spawn_seed=0,
                 pos_csv_path='src/grana_model/res/grana_coordinates/',
                 sprite_path='src/grana_model/res/sprites/',
                 shapes_path='src\\grana_model\\res\\compound_shapes\\'):
        self.type_dict = {"LHCII": {
                              "obj_type": "LHCII",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1542_LHCII" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1703_LHCII" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'lhcii.png')),
                              "color": (0, 51, 0, 255)},
                          "LHCII_monomer": {
                              "obj_type": "LHCII_monomer",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1542_LHCII-monomer" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1718_LHCII-monomer" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'lhcii_monomer.png')),
                              "color": (0, 75, 0, 255)},
                          "C2S2M2":  {
                              "obj_type": "C2S2M2",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1545_C2S2M2" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1338_C2S2M2" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'c2s2m2.png')),
                              "color": (0, 102, 0, 255)},
                          "C2S2M":  {
                              "obj_type": "C2S2M",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1540_C2S2M" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1615_C2S2M" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'c2s2m.png')),
                              "color": (0, 153, 0, 255)},
                          "C2S2": {
                              "obj_type": "C2S2",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1547_C2S2" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1619_C2S2" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'c2s2.png')),
                              "color": (102, 204, 0, 255)},
                          "C2":  {
                              "obj_type": "C2",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1541_C2" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1631_C2" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'c2.png')),
                              "color": (128, 255, 0, 255)},
                          "C1":  {
                              "obj_type": "C1",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1542_C1" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1701_C1" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'c1.png')),
                              "color": (178, 255, 102, 255)},
                          "CP43":  {
                              "obj_type": "CP43",
                              "shapes_simple": glob.glob(shapes_path + "07092021_1542_C1" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "27082021_1701_C1" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'cp43_freecore.png')),
                              "color": (178, 255, 103, 255)},
                          "cytb6f":  {
                              "obj_type": "cytb6f",
                              "shapes_simple": glob.glob(shapes_path + "14092021_1242_cytb6f" + "*.csv"),
                              "shapes_compound": glob.glob(shapes_path + "14092021_1242_cytb6f" + "*.csv"),
                              "sprite": image.load(os.path.join(sprite_path, 'lhcii.png')),
                              "color": (51, 153, 255, 255)}
                          }

        self.pos_list = self._import_pos_data(os.path.join(pos_csv_path, pos_csv_filename))
        self.object_list = self._generate_object_list(pos_list=self.pos_list, type_dict=self.type_dict, spawn_seed=spawn_seed)

    def _import_pos_data(self, file_path):
        ''' Imports the (x, y) positions from the csv data file provided in filename'''
        imported_csv = pd.read_csv(file_path)
        return pd.DataFrame(imported_csv, columns=['x', 'y']).values.tolist()

    def _generate_object_list(self, pos_list: list[tuple[float, float]], type_dict: dict[Any, Any], spawn_seed=0) -> Iterator[Any]:
        '''
            Generates a list of dicts, each containing the data needed to create a PSII structure, in this format:
            {
            "obj_type": str,  # ex. "C2S2M2"
            "pos_xy": list,  # [x, y] coordinates
            "angle": float, # angle in radians
            "sprite": ImageData object, a spirte for the object type
            "color": (0,0,0,255) RGBA color tuple
            "shapes_simple": list of str, # has the file paths for importing simple shapes,
            "shapes_compound": list of str, # has the file paths for importing compound shapes}
            }
            The list will be an iterator object that you can use the next() function on to get the next item
        '''
        obj_list = []
        structure_types = ["C2S2M2", "C2S2M", "C2S2", "C2", "C1", "CP43"]
        structure_p = [0.57, 0.17, 0.12, 0.09, 0.03, 0.02]

        if spawn_seed == 0:
            rng = np.random.default_rng()
        else:
            rng = np.random.default_rng(spawn_seed)

        obj_types = rng.choice(structure_types, len(self.pos_list), replace=True, p=structure_p)

        for pos, obj_type in zip(pos_list, obj_types):
            obj_entry = {
                        "obj_type": obj_type,
                        "pos": pos,
                        "angle": (2 * pi * random()),
                        "sprite": type_dict[obj_type]["sprite"],
                        "color": type_dict[obj_type]["color"],
                        "shapes_simple": type_dict[obj_type]["shapes_simple"],
                        "shapes_compound": type_dict[obj_type]["shapes_compound"]}

            obj_list.append(obj_entry)

        return iter(obj_list)


if __name__ == "__main__":

    obj_data = ObjectData(pos_csv_filename='082620_SEM_final_coordinates.csv')
    for i in range(0, 10):
        print(next(obj_data.object_list))
    print("done")
