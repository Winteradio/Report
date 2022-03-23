from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from bvh import Bvh
from simple_viewer import SimpleViewer
from scipy.spatial.transform import Rotation as R

import math
import sys
import numpy as np
import dartpy as dart
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
import platform

class MainWindow(QOpenGLWidget):

    def  __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setMouseTracking(True)

        self.world=dart.utils.SkelParser.readWorld(os.path.abspath('walk.skel'))
        self.Human=self.world.getSkeleton(0)
        self.Numbody=self.Human.getNumBodyNodes()
        self.Numjoint=self.Human.getNumJoints()
        self.Joint_name=list()
        
        ## 카메라 이동 관련 변수들
        self.L_mouse=False
        self.R_mouse=False
        self.H_mouse=False
        self.radius=1
        self.v_angle=math.pi/4
        self.h_angle=math.pi/10
        self.focus=np.array([0,-0.1,0])
        
        self.Num=0

        for i in range(self.Numjoint):
            self.Joint_name.append(self.Human.getJoint(i).getName())
            
        with open('sample-walk.bvh') as f:
            self.walkfile=Bvh(f.read())

        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        self.kp=5
        self.kd=0.06
        self.frame=45
        
        self.past_pd=np.zeros(3)
        self.position_desired=np.zeros(3)
 
    def initializeGL(self):
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
 
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        ambient = [1.0,1.0,1.0,1.0]
        diffuse=[1.0,1.0,1.0,0.2]
        specular=[1.0,1.0,1.0,0.2]
        position=[5.0,5.0,5.0,5.0]
        
        mat_ambient=[0.5,0.5,0.5,0.0]
        mat_diffuse=[0.6,0.6,0.6,0.0]
        mat_specular=[0.7,0.7,0.7,0.0]
        mat_emissive=[0.0,0.0,0.0,0.0]
        mat_shininess=[30.0]
        
        glPushMatrix()
        glPushMatrix()
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        glEnable(GL_LIGHT0)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,mat_ambient)
        glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,mat_diffuse)
        glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,mat_specular)
        glMaterialfv(GL_FRONT_AND_BACK,GL_SHININESS,mat_shininess)
        glMaterialfv(GL_FRONT_AND_BACK,GL_EMISSION,mat_emissive)
        glPopMatrix()
        glPopMatrix()


        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
 
        glEnable(GL_TEXTURE_2D)
 
    def resizeGL(self, width, height):
        glGetError()
 
        aspect = width if (height == 0) else width / height
 
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def Camera(self):
        R_camera=np.array([self.radius*np.cos(self.v_angle)*np.cos(self.h_angle),self.radius*np.sin(self.h_angle),self.radius*np.sin(self.v_angle)*np.cos(self.h_angle)])
        R_plane=np.array([self.radius*np.sin(self.v_angle)*np.cos(self.h_angle),0,-self.radius*np.cos(self.v_angle)*np.cos(self.h_angle)])
        Upvec=np.cross(R_plane,-R_camera)
        
        gluLookAt(R_camera[0]+self.focus[0],R_camera[1]+self.focus[1],R_camera[2]+self.focus[2],self.focus[0],self.focus[1],self.focus[2],Upvec[0],Upvec[1],Upvec[2])
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.Camera()
        glPushMatrix()
        self.world.step()
        self.Drawskeleton()
        self.Drawbaseline()
        
        glLineWidth(2.0)
        glBegin(GL_LINES)    
        glColor3f(0,0,1)
        glVertex3fv([0,1,0])
        glVertex3fv([0,0,0])
        glEnd()
        glPopMatrix()
        glFlush()
        
        for i in range(40):
            self.world.step()
            self.pd_control()
            
        if self.frame >= 130:
            self.frame =45
        elif self.frame < 130 :
            self.frame+=1
            
        self.Num +=0.03
        print(self.Num)

    def Drawbaseline(self):
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

    def Drawskeleton(self):
        for i in range(self.Numbody):
            Body=np.array(self.Human.getBodyNode(i).getWorldTransform().translation())
            Scale=np.array(self.Human.getBodyNode(i).getShapeNode(0).getShape().getSize())
            Rotation=np.array(self.Human.getBodyNode(i).getWorldTransform().rotation())
            Euler=self.cal_Rotation(Rotation)
            glPushMatrix()
            glTranslatef(Body[0],Body[1],Body[2])
            glMultMatrixf(Euler.T)
            glScalef(Scale[0],Scale[1],Scale[2])
            self.Drawunitbox()
            glPopMatrix()
            glFlush()

    def cal_Rotation(self,Rotation):
        Real_Rotation=np.zeros((4,4))
        for i in range(3):
            for j in range(3):
                Real_Rotation[i][j]=Rotation[i][j]
        Real_Rotation[3][3]=1
        return Real_Rotation
    
    def pd_control(self):
        position=np.zeros(3)
        velocity=np.zeros(3)
        
        position_desired=np.zeros(3)
        velocity_desired=np.zeros(3)
        torque=np.zeros(3)
        logarithm=np.zeros(3)
        for i in self.Joint_name:
            '''`
            if i =='RightUpLeg' or i== 'RightLeg' or i=='RightFoot':
            
            or i=='RightForeArm' or i=='RightHand' 
            or i=='LeftForeArm' or i=='LeftHand'
            '''
            '''
            if i == 'LeftUpLeg' or i=='LeftLeg' or i=='LeftFoot' or i=='RightUpLeg' or i=='RightLeg' or i=='RightFoot' or i=='Spine' or i=='Head' or i=='RightArm' or i=='LeftArm' or i=='RightForeArm' or i=='LeftForeArm' :
            '''
            if i!='Hips':
                Z_angle=self.walkfile.frame_joint_channel(self.frame,i,'ZROTATION')*math.pi/180
                X_angle=self.walkfile.frame_joint_channel(self.frame,i,'XROTATION')*math.pi/180
                Y_angle=self.walkfile.frame_joint_channel(self.frame,i,'YROTATION')*math.pi/180
                
                Z_ROT=np.array([[np.cos(Z_angle),-np.sin(Z_angle),0],
                                [np.sin(Z_angle),np.cos(Z_angle),0],
                                [0,0,1]])
                X_ROT=np.array([[1,0,0],
                                [0,np.cos(X_angle),-np.sin(X_angle)],
                                [0,np.sin(X_angle),np.cos(X_angle)]])
                Y_ROT=np.array([[np.cos(Y_angle),0,np.sin(Y_angle)],
                                [0,1,0],
                                [-np.sin(Y_angle),0,np.cos(Y_angle)]])
                
            ## ZXY 순으로 설정
            ## Rotation Matrix를 만들어야한다
            ## SKel 파일은 T Pose 형식으로 만들어서 진행을 시켜야 한다
            ## 각가의 Joint에 대해서 진행을 해보고 판단을 해보자
                for k in range(3):
                    position[k]=self.Human.getJoint(i).getPositions()[k]
                    velocity[k]=self.Human.getJoint(i).getVelocities()[k]
                #ROTR=self.RotationMatrix(position)
                #ROTD=self.RotationMatrix(position_desired)
                #LOG=self.RotationVector(np.transpose(ROTR.T@ROTD))
                ROTR=(R.from_rotvec(position)).as_matrix()
                ROTD=Z_ROT@X_ROT@Y_ROT
                LOG=(R.from_matrix(ROTR.T@ROTD)).as_rotvec()
                #print(LOG,self.frame)
                torque=self.kp*LOG+self.kd*(0-velocity)
                self.Human.getJoint(i).setForces(np.array(torque))
        
    '''   
    RotationMatrix 실제로 구현하는 함수 
    def RotationMatrix(self,position):
        angle=math.sqrt(position[0]**2+position[1]**2+position[2]**2)
        for i in range(3):
            if angle != 0:
                position[i] = position[i]/angle
            else :
                position[i] =0
        Rotation=np.zeros((3,3))
        
        Rotation[0][0] = np.cos(angle) + position[0]**2*(1-np.cos(angle))
        Rotation[0][1] = position[0]*position[1]*(1-np.cos(angle))-position[2]*np.sin(angle)
        Rotation[0][2] = position[0]*position[2]*(1-np.cos(angle))+position[1]*np.sin(angle)
        
        Rotation[1][1] = np.cos(angle) + position[1]**2*(1-np.cos(angle))
        Rotation[1][2] = position[1]*position[2]*(1-np.cos(angle))-position[0]*np.sin(angle)
        Rotation[1][0] = position[1]*position[0]*(1-np.cos(angle))+position[2]*np.sin(angle)
        
        Rotation[2][2] = np.cos(angle) + position[2]**2*(1-np.cos(angle))
        Rotation[2][0] = position[2]*position[0]*(1-np.cos(angle))-position[1]*np.sin(angle)
        Rotation[2][1] = position[2]*position[1]*(1-np.cos(angle))+position[0]*np.sin(angle)
        return Rotation
    '''
    '''
    RotationVector 실제로 구현하는 함수
    def RotationVector(self,LOG):
        angle = np.arccos((LOG[0][0]+LOG[1][1]+LOG[2][2]-1)/2)
        Vector=np.zeros(3)
        Vector[0]= (LOG[2][1]-LOG[1][2])/(2*np.sin(angle))
        Vector[1]= (LOG[0][2]-LOG[2][0])/(2*np.sin(angle))
        Vector[2]= (LOG[1][0]-LOG[0][1])/(2*np.sin(angle))
        return Vector
    '''
    def Drawunitbox(self):
        glBegin(GL_QUADS)
        glNormal3f(1,0,0)
        glColor3f(0.5,0.5,0.0)
        glVertex3f(0.5,-0.5,-0.5)
        glVertex3f(0.5,-0.5,0.5)
        glVertex3f(0.5,0.5,0.5)
        glVertex3f(0.5,0.5,-0.5)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(0,0,-1)
        glVertex3f(0.5,0.5,-0.5)
        glVertex3f(-0.5,0.5,-0.5)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(0.5,-0.5,-0.5)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(-1,0,0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,0.5,-0.5)
        glVertex3f(-0.5,0.5,0.5)
        glVertex3f(-0.5,-0.5,0.5)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(0,0,1)
        glVertex3f(0.5,0.5,0.5)
        glVertex3f(0.5,-0.5,0.5)
        glVertex3f(-0.5,-0.5,0.5)
        glVertex3f(-0.5,0.5,0.5)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(0,1,0)
        glVertex3f(0.5,0.5,0.5)
        glVertex3f(-0.5,0.5,0.5)
        glVertex3f(-0.5,0.5,-0.5)
        glVertex3f(0.5,0.5,-0.5)
        glEnd()

        glBegin(GL_QUADS)
        glNormal3f(0,-1,0)
        glVertex3f(0.5,-0.5,0.5)
        glVertex3f(0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5,0.5)
        glEnd()
    '''   
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.Human.getJoint('RightArm').setForces([100,0,0])
        elif event.key() == Qt.Key_Down:
            self.Human.getJoint('RightArm').setForces([-100,0,0])
        elif event.key() == Qt.Key_Left:
            self.Human.getJoint('RightArm').setForces([0,0,100])
        elif event.key() == Qt.Key_Right:
            self.Human.getJoint('RightArm').setForces([0,0,-100])
        super().keyPressEvent(event)
    '''
    '''    
    def mouseMoveEvent(self,event):
        if self.L_mouse == True or self.R_mouse == True:
            print('Mouse move {}: [{},{}]'.format(event.button(),event.x(),event.y()))

    def mousePressEvent(self,event):
        if event.button() == 1:
            self.L_mouse=True
        elif event.button() == 2:
            self.R_mouse=True

    def mouseReleaseEvent(self,event):
        if event.button() == 1:
            self.L_mouse=False
        elif event.button() == 2:
            self.R_mouse=False
    '''    
    def wheelEvent(self,event):
        self.radius+= event.angleDelta().y()/480
        
    def onStartButtonClicked(self):
        self.timer.start()
        self.btnStop.setEnabled(True)
        self.btnStart.setEnabled(False)
    def onStopButtonClicked(self):
        self.timer.stop()
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('MainWindow')
    window.setFixedSize(600,600)
    window.show()
    sys.exit(app.exec_())