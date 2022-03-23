from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

global x,y,D_x,D_y
x= 0.0
y= 0.0
D_x = 0.01
D_y = 0.01

def MyDisplay():
    glClearColor(0.0,0.0,0.0,0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glPointSize(5.0)
    glBegin(GL_POINTS)
    
    global x
    global y
    glVertex2f(0.3,0.3)

    glEnd()
    glFlush()

def Mytimer(time):
        

    glutPostRedisplay()
    glutTimerFunc(1000, Mytimer,0)

if __name__=="__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(300,300)
    glutInitWindowPosition(0,0)
    glutCreateWindow("Continous Learning")

    glutDisplayFunc(MyDisplay)
    glutTimerFunc(0,Mytimer,0)
    

    glutMainLoop()
