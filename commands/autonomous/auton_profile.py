import csv

from ctre._impl.motionprofilestatus import MotionProfileStatus
from ctre.trajectorypoint import TrajectoryPoint
from wpilib import Notifier
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
        super().__init__()

        self._talon_FL = subsystems._chassis._talon_FL
        self._talon_FR = subsystems._chassis._talon_FR
        self._talon_BL = subsystems._chassis._talon_BL
        self._talon_BR = subsystems._chassis._talon_BR

        self._talons = [self._talon_FL, self._talon_FR, self._talon_BL, self._talon_BR]

        self._state = 0
        self._loop_timeout = -1
        self.start = False
        self.k_min_points_talon = 5
        self.k_num_loops_timeout = 10

        self.trajectory_L_name = trajectory_name_prefix + "_left"
        self.trajectory_R_name = trajectory_name_prefix + "_right"

        self.notifier = Notifier(Process_Buffer().run())

        for talon in self._talons:
            talon.changeMotionControlFramePeriod(5)

        # self._talon_FL.changeMotionControlFramePeriod(5)
        # self._talon_FR.changeMotionControlFramePeriod(5)
        # self._talon_BL.changeMotionControlFramePeriod(5)
        # self._talon_BR.changeMotionControlFramePeriod(5)

        self.motion_profile_status = MotionProfileStatus()
        self.notifier.startPeriodic(0.005)

    def reset(self):
        self.clear_trajectories()
        self._state = 0
        self._loop_timeout = -1
        self.start = False

    def control(self):
        if self._loop_timeout < 0:
            pass
        else:
            if self._loop_timeout == 0:
                pass
            else:
                self._loop_timeout - 1

        if self._state == 0:
            if self.start:
                self.start = False

    def startFilling(self):
        point_L = TrajectoryPoint()
        point_R = TrajectoryPoint()

        with open(self.trajectory_R_name, newline="") as file_1, open(
            self.trajectory_L_name, newline=""
        ) as file_2:
            csv_file_1 = csv.reader(file_1, delimiter=",", quotechar="|")
            csv_file_2 = csv.reader(file_2, delimiter=",", quotechar="|")
            for values in csv_file_1:
                point_L.time_step = int(values[0])
                point_L.position = float(values[1])
                point_L.velocity = float(values[2])
                point_L.zeroPos = False

                if values == file_1[0]:
                    point_L.zeroPos = True

                point_L.isLastPoint = False
                if values == file_1[-1]:
                    point_L.isLastPoint = True

                self._talon_FR.pushMotionProfileTrajectory()
                self._talon_BR.pushMotionProfileTrajectory()

            for values in csv_file_2:
                point_R.time_step = int(values[0])
                point_R.position = float(values[1])
                point_R.velocity = float(values[2])
                point_R.zeroPos = False

                if values == file_1[0]:
                    point_R.zeroPos = True

                point_R.isLastPoint = False
                if values == file_1[-1]:
                    point_R.isLastPoint = True

                self._talon_FL.pushMotionProfileTrajectory()
                self._talon_BL.pushMotionProfileTrajectory()

    def start_motion_profile(self):
        self.start = True

    def clear_trajectories(self):
        for talon in self._talons:
            talon.clearMotionProfileTrajectories()

        # subsystems._chassis._talon_FL.clearMotionProfileTrajectories()
        # subsystems._chassis._talon_FR.clearMotionProfileTrajectories()
        # subsystems._chassis._talon_BL.clearMotionProfileTrajectories()
        # subsystems._chassis._talon_BR.clearMotionProfileTrajectories()
