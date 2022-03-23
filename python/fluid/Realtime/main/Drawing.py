from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy as np

class Drawing:
    
    def __init__(self):
        
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
                
                glColor3f(0,0,0)
                glVertex3fv([100,0,0])
                glVertex3fv([1,0,0])
                glVertex3fv([0,0,0])
                glVertex3fv([-100,0,0])
                glVertex3fv([0,0,100])
                glVertex3fv([0,0,1])
                glVertex3fv([0,0,0])
                glVertex3fv([0,0,-100])
            else :
                glColor3f(0,0,0)
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

    def Box(self,degree,Position):
        glPushMatrix()
        glTranslatef(Position[0],Position[1],Position[2])
        glScalef(degree,degree,degree)
        glColor3f(1.0,0.0,0.2)
        glutSolidCube(1.0)
        glPopMatrix()
        glFlush()

    def Sphere(self,degree,Position):
        glPushMatrix()
        glTranslatef(Position[0],Position[1],Position[2])
        glScalef(degree,degree,degree)
        glColor3f(0.2,0.0,0.0)
        glutSolidSphere(1.0,30,30)
        glPopMatrix()
        glFlush()

    def Point(self,degree,Position):
        glPushMatrix()
        glPointSize(degree)
        glBegin(GL_POINTS)
        glColor3f(0.2,0.0,0.0)
        glVertex3fv(Position)
        glEnd()
        glPopMatrix()
        glFlush()

    def Points(self,degree,Inf):
        glPointSize(degree)
        glBegin(GL_POINTS)
        glColor3f(0.5,1.0,0.0)
        for i in range(len(Inf)):
            glVertex3fv(Inf[i][3])
        glEnd()
    
