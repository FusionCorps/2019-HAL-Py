import logging

import pathfinder as pf
from math import radians
from pathfinder.followers import EncoderFollower
from wpilib.command import Command

import robotmap
import subsystems


class AutoProfile(Command):
    def __init__(self, *args, **kwargs):
        super().__init__("AutoProfile")
        self.requires(subsystems.chassis)
        self.points = []
        self.left, self.right, self.trajectory, self.encoder_followers, self.modifier = None, None, None, None, None
        self.logger = logging.getLogger("AutoProfile")

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

    def initialize(self):
        self.logger.info(str(self.points))

        info, self.trajectory = pf.generate(
            self.points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            0.05,
            robotmap.chassis_max_vel,
            robotmap.chassis_max_acceleration,
            robotmap.chassis_max_jerk,
        )

        self.logger.info("Trajectory generated")

        self.modifier = pf.modifiers.TankModifier(self.trajectory).modify(0.0254)

        self.left = EncoderFollower(self.modifier.getLeftTrajectory())
        self.right = EncoderFollower(self.modifier.getRightTrajectory())
        self.encoder_followers = [self.left, self.right]

        self.left.configureEncoder(
            subsystems.chassis._talon_FL.getQuadraturePosition(),
            robotmap.chassis_encoder_counts_per_rev,
            robotmap.chassis_whl_diameter,
        )
        self.right.configureEncoder(
            subsystems.chassis._talon_FR.getQuadraturePosition(),
            robotmap.chassis_encoder_counts_per_rev,
            robotmap.chassis_whl_diameter,
        )

        for follower in self.encoder_followers:
            follower.configurePIDVA(0.9, 0.2, 0.0, (1 / robotmap.chassis_max_vel), 0)

    def execute(self):
        heading = subsystems.chassis.gyro.getAngle()

        output_L = self.left.calculate(
            subsystems.chassis._talon_FL.getQuadraturePosition()
        )
        output_R = self.right.calculate(
            subsystems.chassis._talon_FR.getQuadraturePosition()
        )
        heading_target = pf.r2d(self.left.getHeading())
        heading_diff = pf.boundHalfDegrees(heading_target - heading)
        turn_output = 0.8 * (-1.0 / 80.0) * heading_diff

        subsystems.chassis._group_L.set(-output_L + turn_output)
        subsystems.chassis._group_R.set(output_R - turn_output)

    def isFinished(self):
        return self.left.isFinished() and self.right.isFinished()

    def interrupted(self):
        self.end()

    def end(self):
        self.logger.info("Ending")
        self.left.reset()
        self.right.reset()
