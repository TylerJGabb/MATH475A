import matplotlib.pyplot as plt
import math as M
import sys
#VAL = int(sys.argv[1]);
ITERS = 200#int(sys.argv[2]);
def main():
    """
    The main Function
    """
    if len(sys.argv) < 3:
        print("Usage: python3 problem1.py POWER ITERATIONS")
        exit(1)
 

    x = plt.figure(1)
    plt.plot(algo1(VAL),'r--',label="Algo I",linewidth=2.5)
    plt.plot(algo2(VAL),'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For +' + str(VAL))
    plt.yscale('log', basex=10);
    x.show()

    y = plt.figure(2)
    plt.plot(algo1(-VAL),'r--',label="Algo I",linewidth=2.5)
    plt.plot(algo2(-VAL),'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For -' + str(VAL))
    plt.yscale('log', basex=10);
    y.show()

    input()

def algo1(x):
    """
    Returns an array of 200 error terms, each of a sucessive iterative approximation
    for e raised to the power of x. uses "Algorithm I"
    """
    terms = []
    s = 1
    t = x
    N_values = list(range(1,ITERS + 1))
    for n in N_values:
        s = s + t
        t = t * x / (n + 1)
        terms.append(s)

    return [abs(M.exp(x) - y) for y in terms]

def algo2(x):
    """
    Returns an array of error terms, each of a sucessive iterative approximation
    for e raised to the power of x. uses "Algorithm II"
    """
    terms = []
    for i in range(ITERS):
        s = 1
        for n in range(i,0,-1):
            s = s * x / n + 1
        terms.append(s)
        
    return [abs(M.exp(x) - y) for y in terms]


def extra_credit():
    errors1 = []
    errors2 = []
    my_range = list(range(25,51))
    for x in my_range:
        errors1.append(algo1(x)[-1])
        errors2.append(algo2(x)[-1])
    
    z = plt.figure(3)
    plt.plot(my_range,errors1,'r--',linewidth=2.5,label='AlgoI')
    plt.plot(my_range,errors2,'b--',linewidth=2.5,label='AlgoII')
    plt.legend(loc='best')
    plt.title('Final Converged error as a function of size of +x')
    plt.xlabel('Size of x in e^x')
    plt.ylabel('Absolute final error')
    z.show()





   
