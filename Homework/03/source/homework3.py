import math
import sys
import numpy as np
import matplotlib.pyplot as plt

perc_rel_err = lambda x_better,x_worse: 100*abs(x_better-x_worse)/x_better

TOL = 1e-13
if len(sys.argv) > 2:
    TOL = float(sys.argv[2])

def bisection(n):
    if n < 1:
        a = 0
        b = 1
    else:
        a = 1
        b = n
    
    f = lambda x: n - (x * x)

    iters = 0
    x_last = 0
    x = (b + a)/2
    while perc_rel_err(x,x_last) > TOL:
        iters += 1
        if iters > 10000:
            print("\tnewtons is not converging within tolerance given")
            return(None,None)
        if f(x) == 0:
            break
        if f(b)*f(x) < 0:
            a = x
        elif f(a)*f(x) < 0:
            b = x
        x_last = x
        x = (b + a)/2
    return (x,iters)


def newtons(n):
    f = lambda x: n - x * x
    dfdx = lambda x: -2*x
    iterator = lambda x: x - f(x)/dfdx(x)#causes problem if try to find sqrt(0)
    x = n#set initial guess to the right to optimize convergence
    x_last = 0
    iters = 0 
    while perc_rel_err(x,x_last) > TOL:
        iters += 1
        x_last = x
        x = iterator(x)
        if(iters > 10000):
            print("\tnewtons is not converging within tolerance given")
            return(None,None)
    return(x,iters)


def equivalent_newtons(n):
    iterator = lambda x: (x + n/x)/2
    x = n #set initial guess to n;
    x_last = 0
    iters = 0
    while perc_rel_err(x,x_last) > TOL:
        iters += 1
        x_last = x
        x = iterator(x)
        if(iters > 10000):
            print("\tequivalent_newtons is not converging within tolerance given")
            return(None,None)
    return (x,iters)

def fixed_pt(n,alpha):
    '''
    x = (1-alpha)x + alpha*n/x
    '''
    iterator = lambda x: (1-alpha)*x + alpha*n/x
    x_last = 0
    x = n
    iters = 0
    while(perc_rel_err(x,x_last) > TOL):
        iters += 1
        if(iters > 10000):
            print("\tfixed_pt is not converging within tolerance given with supplied alpha={0}".format(alpha))
            return(None,None)        
        x_last = x
        x = iterator(x)
    return (x,iters)


def main():
    #print(sys.argv)
    n = float(sys.argv[1])
    (result,iters) = bisection(n)
    print('TOL = {0}'.format(TOL))
    print()
    print('bisection:\t\tresult={0}\titerations={1}'.format(result,iters))
    (result1,iters1) = newtons(n)
    print('newtons:\t\tresult={0}\titerations={1}'.format(result1,iters1))
    (result2,iters2) = equivalent_newtons(n)
    print('equivalent_newtons:\tresult={0}\titerations={1}'.format(result2,iters2))
    if result1 == result2 and iters1 == iters2:
        print('bit for bit the results from newtons and equivalent_newtons are identical')
    print('------fixed point-------')
    for alpha in [0.25,0.5,0.75]:
        (result,iters) = fixed_pt(n,alpha)
        print('alpha={0}\tresult={1}\titerations={2}'.format(alpha,result,iters))




main()