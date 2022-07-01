from src.grana_model.simulationenv import SimulationEnvironment
from src.grana_model.attractionhandler import AttractionHandler
from src.grana_model.spawner import Spawner
from src.grana_model.objectdata import ObjectData
import pymunk

REPS = 10000

def main():

    for i in range(0, REPS):
        attraction_handler = AttractionHandler()
        space = pymunk.Space()
        batch = None
        object_data = ObjectData(pos_csv_filename="082620_SEM_final_coordinates.csv")

        spawner = Spawner(
            object_data=object_data,
            spawn_type=3,
            # 0: "psii_secondary_noparticles",
            # 1: spawn_type="psii_only",
            # 2: spawn_type="full",
            # 3: LHCII only
            shape_type="simple",
            space=space,
            batch=batch,
            num_particles=0,
            num_psii=0,
            num_lhcii=1,
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
        )

        print(f"run {i}/{REPS}")
        env.run()


if __name__ == "__main__":
    main()
