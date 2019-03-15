import pathfinder as pf
from pathfinder.followers import EncoderFollower
from wpilib.command import Command

import robotmap
import subsystems


class AutoProfile(Command):
    def __init__(self, starting_loc, target_loc=(0, 0, 0)):
        super().__init__("AutoProfile" + str(starting_loc) + " " + str(target_loc))
        self.requires(subsystems._chassis)
        self.starting_loc = starting_loc
        self.target_loc = target_loc

    def initialize(self):
        points = [
            pf.Waypoint(-self.target_loc[0], -self.target_loc[1], self.target_loc[2]),
            pf.Waypoint(0, 0, 0),
        ]

        self.info, self.trajectory = pf.generate(
            points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=0.05,
            max_velocity=robotmap.max_vel,
            max_acceleration=robotmap.max_accel,
            max_jerk=robotmap.max_jerk,
        )

        self.modifier = pf.modifiers.TankModifier(self.trajectory).modify(0.5)

        self.left = EncoderFollower(self.modifier.getLeftTrajectory())
        self.right = EncoderFollower(self.modifier.getRightTrajectory())
        self.encoder_followers = [self.left, self.right]

        self.left.configureEncoder(
            subsystems._chassis._talon_FL.getQuadraturePosition(),
            robotmap.encoder_counts_per_rev,
            robotmap.whl_diameter,
        )
        self.right.configureEncoder(
            subsystems._chassis._talon_FR.getQuadraturePosition(),
            robotmap.encoder_counts_per_rev,
            robotmap.whl_diameter,
        )

        for follower in self.encoder_followers:
            follower.configurePIDVA(1.0, 0.0, 0.0, (1 / robotmap.max_vel), 0)

    def execute(self):
        heading = subsystems._chassis.gyro.getAngle()
        output_L = self.left.calculate(
            subsystems._chassis._talon_FL.getQuadraturePosition()
        )
        output_R = self.right.calculate(
            subsystems._chassis._talon_FR.getQuadraturePosition()
        )
        heading_target = pf.r2d(self.left.getHeading())
        heading_diff = pf.boundHalfDegrees(heading_target - heading)
        turn_output = 0.8 * (-1.0 / 80.0) * heading_diff

        subsystems._chassis._group_L.set(output_L + turn_output)
        subsystems._chassis._group_R.set(output_R - turn_output)

    def isFinished(self):
        return self.left.isFinished() and self.right.isFinished()

    def interrupted(self):
        self.end()

    def end(self):
        self.left.reset()
        self.right.reset()
