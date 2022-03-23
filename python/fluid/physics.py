def add_source(N,x,s,dt):
    size = (N+2)
    for i in range(size):
        for j in range(size):
            x[i][j] += dt * s[i][j]
            
def diffuse(N,b,x,x0,diff,dt):
    a = dt * diff * N * N

def advect(N,b,d,d0,u,v,dt):
    
    
def project(N,u,v,p,div):
    

def lin_solve(N,b,x,x0,a,c):
    for k in range(0,20):
        x
        
def set_bnd(N,b,x):
    for i in range(1, N+1):
        if b==1 :
            x[0][i] = -x[1][i]
            x[N+1][i] = -x[N][i]
        else :
            x[0][i] = x[1][i]
            x[N+1][i] = x[N][i]
        
        if b==2 :
            x[i][0] = -x[i][1]
            x[i][N+1] = -x[i][N]
        else :
            x[i][0] = x[i][1]
            x[i][N+1] = x[i][N]
            
    x[0][0] = 0.5 * (x[1][0] + x[0][1])
    x[0][N+1] = 0.5 * (x[1][N+1] + x[0][N])
    x[N+1][0] = 0.5 * ([x[N][0] + x[N+1][1]])
    x[N+1][N+1] = 0.5 * (x[N][N+1] + x[N+1][N])
    
    
def dens_step(N,x,x0,u,v,diff,dt):
    
def vel_step(N,u,v,u0,v0,visc,dt):
    