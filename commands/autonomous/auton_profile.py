import csv
import logging

from ctre import ControlMode, SetValueMotionProfile, WPI_TalonSRX
from ctre._impl.motionprofilestatus import MotionProfileStatus
from ctre.btrajectorypoint import BTrajectoryPoint
from wpilib import Notifier, SmartDashboard
from wpilib.command import Command

import subsystems


class Process_Buffer:
    def run(self):
        subsystems._chassis._talon_FL.processMotionProfileBuffer()
        subsystems._chassis._talon_FR.processMotionProfileBuffer()
        subsystems._chassis._talon_BL.processMotionProfileBuffer()
        subsystems._chassis._talon_BR.processMotionProfileBuffer()


class Auton_Profile(Command):
    def __init__(self, trajectory_name_prefix):
        super().__init__("Auton_Profile " + trajectory_name_prefix)

        self.requires(subsystems._chassis)
        self.logger = logging.getLogger(
            "Auton Profile (" + trajectory_name_prefix + ")"
        )
        self.trajectory_name_prefix = trajectory_name_prefix
        self._set_value = SetValueMotionProfile.Disable

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
        self._start = False
        self.k_min_points_talon = 5
        self.k_num_loops_timeout = 10

        self.trajectory_L_name = (
            "/home/lvuser/py/commands/autonomous/"
            + trajectory_name_prefix
            + "_left.csv"
        )
        self.trajectory_R_name = (
            "/home/lvuser/py/commands/autonomous/"
            + trajectory_name_prefix
            + "_right.csv"
        )

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
        self._set_value = SetValueMotionProfile.Disable
        self._state = 0
        self._loop_timeout = -1
        self._start = False

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
                self.logger.info("There is a Talon not in MotionProfile Mode")
                self._state = 0
                self._loop_timeout = -1
            else:
                pass

        # Control loop
        if self._state == 0 and self.start:
            self.logger.info("State 0, Start True")
            self._start = False
            self._set_value = SetValueMotionProfile.Disable
            self.startFilling()
            self._state = 1
            self._loop_timeout = self.k_num_loops_timeout
        elif self._state == 1:
            self.logger.info("State 1")
            self._set_value = SetValueMotionProfile.Enable
            self._state = 2
            self._loop_timeout = self.k_num_loops_timeout
        elif self._state == 2:
            self.logger.info("State 2")
            for status in self._statuses:
                if status.isUnderrun == False:
                    self._loop_timeout = self.k_num_loops_timeout
                elif status.activePointValid and status.isLast:
                    self._state = 0
                    self._loop_timeout = -1
                    self._set_value = SetValueMotionProfile.Hold

    def startFilling(self):
        self.logger.info("Started Filling")
        self.state = 1
        # TODO Change how trajectoryPoint is used after updated in robotpy-ctre
        point_L = BTrajectoryPoint()
        point_R = BTrajectoryPoint()

        self.clear_trajectories()

        # Set Back Talons to follower mode so points get pushed to front ones only
        if self._talon_BR.getControlMode() != WPI_TalonSRX.ControlMode.Follower:
            self.logger.info("Talon BR not in Follower Mode")
            self._talon_BR.follow(self._talon_FR)
        if self._talon_BL.getControlMode() != WPI_TalonSRX.ControlMode.Follower:
            self.logger.info("Talon BL not in Follower Mode")
            self._talon_BL.follow(self._talon_FL)

        with open(self.trajectory_R_name, newline="") as file_1, open(
            self.trajectory_L_name, newline=""
        ) as file_2:
            csv_file1 = csv.reader(file_1, delimiter=",", quotechar="|")
            csv_file2 = csv.reader(file_2, delimiter=",", quotechar="|")

            # Fill point values for master point list
            for values in csv_file1:
                self.csv_points1.append(values)
            for values in csv_file2:
                self.csv_points2.append(values)

            self.logger.info("Master point list filling done")

            for values in self.csv_points1:
                # Fill point data from master list point
                point_R = point_R._replace(timeDur=int(values[0]))
                point_R = point_R._replace(position=float(values[1]))
                point_R = point_R._replace(velocity=float(values[2]))
                point_R = point_R._replace(zeroPos=False)

                # Check if point is first point
                if values == self.csv_points1[1]:
                    point_R = point_R._replace(zeroPos=True)

                # Check if point is last point
                point_R = point_R._replace(isLastPoint=False)
                if values == self.csv_points1[-1]:
                    point_R = point_R._replace(isLastPoint=True)
 
                # Pushes points to MPB on Talon
                self._talon_FR.pushMotionProfileTrajectory(point_R)

                self.r_index = self.csv_points1.index(values)
                SmartDashboard().putNumber("Current R Point", self.r_index)
                if values == self.csv_points1[-1]:
                    break

            for values in self.csv_points2:
                if "".join(values) == "Delta Time Position Velocity ":
                    self.logger.info("Skipping headers")
                    continue

                point_L = point_L._replace(timeDur=int(values[0]))
                point_L = point_L._replace(position=float(values[1]))
                point_L = point_L._replace(velocity=float(values[2]))
                point_L = point_L._replace(zeroPos=False)

                if values == self.csv_points2[0]:
                    point_L = point_L._replace(zeroPos=True)

                point_L = point_L._replace(isLastPoint=False)
                if values == self.csv_points2[-1]:
                    point_L = point_L._replace(isLastPoint=True)

                self._talon_FL.pushMotionProfileTrajectory(point_L)

                self.l_index = self.csv_points2.index(values)
                SmartDashboard().putNumber("Current L Point", self.l_index)
                if values == self.csv_points2[-1]:
                    break

    def start_motion_profile(self):
        self._start = True

    def clear_trajectories(self):
        self.logger.info("Clearing trajectories")
        for talon in self._talons:
            talon.clearMotionProfileTrajectories()

    def initialize(self):
        self.logger.info("Initialiing Motion Profile " + self.trajectory_name_prefix)
        self.start_motion_profile()

    def execute(self):
        self.logger.info("Starting Profile " + self.trajectory_name_prefix)
        self.control()

    def interrupted(self):
        self.logger.warning(
            "Auton Profile (" + self.trajectory_name_prefix + ") was interrupted"
        )

    def end(self):
        self._start = False
        self.state = 0
        self._loop_timeout = -1
