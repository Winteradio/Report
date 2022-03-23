#ifndef GLWIDGET_H
#define GLWIDGET_H

#include <QGLWidget>

class QTimer;

class GLWidget : public QGLWidget
{
	Q_OBJECT

	public:
		GLWidget();
		~GLWidget();

	private:
		void paintGL();

		void initalizeGL();

		void resizeGL(int w, int h);

		QTimer *timer;

		GLfloat x1;
		GLfloat y1;
		GLfloat rsize;
		GLfloat xstep;
		GLfloat ystep;

		GLfloat windowWidth;
		GLfloat windowHeight;

		private slot:
			void timerFUnction();
};

#endif // GLWIDGET_H
