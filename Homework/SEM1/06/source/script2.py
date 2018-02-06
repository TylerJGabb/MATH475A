import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from decimal import *
NARGS = len(sys.argv)
ARGS = sys.argv

PI = math.pi
e  = math.exp(1)
XN = lambda n,N: -1 + 2*n/N

#Define given functions
F1 = lambda x: abs(x - PI/10)
TRUE_F1 = 1 + PI**2/100
F2 = lambda x: (x - 1)**2
TRUE_F2 = 8/3
F3 = lambda x: e**x
TRUE_F3 = e -(1/e)
F4 = lambda x: math.sin(x)**2
TRUE_F4 = PI

#define special error functions
approx_error = lambda better,worse: 100 * abs(better - worse)/better
true_error   = lambda true,approx: 100 * abs(true - approx)/true
abs_err = lambda true,approx: abs(true - approx)

#get START and FINISH bounds for N in iterations
#
# START = int(sys.argv[1])
# FINISH = int(sys.argv[2])
# INCREMENT = int(sys.argv[3])
TOL = 0.01

#Define special functions for left, right, and simps approx
#for a given function and number of bins
def right(f,N):
    '''
    f is a function handle/pointer, it must return a numerical value
    '''
    rsum = 0
    for n in range(1,N+1):
        rsum += f(XN(n,N))
    rsum *= (2/N)
    return rsum

def trap(f,N):
    tsum = 0
    for n in range(1,N+1):
        xa = XN(n-1,N)
        xb = XN(n,N)
        tsum += f(xa) + f(xb)
    tsum /= N
    return tsum

def simp(f,N):
    simp_sum = 0
    for n in range(1,N+1):
        xa = XN(n-1,N)
        xb = (XN(n-1,N) + XN(n,N))/2
        xc = XN(n,N)
        simp_sum += f(xa) + 4*f(xb) + f(xc)
    simp_sum *= (1/(3*N))
    return simp_sum

def increment_logarithmic(N):
    incr = int("1" + "0"*(len(str(N)) - 1))
    return N + incr

def do_results_create_plot(func,method,truth,alias):
    N = 1
    results = [method(func,N)]
    iterations = [N]
    err = abs_err(truth,results[-1])
    errs = [err]
    flag = False;
    while err > TOL:
        if N >= 1000:
            N = increment_logarithmic(N)
        else:
            N += 1
        if N >= 1000000:
            flag = True
            break

        iterations.append(N)
        results.append(method(func,N))
        print(10*"-" + alias + " N=" + str(N) + "->" + str(results[-1]))
        err = abs_err(truth,results[-1])
        errs.append(err)

    fig = plt.figure(alias)
    ax = fig.add_subplot(111)
    ax.plot(iterations,errs,'k--',label=alias)
    title = alias + ". "
    if flag:
        title += "\nReached iteration limit with result " + str(results[-1])
    else:
        title += ("\nConverged to within " + str(TOL*100) + "% of solution in " + str(len(iterations)) + "Iterations")
    ax.set_title(title)
    fig.savefig(alias + "_plot")
    return (results[-1],errs[-1],N)

def do_fixed(func,method,truth,alias,amt):
    N = 1
    results = [method(func,N)]
    iterations = [N]
    err = abs_err(truth,results[-1])
    errs = [err]
    flag = False;
    for N in range(1,amt+1):
        iterations.append(N)
        results.append(method(func,N))
        print(10*"-" + alias + " N=" + str(N) + "->" + str(results[-1]))
        err = abs_err(truth,results[-1])
        errs.append(err)

    fig = plt.figure(alias)
    ax = fig.add_subplot(111)
    ax.plot(iterations,errs,'k--',label=alias)
    title = alias + " " + str(amt) + " Iterations"
    ax.set_title(title)
    fig.savefig(alias + "_plot")
    return (results[-1],errs[-1],N)

def main():
    method_names = ["RightSum","Trapezoidal","Simpsons"]
    function_names = ["Function1","Function2","Function3","Function4"]
    methods = [right,trap,simp]
    truths = [TRUE_F1,TRUE_F2,TRUE_F3,TRUE_F4]
    funcs = [F1,F2,F3,F4]
    for i in [0,1,2]:
        for j in [0,1,2,3]:
            alias = method_names[i] + "_" + function_names[j]
            #do_results_create_plot(funcs[j],methods[i],truths[j],alias)
            do_fixed(funcs[j],methods[i],truths[j],alias,100)



















9
