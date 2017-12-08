'''
Program cubicSplines.py
Author: Tyler Gabb
MATH475A

This program takes in a .dat or .csv file as input, parses the data points
and generates a cubic spline between them. This is then output as a .png file
'''
import sys
import os
import numpy as np
from numpy.linalg import inv
from numpy import dot
import matplotlib.pyplot as plt

#define "special" functions
p0 = lambda t: (1 + 2*t)*(t - 1)**2
p1 = lambda t: (t**2)*(3 - 2*t)
q0 = lambda t: t*(t - 1)**2
q1 = lambda t: (t**2)*(t - 1)




def main():
    #obtain data from dat file
    if len(sys.argv) < 2:
        print("USAGE: python3 cubicSpline.py FILE.dat")
        print("FILE MUST BE 2 Columns of data")
        sys.exit(1)
    file = open(sys.argv[1],"r")
    lines = file.readlines()
    file.close()
    data_set = [(float(data[0]),float(data[1])) for data in [line.strip().split() for line in lines]]
    N = len(data_set)
    f_vec = [point[1] for point in data_set]
    x_vec = [point[0] for point in data_set]

    #find differences
    h_vec = [round(x_vec[i+1] - x_vec[i],2) for i in range(0,N-1)]

    #find derivatives
    g_vec = get_g_vec(h_vec,f_vec)
    print(g_vec)

    #generate test data with splines
    test = np.linspace(0,14,1000)
    res = []
    for x in test:
        spline = get_spline(x,g_vec,f_vec,x_vec)
        res.append(spline(x))

    #find absolute error at each point, and find norm of those errors
    l2_abs_err = []
    for i in range(0,N):
        spline = get_spline(x_vec[i],g_vec,f_vec,x_vec)
        abs_err = abs(spline(x_vec[i]) - f_vec[i])
        l2_abs_err.append(abs_err)

    plt.plot(test,res,'b-',label="my cubic spline")
    plt.plot(x_vec,f_vec,'ko',label="data set")
    plt.title("my cubic spline")
    plt.text(0,0,"error norm =" + str(np.linalg.norm(l2_abs_err,2)))
    plt.legend()
    plt.ylim([-6,4])
    plt.savefig(sys.argv[1] + "__spline.png")

def get_g_vec(h_vec,f_vec):
    N = len(f_vec)
    H = [[0.0]*N]*N
    H[0] = [0.0]*N
    H[N-1] = [0.0]*N
    H[0]
    F = [0]*N
    for i in range(1,N-1):
        #--build H
        h = [0]*N
        h[i-1] = h_vec[i]
        h[i] = 2*(h_vec[i-1] + h_vec[i])
        h[i+1] = h_vec[i-1]
        H[i] = h

        #--build F
        F[i] = (f_vec[i-1] - f_vec[i] )*3*h_vec[i]/h_vec[i-1] +\
               (f_vec[i+1] - f_vec[i] )*3*h_vec[i-1]/h_vec[i]


    #keep in mind that t(x_vec[0] = 0 and x_vec[19] = 1)
    #and f_CS^''(x_0 and x_N-1) == 0 --this needs to go in writeup
    #thus our boundary conditions for free conditions become

    F[ 0 ]  = 6*f_vec[ 0 ] - 6*f_vec[ 1 ]
    F[N-1]  = 6*f_vec[N-1] - 6*f_vec[N-2]

    H[ 0 ][ 0 ] = -4*h_vec[ 0 ]
    H[ 0 ][ 1 ] = -2*h_vec[ 0 ]
    H[N-1][N-2] =  2*h_vec[N-2]
    H[N-1][N-1] =  4*h_vec[N-2]

    #for i in range(0,N):
        #print(H[i],F[i])

    return np.linalg.solve(H,F)

def get_spline(x,g_vec,f_vec,x_vec):
    #find x's bin
    found = False
    for i in range(0,len(x_vec) - 1):
        if x >= x_vec[i] and x <= x_vec[i+1]:
            found = True
            break

    if not found:
        if(x < min(x_vec)):
            i = 0
        else:
            i = len(x_vec) - 2
    x_l = x_vec[i]
    x_u = x_vec[i+1]
    #i is now the index marking the position of x_l
    t = lambda x: (x - x_l)/(x_u - x_l)
    f_hat = lambda x: f_vec[i]*p0(t(x)) + f_vec[i+1]*p1(t(x)) +\
        (x_vec[i+1] - x_vec[i])*( g_vec[i]*q0(t(x)) + g_vec[i+1]*q1(t(x)) )

    return f_hat

main()
