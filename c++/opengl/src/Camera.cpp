#include "Camera.h"

void Camera::Rotation(float D_X, float D_Y)
{
	if (angle_Z>= 360)
	{
		angle_Z = 0;
	}
	else 
	{
		angle_Z -= D_X/20;
	}

	if (angle_Y >=80)
	{
		angle_Y = 80;
	}
	angle_Y += D_Y/20;
}

void Camera::Translation(float D_X, float D_Y)
{
	vector<float> U = Ortho_eye;
	vector<float> V = up;
	for (int i=0 ; i<3 ; i++)
	{
		if (i==1)
		{
			U[i] = 0; V[i] = 0;
		}
		else
		{
			U[i] *= D_X / 400;
			V[i] *= -D_Y / 400;
		}
		eye[i] -= U[i] + V[i];
		focus[i] -= U[i] + V[i];
	}
	
}

void Camera::Up()
{
	vector<float> other = vector3_cross(eye,Ortho_eye);
	for (int i =0 ; i<3 ; i++)
	{
		up[i] = other[i];
	}
}

void Camera::Eye()
{
	eye[0] = radius * cos(angle_Y * angle) * sin(angle_Z * angle);
	eye[1] = radius * sin(angle_Y * angle);
	eye[2] = radius * cos(angle_Y * angle) * cos(angle_Z * angle);

	Ortho_eye[0] = radius * cos(angle_Y * angle) * cos(angle_Z * angle);
	Ortho_eye[1] = 0;
	Ortho_eye[2] =- radius * cos(angle_Y * angle) * sin(angle_Z * angle);
}

void Camera::LookAt()
{
	Eye();
	Up();
	for (int i =0; i< 3 ; i++)
	{
		Look[i] = eye[i] + focus[i];
		Look[i+3] = focus[i];
		Look[i+6] = up[i];
	}
}
