import csv
import logging

from ctre import ControlMode, WPI_TalonSRX
from ctre._impl.motionprofilestatus import MotionProfileStatus
from ctre.trajectorypoint import TrajectoryPoint
from wpilib import Notifier, SmartDashboard
from wpilib.command import Command

import subsystems


class Process_Buffer:
    def run(self):
        # TODO Add time delta check for Notifier duration
        subsystems._chassis._talon_FL.processMotionProfileBuffer()
        subsystems._chassis._talon_FR.processMotionProfileBuffer()
        subsystems._chassis._talon_BL.processMotionProfileBuffer()
        subsystems._chassis._talon_BR.processMotionProfileBuffer()


class Auton_Profile(Command):
    def __init__(self, trajectory_name_prefix):
        super().__init__("Auton_Profile " + trajectory_name_prefix)
        self.requires(subsystems._chassis)
        self.logger = logging.getLogger("Auton_Profile")

        # Speed Controllers
        self._talon_FL = subsystems._chassis._talon_FL
        self._talon_FR = subsystems._chassis._talon_FR
        self._talon_BL = subsystems._chassis._talon_BL
        self._talon_BR = subsystems._chassis._talon_BR
        self._talons = [self._talon_FL, self._talon_FR, self._talon_BL, self._talon_BR]
        self.logger.info("Talons constructed")

        # Change Motion Control Frame Period for all Talons
        for talon in self._talons:
            talon.changeMotionControlFramePeriod(5)
        self.logger.info("Talon motionControlFramePeriod changed")

        # Control variables
        self._state = 0
        self._loop_timeout = -1
        self.start = False
        self.k_min_points_talon = 5
        self.k_num_loops_timeout = 10

        # Trajectory .csv file names
        self.trajectory_L_name = trajectory_name_prefix + "_left"
        self.trajectory_R_name = trajectory_name_prefix + "_right"

        self.csv_points1 = []
        self.csv_points2 = []

        # Periodically runs processMotionProfileBuffer
        self.notifier = Notifier(Process_Buffer().run())
        self.notifier.startPeriodic(0.005)
        self.logger.info("Notifier started")

        # Motion Profile Status List
        self._status_FL = self._talon_FL.getMotionProfileStatus()
        self._status_FR = self._talon_FR.getMotionProfileStatus()
        self._status_BL = self._talon_BL.getMotionProfileStatus()
        self._status_BR = self._talon_BR.getMotionProfileStatus()
        self._statuses = [
            self._status_FL,
            self._status_FR,
            self._status_BL,
            self._status_BR,
        ]
        self.logger.info("Statuses constructed")

    # Resets all trajectories and control variables
    def reset(self):
        self.logger.info("Clearing trajectory")
        self.clear_trajectories()
        self._state = 0
        self._loop_timeout = -1
        self.start = False

    # Determines state of motion profile
    def control(self):
        self.logger.info("Controlling...")
        # Populates and updates profile statuses every control loop
        for talon in self._talons:
            index = self._talons.index(talon)
            self._statuses[index] = talon.getMotionProfileStatus()

        if self._loop_timeout < 0:
            pass
        else:
            if self._loop_timeout == 0:
                pass
            else:
                self._loop_timeout -= 1

        for talon in self._talons:
            if talon.getControlMode() is not ControlMode.MotionProfile:
                self._state = 0
                self._loop_timeout = -1
            else:
                pass

        # Control loop
        if self._state == 0 and self.start:
            self.logger.info("Status 0, Start True")
            self.start = False
            self.startFilling()
            self._state = 1
            self._loop_timeout = self.k_num_loops_timeout
        elif self._state == 1:
            self._state = 2
            self._loop_timeout = self.k_num_loops_timeout
        elif self._state == 2:
            for status in self._statuses:
                if status.isUnderrun == False:
                    self._loop_timeout = self.k_num_loops_timeout
                elif status.activePointValid and status.isLast:
                    self._state = 0
                    self._loop_timeout = -1

    def startFilling(self):
        self.logger.info("Started Filling")
        point_L = TrajectoryPoint("position"=0, "velocity"=0, "auxiliaryPos"=0, "profileSlotSelect0"=0. "profileSlotSelect1"=0, "isLastPoint"=0, "zeroPos"=0, "timeDur"=0)
        point_R = TrajectoryPoint()

        # Set Back Talons to follower mode so points get pushed to front ones only
        if self._talon_BR.getControlMode() != WPI_TalonSRX.ControlMode.Follower:
            self._talon_BR.follow(self._talon_FR)
        elif self._talon_BL.getControlMode() != WPI_TalonSRX.ControlMode.Follower:
            self._talon_BL.follow(self._talon_FL)
        else:
            pass

        with open(self.trajectory_R_name, newline="") as file_1, open(
            self.trajectory_L_name, newline=""
        ) as file_2:

            # Fill point values for master point list
            for values in file_1:
                self.csv_points1.append(values)
            for values in file_2:
                self.csv_points2.append(values)

            for values in self.csv_points1:
                # For the first file, skip the header
                if "".join(values) == "Delta Time Position Velocity ":
                    continue

                # Fill point data from master list point
                point_R.time_step = int(values[0])
                point_R.position = float(values[1])
                point_R.velocity = float(values[2])
                point_R.zeroPos = False

                # Check if point is first point
                if values == self.csv_points1[1]:
                    point_R.zeroPos = True

                # Check if point is last point
                point_R.isLastPoint = False
                if values == self.csv_points1[-1]:
                    point_R.isLastPoint = True

                # Pushes points to MPB on Talon
                self._talon_FR.pushMotionProfileTrajectory(point_R)

            for values in self.csv_points2:
                point_L.time_step = int(values[0])
                point_L.position = float(values[1])
                point_L.velocity = float(values[2])
                point_L.zeroPos = False

                if values == file_1[0]:
                    point_L.zeroPos = True

                point_L.isLastPoint = False
                if values == file_1[-1]:
                    point_L.isLastPoint = True

                self._talon_FL.pushMotionProfileTrajectory(point_L)

    def start_motion_profile(self):
        self.start = True

    def clear_trajectories(self):
        for talon in self._talons:
            talon.clearMotionProfileTrajectories()

    def initialize(self):
        self.start_motion_profile()

    def execute(self):
        self.logger.info("Starting Profile")
        self.control()
