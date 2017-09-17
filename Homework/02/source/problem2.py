import sys
import os
import math
import matplotlib.pyplot as plt
VERBOSE = "-v" in sys.argv
"""
inf = math.inf
nan = math.nan
"""


def find_smallest_closest_to(val):
    """
    Finds eps and returns it
    """
    x = 1.0
    divisions = 0
    while (val + x > val):
        x_last = x
        x = x / 2
        divisions += 1
        if VERBOSE:
            print(str.format("Division={0}  Result={1}", divisions, x))
    return x_last


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
    return x_last


def make_a_plot():
    values = range(0,50,1)
    results = []
    for val in values:
        results.append(find_smallest_closest_to(val))
        print('done',val)
    
    plt.plot(values,results);
    plt.show();
    input()


        
        
