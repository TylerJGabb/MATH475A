import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt

sin = lambda x: np.sin(x)
cos = lambda x: np.cos(x)
pi = np.pi
t0 = 5
T = 2*pi
solution = lambda t: 0 if (t > t0 or t < 0) else 1


def x_hat(k, N):
    sum = 0
    for n in range(1, N):
        sum += np.exp(-2*pi*1j*k*n/N)*solution(n*T/N)
    return sum/N

def x_tilda(k):
    if k == 0:
        retval = t0/T
    else:
        retval = (1/(2*pi*1j*k))*(1 - np.exp(-1j*t0*k))
    return retval

def p_tilda(k):
    retval = abs(x_tilda(k))**2
    return retval

def p_hat(k,N):
    retval = abs(x_hat(k,N))**2
    return retval

'''
    p tildas only found once for each k
    p hats found for each value of N for each k
'''

def generate_power_data():
    k_arr = list(range(0,1000))
    p_hat_10 = []
    p_hat_100 = []
    p_hat_1000 = []
    p_tildas = []
    for k in k_arr:
        p_hat_10.append(p_hat(k,100))
        p_hat_100.append(p_hat(k,450))
        p_hat_1000.append(p_hat(k,950))
        p_tildas.append(p_tilda(k))
    plt.plot(k_arr,p_hat_10,label='p hat 100')
    plt.plot(k_arr,p_hat_100,label='p hat 450')
    plt.plot(k_arr,p_hat_1000,label='p hat 950')
    plt.plot(k_arr,p_tildas,label='p tilda')
    plt.legend()
    plt.xlabel('k')
    plt.grid(True)
    plt.title('t0={}, Power Data Comparison With p tilda'.format(t0))
    plt.savefig('power_data_t0={}.png'.format(t0))
    plt.show()


def generate_power_data_differences():
    k_arr = list(range(0, 1000))
    p_hat_10 = []
    p_hat_100 = []
    p_hat_1000 = []
    p_tildas = []
    for k in k_arr:
        ptil = p_tilda(k)
        p_hat_10.append(abs(p_hat(k,100)-ptil))
        p_hat_100.append(abs(p_hat(k,450)-ptil))
        p_hat_1000.append(abs(p_hat(k,950)-ptil))
    plt.scatter(k_arr,p_hat_10,label='p hat 100',s=0.5)
    plt.scatter(k_arr,p_hat_100,label='p hat 450',s=0.5)
    plt.scatter(k_arr,p_hat_1000,label='p hat 950',s=0.5)
    plt.legend()
    plt.xlabel('k')
    plt.grid(True)
    plt.ylim([-10E-5,10E-4])
    plt.title('t0={}, Power Data Differences'.format(t0))
    plt.savefig('power_data_difference_t0={}.png'.format(t0))
    plt.show()
    

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
    delta = 2*pi/N
    if delta > 0.01:
        delta = 0.01
    E = []
    pts = np.arange(0, 2*pi,delta)
    for t in pts:
        E.append(abs(solution(t)-x_approx(N, t)))
    return max(E)


def max_norm_numerical():
    E = []
    N = np.arange(100,2100,100)
    for n in N:
        print(n)
        E.append(max_norm(n))
    plt.plot(N,E)
    plt.savefig('max_norm_data.png')
    plt.show()


def generate_overlay_plot():
    sols = []
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


def generate_one_plot(N):
    sols = []
    appr = []
    pts = np.arange(0, 2*pi,0.01)
    for t in pts:
        print(t,solution(t),x_approx(N,t))
        sols.append(solution(t))
        appr.append(x_approx(N,t))
    plt.plot(pts,sols,'k-', linewidth=2, label='solution')
    plt.plot(pts, appr, label='N='+str(N))
    plt.legend()
    plt.title('t0=' + str(t0))
    plt.show()


if __name__ == '__main__':
    generate_power_data()
    generate_power_data_differences()




