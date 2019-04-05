import logging
import pickle

import pathfinder as pf
from pathfinder.followers import EncoderFollower
from wpilib.command import Command

import robotmap
import subsystems


class ProfileFollower(Command):
    def __init__(self, file_name="none"):
        self.file_name = f"AutoProfile_{file_name}"
        super().__init__(f"{self.file_name}")

        if self.file_name == "AutoProfile_none":
            raise ValueError

        with open(f"{self.file_name}", "rb") as f:
            self.trajectory = pickle.load(f)
        self.left, self.right, self.trajectory, self.encoder_followers, self.modifier = None, None, None, None, None
        self.logger = logging.getLogger("ProfileFollower")

    def initialize(self):
        self.logger.warning(f"{self.file_name} is starting...")
        self.modifier = pf.modifiers.TankModifier(self.trajectory).modify(0.0254)

        self.left = EncoderFollower(self.modifier.getLeftTrajectory())
        self.right = EncoderFollower(self.modifier.getRightTrajectory())
        self.encoder_followers = [self.left, self.right]

        self.left.configureEncoder(
            subsystems.chassis.get_right_position(),
            robotmap.chassis_encoder_counts_per_rev,
            robotmap.chassis_whl_diameter,
        )
        self.right.configureEncoder(
            subsystems.chassis.get_left_position(),
            robotmap.chassis_encoder_counts_per_rev,
            robotmap.chassis_whl_diameter,
        )

        for follower in self.encoder_followers:
            follower.configurePIDVA(0.9, 0.0, 0.0, (1 / robotmap.chassis_max_vel), 0)

    def execute(self):
        heading = subsystems.chassis.gyro.getAngle()

        output_l = self.left.calculate(subsystems.chassis.get_left_position())
        output_r = self.right.calculate(subsystems.chassis.get_right_position())

        heading_target = pf.r2d(self.left.getHeading())
        heading_diff = pf.boundHalfDegrees(heading_target - heading)
        turn_output = 0.8 * (-1.0 / 80.0) * heading_diff

        subsystems.chassis.set_left(output_l + turn_output)
        subsystems.chassis.set_right(output_r - turn_output)

    def isFinished(self):
        return self.left.isFinished() and self.right.isFinished()

    def interrupted(self):
        self.end()

    def end(self):
        self.left.reset()
        self.right.reset()
        self.logger.info(f"{self.file_name} is ending.")
