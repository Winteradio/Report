import numpy as np
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Camera:

    def __init__(self):
        self.radius = 10
        self.angle_Z = 0
        self.angle_Y = 90
        self.angle = math.pi/180
        
        self.focus = np.array([0.0,0.0,0.0])
        
        self.eye = np.zeros(3)
        self.Ortho_eye = np.zeros(3)
        self.up = np.zeros(3)

        self.Look = np.zeros(9)

    def Rotation(self,D_X,D_Y):
        if self.angle_Z >=360:
            self.angle_Z =0
        else:    
            self.angle_Z -= D_X/20

        if self.angle_Y >=80:
            self.angle_Y = 80
        self.angle_Y += D_Y/20

    def Translate(self,D_X,D_Y):
        self.U = self.Ortho_eye / np.sqrt(self.Ortho_eye.dot(self.Ortho_eye))
        self.V = self.up / np.sqrt(self.up.dot(self.up))

        for i in range(3):
            if i == 1:
                self.U[i] = 0
                self.V[i] = 0
            self.U[i] *=D_X / 100
            self.V[i] *= -D_Y / 50
        self.eye -= self.U + self.V
        self.focus -= self.U + self.V

    def Up(self):
        self.up = np.cross(self.eye,self.Ortho_eye)

    def Eye(self):
        self.eye[0] = self.radius * math.cos(self.angle_Y*self.angle) * math.sin(self.angle_Z*self.angle) 
        self.eye[1] = self.radius * math.sin(self.angle_Y*self.angle)
        self.eye[2] = self.radius * math.cos(self.angle_Y*self.angle) * math.cos(self.angle_Z*self.angle)
        
        self.Ortho_eye[0] = self.radius * math.cos(self.angle_Y*self.angle) * math.cos(self.angle_Z*self.angle)
        self.Ortho_eye[1] = 0
        self.Ortho_eye[2] =- self.radius * math.cos(self.angle_Y*self.angle) * math.sin(self.angle_Z*self.angle)

    def LookAt(self):
        self.Eye()
        self.Up()
        
        for i in range(3):
            self.Look[i] = self.eye[i] + self.focus[i]
            self.Look[i+3] = self.focus[i]
            self.Look[i+6] = self.up[i]
   
    def Win2World(self,posX,posY,modelview,proj,viewport):
        winX = posX
        winY = 600 - posY
        winZ = 0
        
        #winZ = glReadPixels(int(winX),int(winY),1,1,GL_DEPTH_COMPONENT,GL_FLOAT) 
        #world = gluUnProject(winX,winY,winZ,modelview,proj,viewport)
        
        return world
    
if __name__=="__main__":
   camera=Camera()

   camera.LookAt()

   print(camera.angle)
