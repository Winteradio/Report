from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
 
def initFun():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
 
    ambient = [1.0, 1.0, 1.0, 0.0]
    diffuse = [1.0, 1.0, 1.0, 0.0]
    specular = [1.0, 1.0, 1.0, 0.0]
    position = [6.0, 6.0, 5.0, 0.0]
 
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)
 
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_DEPTH_TEST)
    
def displayFun():
    mat_ambient = [0.2, 0.2, 0.2, 0.0]
    mat_diffuse = [0.6, 0.6, 0.6, 0.0]
    mat_specular = [0.2, 0.2, 0.2, 0.0]
    mat_emissive = [0.0, 0.0, 0.0, 0.0]
    mat_shininess = [50.0]
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
 
    glLoadIdentity()
 
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emissive)
    
    glPushMatrix()
    glTranslatef(0.0,0.0,-5.0)
    glBegin(GL_QUADS)
    glColor3f(0.5,0.5,0.5)
    glVertex3f(1,1,1)
    glVertex3f(1,1,-1)
    glVertex3f(-1,1,-1)
    glVertex3f(-1,1,1)
    glEnd()
    glPopMatrix()
 
    glFlush()
 
def reshapeFun(width, height):
    glGetError()
 
    aspect = width if (height == 0) else width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
 
if __name__=='__main__':
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Cube")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(reshapeFun)
    initFun()
    glutMainLoop()
