import sys
import os
import numpy as np
from numpy.linalg import inv
from numpy import dot
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

#define "special" functions
p0 = lambda t: (1 + 2*t)*(t - 1)**2
p1 = lambda t: (t**2)*(3 - 2*t)
q0 = lambda t: t*(t - 1)**2
q1 = lambda t: (t**2)*(t - 1)

#obtain data from dat file
file = open("duck.dat","r")
lines = file.readlines()
file.close()
data_set = [(float(data[0]),float(data[1])) for data in [line.strip().split() for line in lines]]
size = len(data_set)
f_vec = [point[1] for point in data_set]
x_vec = [point[0] for point in data_set]

def f_hat(x):
    #find x's bin
    found = False
    for i in range(0,len(x_vec) - 1):
        if x >= x_vec[i] and x <= x_vec[i+1]:
            x_l = x_vec[i]
            x_u = x_vec[i+1]
            found = True
            break
    assert found, 'x=' + str(x) + ' not within data_set'
    print(x_l,x,x_u)

def main():
    pass
main()
