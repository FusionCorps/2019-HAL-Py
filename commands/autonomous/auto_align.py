import logging
from math import atan2, cos, radians, sin, tan

import pathfinder as pf
from networktables import NetworkTables
from pathfinder import modifiers
from pathfinder.followers import EncoderFollower
from wpilib import Ultrasonic
from wpilib.command import Command

import robotmap
import subsystems


class AutoAlign(Command):
    def __init__(self, target):
        super().__init__("AutoAlign")
        self.requires(subsystems._chassis)
        self.target = target

        self.nt = NetworkTables.getTable("limelight")

        self.k_aim = robotmap.k_aim
        self.k_distance = robotmap.k_distance
        self.min_aim_command = robotmap.min_aim_command

        self.logger = logging.getLogger("Automatic Alignment")

    # # Get normalized x pixel values from resolution
    # def getNX(self, xPixel):
    #     return (1 / robotmap.limelight_x_res) * (
    #         xPixel - (robotmap.limelight_x_res - 0.5)
    #     )

    # # Get normalized y pixel values from resolution
    # def getNY(self, yPixel):
    #     return (1 / robotmap.limelight_y_res) * (
    #         yPixel - (robotmap.limelight_y_res - 0.5)
    #     )

    # # Get virtual plane width with imaginary distance of 1
    # def getVPW(self, horiz_fov):
    #     return 2 * tan(horiz_fov / 2)

    # # Get virtual plane height
    # def getVPH(self, vert_fov):
    #     return 2 * tan(vert_fov / 2)

    # def getVPX(self, vpw, nx):
    #     return (vpw / 2) * nx

    # def getVPY(self, vpy, ny):
    #     return (vpy / 2) * ny

    # def getAngle(self, vpa):
    #     return atan2(1, vpa)

    def initialize(self):
        subsystems._chassis.sonar.setDistanceUnits(Ultrasonic.Unit.kMillimeters)
        tv = self.nt.getNumber("tv", 0)

        if tv is 0.0:
            self.end()
        else:
            pass

        tx = self.nt.getNumber("tx", 0)
        ty = self.nt.getNumber("ty", 0)
        ta = self.nt.getNumber("ta", 0)
        camtran = self.nt.getNumberArray("camtran", 0)

        distance = subsystems._chassis.sonar.getDistanceUnits()
        drive_x = sin(tx) * distance

        self.logger.info("Angle to target in radians is " + str(tx))
        points = [pf.Waypoint(0, -drive_x, -tx), pf.Waypoint(0, 0, 0)]

        info, trajectory = pf.generate(
            points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=0.05,
            max_velocity=robotmap.max_vel,
            max_acceleration=robotmap.max_accel,
            max_jerk=robotmap.max_jerk,
        )

        self.modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

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
        if robotmap.control_mode == 0:
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
        else:
            pass

    def isFinished(self):
        return self.left.isFinished() and self.right.isFinished()

    def end(self):
        pass

    def interrupted(self):
        self.end()
