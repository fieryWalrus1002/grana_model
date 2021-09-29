import pymunk
import pyglet
from grana_model.collisionhandler import CollisionHandler
from grana_model.simulationtimer import SimulationTimer
from grana_model.scoreboard import Scoreboard
from grana_model.diffusionhandler import DiffusionHandler
from grana_model.collisionobserver import CollisionObserver
from grana_model.spritehandler import SpriteHandler
from grana_model.objectdata import ObjectData
from grana_model.spawner import Spawner
from grana_model.simulationwindow import SimulationWindow


def main():
    my_space = pymunk.Space()
    my_batch = pyglet.graphics.Batch()
    my_spawner = Spawner(
        object_data=ObjectData(
            pos_csv_filename="082620_SEM_final_coordinates.csv"
        ),
        spawn_type="psii_only",
        shape_type="simple",
        space=my_space,
        batch=my_batch,
    )
    collision_handler = CollisionHandler(my_space)

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
