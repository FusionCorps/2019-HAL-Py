import logging

import pathfinder as pf
from pathfinder.followers import EncoderFollower
from wpilib.command import Command
from wpilib.timer import Timer

import robotmap
import subsystems


class ProfileFollower(Command):
    def __init__(self, file_loc="", name="none"):
        self.file_name = f"{file_loc}AutoProfile_{name}"
        super().__init__(f"{self.file_name}")
        self.logger = logging.getLogger("ProfileFollower")
        self.is_done_loading = False
        self.trajectory = []
        self.timer = Timer()

        if self.file_name == "AutoProfile_none":
            raise ValueError

        self.left, self.right, self.trajectory, self.encoder_followers, self.modifier = None, None, None, None, None

    def initialize(self):
        self.timer.reset()
        self.timer.start()

        self.logger.warning(f"File name is {self.file_name}")

        try:
            self.trajectory = pf.deserialize_csv(f"{self.file_name}")

            self.logger.warning(f"{self.file_name} Profile is starting...")
            self.modifier = pf.modifiers.TankModifier(self.trajectory).modify(robotmap.chassis_whl_diameter)

            self.left = EncoderFollower(self.modifier.getLeftTrajectory())
            self.right = EncoderFollower(self.modifier.getRightTrajectory())
            self.encoder_followers = [self.left, self.right]

            self.left.configureEncoder(
                subsystems.chassis.get_right_position(),
                robotmap.chassis_encoder_counts_per_rev,
                robotmap.chassis_whl_diameter,
            )
            self.right.configureEncoder(
                -subsystems.chassis.get_left_position(),
                -robotmap.chassis_encoder_counts_per_rev,
                robotmap.chassis_whl_diameter,
            )

            for follower in self.encoder_followers:
                follower.configurePIDVA(0.9, 0.0, 0.0, (1 / robotmap.chassis_max_vel), 0)

            self.logger.warning("Profile Initialized.")
        except FileNotFoundError as e:
            self.logger.error(f"File not found! {e}")
        except IOError as e:
            self.logger.error(f"An I/O error occurred while loading the profile: {e}")

    def execute(self):
        try:
            heading = subsystems.chassis.gyro.getAngle()

            output_l = self.left.calculate(-subsystems.chassis.get_left_position())
            output_r = self.right.calculate(subsystems.chassis.get_right_position())

            heading_target = pf.r2d(self.left.getHeading())
            heading_diff = pf.boundHalfDegrees(heading_target - heading)
            turn_output = 0.8 * (-1.0 / 80.0) * heading_diff

            subsystems.chassis.set_left(output_l + turn_output)
            subsystems.chassis.set_right(output_r - turn_output)

            if self.timer.hasPeriodPassed(2):
                self.logger.warning(f"Left output is {round(output_l, 2): ^4}. Right output is {round(output_r,
                                                                                                      2): ^4}. Turn
                output is {round(
                    turn_output, 2): ^4}")
        except AttributeError as e:
            self.logger.error(f"Error while executing! {e}")

    def isFinished(self):
        try:
            return self.left.isFinished() and self.right.isFinished()
        except AttributeError as e:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        if self.left is not None and self.right is not None:
            self.left.reset()
            self.right.reset()
        self.timer.stop()
        self.logger.info("Profile ending.")
