import numpy as np;
import matplotlib.pyplot as plt;
import math;
from scipy.optimize import fsolve;
import time
#Setup functions to be used in script environment
abs = lambda a : np.abs(a)

def orderOfDecade(decade,N,E):
    decade = int(decade)
    i = N.index(decade)
    j = 0;
    while N[j] < decade*10 : j += 1;
    return str(abs(round(math.log(E[j],10) - math.log(E[i],10),3)))

f = lambda x : 1 / (1 + x) #Note is only a function of x
soln = lambda t: np.sqrt(4 + 2*t) - 1
Emax = lambda x,t: np.max(abs(x - soln(t)))
Eend = lambda x,t: abs(x[-1] - soln(t[-1]))



gp = lambda xn, delta : lambda xnplus1 : xn - xnplus1 + ( f(xn) + f(xnplus1) )*delta/2
def trapIter(xn,delta,guess=0):
    g = gp(xn,delta)
    return fsolve(g,guess)[0]

def TRAP(N):
    delta = 16/N
    t = np.arange(0,16+delta,delta)
    x = [1];
    while len(x) < len(t):
        x.append(trapIter(x[-1],delta,x[-1]))
    x = np.array(x);
    return (t,x,Emax(x,t),Eend(x,t));

#RK Part
def RK4(N):
    delta = 16/N
    def __RK4(xn):
        z1 = f(xn)
        z2 = f(xn + z1*delta/2)
        z3 = f(xn + z2*delta/2)
        z4 = f(xn + z3*delta)
        return xn + (z1 + 2*z2 + 2*z3 + z4)*delta/6
    t = np.arange(0,16+delta,delta)
    x = [1];
    while len(x) < len(t):
        x.append(__RK4(x[-1]))
    x = np.array(x);
    return (t,x,Emax(x,t),Eend(x,t))








#==================================================================================================
#==================================================================================================

def plotRK4():
    N = [n*10**m for m in [2,3,4,5] for n in range(1,10)]
    N.append(1000000)
    Eendings = []
    Emaxes = []

    print("__RK4__".center(40,'#'))
    try:
        tic = time.time()
        for n in N:
            (t,x,Emax,Eend) = RK4(n);
            print("n="+str(n)+", time="+str(round(time.time() - tic,2)) + "[s]")
            Eendings.append(Eend)
            Emaxes.append(Emax)
    except KeyboardInterrupt as ki:
        minlen = min([len(Eendings),len(Emaxes)])
        N = N[0:minlen]
        Eendings = Eendings[0:minlen]
        Emaxes = Emaxes[0:minlen]

    plt.plot(N,Emaxes,label="Emax O="+orderOfDecade(10**2,N,Emaxes))
    plt.plot(N,Eendings,label="Eend O="+orderOfDecade(10**2,N,Eendings))
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.legend();
    plt.show()

def plotTRAP():
    N = [n*10**m for m in [2,3,4,5] for n in range(1,10)]
    N = [N[i] for i in range(len(N)) if i % 2 == 0]
    N.append(1000000)
    Eendings = []
    Emaxes = []

    print("__TRAP__".center(40,'#'))

    try:
        tic = time.time()
        for n in N:
            (t,x,Emax,Eend) = TRAP(n);
            print("n="+str(n)+", time="+str(round(time.time() - tic,2)) + "[s]")
            Eendings.append(Eend)
            Emaxes.append(Emax)
    except KeyboardInterrupt as ki:
        minlen = min([len(Eendings),len(Emaxes)])
        N = N[0:minlen]
        Eendings = Eendings[0:minlen]
        Emaxes = Emaxes[0:minlen]

    plt.plot(N,Emaxes,label="Emax O="+orderOfDecade(10**2,N,Emaxes))
    plt.plot(N,Eendings,label="Eend O="+orderOfDecade(10**2,N,Eendings))
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.legend();
    plt.show()

def plotMethod(method,everyOther=False):
    distribution = (1,2,4,6,8) if everyOther else (1,2,3,4,5,6,7,8,9)
    N = [n*10**m for m in [2,3,4,5] for n in distribution]
    N.append(1000000)

    Eendings = []
    Emaxes = []

    print(str(method).split(' ')[1].center(40,'#'))
    tics = [];
    try:
        tic = time.time()
        for n in N:
            (t,x,Emax,Eend) = method(n);
            print("n="+str(n)+", time="+str(round(time.time() - tic,2)) + "[s]")
            tics.append(round(time.time() - tic,2))
            Eendings.append(Eend)
            Emaxes.append(Emax)
    except KeyboardInterrupt as ki:
        minlen = min([len(Eendings),len(Emaxes)])
        N = N[0:minlen]
        Eendings = Eendings[0:minlen]
        Emaxes = Emaxes[0:minlen]

    plt.plot(N,Emaxes,label="Emax O="+orderOfDecade(10**2,N,Emaxes))
    plt.plot(N,Eendings,label="Eend O="+orderOfDecade(10**2,N,Eendings))
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.legend();
    plt.show()

    plt.cla();
    plt.clf();
    plt.plot(N,tics,'r-',label="iteration time in seconds")
    plt.title("Iteration Time VS. N")
    plt.ylabel('[sec]')
    plt.xlabel('discretization size')
    plt.legend();
    plt.grid(True);
    plt.show();

