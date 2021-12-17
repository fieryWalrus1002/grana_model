import pymunk
import pyglet
import argparse

from grana_model.simulationtimer import SimulationTimer
from grana_model.scoreboard import Scoreboard
from grana_model.spritehandler import SpriteHandler

from grana_model.objectdata import ObjectData, ObjectDataExistingData

from grana_model.spawner import Spawner

from grana_model.simulationwindow import SimulationWindow
from grana_model.simulationenv import SimulationEnvironment
from pathlib import Path


def main(filename: str, object_data_exists: bool):
    """main function, creates simulation window, sim environment, etc"""
    sim_env = SimulationEnvironment(
        pos_csv_filename=filename,
        object_data_exists=object_data_exists,
    )

    window = SimulationWindow(
        width=600,
        height=600,
        sim_env=sim_env,
        window_offset=(int(0.25 * 3440), int(0.05 * 1440)),
        timer=SimulationTimer(),
        scoreboard=Scoreboard(),
        sprite_handler=SpriteHandler(),
    )

    pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)

    pyglet.app.run()


if __name__ == "__main__":
    print(Path.cwd())
    parser = argparse.ArgumentParser(description="launches a grana simulation")

    parser.add_argument(
        "-filename",
        help="filename of csv position datafile in res/grana_coordinates/",
        type=str,
        default="01112021_182946_jobid_1_step_88_overlap_0_data.csv",
    )

    parser.add_argument(
        "-object_data_exists",
        help="object data exists. False: generate new object types for XY coordinates. True: load xy, object type, angle from datafile",
        type=bool,
        default=True,
    )

    args = parser.parse_args()

    main(**vars(args))
