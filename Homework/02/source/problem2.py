import sys
import os
import math
import matplotlib.pyplot as plt
VERBOSE = "-v" in sys.argv
"""
inf = math.inf
nan = math.nan

each floating-point number is given the standard form

(-1)**s * 2**(c-1023) * (1 + f)

f: binary fraction (mantissa)
c: exponent (characteristic)


"""

def find_smallest_closest_to(val):
    """
    Finds the smallest value to the right of val on the real-number line
    """
    x = 1.0
    divisions = 0
    while (val + x > val):
        x_last = x
        x = x / 2
        divisions += 1
        if VERBOSE:
            print(str.format("Division={0}  Result={1}", divisions, x))
    return (str(val) + "+" + str( x_last),divisions-1)


def find_largest():
    """
    Finds largest representable number in environment
    """
    x = 1.0;
    stage = 0
    while (x != math.inf and x != math.nan):
        x_last = x
        x = x * 2
        stage += 1
        if VERBOSE:
            print(str.format("Stage={0} Result={1}",stage,x))
    return (str(x_last),stage-1)


def make_a_plot():
    values = range(0,1000,50)
    results = []
    for val in values:
        results.append(find_smallest_closest_to(val))
        print('done',val)
    
    plt.plot(values,results);
    plt.show();
    input()

def main():
    (s0,n) = find_smallest_closest_to(0);
    (s1,m) = find_smallest_closest_to(1);
    (S2,N) = find_largest();
    F = 2**N*(2-0.5**m) 
    print("The smallest value closest to 0 is {0} and n = {1}".format(s0,n))
    print("The smallest value closest to 1 is {0} and m = {1}".format(s1,m))
    print("The largest integer is {0} and N = {1}".format(S2,N))
    print("The largest float   is {0}".format(F))
    return F
    
        
