
import os 
import sys
CWD_PATH = os.getcwd()
sys.path.append(CWD_PATH)

import math
import dartpy as dart
import numpy as np

PI_HALF = math.pi / 2.0

class MagentoSimulation():
    def __init__(self):
        # set world and robot/ground skeletons
        self.world = dart.simulation.World()
        urdfParser = dart.utils.DartLoader()
        self.robot = urdfParser.parseSkeleton( CWD_PATH + 
            "/gn_inverse_dynamics/robot_simulator/config/magneto/MagnetoSim_Dart.urdf")
        self.ground = urdfParser.parseSkeleton( CWD_PATH + 
            "/gn_inverse_dynamics/robot_simulator/config/ground/ground_inclined03.urdf")
        self.world.addSkeleton(self.robot)
        self.world.addSkeleton(self.ground)
        self.world.setGravity([0, 0, -9.81])
        self.world.setTimeStep(0.001)

        self._set_init_robot_config()
        self._set_friction_coeff(0.5)

    def _set_init_robot_config(self):
        ## INITIAL CONFIGURATIONS        
        femur_init = -1.0/10.0*PI_HALF
        tibia_init = -PI_HALF-femur_init
        q_foot_init = [0.0, femur_init, tibia_init, 0.0, 0.0, 0.0 ]
        q = [0.0, 0.0, 0.15 , 0.0, 1.0, 0.0] # base init pose 
        q.extend(q_foot_init*4) #AL,AR,BL, BR
        print(q)
        self.robot.setPositions(q)

    def _set_friction_coeff(self, mu):
        self.ground.getBodyNode("ground_link").setFrictionCoeff(mu)
        self.robot.getBodyNode("BL_foot_link").setFrictionCoeff(mu)
        self.robot.getBodyNode("AL_foot_link").setFrictionCoeff(mu)
        self.robot.getBodyNode("AR_foot_link").setFrictionCoeff(mu)
        self.robot.getBodyNode("BR_foot_link").setFrictionCoeff(mu)

        self.robot.getBodyNode("BL_foot_link_3").setFrictionCoeff(mu)
        self.robot.getBodyNode("AL_foot_link_3").setFrictionCoeff(mu)
        self.robot.getBodyNode("AR_foot_link_3").setFrictionCoeff(mu)
        self.robot.getBodyNode("BR_foot_link_3").setFrictionCoeff(mu)

    def set_robot_state(self, q, qdot):
        self.robot.setPositions(q)
        self.robot.setVelocities(qdot)

    def get_robot_state(self):
        q = self.robot.getPositions()
        qdot = self.robot.getVelocities()
        return q, qdot

    def step(self, action):
        self.robot.setForces(action)
        self.world.step()


## TEST
if __name__ == "__main__":
    magsim = MagentoSimulation()
    numCycle = 100
    for i in range(10):
        print("{} th step".format(i*numCycle))
        q, qdot = magsim.get_robot_state()
        print(magsim.get_robot_state())
        a = [0] * len(q)
        for _ in range(numCycle):
            magsim.step(a)
