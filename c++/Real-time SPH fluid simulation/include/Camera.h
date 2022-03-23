#include "base.h"
#include "vec.h"

class Camera
{
	private :

	public :
		float radius = 6;
		float angle_Z = 45;
		float angle_Y = 45;
		float angle = M_PI / 180;

		vector<float> focus = { 0,0,0};
		vector<float> eye = { 0,0,0};
		vector<float> Ortho_eye = {0,0,0};
		vector<float> up = {0,0,0};

		vector<float> Look = {0,0,0,0,0,0,0,0,0};

		void Rotation(float D_X, float D_Y);

		void Translation(float D_X, float D_Y);

		void Up();

		void Eye();

		void LookAt();
};
