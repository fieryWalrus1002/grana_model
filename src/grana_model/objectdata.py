from typing import Any, Iterator
import pandas as pd
from random import random
from pyglet import image

from math import pi

import numpy as np

import pickle


# @dataclass
# class ObjectDataCollection:
#     """represents an object, holding information for shape coordinates, name, angles, sprites etc.
#     that you need for object instatiatiion in the spawner module"""
#     obj_type: str
#     pos_xy: list

#         "pos_xy": list,  # [x, y] coordinates
#         "angle": float, # angle in radians
#         "sprite": ImageData object, a spirte for the object type
#         "color": (0,0,0,255) RGBA color tuple
#         "shapes_simple": list of str, # has the file paths for importing simple shapes,
#         "shapes_compound": list of str, # has the file paths for importing compound shapes}
#         }
#         The list
#     pass


class ObjectData:
    """This data structure"""

    def __init__(self, pos_csv_filename: str, spawn_seed=0):
        self.__object_colors_dict = {
            "LHCII": (0, 51, 0, 255),  # darkest green
            "LHCII_monomer": (0, 75, 0, 255),  # darkest green
            "C2S2M2": (0, 102, 0, 255),
            "C2S2M": (0, 153, 0, 255),
            "C2S2": (102, 204, 0, 255),
            "C2": (128, 255, 0, 255),
            "C1": (178, 255, 102, 255),  # lightest green
            "CP43": (178, 255, 103, 255),  # same coordinates as C1, same color
            "cytb6f": (51, 153, 255, 255),  # light blue
        }
        self.res_path = "src/grana_model/res/"
        self.type_dict = {
            obj_type: self.__generate_object_dict(obj_type)
            for obj_type in self.__object_colors_dict.keys()
        }

        self.pos_list = self.__import_pos_data(
            f"{self.res_path}/grana_coordinates/{pos_csv_filename}"
        )

        self.object_list = self.__generate_object_list(
            pos_list=self.pos_list,
            type_dict=self.type_dict,
            spawn_seed=spawn_seed,
        )

    def __generate_object_dict(self, obj_type: str):
        obj_dict = {
            "obj_type": obj_type,
            "shapes_compound": self.__load_pickled_coordinates(
                obj_type, shape_type="compound"
            ),
            "shapes_simple": self.__load_pickled_coordinates(
                obj_type, shape_type="simple"
            ),
            "sprite": image.load(f"{self.res_path}/sprites/{obj_type}.png"),
            "color": self.__object_colors_dict[obj_type],
        }
        return obj_dict

    def __import_pos_data(self, file_path):
        """Imports the (x, y) positions from the csv data file provided in filename"""
        imported_csv = pd.read_csv(file_path)
        return pd.DataFrame(imported_csv, columns=["x", "y"]).values.tolist()

    def __load_pickled_coordinates(self, obj_type, shape_type):
        if shape_type == "compound":
            with open(f"{self.res_path}shapes/{obj_type}.pickle", "rb") as f:
                export_coordinates = pickle.load(f)
        else:
            with open(
                f"{self.res_path}shapes/{obj_type}_simple.pickle", "rb"
            ) as f:
                export_coordinates = pickle.load(f)

        return export_coordinates

        #     "obj_type": "cytb6f",
        #     "shapes_simple": glob.glob(
        #         shapes_path + "14092021_1242_cytb6f" + "*.csv"
        #     ),
        #     "shapes_compound":
        #     "sprite": image.load(os.path.join(sprite_path, "lhcii.png")),
        #     "color": (51, 153, 255, 255),
        # pass

    def __generate_object_list(
        self,
        pos_list: list[tuple[float, float]],
        type_dict: dict[Any, Any],
        spawn_seed=0,
    ) -> Iterator[Any]:
        """
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
        """
        obj_list = []
        structure_types = ["C2S2M2", "C2S2M", "C2S2", "C2", "C1", "CP43"]
        structure_p = [0.57, 0.17, 0.12, 0.09, 0.03, 0.02]

        if spawn_seed == 0:
            rng = np.random.default_rng()
        else:
            rng = np.random.default_rng(spawn_seed)

        obj_types = rng.choice(
            structure_types, len(self.pos_list), replace=True, p=structure_p
        )

        for pos, obj_type in zip(pos_list, obj_types):
            obj_entry = {
                "obj_type": obj_type,
                "pos": pos,
                "angle": (2 * pi * random()),
                "sprite": type_dict[obj_type]["sprite"],
                "color": type_dict[obj_type]["color"],
                "shapes_simple": type_dict[obj_type]["shapes_simple"],
                "shapes_compound": type_dict[obj_type]["shapes_compound"],
            }

            obj_list.append(obj_entry)

        return iter(obj_list)

    # def convert_shape_csv_to_shape_list(self, obj_dict):
    #     return [
    #         pd.read_csv(file).values.tolist()
    #         for file in obj_dict["shapes_simple"]
    #     ]


if __name__ == "__main__":

    obj_data = ObjectData(pos_csv_filename="082620_SEM_final_coordinates.csv")
    type_dict = obj_data.type_dict

    # for obj_type in type_dict.keys():
    #     # for shape in type_dict[obj_type]["shapes_compound"]:
    #     #     for pos in shape:
    #     #         print(pos)

    #     # pickle this shit
    #     pickleit = obj_data.convert_shape_csv_to_shape_list(type_dict[obj_type])
    #     pickle_name = obj_type + "_simple.pickle"
    #     pickle.dump(pickleit, open(pickle_name, "wb"))

    # obj_data_dict = {
    #     {
    #         "obj_type": obj_type,
    #         "coordinates": obj_data.convert_shape_csv_to_shape_list(
    #             type_dict[obj_type]
    #         ),
    #     }
    #     for obj_type in type_dict.keys()
    # }

    # obj_dict = {
    #     {
    #         "obj_type": obj_type,
    #         "coordinates": obj_data.convert_shape_csv_to_shape_list(
    #             type_dict[obj_type]["shapes_compound"]
    #         ),
    #     }
    #     for obj_type in type_dict.keys()
    # }
