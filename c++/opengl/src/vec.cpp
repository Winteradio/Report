#include "vec.h"

float vector3_dot(vector<float> &A, vector<float> &B)
{	
	float sum = 0;
	for (int i =0; i <3 ; i++)
	{
		sum += A[i] * B[i];
	}
	return sum;
}

vector<float> vector3_cross(vector<float> &A, vector<float> &B)
{
	vector<float> cross(3,0);

	cross[0] = A[1] * B[2] - A[2] * B[1];
	cross[1] = A[2] * B[0] - A[0] * B[2];
	cross[2] = A[0] * B[1] - A[1] * B[0];

	return cross;
}

float Poly6(vector<float> &Vec, float H)
{
	float R = sqrt(vector3_dot(Vec,Vec));
	if (R>=0 and pow(R,2)<=H)
	{
		return pow( (pow(H,2) - pow(R,2)), 3)* 315 / (M_PI * 64 * pow(H,9));
	}
	else
	{
		return 0.0f;
	}
}

float Viscosity(vector<float> &Vec,float H)
{
	return 0.0f;
}

vector<float> Spiky(vector<float> &Vec, float H)
{
	float R = sqrt(vector3_dot(Vec,Vec));
	vector<float> Sp(Vec);
	if (R >=0 and R<=H)
	{
		for (int i= 0; i < 3; i++)
		{
			Sp[i] *= pow(H-R,2) * (-45.0f) / (M_PI * pow(H,6));
		}
		return Sp;
	}	
}
