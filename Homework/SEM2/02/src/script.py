import numpy as np;
import matplotlib.pyplot as plt;
import math;
#Setup functions to be used in script environment
abs = lambda a : np.abs(a)

def orderOfDecade(decade,N_arr,E_arr):
	decade = int(decade)
	i = N_arr.index(decade);
	return str(abs(round(math.log(E_arr[i+9],10) - math.log(E_arr[i],10),3)))




#Define Special Functions 
f = lambda x : 1 / (1 + x) #Note is only a function of x
soln = lambda t: np.sqrt(4 + 2*t) - 1
Emax = lambda x,t: np.max(abs(x - soln(t)))
Eend = lambda x,t: abs(x[-1] - soln(t[-1]))

#How does the error at t=16 depend on N with TRAP?

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

def plotRK4():
    N = [n*10**m for m in [2,3,4,5] for n in range(1,10)]
    N.append(1000000)
    Eendings = []
    Emaxes = []

    print("__RK4__".center(40,'#'))
    for n in N:
        print("n="+str(n))
        (t,x,Emax,Eend) = RK4(n);
        Eendings.append(Eend)
        Emaxes.append(Emax)
    plt.plot(N,Emaxes,label="Emax O="+orderOfDecade(10**2,N,Emaxes))
    plt.plot(N,Eendings,label="Eend O="+orderOfDecade(10**2,N,Eendings))
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.legend();
    plt.show()

plotRK4()
