from src.grana_model.simulationenv import SimulationEnvironment
from src.grana_model.simulationwindow import SimulationWindow
from src.grana_model.attractionhandler import AttractionHandler
from src.grana_model.spawner import Spawner
from src.grana_model.objectdata import ObjectData
from src.grana_model.densityhandler import DensityHandler
from src.grana_model.collisionhandler import CollisionHandler
import pymunk
from src.grana_model.overlapagent import OverlapAgent
import pyglet
from itertools import product

REPS = 1

# constants for sim window, if gui == True
OVERLAP_AGENT_STATE = True
GUI_STATE = False
SIM_WIDTH = 500
SIM_HEIGHT = 500
SHAPE_COMBOS = [
    f"lhcii_circle_{r}_{n}" for (r, n) in product([3.75, 4.5], range(94, 100, 20))
]
STEP_LIMIT = 500


def configure_space(threaded: bool = False, damping: float = 0.1):
    space = pymunk.Space(threaded=threaded)
    space.damping = damping
    return space


def main(
    gui: bool = False,
    shape_type: str = "simple",
    step_limit: int = STEP_LIMIT,
    use_overlap_agent: bool = False,
):
    attraction_handler = AttractionHandler(
        thermove_enabled=False, attraction_enabled=False
    )
    space = configure_space(threaded=True, damping=0.9)
    batch = None
    object_data = ObjectData(pos_csv_filename="082620_SEM_final_coordinates.csv")

    overlap_handler = CollisionHandler(space)

    densityhandler = DensityHandler(
        space=space,
        x=200,
        y=200,
        width=100,
        height=100,
    )

    spawner = Spawner(
        object_data=object_data,
        spawn_type=3,
        # 0: "psii_secondary_noparticles",
        # 1: spawn_type="psii_only",
        # 2: spawn_type="full",
        # 3: LHCII only
        # shape_type="circle_large",
        shape_type=shape_type,
        circle_radius=0.1,
        space=space,
        batch=batch,
        num_particles=0,
        num_psii=0,
        num_lhcii=200,
        section=(
            200,
            200,
            100,
            100,
        ),  # determines the section of grana that the LHCII will use for the ensemble area
        structure_dict={
            "LHCII": {
                "d": 1.8e-9,  # 1.8e-9 in cm2/s
                "d_rot": 2e3,  # 2 x 10^3  rad^2 s^(-1)
                "simulation_limit": 1000,
                "distance_scalar": "well",
                "diffusion_scalar": 1.22e3,  # average over 250 steps, gave us this number for keeping step_nm equal to calculated step
                "distance_threshold": 50.0,
                "mass": 1.0e3,
                "mass_scalar": 1.0,
                "rotation_scalar": 1.785e-3,  # average over 250 steps, gave us this number to use
                "time_per_step": 2,  # in ns
                "average_step_over": 250,
                "calibrate_rot_d": False,
                "calibrate_diff_d": False,
            }
        },
    )

    env = SimulationEnvironment(
        spawner=spawner,
        space=space,
        object_data=object_data,
        attraction_handler=attraction_handler,
        densityhandler=densityhandler,
        overlap_handler=overlap_handler,
        gui=gui,
        step_limit=step_limit,
        use_overlap_agent=use_overlap_agent,
    )

    if gui:
        window = SimulationWindow(
            width=SIM_WIDTH,
            height=SIM_HEIGHT,
            resizable=True,
            window_offset=(int(0.25 * 3440), int(0.05 * 1440)),
            timer=None,
            draw_shapes=True,
            env=env,
        )

        pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
        print("run app")
        pyglet.app.run()
        print("app done")
        window.close()

    else:
        # RUN WITH NO WINDOW
        env.run()


if __name__ == "__main__":

    if GUI_STATE == False:
        # no window, just sim environment
        for i in range(REPS):
            for j in SHAPE_COMBOS:
                print(f"starting {j}, rep {i}")
                main(
                    gui=False,
                    shape_type=j,
                    step_limit=STEP_LIMIT,
                    use_overlap_agent=OVERLAP_AGENT_STATE,
                )

    else:
        # if GUI_STATE == True, run it once with a window
        main(gui=GUI_STATE)
