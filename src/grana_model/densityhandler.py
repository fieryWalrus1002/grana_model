from pyglet.text import Label
from math import pi
from pyglet.shapes import Circle, Rectangle


class DensityHandler:
    def __init__(self, space,  x: float = 150.0, y: float = 150.0, width: int = 100, height: int = 100):
        self.space = space
        self.num_objects = 0
        self.width = width
        self.height = height
        self.x = x
        self.y = y
     
    def draw_density_label(self, label_pos, num_objects: int = 1):

        area_text = f"subsection density({num_objects}/{self.width * self.height} nm^2) = {num_objects / (self.width * self.height)}"
        area_label = Label(
            area_text,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )
        area_label.draw()

    def draw_rectangle(self,opacity:int = 75, color:tuple = (255, 0, 0)):
        rectangle = Rectangle(self.x, self.y, self.width, self.height, color=color)
        rectangle.opacity = opacity
        rectangle.draw()

    def print_shapes_in_section(self, objects_list, section_x:float = 200.0, section_y:float = 200.0, width:float = 100.0, height:float = 100.0):
        for i, o in enumerate(objects_list):
            # get body position
            x, y = o.body.position

            for j, s in enumerate(o.shape_list):
                # get transform for shape attached to body
                x1, y1 = s.center_of_gravity

                # calculate shape position
                x2 = x + x1
                y2 = y + y1

                # is shape in section
                if section_x < x2 < section_x + width and section_y < y1 < section_y + height:
                    # print(f"s.color: {s.color}")
                    s.color = (0, 255, 0, 100)
                else:
                    s.color = (255, 0, 0, 100)
                    

                # print shape position
                print(f"{i}, {j}: {x2}, {y2}")
