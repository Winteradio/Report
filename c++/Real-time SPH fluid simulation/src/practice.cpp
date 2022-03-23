#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <cmath>
#include <list>

using namespace std;

void getCell(float position[],float Grid_Cell_Size)
{
	for (int i = 0 ; i < 3 ; i ++)
	{
		position[i] /= Grid_Cell_Size;
	}
}

float getKey(float result[],int Grid_Cell_Count)
{
	int P1 = 73856093;
	int P2 = 19349663;
	int P3 = 83492791;
	return (int)(((((result[0] + P1) * result[1]) + P2) * result[2]) + P3) % Grid_Cell_Count;
}

void gridSearch(int Number,float Key)
{
}

int main()
{
	unordered_multimap<float,int> um;

	int Particle_Num = 3000;
	float Particle_Radius = 0.1f;
	float Smoothing_Radius = 4*Particle_Radius;
	float Bounding_Box_Width = 10.0f;
	float Grid_Cell_Size = Smoothing_Radius;
	int Grid_Cell_Count =pow(Bounding_Box_Width/Grid_Cell_Size,3);

	float Particle_Inf[Particle_Num][3][3];

	int range = (int)(Bounding_Box_Width/0.2f);
	for (int i = 0 ; i < Particle_Num ; i++)
	{
		float PosX,PosY,PosZ;
		PosX = i % range;
		PosZ = (i / range) % range;
		PosY = ( (i / range) / range ) % range;

		Particle_Inf[i][0][0] = PosX * 0.2f;
		Particle_Inf[i][0][1] = PosY * 0.2f;
		Particle_Inf[i][0][2] = PosZ * 0.2f;
//		cout << Particle_Inf[i][0][0] << Particle_Inf[i][0][1] << Particle_Inf[i][0][2]<<endl;
	}

	// populate spatial grid;

	for (int i =0; i < Particle_Num ; i++)
	{
		float dis_Pos[3] = {Particle_Inf[i][0][0],Particle_Inf[i][0][1],Particle_Inf[i][0][2]};
		getCell(dis_Pos,Grid_Cell_Size);
		//cout << dis_Pos[0] << dis_Pos[1] << dis_Pos[2] << endl;
		float Key = getKey(dis_Pos,Grid_Cell_Count);
		um.insert({Key,i});
		//cout << Key << endl;
	}

	auto its = um.equal_range(6795);
	list<int> Inf;
	for (auto it = its.first; it !=its.second ; it++)
	{
		Inf.push_back(it->second);
	}
	Inf.sort();
	list<int>::iterator itor;
	for (itor = Inf.begin() ; itor !=Inf.end() ; itor ++)
	{
		cout << *itor <<endl;
	}

	return 0;
}

