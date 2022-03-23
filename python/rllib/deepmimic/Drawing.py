from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import math
import dartpy as dart
import numpy as np

class Drawing:

    def __init__(self):
        self.world  = dart.utils.SkelParser.readWorld(os.path.abspath('human32.skel'))
        self.world.setGravity([0,0,0])
        self.Num_Skeleton = self.world.getNumSkeletons()

        ## World.getNumSkeletons() : World상에서 존재하는 Skeleton의 개수들을 추출한다

        ## World 상에 존재하는 Skeleton 이름 추출하기
        return None


    def Baseline(self):
        for i in range(200):
            glLineWidth(2.0)
            glBegin(GL_LINES)
            if i==100:
                glColor3f(1,1,0) # x축
                glVertex3fv([1,0,0])
                glVertex3fv([0,0,0])
                glColor3f(0,1,0) # z축
                glVertex3fv([0,0,1])
                glVertex3fv([0,0,0])
                
                glColor3f(0.5,0.5,0.5)
                glVertex3fv([100,0,0])
                glVertex3fv([1,0,0])
                glVertex3fv([0,0,0])
                glVertex3fv([-100,0,0])
                glVertex3fv([0,0,100])
                glVertex3fv([0,0,1])
                glVertex3fv([0,0,0])
                glVertex3fv([0,0,-100])
            else :
                glColor3f(0.5,0.5,0.5)
                glVertex3fv([-100+i,0,-100])
                glVertex3fv([-100+i,0,100])
                glVertex3fv([100,0,-100+i])
                glVertex3fv([-100,0,-100+i])
            glEnd()

        glLineWidth(2.0)
        glBegin(GL_LINES)    
        glColor3f(0,0,1)
        glVertex3fv([0,1,0])
        glVertex3fv([0,0,0])
        glEnd()


    def Box(self,degree):
        glutSolidCube(1.0)

    def Sphere(self,degree):
        glutSolidSphere(degree,30,30)

    def Capsule(self,degree,height):
        obj = gluNewQuadric()
        gluQuadricDrawStyle(obj,GLU_LINE)
        gluCylinder(obj,degree,degree,height,30,30)

    def Skeleton(self):
        for i in range(self.Num_Skeleton):
            Skel = self.world.getSkeleton(i)
            Num_Body = Skel.getNumBodyNodes()
            Num_Joint = Skel.getNumJoints()

            for j in range(Num_Body):
                Body = Skel.getBodyNode(j)
                Position = np.array(Body.getWorldTransform().translation())
                Rotation = np.array(Body.getWorldTransform().rotation())
                Scale = np.array(Body.getShapeNode(0).getShape().getSize())/2
                Euler = self.Euler(Rotation)

                glPushMatrix()
                glTranslatef(Position[0],Position[1],Position[2])
                glMultMatrixf(Euler.T)
                glScalef(Scale[0],Scale[1],Scale[2])

                if Skel.getName() == "Ground" :
                    glColor3f(0.1,0.1,0.0)
                    self.Box(1.0)
                else : 
                    glColor3f(0.0,0.5,0.2)
                    self.Sphere(1.0)
                glPopMatrix()
                glFlush()
        
    def Euler(self,Rot):
        Real_Rot = np.zeros((4,4))

        for i in range(3):
            for j in range(3):
                Real_Rot[i][j] = Rot[i][j]
        Real_Rot[3][3] = 1
        return Real_Rot
    
    def Counter(self):
        self.Skeleton()

        for i in range(30):
            self.world.step()

if __name__=="__main__":
    draw = Drawing()
    draw.Skeleton()
