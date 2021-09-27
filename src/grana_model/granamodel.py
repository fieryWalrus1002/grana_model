import pymunk
import pyglet
from grana_model.simulationtimer import SimulationTimer
from grana_model.scoreboard import Scoreboard
from grana_model.diffusionhandler import DiffusionHandler
from grana_model.collisionobserver import CollisionObserver
from grana_model.spritehandler import SpriteHandler
from grana_model.objectdata import ObjectData
from grana_model.spawner import Spawner
from grana_model.simulationwindow import SimulationWindow


def main():
    window = SimulationWindow(
        width=450,
        height=450,
        resizable=True,
        window_offset=(int(0.25 * 3440), int(0.05 * 1440)),
        batch=pyglet.graphics.Batch(),
        space=pymunk.Space(),
        spawner=Spawner(
            object_data=ObjectData(
                pos_csv_filename="082620_SEM_final_coordinates.csv"
            )
        ),
        timer=SimulationTimer(),
        scoreboard=Scoreboard(),
        collision_observer=CollisionObserver(),
        diffusion_handler=DiffusionHandler(),
        sprite_handler=SpriteHandler(),
    )

    # fps_display = pyglet.window.FPSDisplay(window=window)
    pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
