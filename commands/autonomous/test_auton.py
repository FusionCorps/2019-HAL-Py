from ctre.btrajectorypoint import BTrajectoryPoint
import csv


def testFill():
    # Read to list
    with open('./commands/autonomous/example_right.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar="|")
        csv_points = list(reader)

    # convert to BtTrajectoryPoints
    trajectoryPoints = [BTrajectoryPoint(timeDur=int(x[0]), position=float(
        x[1]), velocity=float(x[2]), zeroPos=False) for x in csv_points]
    trajectoryPoints[0] = trajectoryPoints[0]._replace(zeroPos=True)
    trajectoryPoints[-1] = trajectoryPoints[-1]._replace(isLastPoint=True)

    # now you should be able to loop through your trajectory point list
    # and push those items
    
    #     # Pushes points to MPB on Talon
    #     self._talon_FR.pushMotionProfileTrajectory(point_R)

    #     self.r_index = self.csv_points1.index(values)
    #     SmartDashboard().putNumber("Current R Point", self.r_index)
    #     if values == self.csv_points1[-1]:
    #         break


testFill()
