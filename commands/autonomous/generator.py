import logging

import pathfinder as pf

import robotmap


class Generator(object):
    """Creates trajectory csv files to be used by the executing MotionProfile program."""

    def __init__(self):
        self.logger = logging.getLogger("ProfileGenerator")
        self.logger.setLevel(level=logging.DEBUG)

    # TODO Check if trajectory exists already
    def generate(self, *args, **kwargs):
        self.logger.warning(f"ProfileGenerator called with args: {args}. Called with kwargs: {kwargs}.")

        # Trajectory generation conditions (all units SI)
        conditions = {
            'name': f"{str(args).strip(' ')}",
            'v': robotmap.chassis_max_vel,
            'a': robotmap.chassis_max_acceleration,
            'j': robotmap.chassis_max_jerk,
            'deploy': False
        }

        # Updates conditions if changed in kwargs
        for key, value in kwargs.items():
            conditions.update(key=value)

        try:
            info, trajectory = pf.generate((pf.Waypoint(loc[0], loc[1], loc[2]) for loc in args),
                                           pf.FIT_HERMITE_CUBIC,
                                           pf.SAMPLES_HIGH,
                                           0.05,
                                           conditions['v'],
                                           conditions['a'],
                                           conditions['j'])
        except ValueError as e:
            self.logger.error(f"Trajectory generation failed! {e}")
        else:
            self.logger.warning("Trajectory generated.")
            pf.serialize_csv(f"AutoProfile_{conditions['name']}", trajectory)
            self.logger.warning("Trajectory saved.")
