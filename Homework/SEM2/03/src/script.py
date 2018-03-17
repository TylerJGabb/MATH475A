import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
sin = lambda x: np.sin(x)
pi = np.pi
t0 = 1
solution = lambda t : 0 if (t > t0 or t < 0) else 1

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
    sols = []
    appr4 = []
    appr8 = []
    appr16 = []
    appr32 = []
    appr64 = [] 
    apprs = [(appr4,4),(appr8,8),(appr16,16),(appr32,32)]
    pts = np.arange(0,2*pi+0.01,0.01)
    for t in pts:
        sols.append(solution(t))
        for appr in apprs:
            # print(t,appr)
            appr[0].append(x_approx(appr[1],t))
    plt.plot(pts,sols,'k-',linewidth=2,label='solution')
    for appr in apprs:
        plt.plot(pts,appr[0],label='N='+str(appr[1]))
    plt.legend()
    plt.title('t0=' + str(t0))
    plt.show()


main()


