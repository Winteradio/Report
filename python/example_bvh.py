from bvh import Bvh
import dartpy as dart
import numpy as np
import sys
import math
import os
with open('sample-walk.bvh') as f:
    bvh_file=Bvh(f.read())
Joint_bvh=bvh_file.get_joints_names()

world=dart.utils.SkelParser.readWorld(os.path.abspath('human.skel'))
Human=world.getSkeleton(1)
Numjoint=Human.getNumJoints()

Joint_dart=list()

for i in range(Numjoint):
    Joint_dart.append(Human.getJoint(i).getName())

for i in Joint_dart:
    print(bvh_file.frame_joint_channel(0,i,'XROTATION'))
    print(bvh_file.frame_joint_channel(198,i,'XROTATION'))

for i in range(Numjoint):
    print(Human.getJoint(i).getPositions())
    print(Human.getJoint(i).getVelocities())
