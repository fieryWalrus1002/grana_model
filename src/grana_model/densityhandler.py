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
