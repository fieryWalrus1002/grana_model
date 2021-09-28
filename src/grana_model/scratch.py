import os
import glob
from pyglet import image
import pickle


class TestClass:
    def __init__(self):

        self.res_path = "src/grana_model/res/"
        self.object_colors_dict = {
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

    def __load_pickled_coordinates(self, obj_type, shape_type):
        if shape_type == "compound":
            export_coordinates = pickle.load(
                open(
                    f"{self.res_path}shapes/{obj_type}.pickle",
                    "rb",
                )
            )
        else:
            export_coordinates = pickle.load(
                open(
                    f"{self.res_path}shapes/{obj_type}_simple.pickle",
                    "rb",
                )
            )
        return export_coordinates

    def generate_object_dict(self, obj_type: str):
        obj_dict = {
            "obj_type": obj_type,
            "shapes_compound": self.__load_pickled_coordinates(
                obj_type, shape_type="compound"
            ),
            "shapes_simple": self.__load_pickled_coordinates(
                obj_type, shape_type="simple"
            ),
            "sprites": image.load(f"{self.res_path}/sprites/{obj_type}.png"),
            "color": self.object_colors_dict.get(obj_type),
        }
        return obj_dict


if __name__ == "__main__":
    test_class = TestClass()

    type_dict = {
        obj_type: test_class.generate_object_dict(obj_type)
        for obj_type in test_class.object_colors_dict.keys()
    }
