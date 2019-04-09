import logging

import pathfinder as pf
from pathfinder.followers import EncoderFollower
from wpilib.command import Command
from wpilib.timer import Timer

import robotmap
import subsystems
from .generator import Generator


class ProfileFollower(Command):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("ProfileFollower")

        self.timer = Timer()  # Used to log output after certain time

        self.critical_error = False

        self.left = self.right = self.trajectory = self.encoder_followers = self.modifier = None
        file_loc, file_name, generate = None, None, None

        for key, value in kwargs:
            file_loc = value if key == 'file_loc' else None
            file_name = value if key == 'file_name' else None
            generate = value if key == 'generate' else False

        self.file_name = f"{file_loc}AutoProfile_{file_name}"
        if self.file_name == "AutoProfile_none":
            raise ValueError

        super().__init__(str(self.file_name))
        self.requires(subsystems.chassis)

        if generate:
            Generator().generate(args, kwargs)

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

            self.left.configureEncoder(
                subsystems.chassis.get_right_position(),
                robotmap.chassis_encoder_counts_per_rev,
                robotmap.chassis_whl_diameter,
            )
            self.right.configureEncoder(
                -subsystems.chassis.get_left_position(),
                robotmap.chassis_encoder_counts_per_rev,
                robotmap.chassis_whl_diameter,
            )

            self.left.configurePIDVA(0.8, 0.0, 0.0, (1 / robotmap.chassis_max_vel), 0.0)
            self.right.configurePIDVA(0.8, 0.0, 0.0, (1 / robotmap.chassis_max_vel), 0.0)

            self.logger.warning("Profile initialized!")
        except FileNotFoundError as e:
            self.logger.error(f"File not found! {e}")
            self.critical_error = True
            self.end()
        except IOError as e:
            self.logger.error(f"An I/O error occurred while loading the profile: {e}")
            self.critical_error = True
            self.end()

    def execute(self):
        if not self.critical_error:
            heading = subsystems.chassis.gyro.getAngle()

            output_l = self.left.calculate(-subsystems.chassis.get_left_position())
            output_r = self.right.calculate(subsystems.chassis.get_right_position())

            heading_target = pf.r2d(self.left.getHeading())
            heading_diff = pf.boundHalfDegrees(heading_target - heading)
            turn_output = 0.8 * (-1.0 / 80.0) * heading_diff

            subsystems.chassis.set_left((output_l - turn_output))
            subsystems.chassis.set_right((output_r - turn_output))

            if self.timer.hasPeriodPassed(1):
                self.logger.info(f"Left is {round(output_l, 2): ^4}. Right is {round(output_r, 2): ^4}."
                                 f" Turn is {round(turn_output, 2): ^4}")
        else:
            pass

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
        self.logger.info("Execution has ended!")
