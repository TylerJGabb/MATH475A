import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt

sin = lambda x: np.sin(x)
cos = lambda x: np.cos(x)
pi = np.pi
t0 = 1
T = 2*pi
solution = lambda t: 0 if (t > t0 or t < 0) else 1


def x_hat(k, N):
    sum = 0
    for n in range(1, N):
        sum += np.exp(-2*pi*1j*k*n/N)*solution(n*T/N)
    return sum/N

def x_tilda(k):
    if(k == 0):
        return t0/T
    return (1/(2*pi*1j*k))(1 - np.exp(-1j*t0*k))

def p_tilda(k):
    return abs(x_tilda(k))**2

def p_hat(k,N):
    return abs(x_hat(k,N))**2

def plot_power_spectrum(N):
    p_hats = []
    p_tildas = []
    for k in range(N):
        p_hats.append(p_hat(k,N))
        p_tildas.append(p_tilda(k))
    plt.plot(range(N),p)






def x_approx(N, t):
    # returns functions of t
    def term(k):
        global t0
        return lambda tt: (1 / k) * (sin(k * tt) - sin(k * (tt - t0)))

    global t0, pi
    sum = 0
    for k in range(1,N+1):
        sum += term(k)(t)
    sum *= 1/pi
    sum += t0/(2*pi)
    return sum

def max_norm(N):
    delta = 2*pi/N;
    if delta > 0.01:
        delta = 0.01
    E = []
    pts = np.arange(0, 2*pi+delta,delta)
    for t in pts:
        E.append(abs(solution(t)-x_approx(N,t)))
    return max(E)

def do_max_norm_numerical():
    E = []
    N = np.arange(100,2100,100)
    for n in N:
        print(n)
        E.append(max_norm(n))
    plt.plot(N,E,'k-', label='inf norm')
    plt.savefig('max_norm.png')



def generate_overlay_plot():
    sols = []
    appr4 = []
    appr8 = []
    appr16 = []
    appr32 = []
    apprs = [([], 2**i) for i in [2, 3, 4, 5]]
    pts = np.arange(0, 2*pi+0.01,0.01)
    for t in pts:
        sols.append(solution(t))
        for appr in apprs:
            # print(t,appr)
            appr[0].append(x_approx(appr[1],t))
    plt.plot(pts,sols,'k-', linewidth=2, label='solution')
    for appr in apprs:
        plt.plot(pts, appr[0], label='N='+str(appr[1]))
    plt.legend()
    plt.title('t0=' + str(t0))
    plt.savefig('overlay.png')








