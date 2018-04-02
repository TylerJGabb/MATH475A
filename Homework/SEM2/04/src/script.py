import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial as ss
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

sin = np.sin
cos = np.cos
pi = np.pi
c0 = lambda x: x * sin(pi * x)


def generate_euler_D(N):
    D = []
    Delta = 1 / N
    sub = [1, -2, 1]
    for i in range(N):
        if i == 0:
            row = [-2, 1, *([0] * (N - 3)), 1]
        elif i == N - 1:
            row = [1, *([0] * (N - 3)), 1, -2]
        else:
            row = [*([0] * (i - 1)), *sub, *([0] * (N - 3 - (i - 1)))]
        D.append(row)
    return np.asmatrix(D) / Delta ** 2


def generate_sym_D(N):
    D = []
    Delta = 1 / N
    sub = [1, -2, 1]
    for i in range(N):
        if i == 0:
            row = [-1, 1, *([0] * (N - 2))]
        elif i == N - 1:
            row = [*([0] * (N - 2)), 1, -1]
        else:
            row = [*([0] * (i - 1)), *sub, *([0] * (N - 3 - (i - 1)))]
        D.append(row)
    return np.asmatrix(D) / Delta ** 2


def generate_non_D(N):
    D = []
    Delta = 1 / N
    sub = [1, -2, 1]
    for i in range(N):
        if i == 0:
            row = [-2, 2, *([0] * (N - 2))]
        elif i == N - 1:
            row = [*([0] * (N - 2)), 2, -2]
        else:
            row = [*([0] * (i - 1)), *sub, *([0] * (N - 3 - (i - 1)))]
        D.append(row)
    return np.asmatrix(D) / Delta ** 2


def forward_euler(cm, delta, D):
    multiplier = np.identity(len(D)) + delta * D
    return multiplier * cm


def backward_euler(cm, delta, D):
    multiplier = np.identity(len(D)) - delta * D
    inv = np.linalg.inv(multiplier)
    return inv * cm


def get_c0(N):
    Delta = 1 / N
    return np.array([[c0(n * Delta)] for n in range(N)])


def do_a_plot(M, color, ax, maxt=0.2, label=None):
    N = 100
    Delta = 1 / N
    delta = 2 / M
    n_arr = np.arange(0, 1, Delta)
    t_arr = np.arange(0, maxt + delta, delta)
    D = generate_euler_D(N)
    c = [get_c0(N)]
    while len(c) < len(t_arr):
        func = backward_euler if label[0] == 'b' else forward_euler
        cp = func(c[-1], delta, D)
        c.append(cp)
    print('done')
    Z = np.array([[float(np.nan if abs(ccc - 0.3) > 0.7 else ccc) for ccc in cc] for cc in c])
    X, Y = np.meshgrid(n_arr, t_arr)
    ax.plot_wireframe(X, Y, Z, color=color, label='{} delta={}, M={}'.format(label, delta, M), rstride=M // 100 + 1,
                      cstride=N // 20 + 1)


def get_vol(N,D):
    Delta = 1 / N
    delta = Delta
    n_arr = np.arange(0, 1, Delta)
    t_arr = np.arange(0, 1 + delta, delta)
    c = [get_c0(N)]
    i = 0
    #print('calculating surface')
    while len(c) < len(t_arr):
        cp = backward_euler(c[-1], delta, D)
        #if i % 50 == 0:
            #print('iter=',i)
        #i += 1
        c.append(cp)
    #print('done')
    X, Y = np.meshgrid(n_arr, t_arr)
    Z = np.array([[float(np.nan if abs(ccc - 0.3) > 0.7 else ccc) for ccc in cc] for cc in c])
    XX = []
    for x in X:
        for xx in x:
            XX.append(float(xx))
    YY = []
    for y in Y:
        for yy in y:
            YY.append(float(yy))
    ZZ = []
    for z in Z:
        for zz in z:
            ZZ.append(float(zz))
    points = [[XX[i],YY[i],ZZ[i]] for i in range(len(ZZ))]
    #print('calculating volume')
    vol = ss.ConvexHull(points).volume
    #print('done')
    return vol

def do_eyeball():
    M1 = 512
    M2 = 1024
    ax = plt.axes(projection='3d')
    do_a_plot(M1, 'red', ax, maxt=0.2, label='backward')
    do_a_plot(M2, 'blue', ax, maxt=0.2, label='backward')
    plt.legend()
    plt.show()


def generate_between(n1,n2,step):
    truth = 0.2475028472196835
    vols_sym = []
    vols_non = []
    N_arr = np.arange(n1, n2, step)
    for n in N_arr:
        Dn = generate_non_D(n)
        Ds = generate_sym_D(n)
        voln = abs(truth-get_vol(n,Dn))
        vols = abs(truth-get_vol(n,Ds))
        vols_sym.append(vols)
        vols_non.append(voln)
        print(n, voln, vols)
    print(vols)

def plot_results():
    results = pd.read_csv("results.txt",delimiter='\s+').to_dict('list')
    N = results['N']
    non_sym = results['non_sym']
    sym = results['sym']
    lognon = np.log(non_sym)
    logsym = np.log(sym)
    logN = np.log(N)
    order_non = (lognon[-1] - lognon[0])/(logN[-1] - logN[0])
    order_sym = (logsym[-1] - logsym[0])/(logN[-1] - logN[0])
    plt.plot(N,non_sym,label='non symmetrical O={}'.format(round(order_non,2)))
    plt.plot(N,sym,label='symmetrical O={}'.format(round(order_sym,1)))
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('distance from true volume')
    plt.xlabel('N')
    plt.title('Convergence: Volume Under Surface\n Truth is considered at N=1024')
    plt.legend()

    plt.show()

plot_results()


def attempt(N, D):
    Delta = 1 / N
    delta = Delta
    n_arr = np.arange(0, 1, Delta)
    t_arr = np.arange(0, 1 + delta, delta)
    c = [get_c0(N)]
    i = 0
    while len(c) < len(t_arr):
        cp = backward_euler(c[-1], delta, D)
        c.append(cp)
    X, Y = np.meshgrid(n_arr, t_arr)
    Z = np.array([[float(np.nan if abs(ccc - 0.3) > 0.7 else ccc) for ccc in cc] for cc in c])
    XX = []
    for x in X:
        for xx in x:
            XX.append(float(xx))
    YY = []
    for y in Y:
        for yy in y:
            YY.append(float(yy))
    ZZ = []
    for z in Z:
        for zz in z:
            ZZ.append(float(zz))
    points = [[XX[i],YY[i],ZZ[i]] for i in range(len(ZZ))]
    #print('calculating volume')
    vol = ss.ConvexHull(points).volume
    #print('done')



