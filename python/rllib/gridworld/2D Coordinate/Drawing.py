from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

def baseline():
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
                
            glColor3f(1,1,1)
            glVertex3fv([100,0,0])
            glVertex3fv([1,0,0])
            glVertex3fv([0,0,0])
            glVertex3fv([-100,0,0])
            glVertex3fv([0,0,100])
            glVertex3fv([0,0,1])
            glVertex3fv([0,0,0])
            glVertex3fv([0,0,-100])
        else :
            glColor3f(1,1,1)
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

def box(degree):
    glColor3f(0.5,0.0,0.2)
    glutSolidCube(1.0)
