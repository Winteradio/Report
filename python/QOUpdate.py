import numpy as np
from PyQt5 import QtCore, QtWidgets
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo


class GLWidget(QtWidgets.QOpenGLWidget):
import numpy as np

from PyQt5 import QtCore, QtWidgets
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo


class GLWidget(QtWidgets.QOpenGLWidget):

    VERTEX_SHADER = """
        #extension GL_ARB_explicit_attrib_location : enable
        attribute vec4 in_position;
        attribute vec2 in_tex_coord;
        varying vec2 vs_tex_coord;

        void main(void){
            gl_Position = in_position;
            vs_tex_coord = in_tex_coord;
        }"""

    FRAGMENT_SHADER = """
        uniform sampler2D tex;
        varying vec2 vs_tex_coord;

        void main(void){
            gl_FragColor = texture2D(tex, vs_tex_coord);
        }"""

    vbov = vbo.VBO(np.array([[-1.0, -1.0, 0.0, 1.0, 0.0, 0.0],
                             [1.0, -1.0, 0.0, 1.0, 1.0, 0.0],
                             [1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
                             [-1.0, 1.0, 0.0, 1.0, 0.0, 1.0]], 'f'))

    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def initializeGL(self):
        glClearColor(0, 0, 0, 0)

        vs = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fs = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vs, fs)

        self.position = glGetAttribLocation(self.shader, 'in_position')
        self.tex_coord = glGetAttribLocation(self.shader, 'in_tex_coord')

        self.timer.start(250)

    def paintGL(self):
        print 'paintGL'
        w, h, = 16, 16
        img = np.uint8(np.random.rand(w, h)*255)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shaders.glUseProgram(self.shader)
        try:
            self.vbov.bind()
            try:
                tex = glGenTextures(1)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, img)
                tex_uloc = glGetUniformLocation(self.shader, "tex")
                glUniform1i(tex_uloc, 1)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, tex)

                glEnableVertexAttribArray(self.position)
                glEnableVertexAttribArray(self.tex_coord)
                stride = 6 * 4
                glVertexAttribPointer(self.position, 4, GL_FLOAT, False, stride, self.vbov)
                glVertexAttribPointer(self.tex_coord, 2, GL_FLOAT, False, stride, self.vbov + 16)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            finally:
                self.vbov.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.tex_coord)
        finally:
            shaders.glUseProgram(0)



    VERTEX_SHADER = """
        #extension GL_ARB_explicit_attrib_location : enable
        attribute vec4 in_position;
        attribute vec2 in_tex_coord;
        varying vec2 vs_tex_coord;

        void main(void){
            gl_Position = in_position;
            vs_tex_coord = in_tex_coord;
        }"""

    FRAGMENT_SHADER = """
        uniform sampler2D tex;
        varying vec2 vs_tex_coord;

        void main(void){
            gl_FragColor = texture2D(tex, vs_tex_coord);
        }"""

    vbov = vbo.VBO(np.array([[-1.0, -1.0, 0.0, 1.0, 0.0, 0.0],
                             [1.0, -1.0, 0.0, 1.0, 1.0, 0.0],
                             [1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
                             [-1.0, 1.0, 0.0, 1.0, 0.0, 1.0]], 'f'))

    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def initializeGL(self):
        glClearColor(0, 0, 0, 0)

        vs = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fs = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vs, fs)

        self.position = glGetAttribLocation(self.shader, 'in_position')
        self.tex_coord = glGetAttribLocation(self.shader, 'in_tex_coord')

        self.timer.start(250)

    def paintGL(self):
        print ('paintGL')
        w, h, = 16, 16
        img = np.uint8(np.random.rand(w, h)*255)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shaders.glUseProgram(self.shader)
        try:
            self.vbov.bind()
            try:
                tex = glGenTextures(1)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, img)
                tex_uloc = glGetUniformLocation(self.shader, "tex")
                glUniform1i(tex_uloc, 1)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, tex)

                glEnableVertexAttribArray(self.position)
                glEnableVertexAttribArray(self.tex_coord)
                stride = 6 * 4
                glVertexAttribPointer(self.position, 4, GL_FLOAT, False, stride, self.vbov)
                glVertexAttribPointer(self.tex_coord, 2, GL_FLOAT, False, stride, self.vbov + 16)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            finally:
                self.vbov.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.tex_coord)
        finally:
            shaders.glUseProgram(0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = GLWidget()
    win.show()
    app.exec_()
