import argparse
import ast
import logging
import os

import hal
import pathfinder as pf


class Generator(object):
    """Creates trajectory csv files to be used by the executing MotionProfile program."""

    def __init__(self):
        self.logger = logging.getLogger("ProfileGenerator")
        self.logger.setLevel(level=logging.DEBUG)

        # Trajectory generation conditions (all units SI)
        if not hal.isSimulation():
            import robotmap

            self.conditions = {
                'name': "",
                'v': robotmap.chassis_max_vel,
                'a': robotmap.chassis_max_acceleration,
                'j': robotmap.chassis_max_jerk,
                'deploy': False
                }
        else:
            self.conditions = {
                'name': "",
                'v': 5.2,
                'a': 1.0,
                'j': 1.0,
                'deploy': False
                }

    def generate(self, *args, **kwargs):
        self.logger.info(f"ProfileGenerator called with args: {args}. Called with kwargs: {kwargs}.")

        self.conditions['name'] = f"{str(args).strip(' ')}"

        # Updates conditions if changed in kwargs
        for key, value in kwargs.items():
            self.conditions[key] = value

        for fname in os.listdir('./trajectories/'):
            if fname == f"AutoProfile_{self.conditions['name']}":
                os.remove(f"./trajectories/AutoProfile_{self.conditions['name']}")
                self.logger.warning(f"Removed duplicate trajectory '{self.conditions['name']}.'")

        points = [pf.Waypoint(loc[0], loc[1], loc[2]) for loc in args]
        print("Generating trajectory.", end="\r")

        try:
            info, trajectory = pf.generate(points,
                                           pf.FIT_HERMITE_CUBIC,
                                           pf.SAMPLES_HIGH,
                                           0.02,
                                           self.conditions['v'],
                                           self.conditions['a'],
                                           self.conditions['j'])
        except ValueError as e:
            self.logger.error(f"Trajectory generation failed! {e}")
        else:
            print("\rTrajectory generated.", end="\r")
            print("\rSerializing trajectory...", end="\r")
            pf.serialize_csv(f"trajectories/AutoProfile_{self.conditions['name']}", trajectory)
            print("\rSerialized trajectory.", end="\r")
            print("\rDone.                           ")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='CLI args for Generator')
    gen = Generator()

    for cond_name in gen.conditions.keys():
        ty = type(gen.conditions[cond_name])
        ap.add_argument(f"--{cond_name}", dest=cond_name, default=gen.conditions[cond_name], help='', type=ty)
    ap.add_argument("--args", nargs="+", dest="args", default="none")

    parsed_args = ap.parse_args()
    point_args = (ast.literal_eval(arg) for arg in parsed_args.args)
    condition_args = dict([(key, value) for key, value in vars(parsed_args).items() if not key == "args"])

    gen.generate(*point_args, **condition_args)
