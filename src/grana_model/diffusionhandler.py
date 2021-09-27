from grana_model.particle import Particle


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
