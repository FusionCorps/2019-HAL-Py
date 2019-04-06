import logging

import pathfinder as pf
from math import radians

import robotmap


class ProfileGenerator(object):
    def __init__(self):
        super(ProfileGenerator, self).__init__()
        self.logger = logging.getLogger("ProfileGenerator")
        self.logger.setLevel(level=logging.DEBUG)

    def generate(self, *args, **kwargs):
        points = []
        v, a, j, name = None, None, None, None

        self.logger.warning(f"ProfileGenerator called with args: {args}. Called with kwargs: {kwargs}.")
        for loc in args:
            # Check to make sure angle is not -0
            if loc[2] == 0:
                a = loc[2]
            else:
                a = radians(loc[2])

            # Check whether list has a first element
            if len(points) is 0:
                points.append(pf.Waypoint(loc[0], loc[1], a))
                continue

            # Append new points that are not the last point
            if len(points) > 0:
                if loc == points[len(points) - 1]:
                    continue
                else:
                    points.append(pf.Waypoint(loc[0], loc[1], a))

        for key, value in kwargs.items():
            if key == 'name':
                if value is not None:
                    name = value
                else:
                    name = f"{str(args).strip(' ')}"
            elif key == 'v':
                if value is not None:
                    v = float(value)
                else:
                    v = robotmap.chassis_max_vel
            elif key == 'a':
                if value is not None:
                    a = float(value)
                else:
                    a = robotmap.chassis_max_acceleration
            elif key == 'j':
                if j is not None:
                    j = float(value)
                else:
                    j = robotmap.chassis_max_jerk
            else:
                continue

        self.logger.warning(f"Requested points {str(points)}.")

        try:
            info, trajectory = pf.generate(
                points,
                pf.FIT_HERMITE_CUBIC,
                pf.SAMPLES_HIGH,
                0.05,
                v,
                a,
                j,
            )

            self.logger.warning("Trajectory generated.")

            pf.serialize_csv(f"AutoProfile_{name}", trajectory)

            self.logger.warning("Trajectory saved.")
        except ValueError as e:
            self.logger.error(f"Trajectory generation failed! {e}")
