#include "Physics.h"

void Physics::Initialize()
{
	int Width = (int)(Space_Width/Space_Interval);
	int Depth = (int)(Space_Depth/Space_Interval);
	int Height = (int)(Space_Height/Space_Interval);
	for (int i =0 ; i< Particle_Num; i ++)
	{
		float Pos_X,Pos_Y,Pos_Z;
		Pos_X = i % Width;
		Pos_Z = ( i / Width ) % Depth;
		Pos_Y = (( i / Width ) / Depth ) % Height;

		Particle_Inf[i][3][0] = Pos_X * Space_Interval;
		Particle_Inf[i][3][1] = Pos_Y * Space_Interval + Space_Height_Range;
		Particle_Inf[i][3][2] = Pos_Z * Space_Interval;

		Particle_Inf[i][0][0] = Density;
		Particle_Inf[i][0][2] = Particle_Mass;
	}
}

void Physics::Collision(int Num)
{
	if (Particle_Inf[Num][3][1] < 0)
	{
		Particle_Inf[Num][3][1] = 0;
		Particle_Inf[Num][2][1] *= - Collision_Coefficient;
	}
	else if (Particle_Inf[Num][3][1] > Space_Height)
	{
		Particle_Inf[Num][3][1] = Space_Height;
		Particle_Inf[Num][2][1] *= - Collision_Coefficient;
	}

	if (Particle_Inf[Num][3][0] < 0)
	{
		Particle_Inf[Num][3][0] = 0;
		Particle_Inf[Num][2][0] *= - Collision_Coefficient;
	}
	else if (Particle_Inf[Num][3][0] > Space_Width)
	{
		Particle_Inf[Num][3][0] = Space_Width;
		Particle_Inf[Num][2][0] *= - Collision_Coefficient;
	}

	if (Particle_Inf[Num][3][2] < 0)
	{
		Particle_Inf[Num][3][2] = 0;
		Particle_Inf[Num][2][2] *= - Collision_Coefficient;
	}
	else if (Particle_Inf[Num][3][2] > Space_Depth)
	{
		Particle_Inf[Num][3][2] = Space_Depth;
		Particle_Inf[Num][2][2] *= - Collision_Coefficient;
	}
}

void Physics::Update()
{
	Compute_Density_Pressure();
	Compute_Forces();

	for (int i =0; i< Particle_Num ; i++)
	{
		for (int j =0 ; j  <3 ; j ++)
		{
			float Accel = Particle_Inf[i][1][j] / Particle_Inf[i][0][0];
			Particle_Inf[i][2][j] += (float)(Accel * time_step);
			Particle_Inf[i][3][j] += (float)(Particle_Inf[i][2][j] * time_step);
			Collision(i);
		}
	}
}

void Physics::Compute_Forces()
{
	vector<float> Force_V = {0.0f,0.0f,0.0f};
	vector<float> Force_P = {0.0f,0.0f,0.0f};

	for (int i =0; i< Particle_Num ; i++)
	{
		for (int j =0; j < Particle_Num ; j++)
		{
			if (i !=j)
			{
				vector<float> Vec = {0.0f,0.0f,0.0f};

				for (int k = 0; k < 3 ; k++)
				{
					Vec[k] = Particle_Inf[i][3][k] - Particle_Inf[j][3][k];
				}
				float R = sqrt(vector3_dot(Vec,Vec));


				if (R < Particle_H)
				{
					vector<float> Spi(Spiky(Vec,Particle_H));
					for (int k = 0; k < 3; k++)
					{
						Force_V[k] += Particle_Inf[i][0][2] *  (Particle_Inf[i][2][k] - Particle_Inf[j][2][k]) / Particle_Inf[j][0][0] * ( (Particle_H - R) * 45.0f / (M_PI * pow(Particle_H,6))); 
						Force_P[k] -= Particle_Inf[i][0][2] *  (Particle_Inf[i][0][1] - Particle_Inf[j][0][1] ) * Spi[k] / (2 * Particle_Inf[j][0][0]);
					}
				}

			}
		}

		for (int k = 0 ; k <3 ; k++)
		{
			Particle_Inf[i][1][k] = Force_V[k] * Viscosity + Force_P[k];
		}
		Particle_Inf[i][1][1] += Gravity * Particle_Inf[i][0][0];
	}

}

void Physics::Compute_Density_Pressure()
{
	for (int i =0; i < Particle_Num ; i++)
	{
		Particle_Inf[i][0][0] = 0;

		for (int j =0 ; i < Particle_Num ; i++)
		{
			vector<float> Vec = {0.0f,0.0f,0.0f};
			for (int k =0 ; k <3 ; k ++)
			{
				Vec[k] = Particle_Inf[i][3][k] - Particle_Inf[j][3][k];
			}
			float R = sqrt(vector3_dot(Vec,Vec));

			if (R < Particle_H)
			{
				Particle_Inf[i][0][0] += Particle_Inf[i][0][2] * Poly6(Vec,Particle_H);
			}

		}

		Particle_Inf[i][0][1] = Gas_Stiffness * (Particle_Inf[i][0][0] - Density);
	}

}


