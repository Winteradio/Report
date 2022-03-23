#include "Drawing.h"

Physics Phy;

void Drawing::Baseline()
{	
	glLineWidth(2.0f);
	glBegin(GL_LINES);
	/*
	for (int i=0 ; i< 200; i++)
	{
		glColor3f(0.5f,0.5f,0.5f);
		glVertex3f(-100+i,0,-100);
		glVertex3f(-100+i,0,100);
		glVertex3f(100,0,-100+i);
		glVertex3f(-100,0,-100+i);
	}
	*/
	glColor3f(0.0f,0.0f,0.2f);
			glVertex3f(0.0f,0.0f,0.0f);
			glVertex3f(0.0f,Phy.Space_Height,0.0f);

			glVertex3f(0.0f,0.0f,0.0f);
			glVertex3f(Phy.Space_Width,0.0f,0.0f);

			glVertex3f(0.0f,0.0f,0.0f);
			glVertex3f(0.0f,0.0f,Phy.Space_Depth);
	glEnd();
}

void Drawing::Box(float degree,float Position[3])
{
	glPushMatrix();
	glTranslatef(Position[0],Position[1],Position[2]);
	glutSolidCube(degree);
	glPopMatrix();
}

void Drawing::Sphere(float degree,float Position[3])
{
	glTranslatef(Position[0],Position[1],Position[2]);
	glScalef(degree,degree,degree);
	glutSolidSphere(1.0f,50,50);
}

void Drawing::Initialize()
{
	glPolygonMode(GL_FRONT, GL_FILL);
    glPolygonMode(GL_BACK, GL_FILL);

    glShadeModel(GL_SMOOTH);
    glEnable(GL_NORMALIZE);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);

    float ambient[4] = {1.0,1.0,1.0,1.0};
    float diffuse[4] ={1.0,1.0,1.0,0.2};
    float specular[4] ={1.0,1.0,1.0,0.2};
    float position[4] ={5.0,5.0,5.0,5.0};

    float mat_ambient[4] ={0.5,0.5,0.5,0.0};
    float mat_diffuse[4] ={0.6,0.6,0.6,0.0};
    float mat_specular[4] ={0.7,0.7,0.7,0.0};
    float mat_emissive[4] ={0.0,0.0,0.0,0.0};
	static GLfloat mat_shininess[] ={30.0};

    glPushMatrix();
    glPushMatrix();
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular);
    glLightfv(GL_LIGHT0, GL_POSITION, position);
    glEnable(GL_LIGHT0);
    glPopMatrix();

    glPushMatrix();
    glEnable(GL_COLOR_MATERIAL);
    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,mat_ambient);
    glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,mat_diffuse);
    glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,mat_specular);
    glMaterialfv(GL_FRONT_AND_BACK,GL_EMISSION,mat_emissive);
    glPopMatrix();
    glPopMatrix();


    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_BLEND);

    glEnable(GL_TEXTURE_2D);

}
