from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget

import math
import sys
import numpy as np
import dartpy as dart
import os

## File Upload
import Drawing
import Camera
import Shading
import Physics

class MainWindow(QOpenGLWidget):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        ## Using GLUT
        glutInit()

        ## Window Inital Size
        self.width = 640
        self.height = 480
        self.winX = 100
        self.winY = 100
        self.setGeometry(self.winX,self.winY,self.width,self.height)
        
        ## Mouse Events
        self.setMouseTracking(True)
        self.mouse_left = False
        self.mouse_right = False
        self.mouse_middle = False

        self.new_posX = 0
        self.new_posY = 0

        self.old_posX = 0
        self.old_posY = 0
        
        ## Load Other Pythone File
        self.Drawing = Drawing.Drawing()
        self.Camera = Camera.Camera()
        self.Physics = Physics.Physics()
        self.Shading = Shading

        ## Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(int(self.Physics.timestep*1000))
   
   ## Main Update Functions

    def initializeGL(self):
        glClearColor(0.2,0.2,0.2,0.0)
        glClearDepth(1.0)
        self.Shading.Shading()

    def resize(self,width,height):
        self.width = width
        self.height = height

        if self.height ==0 :
            self.height = 1

        if self.width ==0 :
            self.width = 1

        self.aspect = self.width/self.height
        glViewport(0,0,self.width,self.height)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
       
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45,self.width/self.height,1,100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.Camera.LookAt()
        Look = self.Camera.Look
        gluLookAt(Look[0], Look[1], Look[2], Look[3], Look[4], Look[5], Look[6], Look[7], Look[8])
        
        self.Physics.Leapfrog_Integration()

        self.drawGL()

    ## Draw on the OpenGL Window Display

    def drawGL(self):
        glPushMatrix()
        self.Drawing.Baseline()
        self.Physics.Draw_Particle() 
        glPopMatrix()
        glFlush()
    
    ## Function of Mouse Event 

    def mouseMoveEvent(self,event):
        if self.mouse_left == True or self.mouse_right == True:
            self.old_posX = self.new_posX
            self.old_posY = self.new_posY

            self.new_posX = event.globalX()-self.winX
            self.new_posY = event.globalY()-self.winY
            
            self.D_X = self.new_posX - self.old_posX
            self.D_Y = self.new_posY - self.old_posY
            
            if self.mouse_left == True :
                self.Camera.Rotation(self.D_X,self.D_Y)
            elif self.mouse_right ==True :
                self.Camera.Translate(self.D_X,self.D_Y)

    def mousePressEvent(self,event):
        if event.buttons() == Qt.LeftButton or event.buttons() == Qt.RightButton :
            self.new_posX = event.globalX()-self.winX
            self.new_posY = event.globalY()-self.winY

            if event.buttons() == Qt.LeftButton:
                self.mouse_left = True
                self.mouse_right = False

            if event.buttons() == Qt.RightButton:
                self.mouse_right = True
                self.mouse_left = False

        if event.buttons() == Qt.MidButton:
            self.mouse_middle = True
    
    def mouseReleaseEvent(self,event):
        if self.mouse_left == True:
            self.mouse_left = False
        
        elif self.mouse_right == True:
            self.mouse_right = False

        elif self.mouse_middle == True:
            self.mouse_middle = False

    def wheelEvent(self,event):
        Update_radius = self.Camera.radius - event.angleDelta().y()*0.0025

        if Update_radius >= 0.5 and Update_radius <= 50:
            self.Camera.radius = Update_radius


if __name__=="__main__":
    app=QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Deepmimic")
    window.show()
    sys.exit(app.exec_())
