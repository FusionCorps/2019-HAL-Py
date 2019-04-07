import logging

import pathfinder as pf
from pathfinder.followers import EncoderFollower
from wpilib.command import Command
from wpilib.timer import Timer

import robotmap
import subsystems


class ProfileGenerator(object):
    def __init__(self):
        self.logger = logging.getLogger("ProfileGenerator")
        self.logger.setLevel(level=logging.DEBUG)

    def generate(self, *args, **kwargs):
        self.logger.warning(f"ProfileGenerator called with args: {args}. Called with kwargs: {kwargs}.")
        points = [pf.Waypoint(loc[0], loc[1], loc[2]) for loc in args]
        conditions = {'name': f"{str(args).strip(' ')}", 'v': robotmap.chassis_max_vel,
                      'a': robotmap.chassis_max_acceleration, 'j': robotmap.chassis_max_jerk}
        for key, value in kwargs.items():
            conditions.update(key=value)
        self.logger.warning(f"Requested points {str(points)}.")

        try:
            info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH, 0.05, conditions.get('v'),
                                           conditions.get('a'), conditions.get('j'), )
        except ValueError as e:
            self.logger.error(f"Trajectory generation failed! {e}")
        else:
            self.logger.warning("Trajectory generated.")
            pf.serialize_csv(f"AutoProfile_{conditions.get('name')}", trajectory)
            self.logger.warning("Trajectory saved.")


class ProfileFollower(Command):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        file_loc, file_name = None, None

        for key, value in kwargs:
            file_loc = value if key == 'file_loc' else None
            file_name = value if key == 'file_name' else None
            self.generate = value if key == 'generate' else False

        self.file_name = f"{file_loc}AutoProfile_{file_name}"
        super().__init__(f"{self.file_name}:^20")
        self.requires(subsystems.chassis)
        self.logger = logging.getLogger("ProfileFollower")
        self.critical_error = False
        self.timer = Timer()

        if self.file_name == "AutoProfile_none":
            raise ValueError

        self.left, self.right, self.trajectory, self.encoder_followers, self.modifier = None, None, None, None, None

    def initialize(self):
        if self.generate:
            ProfileGenerator().generate(self.args, self.kwargs)

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
