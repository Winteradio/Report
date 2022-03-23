#include "base.h"
#include "Drawing.h"
#include "Camera.h"
#include "Physics.h"

Drawing draw;
Camera camera;
Physics physics;

bool mouse_right,mouse_left = false;
float mousePos[2],mouseMove[2];

void Inital()
{	
	glClearDepth(1.0);
	physics.Initialize();
	draw.Initialize();
}

void display()
{
	glClearColor(0.2,0.2,0.2,0.0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	gluPerspective(45,1,1,100);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

   	camera.LookAt();
	vector<float> Look(camera.Look);
	gluLookAt(Look[0],Look[1],Look[2],Look[3],Look[4],Look[5],Look[6],Look[7],Look[8]);
	
	glPushMatrix();	
	draw.Baseline();
	glPopMatrix();

	/*		
	glPushMatrix();
	glPointSize(1.0);
	glColor3f(1.0,1.0,1.0);
	glBegin(GL_POINTS);
	{
		for (int i=0 ; i< physics.Particle_Num; i++){
			float Pos[3];
			for (int j =0 ; j <3 ; j++)
			{
				Pos[j] = physics.Particle_Inf[i][3][j];
			}
			glVertex3f(Pos[0],Pos[1],Pos[2]);
		}
	}

	glEnd();
	glPopMatrix();
	*/
	glPushMatrix();
	for (int i =0 ; i < physics.Particle_Num; i++)
	{
		float Pos[3];
		for (int j = 0; j <3 ; j++)
		{
			Pos[j] = physics.Particle_Inf[i][3][j];
		}
		glColor3f(0.8,0.0,0.8);
		draw.Box(physics.Particle_Degree,Pos);

	}
	glPopMatrix();
	glFlush();

	glutSwapBuffers();
}

void timer(int value)
{
	physics.Update();
	glutPostRedisplay();
	glutTimerFunc(6, timer, 1);
}

void reshape(int width,int height)
{	
	if (height ==0)
	{
		height = 1;
	}
	glViewport(0,0, width,height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
}

void mouse_click(int button,int state, int x, int y)
{
	switch(button)
	{
		case GLUT_LEFT_BUTTON :
			if (state == GLUT_DOWN)
			{
				mouse_left = true;
				mousePos[0] = x; mousePos[1] = y;
			}
			else
			{
				mouse_left = false;
			}

			break;

		case GLUT_RIGHT_BUTTON :
			if (state == GLUT_DOWN)
			{
				mouse_right = true;
				mousePos[0] = x; mousePos[1] = y;
			}
			else
			{
				mouse_right = false;
			}
			break;
	}
}

void mouse_move(int x, int y)
{
	if (mouse_right ==true or mouse_left ==true)
	{	
		mouseMove[0] = x - mousePos[0];
		mouseMove[1] = y - mousePos[1];
		if (mouse_right ==true)
		{
			camera.Translation(mouseMove[0],mouseMove[1]);
		}
		else if (mouse_left ==true)
		{
			camera.Rotation(mouseMove[0],mouseMove[1]);
		}

		mousePos[0] = x;
		mousePos[1] = y;
	}
}

void mouse_wheel(int button, int dir, int x, int y)
{
	std::cout << x << std::endl;
	if ( dir > 0 )
	{
		camera.radius += 0.1f;
		std::cout << "확대중 " << std::endl;
	}
	else
	{
		camera.radius -= 0.1;
	}
	return ;
}



int main(int argc, char* argv[])
{
	Inital();
	glutInit(&argc,argv);
	
	glutInitDisplayMode(GLUT_RGBA);
	glutInitWindowSize(640,480);
	glutInitWindowPosition(400,400);
	glutCreateWindow("Opengl Project");

	glutDisplayFunc(display);
	glutTimerFunc(0, timer, 1);
	glutReshapeFunc(reshape);
	
	glutMouseFunc(mouse_click);
	glutMotionFunc(mouse_move);
	glutMouseWheelFunc(mouse_wheel);
	glutMainLoop();

	return 0;
}

