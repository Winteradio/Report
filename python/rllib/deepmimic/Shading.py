from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *

def Shading():
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)
 
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

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
