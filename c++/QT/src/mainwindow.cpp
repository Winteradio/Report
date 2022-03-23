#include <include/mainwindow.h>

MainWindow::MainWindow(QWidget *parent)
	: MainWindow(parent);
{
	setSurfaceType(QWindow::OpenGLSurface);
}

MainWindow::~MainWindow()
{
}

void MainWindow::initializeGL()
{
}

void MainWindow::resizeGL(int w, int h)
{
}

void MainWindow::paintGL()
{
}
