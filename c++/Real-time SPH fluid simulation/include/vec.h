#include <cmath>
#include <vector>

using namespace std;

float vector3_dot(vector<float> &A, vector<float> &B);

vector<float> vector3_cross(vector<float> &A, vector<float> &B);

float Poly6(vector<float> &Vec,float H);

float Viscosity(vector<float> &Vec,float H);

vector<float> Spiky(vector<float> &Vec,float H);
