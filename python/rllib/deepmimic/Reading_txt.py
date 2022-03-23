import numpy as np
import sys
import os
import re


INF=[[1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]]

def Reading_txt():
    f = open("humanoid3d_walk.txt","r")
    lines = f.readlines()

    for i in range(4,43):
        numbers = re.findall("\d+\.\d+",lines[i])
        for j in range(len(numbers)):
            numbers[j] = float(numbers[j])
        
        List_1=[]
        Count = 0
        for k in INF[0]: 
            List_2=[]

            for l in range(k):
                List_2.append(numbers[Count+l])
            
            List_1.append(List_2)
            Count += k

        INF.append(List_1)

if __name__=="__main__":
    Read_txt()
    print(INF[1][0][0])
