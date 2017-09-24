import math
import sys

perc_rel_err = lambda x_better,x_worse: 100*abs(x_better-x_worse)/x_better

TOL = 1e-13
if len(sys.argv) > 2:
    TOL = float(sys.argv[2])

def bisection(n):
    true = math.sqrt(n)

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
    true = math.sqrt(n)
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
    return(x,iters)


def equivalent_newtons(n):
    true = math.sqrt(n)
    iterator = lambda x: (x + n/x)/2
    x = n #set initial guess to n;
    x_last = 0
    iters = 0
    while perc_rel_err(x,x_last) > TOL:
        iters += 1
        x_last = x
        x = iterator(x)
    return (x,iters)

def fixed_pt(n):
    '''
    n = x*x
    x = n/x #problems with 0
    x = x*x - n + x #no problems with 0 but doesn't converge
    x = x*x*x/n

    '''
    true = math.sqrt(n)


def main():
    print(sys.argv)
    n = float(sys.argv[1])
    print(bisection(n))
    print(newtons(n))
    print(equivalent_newtons(n))    
