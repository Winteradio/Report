#ifndef PHYSICS_H
#define PHYSICS_H

#include "vec.h"

class Physics
{
	private :

	public :
		float Space_Width = 2.0f;
		float Space_Height = 2.0f;
		float Space_Height_Range = 0.001;
		float Space_Depth = 2.0f;
		float Space_Interval = 0.15f;

		float Error = 0.01;

		float Particle_Degree = 0.05f;
		float Particle_Mass = 28.0f;
		float Particle_H = Particle_Degree * 4.0f;
		float Particle_Volume = M_PI * 4 / 3 * pow((Particle_Degree/2),3);
		float Particle_Inf[1000][4][3];
		int Particle_Num = sizeof(Particle_Inf)/sizeof(Particle_Inf[0]);

		float Gravity = -9.81f;
		float Density = 59.0f;
		float Viscosity = 0.001;
		float Drag_Coefficient = 0.0f;
		float Collision_Coefficient = 0.25f;
		float Gas_Stiffness = 0.0001;

		float time_step = 1.0f/170.0f;

		void Initialize();

		void Update();

		void Collision(int Num);

		void Compute_Forces();

		void Compute_Density_Pressure();
};

#endif
