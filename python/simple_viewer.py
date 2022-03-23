# simple_viewer.py

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL

class SimpleViewer(QtOpenGL.QGLWidget):

    initialize_cb    = QtCore.pyqtSignal()
    resize_cb        = QtCore.pyqtSignal(int,int)
    idle_cb          = QtCore.pyqtSignal()
    render_cb        = QtCore.pyqtSignal()

    mouse_move_cb    = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_press_cb   = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_release_cb = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_wheel_cb   = QtCore.pyqtSignal( QtGui.QWheelEvent )

    key_press_cb     = QtCore.pyqtSignal( QtGui.QKeyEvent )
    key_release_cb   = QtCore.pyqtSignal( QtGui.QKeyEvent )

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setMouseTracking(True)

    def mouseMoveEvent( self, evt ):
        self.mouse_move_cb.emit( evt )

    def mousePressEvent( self, evt ):
        self.mouse_press_cb.emit( evt )

    def mouseReleaseEvent( self, evt ):
        self.mouse_release_cb.emit( evt )

    def keyPressEvent( self, evt ):
        self.key_press_cb.emit(evt)

    def keyReleaseEvent( self, evt ):
        self.key_release_cb.emit(evt)

    def initializeGL(self):
        self.initialize_cb.emit()

    def resizeGL(self, width, height):
        if height == 0: height = 1
        self.resize_cb.emit(width,height)

    def paintGL(self):
        self.render_cb.emit()
 
## cube_main.py       
        for r in self.Joint_name:
            print(r)
            if r == 'RightArm':
                
                Rotation=np.array(self.Human.getJoint(r).getRelativeTransform().rotation())
                self.position_desired[0][0]=self.walkfile.frame_joint_channel(self.frame,r,'XROTATION')
                self.position_desired[0][1]=self.walkfile.frame_joint_channel(self.frame,r,'YROTATION')
                self.position_desired[0][2]=self.walkfile.frame_joint_channel(self.frame,r,'ZROTATION')
                for k in range(3):
                    velocity[0][k]=self.Human.getJoint(r).getVelocities()[k]
                    velocity_desired[0][k]=(self.position_desired[0][k]-self.past_pd[0][k])/self.walkfile.frame_time
                    self.past_pd[0][k]=self.position_desired[0][k]

                RD=R.from_rotvec(self.position_desired).as_matrix()
                for i in range(3):
                    for j in range(3):
                        ROTD[i][j]=RD[0][i][j]
                ROT=Rotation.T@ROTD
                logarithm=R.from_matrix(ROT).as_rotvec()
                torque=self.kp*logarithm+self.kd*(velocity_desired-velocity)
                self.Human.getJoint(r).setForces([torque[0][0],torque[0][1],torque[0][2]])
                print(torque)