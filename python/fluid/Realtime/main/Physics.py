import numpy as np
import math
import Drawing

class Physics:

    def __init__(self):
        self.Drawing = Drawing.Drawing()
        ## Number of Particles
        self.Num_Particle = 100
        self.Particle_Inf = np.zeros((self.Num_Particle,4,3))
        '''
        Particle_Inf Shape 구성 
            정보의 개수 : 1000개의 Particle들의 위치정보 + 속도정보 + 힘정보 + 물리정보(밀도,질량,압력)
            순서 : 
                첫번째 [0][3] 물리 정보(밀도,압력,질량)
                두번째 [1][3] 힘 정보( X , Y , Z )
                세번째 [2][3] 속도 정보 ( X , Y , Z )
                네번째 [3][3] 위치 정보 ( X , Y , Z )
        '''

        ## Setting Space range & Particle
        self.Space_Width = 1
        self.Space_Height = 20
        self.Space_Height_Range = 0.001
        self.Space_Depth = 1

        self.Particle_Degree = 0.1
        self.Particle_Volume = (np.pi * 4 / 3) * (self.Particle_Degree/2)**3

        self.Space_Interval = 0.2
        self.Error = 0.01

        ## Coefficient & Other
        self.Gravity = -9.81
        self.Density = 0.999
        self.Viscosity = 0.005
        self.Drag_Coefficient = 0.00
        self.Collision_Coefficient = 0.5
        self.Gas_Stiffness = 0.0001

        self.timestep = 33/1000

        ## Initialization
        self.Initialize()

        return None
    
    def Initialize(self):
        for i in range(self.Num_Particle):
            Pos_X = i % (int (self.Space_Width / self.Space_Interval))
            Pos_Z = ( i // (int (self.Space_Width / self.Space_Interval) ) ) % (int (self.Space_Depth/self.Space_Interval))
            Pos_Y = ( ( i // (int (self.Space_Width/self.Space_Interval) ) ) // (int (self.Space_Depth/self.Space_Interval)) ) % (int (self.Space_Height / self.Space_Interval))
            self.Particle_Inf[i][3][0] = Pos_X * self.Space_Interval
            self.Particle_Inf[i][3][1] = Pos_Y * self.Space_Interval + self.Space_Height_Range
            self.Particle_Inf[i][3][2] = Pos_Z * self.Space_Interval

            self.Particle_Inf[i][0][0] = self.Density
            self.Particle_Inf[i][0][2] = self.Particle_Volume * self.Particle_Inf[i][0][0]
            
            for j in range(3):
                self.Particle_Inf[i][2][j] = np.random.rand()*0.01

    def Collision_Other(self,Num):
        for i in range(self.Num_Particle):
            Vector = self.Particle_Inf[Num][3] - self.Particle_Inf[i][3]
            if np.sqrt(Vector.dot(Vector)) <= self.Error :
                for j in range(3):
                    self.Particle_Inf[Num][2][j] *= -1
                    self.Particle_Inf[i][2][j] *= -1

    def Collision_Space(self,Num):
        if self.Particle_Inf[Num][3][1] < 0 :
            self.Particle_Inf[Num][2][1] *= -1 * self.Collision_Coefficient
            
        if self.Particle_Inf[Num][3][0] < 0 or self.Particle_Inf[Num][3][0] > self.Space_Width:
            self.Particle_Inf[Num][2][0] *= -1 * self.Collision_Coefficient
            
        if self.Particle_Inf[Num][3][2] < 0 or self.Particle_Inf[Num][3][2] > self.Space_Depth:
            self.Particle_Inf[Num][2][2] *= -1 * self.Collision_Coefficient

    def Compute_Density_Pressure(self):
        for i in range(self.Num_Particle):
            Old_Density = self.Particle_Inf[i][0][0]
            self.Particle_Inf[i][0][0] = 0
            
            for j in range(self.Num_Particle):
                Vector = self.Particle_Inf[i][3] - self.Particle_Inf[j][3]
                R = np.sqrt(Vector.dot(Vector))
                H = self.Particle_Degree/2
                if R < H :
                    self.Particle_Inf[i][0][0] += self.Particle_Inf[i][0][2] * self.Poly6(Vector)
            
            self.Particle_Inf[i][0][1] = self.Gas_Stiffness * (self.Particle_Inf[i][0][0] - Old_Density)

    def Compute_Forces(self):
        for i in range(self.Num_Particle):
            self.Particle_Inf[i][1] = self.Force_Viscosity_Pressure(i) + self.Force_External(i)

    def Force_Viscosity_Pressure(self,Num):
        Force_V = np.zeros(3)
        Force_P = np.zeros(3)

        for i in range(self.Num_Particle):
            if Num != i :
                Vector = self.Particle_Inf[Num][3] - self.Particle_Inf[i][3]
                R = np.sqrt(Vector.dot(Vector))
                H = self.Particle_Degree/2

                if R < H :

                    Force_V += self.Particle_Inf[Num][0][2] * ( self.Particle_Inf[Num][2] - self.Particle_Inf[i][2]) * ((H - R) * 45 / (np.pi * (H**6))) / self.Particle_Inf[i][0][0]

                    Force_P -= self.Particle_Inf[Num][0][2] * ( self.Particle_Inf[Num][0][1] - self.Particle_Inf[i][0][1]) * self.Spiky(Vector) / (2*self.Particle_Inf[i][0][0])     
        return Force_V * self.Viscosity + Force_P  

    def Force_External(self,Num):
        Force_G = np.zeros(3)
        Force_G[1] = self.Particle_Inf[Num][0][2] *  self.Gravity
        return Force_G
    
    def Leapfrog_Integration(self):
        self.Compute_Density_Pressure()
        self.Compute_Forces()
        for i in range(self.Num_Particle):
            for j in range(3):
                Accel = self.Particle_Inf[i][1][j] / self.Density
                self.Particle_Inf[i][2][j] += Accel * self.timestep*10
                self.Collision_Space(i)
                self.Particle_Inf[i][3][j] += self.Particle_Inf[i][2][j] * self.timestep*10

    def Draw_Particle(self):
        '''
        self.Drawing.Points(self.Particle_Degree,self.Particle_Inf)
        '''
        for i in range(self.Num_Particle):
            #self.Drawing.Point(self.Particle_Degree,self.Particle_Inf[i][3])
            self.Drawing.Sphere(self.Particle_Degree,self.Particle_Inf[i][3])

    def Poly6(self,Vector):
        R = np.sqrt(Vector.dot(Vector))
        H = self.Particle_Degree /2
        if R**2 >= 0 and R**2<= H :
            return ((H**2 - R**2 )**3) * 315 / (np.pi * 64 * (H **9))
        else : 
            return 0

    def Spiky(self,Vector):
        R = np.sqrt(Vector.dot(Vector))
        H = self.Particle_Degree/2
        if R >= 0 and R <= H:
            return ((H - R)**2)*Vector * (-45) / (np.pi * (H**6))
        else : 
            return 0

    def Viscosity(self,Vector) :
        R = np.sqrt(Vector.dot(Vector))
        H = self.Particle_Degree/2
        return (H - R) * 45 / (np.pi * (H**6))


if __name__=="__main__":
    Physics = Physics()
    print(len(Physics.Particle_Inf))
    for i in len(Physics.Particle_Inf):
        print(i)
