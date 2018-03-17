import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
solution = lambda t : 0 if (t > 1 or t < 0) else 1

sin = lambda x: np.sin(x)
pi = np.pi
t0 = 1

#returns functions of t
def term(k):    
    global t0
    return lambda t : (1/k)*(sin(k*t) - sin(k*(t-t0)))

#also returns a function of t
def x_approx(N,t):
    global t0, pi
    sum = 0
    for k in range(1,N+1):
        sum += term(k)(t)
    sum *= 1/pi
    sum += t0/(2*pi)
    return sum

def main():
    ret = x_approx(5,0.5)
    sols = []
    pts = np.arange(0,2*pi+0.01,0.01)
    for t in pts:
        sols.append(solution(t))
    plt.plot(pts,sols)
    plt.show()


main()


