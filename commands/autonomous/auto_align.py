import logging
from math import atan2, cos, radians, sin, tan

import pathfinder as pf
from networktables import NetworkTablesInstance
from pathfinder import modifiers
from pathfinder.followers import EncoderFollower
from wpilib.command import Command

import robotmap
import subsystems


class AutoAlign(Command):
    def __init__(self, target):
        super().__init__("AutoAlign")
        self.requires(subsystems._chassis)
        self.target = target

        self.nt = NetworkTablesInstance().getTable("limelight")

        self.k_aim = robotmap.k_aim
        self.k_distance = robotmap.k_distance
        self.min_aim_command = robotmap.min_aim_command
        self.logger = logging.getLogger("Automatic Alignment")

    # Get normalized x pixel values from resolution
    def getNX(self, xPixel):
        return (1 / robotmap.limelight_x_res) * (
            xPixel - (robotmap.limelight_x_res - 0.5)
        )

    # Get normalized y pixel values from resolution
    def getNY(self, yPixel):
        return (1 / robotmap.limelight_y_res) * (
            yPixel - (robotmap.limelight_y_res - 0.5)
        )

    # Get virtual plane width with imaginary distance of 1
    def getVPW(self, horiz_fov):
        return 2 * tan(horiz_fov / 2)

    # Get virtual plane height
    def getVPH(self, vert_fov):
        return 2 * tan(vert_fov / 2)

    def getVPX(self, vpw, nx):
        return (vpw / 2) * nx

    def getVPY(self, vpy, ny):
        return (vpy / 2) * ny

    def getAngle(self, vpa):
        return atan2(1, vpa)

    # Needs to calculate angle from target center pixel values
    def initialize(self):
        tv = self.nt.getNumber("tv")
        tx = self.nt.getNumber("tx")
        ty = self.nt.getNumber("ty")

        distance = subsystems._chassis.sonar.getDistanceUnits()

        angle = self.getAngle(
            self.getVPX(self.getVPW(robotmap.limelight_x_fov), self.getNX(tx))
        )

        # Waypoint values converted to meters
        drive_x = sin(angle) * (distance * 1000)
        drive_y = cos(angle) * (distance * 1000)

        self.logger.info("Angle to target in radians is " + str(angle))

        points = [pf.Waypoint[0, 0, 0], pf.Waypoint[drive_x, drive_y, angle]]

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
        heading = subsystems._chassis.gyro.getAngle()
        output_L = self.left.calculate(
            subsystems._chassis._talon_FL.getQuadraturePosition()
        )
        output_R = self.right.calculate(
            subsystems._chassis._talon_FR.getQuadraturePosition()
        )
        heading_target = pf.r2d(self.left.getHeading())
        heading_diff = pf.boundHalfDegrees(heading_target - heading)
        turn_output = robotmap.spd_chassis_rotate * (-1 / 80)

    def isFinished(self):
        pass

    def end(self):
        pass

    def interrupted(self):
        self.end()
