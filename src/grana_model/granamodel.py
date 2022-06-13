import pymunk
import pyglet
from collisionhandler import CollisionHandler
from simulationtimer import SimulationTimer
from scoreboard import Scoreboard
from diffusionhandler import DiffusionHandler
from spritehandler import SpriteHandler
from objectdata import ObjectData
from spawner import Spawner

# from grana_model.scale_test import Spawner
from simulationwindow import SimulationWindow


def main():
    my_space = pymunk.Space()
    my_batch = pyglet.graphics.Batch()
    my_spawner = Spawner(
        object_data=ObjectData(
            pos_csv_filename="082620_SEM_final_coordinates.csv"
        ),
        spawn_type="psii_secondary_noparticles",
        # spawn_type="psii_only",
        # spawn_type="full",
        shape_type="complex",
        space=my_space,
        batch=my_batch,
        num_particles=0,
        num_psii=200,
    )
    collision_handler = CollisionHandler(
        my_space
    )  # has some custom collision callbacks

    window = SimulationWindow(
        width=425,
        height=475,
        resizable=True,
        window_offset=(int(0.25 * 3440), int(0.05 * 1440)),
        batch=my_batch,
        space=my_space,
        spawner=my_spawner,
        timer=SimulationTimer(),
        scoreboard=Scoreboard(),
        diffusion_handler=DiffusionHandler(),
        sprite_handler=SpriteHandler(),
        collision_handler=collision_handler,
    )

    # fps_display = pyglet.window.FPSDisplay(window=window)
    pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
