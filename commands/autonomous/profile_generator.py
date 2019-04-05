import logging
import pickle

import pathfinder as pf
from math import radians


class ProfileGenerator(object):
    def __init__(self, *args, **kwargs):
        super(ProfileGenerator, self).__init__()
        self.logger = logging.getLogger("ProfileGenerator")
        self.points = []
        self.left, self.right = None, None
        self.v_max, self.a_max, self.j_max, self.name = None, None, None, None

        for loc in args:
            # Check to make sure angle is not -0
            if loc[2] is 0:
                a = loc[2]
            else:
                a = radians(loc[2])

            # Check whether list has a first element
            if len(self.points) is 0:
                self.points.append(pf.Waypoint(loc[0], loc[1], a))
                continue

            # Append new points that are not the last point
            if len(self.points) > 0:
                if loc == self.points[len(self.points) - 1]:
                    continue
                else:
                    self.points.append(pf.Waypoint(loc[0], loc[1], a))

        for key, value in kwargs:
            if key == 'name':
                self.name = value
            elif key == 'v_max':
                self.v_max = value
            elif key == 'a_max':
                self.a_max = value
            elif key == 'j_max':
                self.j_max = value
            else:
                continue

        if self.name is None:
            self.name = f"{str(args)}"
        if self.v_max is None:
            self.v_max = 5000
        if self.a_max is None:
            self.a_max = 1000
        if self.j_max is None:
            self.j_max = 500

    def generate(self):
        self.logger.error(f"Requested points {str(self.points)}")

        info, trajectory = pf.generate(
            self.points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            0.05,
            self.v_max,
            self.a_max,
            self.j_max,
        )

        self.logger.error("Trajectory generated")

        with open(f"AutoProfile_{self.name}", "wb") as f:
            pickle.dump(trajectory, f)
