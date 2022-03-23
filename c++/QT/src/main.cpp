#include <include/mainwindow.h>
#include <QApplication>

int main(int argc, char *argv[]){

	QApplication app(argc,argv);
	MainWindow w;

	w.setTitle("Opengl");
	w.resize(640,480);
	w.show();

	return app.exec();
}

