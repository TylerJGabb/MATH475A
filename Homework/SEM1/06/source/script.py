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

START = int(sys.argv[1])
FINISH = int(sys.argv[2])
INCREMENT = int(sys.argv[3])

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

def find_largest(vectors):
    ret = 0
    for arr in vectors:
        val = max(arr)
        if val > ret:
            ret = val
    return ret

def find_smallest(vectors):
    ret = find_largest(vectors)
    for arr in vectors:
        val = min(arr)
        if val < ret:
            ret = val
    return ret

def do_results_and_create_fig(func,truth,alias):
        err_right = []
        err_trap = []
        err_simp = []
        N = START
        bins = []
        increment = 10
        while N <= FINISH:
            print("-----------N = ",N,"--------------------")
            ret_right = right(func,N)
            ret_trap = trap(func,N)
            ret_simp = simp(func,N)

            abs_err_right = abs_err(truth,ret_right)
            abs_err_trap = abs_err(truth,ret_trap)
            abs_err_simp = abs_err(truth,ret_simp)

            print(ret_right,ret_trap,ret_simp)
            print(abs_err_right,abs_err_trap,abs_err_simp)

            err_right.append(abs_err_right)
            err_trap.append(abs_err_trap)
            err_simp.append(abs_err_simp)

            bins.append(N)

            #increment N linearly
            N += INCREMENT

            # -----------  logarithmic incrementation below ------------------
            #if(N % (increment * 10) == 0):
            #    increment *= 10
            #N += increment

        fig = plt.figure(alias)
        ax = fig.add_subplot(111)
        min_bound = find_smallest([err_right,err_trap,err_simp])
        max_bound = 0.01#find_largest([err_right,err_trap,err_simp])

        ax.set_ylim([min_bound,max_bound])
        ax.plot(bins,err_right,'k--',label='Right Sum')
        ax.plot(bins,err_trap,'b--',label='Trapezoidal')
        ax.plot(bins,err_simp,'r--',label='Simpsons Rule')
        handles,labels = ax.get_legend_handles_labels()
        ax.legend(handles,labels)
        ax.set_title("Plotted results for " + alias + " N in [" + str(START) + "," + str(FINISH) + "]")
        fig.savefig(alias + "_plots")

#error as a function of N
def main():
    funcs = [F1,F2,F3]
    truths = [TRUE_F1,TRUE_F2,TRUE_F3]
    names = ["Function1","Function2","Function3"]
    for i in range(3):
        do_results_and_create_fig(funcs[i],truths[i],names[i])

    do_results_and_create_fig(F4,TRUE_F4,"Periodic")

main()





























9
